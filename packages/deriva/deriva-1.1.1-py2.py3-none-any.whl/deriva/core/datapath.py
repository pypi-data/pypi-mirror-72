from . import urlquote
from datetime import date
import logging
import re
from requests import HTTPError
import warnings

logger = logging.getLogger(__name__)
"""Logger for this module"""

_system_defaults = {'RID', 'RCT', 'RCB', 'RMT', 'RMB'}
"""Set of system default column names"""


def _kwargs(**kwargs):
    """Helper for extending datapath with sub-types for the whole model tree."""
    kwargs2 = {
        'schema_class': Schema,
        'table_class': Table,
        'column_class': Column
    }
    kwargs2.update(kwargs)
    return kwargs2


def from_catalog(catalog):
    """Creates a datapath.Catalog object from an ErmrestCatalog object.
    :param catalog: an ErmrestCatalog object
    :return: a datapath.Catalog object
    """
    return Catalog(catalog.getCatalogSchema(), **_kwargs(catalog=catalog))


def _isidentifier(a):
    """Tests if string is a valid python identifier.
    This function is intended for internal usage within this module.
    :param a: a string
    """
    if hasattr(a, 'isidentifier'):
        return a.isidentifier()
    else:
        return re.match("[_A-Za-z][_a-zA-Z0-9]*$", a) is not None


def _http_error_message(e):
    """Returns a formatted error message from the raw HTTPError.
    """
    return '\n'.join(e.response.text.splitlines()[1:]) + '\n' + str(e)


class DataPathException (Exception):
    """DataPath exception
    """
    def __init__(self, message, reason=None):
        super(DataPathException, self).__init__(message, reason)
        self.message = message
        self.reason = reason

    def __str__(self):
        return self.message


class Catalog (object):
    """Handle to a Catalog.
    """
    def __init__(self, model_doc, **kwargs):
        """Creates the Catalog.
        :param model_doc: the schema document for the catalog
        """
        super(Catalog, self).__init__()
        self.schemas = {
            sname: kwargs.get('schema_class', Schema)(sname, sdoc, **kwargs)
            for sname, sdoc in model_doc.get('schemas', {}).items()
        }

    def __dir__(self):
        return dir(Catalog) + ['schemas'] + [key for key in self.schemas if _isidentifier(key)]

    def __getattr__(self, a):
        if a in self.schemas:
            return self.schemas[a]
        else:
            return getattr(super(Catalog, self), a)


class Schema (object):
    """Represents a Schema.
    """
    def __init__(self, sname, schema_doc, **kwargs):
        """Creates the Schema.
        :param sname: the schema's name
        :param schema_doc: the schema document
        """
        super(Schema, self).__init__()
        self.name = sname
        self.tables = {
            tname: kwargs.get('table_class', Table)(sname, tname, tdoc, **kwargs)
            for tname, tdoc in schema_doc.get('tables', {}).items()
        }

    def __dir__(self):
        return dir(Schema) + ['name', 'tables'] + [key for key in self.tables if _isidentifier(key)]

    def __getattr__(self, a):
        if a in self.tables:
            return self.tables[a]
        else:
            return getattr(super(Schema, self), a)

    def describe(self):
        """Provides a description of the model element.

        :return: a user-friendly string representation of the model element.
        """
        s = "Schema name: '%s'\nList of tables:\n" % self.name
        if len(self.tables) == 0:
            s += "none"
        else:
            s += "\n".join("  '%s'" % tname for tname in self.tables)
        return s

    def _repr_html_(self):
        return self.describe()


class DataPath (object):
    """Represents an arbitrary data path."""
    def __init__(self, root):
        assert isinstance(root, TableAlias)
        self._path_expression = Root(root)
        self._root = root
        self._base_uri = root.catalog._server_uri
        self._table_instances = dict()  # map of alias_name => TableAlias object
        self._context = None
        self._identifiers = []
        self._bind_table_instance(root)

    def __dir__(self):
        return dir(DataPath) + self._identifiers

    def __getattr__(self, a):
        if a in self._table_instances:
            return self._table_instances[a]
        else:
            return getattr(super(DataPath, self), a)

    @property
    def table_instances(self):
        return self._table_instances

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value):
        assert isinstance(value, TableAlias)
        assert value.name in self._table_instances
        if self._context != value:
            self._path_expression = ResetContext(self._path_expression, value)
            self._context = value

    @property
    def uri(self):
        return self._base_uri + str(self._path_expression)

    def _contextualized_uri(self, context):
        """Returns a path uri for the specified context.

        :param context: a table instance that is bound to this path
        :return: string representation of the path uri
        """
        assert isinstance(context, TableAlias)
        assert context.name in self._table_instances
        if self._context != context:
            return self._base_uri + str(ResetContext(self._path_expression, context))
        else:
            return self.uri

    def _bind_table_instance(self, alias):
        """Binds a new table instance into this path.
        """
        assert isinstance(alias, TableAlias)
        alias.path = self
        self._table_instances[alias.name] = self._context = alias
        if _isidentifier(alias.name):
            self._identifiers.append(alias.name)

    def delete(self):
        """Deletes the entity set referenced by the data path.
        """
        try:
            path = str(self._path_expression)
            logger.debug("Deleting: {p}".format(p=path))
            self._root.catalog.delete(path)
        except HTTPError as e:
            logger.debug(e.response.text)
            if 400 <= e.response.status_code < 500:
                raise DataPathException(_http_error_message(e), e)
            else:
                raise e

    def filter(self, filter_expression):
        """Filters the path based on the specified formula.

        :param filter_expression: should be a valid Predicate object
        :return: self
        """
        assert isinstance(filter_expression, Predicate)
        self._path_expression = Filter(self._path_expression, filter_expression)
        return self

    def link(self, right, on=None, join_type=''):
        """Links this path with another table.

        To link a table with an unambigious relationship where table A is related to table B via a single foreign key
        reference, the `on` clause is not.

        ```
        # let A and B be variables for tables from the catalog
        path = A.link(B)
        ```

        To link tables with more than one foreign key reference between them, use explicit `on` clause.

        ```
        # let A.c1 be a column that is a simple foreign key to B.c1 that is a simple key in B
        path = A.link(B, on=(A.c1 == B.c1))
        ```

        To link tables with foreign keys on composite keys, use a conjunction of 2 or more equality comparisons in the
        `on` clause.

        ```
        # let A.c1, A.c2 be columns that form a foreign key to B.c1, B.c2 that are a composite key in B
        path = A.link(B, on=((A.c1 == B.c1) & (A.c2 == B.c2)))
        ```

        By default links use inner join semantics on the foreign key / key equality comparison. The `join_type`
        parameter can be used to specify `left`, `right`, or `full` outer join semantics.

        :param right: the right hand table of the link expression
        :param on: an equality comparison between key and foreign key columns or a conjunction of such comparisons
        :param join_type: the join type of this link which may be 'left', 'right', 'full' outer joins or '' for inner
        join link by default.
        :return: self
        """
        if not isinstance(right, Table):
            raise ValueError("'right' must be a 'Table' instance")
        if on and not (isinstance(on, ComparisonPredicate) or (isinstance(on, ConjunctionPredicate) and
                                                               on.is_valid_join_condition)):
            raise ValueError("'on' must be a comparison or conjuction of comparisons")
        if join_type and on is None:
            raise ValueError("'on' must be specified for outer joins")
        if right.catalog != self._root.catalog:
            raise ValueError("'right' is from a different catalog. Cannot link across catalogs.")
        if isinstance(right, TableAlias) and right.name in self._table_instances:
            raise ValueError("'right' is a table alias that has already been used.")
        else:
            # Generate an unused alias name for the table
            table_name = right.name
            alias_name = table_name
            counter = 1
            while alias_name in self._table_instances:
                counter += 1
                alias_name = table_name + str(counter)
            right = right.alias(alias_name)

        if on is None:
            on = right

        # Extend path expression
        self._path_expression = Link(self._path_expression, on, right, join_type)

        # Bind alias and this data path
        self._bind_table_instance(right)

        return self

    def entities(self):
        """Returns a results set of whole entities from this data path's current context.

        ```
        results1 = my_path.entities()
        ```

        :return: a result set of entities where each element is a whole entity per the table definition and policy.
        """
        return self._query()

    def aggregates(self, *functions):
        """Returns a results set of computed aggregates from this data path.

        By using the built-in subclasses of the `AggregateFunction` class, including `Min`, `Max`, `Sum`, `Avg`, `Cnt`,
        `CntD`, `Array`, and `ArrayD`, aggregates can be computed and fetched. These aggregates must be passed as named
        parameters since they require _alias names_.

        ```
        results1 = my_path.aggregates(Min(col1).alias('mincol1'), Array(col2).alias('arrcol2'))
        results2 = my_path.aggregates(Min(col1), Array(col2))  # Error! Aggregates must be aliased.
        results3 = my_path.aggregates(col1, Array(col2).alias('arrcol2'))  # Error! Cannot mix columns and aggregate functions.
        ```

        :param functions: aliased functions of type AggregateFunctionAlias
        :return: a results set with a single row of results.
        """
        return self._query(mode=Project.AGGREGATE, projection=list(functions))

    def attributes(self, *attributes):
        """Returns a results set of attributes projected and optionally renamed from this data path.

        ```
        results1 = my_path.attributes(col1, col2)  # fetch a subset of attributes of the path
        results2 = my_path.attributes(col1.alias('col_1'), col2.alias('col_2'))  # fetch and rename the attributes
        results3 = my_path.attributes(col1, col2.alias('col_2'))  # rename some but not others
        ```

        :param attributes: a list of Columns.
        :return: a results set of the projected attributes from this data path.
        """
        return self._query(mode=Project.ATTRIBUTE, projection=list(attributes))

    def groupby(self, *keys):
        """Returns an attribute group object.

        The attribute group object returned by this method can be used to get a results set of computed aggregates for
        groups of attributes from this data path.

        With a single group key:
        ```
        results1 = my_path.groupby(col1).attributes(Min(col2).alias('min_col1'), Array(col3).alias('arr_col2'))
        ```

        With more than one group key:
        ```
        results2 = my_path.groupby(col1, col2).attributes(Min(col3).alias('min_col1'), Array(col4).alias('arr_col2'))
        ```

        With aliased group keys:
        ```
        results3 = my_path.groupby(col1.alias('key_one'), col2.alias('keyTwo'))\
                          .attributes(Min(col3).alias('min_col1'), Array(col4).alias('arr_col2'))
        ```

        With binning:
        ```
        results3 = my_path.groupby(col1.alias('key_one'), Bin(col2;10;0;9999).alias('my_bin'))\
                          .attributes(Min(col3).alias('min_col1'), Array(col4).alias('arr_col2'))
        ```

        :param keys: a list of columns, aliased columns, or aliased bins, to be used as the grouping key.
        :return: an attribute group that supports an `.attributes(...)` method that accepts columns, aliased columns,
        and/or aliased aggregate functions as its arguments.
        """
        return AttributeGroup(self, self._query, keys)

    def _query(self, mode='entity', projection=[], group_key=[], context=None):
        """Internal method for querying the data path from the perspective of the given 'context'.

        :param mode: a valid mode in Project.MODES
        :param projection: a projection list.
        :param group_key: a group key list (only for attributegroup queries).
        :param context: optional context for the query.
        :return: a results set.
        """
        assert context is None or isinstance(context, TableAlias)
        catalog = self._root.catalog

        expression = self._path_expression
        if context:
            expression = ResetContext(expression, context)
        if mode != Project.ENTITY:
            expression = Project(expression, mode, projection, group_key)
        base_path = str(expression)

        def fetcher(limit=None, sort=None):
            assert limit is None or isinstance(limit, int)
            assert sort is None or hasattr(sort, '__iter__')
            limiting = '?limit=%d' % limit if limit else ''
            sorting = '@sort(' + ','.join([col.uname for col in sort]) + ')' if sort else ''
            path = base_path + sorting + limiting
            logger.debug("Fetching " + path)
            try:
                resp = catalog.get(path)
                return resp.json()
            except HTTPError as e:
                logger.debug(e.response.text)
                if 400 <= e.response.status_code < 500:
                    raise DataPathException(_http_error_message(e), e)
                else:
                    raise e

        return ResultSet(self._base_uri + base_path, fetcher)


class ResultSet (object):
    """A set of results for various queries or data manipulations.

    The ResultSet is produced by a path. The results may be explicitly fetched. The ResultSet behaves like a
    container. If the ResultSet has not been fetched explicitly, on first use of container operations, it will
    be implicitly fetched from the catalog.
    """
    def __init__(self, uri, fetcher_fn):
        """Initializes the ResultSet.
        :param uri: the uri for the entity set in the catalog.
        :param fetcher_fn: a function that fetches the entities from the catalog.
        """
        assert fetcher_fn is not None
        self._fetcher_fn = fetcher_fn
        self._results_doc = None
        self._sort_keys = None
        self.uri = uri

    @property
    def _results(self):
        if self._results_doc is None:
            self.fetch()
        return self._results_doc

    def __len__(self):
        return len(self._results)

    def __getitem__(self, item):
        return self._results[item]

    def __iter__(self):
        return iter(self._results)

    def sort(self, *attributes):
        """Orders the results set by the given attributes.

        :param keys: Columns, column aliases, or aggregate function aliases. The sort attributes must be projected by
        the originating query.
        :return: self
        """
        if not attributes:
            raise ValueError("No sort attributes given.")
        if not all(isinstance(a, Column) or isinstance(a, ColumnAlias) or (a, AggregateFunctionAlias) for a in attributes):
            raise ValueError("Sort keys must be column, column alias, or aggregate function alias")
        self._sort_keys = attributes
        self._results_doc = None
        return self

    def fetch(self, limit=None):
        """Fetches the results from the catalog.

        :param limit: maximum number of results to fetch from the catalog.
        :return: self
        """
        limit = int(limit) if limit else None
        self._results_doc = self._fetcher_fn(limit, self._sort_keys)
        logger.debug("Fetched %d entities" % len(self._results_doc))
        return self


class Table (object):
    """Represents a Table.
    """
    def __init__(self, sname, tname, table_doc, **kwargs):
        """Creates a Table object.
        :param sname: name of the schema
        :param tname: name of the table
        :param table_doc: deserialized json document of the table definition
        :param kwargs: must include `catalog`
        """
        self.catalog = kwargs['catalog']
        self.sname = sname
        self.name = tname
        self._table_doc = table_doc
        self._kwargs = kwargs

        kwargs.update(table=self)
        self.column_definitions = {
            cdoc['name']: kwargs.get('column_class', Column)(sname, tname, cdoc, **kwargs)
            for cdoc in table_doc.get('column_definitions', [])
        }

    def __dir__(self):
        return dir(Table) + ['catalog', 'sname', 'name'] + [key for key in self.column_definitions if _isidentifier(key)]

    def __getattr__(self, a):
        if a in self.column_definitions:
            return self.column_definitions[a]
        else:
            return getattr(super(Table, self), a)

    def describe(self):
        """Provides a description of the model element.

        :return: a user-friendly string representation of the model element.
        """
        s = "Table name: '%s'\nList of columns:\n" % self.name
        if len(self.column_definitions) == 0:
            s += "none"
        else:
            s += "\n".join("  %s" % col.name for col in self.column_definitions.values())
        return s

    def _repr_html_(self):
        return self.describe()

    @property
    def uname(self):
        """the url encoded name"""
        return urlquote(self.name)

    @property
    def fqname(self):
        """the url encoded fully qualified name"""
        return "%s:%s" % (urlquote(self.sname), self.uname)

    @property
    def instancename(self):
        return '*'

    @property
    def projection_name(self):
        """In a projection, the object uses this name."""
        return self.instancename

    @property
    def fromname(self):
        return self.fqname

    @property
    def path(self):
        """Always a new DataPath instance that is rooted at this table.
        Note that this table will be automatically aliased using its own table name.
        """
        return DataPath(self.alias(self.name))

    @path.setter
    def path(self, value):
        """Not allowed on base tables.
        """
        raise Exception("Path assignment not allowed on base table objects.")

    @property
    def _contextualized_path(self):
        """Returns the path as contextualized for this table instance.

        Conditionally updates the context of the path to which this table instance is bound.
        """
        return self.path

    @property
    def uri(self):
        return self.path.uri

    def alias(self, alias_name):
        """Returns a table alias object.
        :param alias_name: a string to use as the alias name
        """
        return TableAlias(self, alias_name)

    def filter(self, filter_expression):
        """See the docs for this method in `DataPath` for more information."""
        return self._contextualized_path.filter(filter_expression)

    def link(self, right, on=None, join_type=''):
        """See the docs for this method in `DataPath` for more information."""
        return self._contextualized_path.link(right, on, join_type)

    def _query(self, mode='entity', projection=[], group_key=[], context=None):
        """Invokes query on the path for this table."""
        return self.path._query(mode, projection, group_key=group_key, context=context)

    def entities(self):
        """Returns a results set of whole entities from this data path's current context.

        See the docs for this method in `DataPath` for more information.
        """
        return self._query()

    def aggregates(self, *functions):
        """Returns a results set of computed aggregates from this data path.

        See the docs for this method in `DataPath` for more information.
        """
        return self._query(mode=Project.AGGREGATE, projection=list(functions))

    def attributes(self, *attributes):
        """Returns a results set of attributes projected and optionally renamed from this data path.

        See the docs for this method in `DataPath` for more information.
        """
        return self._query(mode=Project.ATTRIBUTE, projection=list(attributes))

    def groupby(self, *keys):
        """Returns an attribute group object.

        See the docs for this method in `DataPath` for more information.
        """
        return AttributeGroup(self, self._query, keys)

    def insert(self, entities, defaults=set(), nondefaults=set(), add_system_defaults=True):
        """Inserts entities into the table.
        :param entities: an iterable collection of entities (i.e., rows) to be inserted into the table.
        :param defaults: optional, set of column names to be assigned the default expression value.
        :param nondefaults: optional, set of columns names to override implicit system defaults
        :param add_system_defaults: flag to add system columns to the set of default columns.
        :return a ResultSet of newly created entities.
        """
        # empty entities will be accepted but results are therefore an empty entity set
        if not entities:
            return ResultSet(self.path.uri, lambda ignore1, ignore2: [])

        options = []

        if defaults or add_system_defaults:
            defaults_enc = {urlquote(cname) for cname in defaults}
            if add_system_defaults:
                defaults_enc |= _system_defaults - nondefaults
            options.append("defaults={cols}".format(cols=','.join(defaults_enc)))

        if nondefaults:
            nondefaults_enc = {urlquote(cname) for cname in nondefaults}
            options.append("nondefaults={cols}".format(cols=','.join(nondefaults_enc)))

        path = '/entity/' + self.fqname
        if options:
            path += "?" + "&".join(options)
        logger.debug("Inserting entities to path: {path}".format(path=path))

        # JSONEncoder does not handle general iterable objects, so we have to make sure its an acceptable collection
        if not hasattr(entities, '__iter__'):
            raise ValueError('entities is not iterable')
        entities = entities if isinstance(entities, (list, tuple)) else list(entities)

        # test the first entity element to make sure that it looks like a dictionary
        if not hasattr(entities[0], 'keys'):
            raise ValueError('entities[0] does not look like a dictionary -- does not have a "keys()" method')

        try:
            resp = self.catalog.post(path, json=entities, headers={'Content-Type': 'application/json'})
            return ResultSet(self.path.uri, lambda ignore1, ignore2: resp.json())
        except HTTPError as e:
            logger.debug(e.response.text)
            if 400 <= e.response.status_code < 500:
                raise DataPathException(_http_error_message(e), e)
            else:
                raise e

    def update(self, entities, correlation={'RID'}, targets=None):
        """Update entities of a table.

        For more information see the ERMrest protocol for the `attributegroup` interface. By default, this method will
        correlate the input data (entities) based on the `RID` column of the table. By default, the method will use all
        column names found in the first row of the `entities` input, which are not found in the `correlation` set and
        not defined as 'system columns' by ERMrest, as the targets if `targets` is not set.

        :param entities: an iterable collection of entities (i.e., rows) to be updated in the table.
        :param correlation: an iterable collection of column names used to correlate input set to the set of rows to be
        updated in the catalog. E.g., `{'col name'}` or `{mytable.mycolumn}` will work if you pass a Column object.
        :param targets: an iterable collection of column names used as the targets of the update operation.
        :return: a ResultSet of updated entities as returned by the corresponding ERMrest interface.
        """
        # empty entities will be accepted but results are therefore an empty entity set
        if not entities:
            return ResultSet(self.path.uri, lambda ignore1, ignore2: [])

        # JSONEncoder does not handle general iterable objects, so we have to make sure its an acceptable collection
        if not hasattr(entities, '__iter__'):
            raise ValueError('entities is not iterable')
        entities = entities if isinstance(entities, (list, tuple)) else list(entities)

        # test the first entity element to make sure that it looks like a dictionary
        if not hasattr(entities[0], 'keys'):
            raise ValueError('entities[0] does not look like a dictionary -- does not have a "keys()" method')

        # Form the correlation keys and the targets
        correlation_cnames = {urlquote(str(c)) for c in correlation}
        if targets:
            target_cnames = {urlquote(str(t)) for t in targets}
        else:
            exclusions = correlation_cnames | _system_defaults
            target_cnames = {urlquote(str(t)) for t in entities[0].keys() if urlquote(str(t)) not in exclusions}

        # test if there are any targets after excluding for correlation keys and system columns
        if not target_cnames:
            raise ValueError('No "targets" for the update. There must be at least one column as a target of the update,'
                             ' and targets cannot overlap with "correlation" keys and system columns.')

        # Form the path
        path = '/attributegroup/{table}/{correlation};{targets}'.format(
            table=self.fqname,
            correlation=','.join(correlation_cnames),
            targets=','.join(target_cnames)
        )

        try:
            resp = self.catalog.put(path, json=entities, headers={'Content-Type': 'application/json'})
            return ResultSet(self.path.uri, lambda ignore1, ignore2: resp.json())
        except HTTPError as e:
            logger.debug(e.response.text)
            if 400 <= e.response.status_code < 500:
                raise DataPathException(_http_error_message(e), e)
            else:
                raise e


class TableAlias (Table):
    """Represents a table alias.
    """
    def __init__(self, base_table, alias_name):
        """Initializes the table alias.

        :param base_table: the base table to be given an alias name
        :param alias_name: the alias name
        """
        assert isinstance(base_table, Table)
        super(TableAlias, self).__init__(base_table.sname, base_table.name, base_table._table_doc, **base_table._kwargs)
        self._base_table = base_table
        self.name = alias_name
        self._parent = None

    @property
    def uname(self):
        """the url encoded name"""
        return urlquote(self.name)

    @property
    def fqname(self):
        """the url encoded fully qualified name"""
        return self._base_table.fqname

    @property
    def instancename(self):
        return self.uname + ":*"

    @property
    def projection_name(self):
        """In a projection, the object uses this name."""
        return self.instancename

    @property
    def fromname(self):
        return "%s:=%s" % (self.uname, self._base_table.fqname)

    @property
    def path(self):
        """Returns the parent path for this alias.
        """
        if not self._parent:
            self._parent = DataPath(self)
        return self._parent

    @path.setter
    def path(self, value):
        if self._parent:
            raise Exception("Cannot bind a table instance that has already been bound.")
        elif not isinstance(value, DataPath):
            raise Exception("value must be a DataPath instance.")
        self._parent = value

    @property
    def _contextualized_path(self):
        """Returns the path as contextualized for this table instance.

        Conditionally updates the context of the path to which this table instance is bound.
        """
        path = self.path
        if path.context != self:
            path.context = self
        return path

    @property
    def uri(self):
        return self.path._contextualized_uri(self)

    def _query(self, mode='entity', projection=[], group_key=[], context=None):
        """Overridden method to set context of query to this table instance."""
        return self.path._query(mode, projection, group_key=group_key, context=self)


class Column (object):
    """Represents a column in a table.
    """
    def __init__(self, sname, tname, column_doc, **kwargs):
        """Creates a Column object.
        :param sname: schema name
        :param tname: table name
        :param column_doc: column definition document
        :param kwargs: kwargs must include `table` a Table instance
        """
        super(Column, self).__init__()
        assert 'table' in kwargs
        assert isinstance(kwargs['table'], Table)
        self._table = kwargs['table']
        self.sname = sname
        self.tname = tname
        self.name = column_doc['name']
        self.type = column_doc['type']
        self.comment = column_doc['comment']

    def describe(self):
        """Provides a description of the model element.

        :return: a user-friendly string representation of the model element.
        """
        return "Column name: '%s'\tType: %s\tComment: '%s'" % \
               (self.name, self.type['typename'], self.comment)

    def _repr_html_(self):
        return self.describe()

    @property
    def uname(self):
        """the url encoded name"""
        return urlquote(self.name)

    @property
    def fqname(self):
        """the url encoded fully qualified name"""
        return "%s:%s" % (self._table.fqname, self.uname)

    @property
    def instancename(self):
        if isinstance(self._table, TableAlias):
            return "%s:%s" % (self._table.uname, self.uname)
        else:
            return self.uname

    @property
    def projection_name(self):
        """In a projection, the object uses this name."""
        return self.instancename

    @property
    def desc(self):
        """A descending sort modifier based on this column."""
        return SortDescending(self)

    def __str__(self):
        return self.name

    def eq(self, other):
        """Returns an 'equality' comparison predicate.

        :param other: `None` or any other literal value.
        :return: a filter predicate object
        """
        if other is None:
            return ComparisonPredicate(self, "::null::", '')
        else:
            return ComparisonPredicate(self, "=", other)

    __eq__ = eq

    def lt(self, other):
        """Returns a 'less than' comparison predicate.

        :param other: a literal value.
        :return: a filter predicate object
        """
        return ComparisonPredicate(self, "::lt::", other)

    __lt__ = lt

    def le(self, other):
        """Returns a 'less than or equal' comparison predicate.

        :param other: a literal value.
        :return: a filter predicate object
        """
        return ComparisonPredicate(self, "::leq::", other)

    __le__ = le

    def gt(self, other):
        """Returns a 'greater than' comparison predicate.

        :param other: a literal value.
        :return: a filter predicate object
        """
        return ComparisonPredicate(self, "::gt::", other)

    __gt__ = gt

    def ge(self, other):
        """Returns a 'greater than or equal' comparison predicate.

        :param other: a literal value.
        :return: a filter predicate object
        """
        return ComparisonPredicate(self, "::geq::", other)

    __ge__ = ge

    def regexp(self, other):
        """Returns a 'regular expression' comparison predicate.

        :param other: a _string_ literal value.
        :return: a filter predicate object
        """
        if not isinstance(other, str):
            logger.warning("'regexp' method comparison only supports string literals.")
        return ComparisonPredicate(self, "::regexp::", other)

    def ciregexp(self, other):
        """Returns a 'case-insensitive regular expression' comparison predicate.

        :param other: a _string_ literal value.
        :return: a filter predicate object
        """
        if not isinstance(other, str):
            logger.warning("'ciregexp' method comparison only supports string literals.")
        return ComparisonPredicate(self, "::ciregexp::", other)

    def ts(self, other):
        """Returns a 'text search' comparison predicate.

        :param other: a _string_ literal value.
        :return: a filter predicate object
        """
        if not isinstance(other, str):
            logger.warning("'ts' method comparison only supports string literals.")
        return ComparisonPredicate(self, "::ts::", other)

    def alias(self, name):
        """Returns an alias for this column."""
        return ColumnAlias(self, name)


class ColumnAlias (object):
    """Represents an (output) alias for a column instance in a path.
    """
    def __init__(self, base_column, alias_name):
        """Initializes the column alias.

        :param base_column: the base column to be given an alias name
        :param alias_name: the alias name
        """
        assert isinstance(base_column, Column)
        super(ColumnAlias, self).__init__()
        self.name = alias_name
        self.base_column = base_column

    def describe(self):
        """Provides a description of the model element.

        :return: a user-friendly string representation of the model element.
        """
        return "Column name: '%s'\tAlias for: %s" % \
               (self.name, self.base_column.describe())

    def _repr_html_(self):
        return self.describe()

    @property
    def uname(self):
        """the url encoded name"""
        return urlquote(self.name)

    @property
    def fqname(self):
        """the url encoded fully qualified name"""
        return self.base_column.fqname

    @property
    def instancename(self):
        return self.base_column.instancename

    @property
    def projection_name(self):
        """In a projection, the object uses this name."""
        return "%s:=%s" % (self.uname, self.base_column.instancename)

    @property
    def desc(self):
        """A descending sort modifier based on this column."""
        return SortDescending(self)

    def __str__(self):
        return self.name

    def eq(self, other):
        """Returns an 'equality' comparison predicate.

        :param other: `None` or any other literal value.
        :return: a filter predicate object
        """
        return self.base_column.eq(other)

    __eq__ = eq

    def lt(self, other):
        """Returns a 'less than' comparison predicate.

        :param other: a literal value.
        :return: a filter predicate object
        """
        return self.base_column.lt(other)

    __lt__ = lt

    def le(self, other):
        """Returns a 'less than or equal' comparison predicate.

        :param other: a literal value.
        :return: a filter predicate object
        """
        return self.base_column.le(other)

    __le__ = le

    def gt(self, other):
        """Returns a 'greater than' comparison predicate.

        :param other: a literal value.
        :return: a filter predicate object
        """
        return self.base_column.gt(other)

    __gt__ = gt

    def ge(self, other):
        """Returns a 'greater than or equal' comparison predicate.

        :param other: a literal value.
        :return: a filter predicate object
        """
        return self.base_column.ge(other)

    __ge__ = ge

    def regexp(self, other):
        """Returns a 'regular expression' comparison predicate.

        :param other: a _string_ literal value.
        :return: a filter predicate object
        """
        return self.base_column.regexp(other)

    def ciregexp(self, other):
        """Returns a 'case-insensitive regular expression' comparison predicate.

        :param other: a _string_ literal value.
        :return: a filter predicate object
        """
        return self.base_column.ciregexp(other)

    def ts(self, other):
        """Returns a 'text search' comparison predicate.

        :param other: a _string_ literal value.
        :return: a filter predicate object
        """
        return self.base_column.ts(other)


class SortDescending (object):
    """Represents a descending sort condition.
    """
    def __init__(self, attr):
        """Creates sort descending object.

        :param attr: a column, column alias, or aggrfn alias object
        """
        assert isinstance(attr, Column) or isinstance(attr, ColumnAlias) or isinstance(attr, AggregateFunctionAlias)
        self._attr = attr

    @property
    def uname(self):
        """the url encoded name"""
        return urlquote(self._attr.uname) + "::desc::"


class PathOperator (object):
    def __init__(self, r):
        assert isinstance(r, PathOperator) or isinstance(r, Table)
        if isinstance(r, Project):
            raise Exception("Cannot extend a path after an attribute projection")
        self._r = r

    @property
    def _path(self):
        assert isinstance(self._r, PathOperator)
        return self._r._path

    @property
    def _mode(self):
        assert isinstance(self._r, PathOperator)
        return self._r._mode

    def __str__(self):
        return "/%s/%s" % (self._mode, self._path)


class Root (PathOperator):
    def __init__(self, r):
        super(Root, self).__init__(r)
        assert isinstance(r, Table)
        self._table = r

    @property
    def _path(self):
        return self._table.fromname

    @property
    def _mode(self):
        return 'entity'


class ResetContext (PathOperator):
    def __init__(self, r, alias):
        if isinstance(r, ResetContext):
            r = r._r  # discard the previous context reset operator
        super(ResetContext, self).__init__(r)
        assert isinstance(alias, TableAlias)
        self._alias = alias

    @property
    def _path(self):
        assert isinstance(self._r, PathOperator)
        return "%s/$%s" % (self._r._path, self._alias.uname)


class Filter(PathOperator):
    def __init__(self, r, formula):
        super(Filter, self).__init__(r)
        assert isinstance(formula, Predicate)
        self._formula = formula

    @property
    def _path(self):
        assert isinstance(self._r, PathOperator)
        return "%s/%s" % (self._r._path, str(self._formula))


class Project (PathOperator):
    """Projection path component."""

    ENTITY = 'entity'
    ATTRIBUTE = 'attribute'
    AGGREGATE = 'aggregate'
    ATTRGROUP = 'attributegroup'
    MODES = (ENTITY, ATTRIBUTE, AGGREGATE, ATTRGROUP)

    def __init__(self, r, mode=ENTITY, projection=[], group_key=[]):
        """Initializes the projection component.

        :param r: the parent path component.
        :param projection_type: valid type in MODES
        :param projection: projection list
        """
        super(Project, self).__init__(r)
        assert mode in self.MODES
        assert mode == self.ENTITY or mode == self.ATTRGROUP or len(projection) > 0
        assert mode != self.ATTRGROUP or len(group_key) > 0
        self._projection_mode = mode
        self._projection = []
        self._group_key = []

        if mode == self.ATTRIBUTE:
            if not all(isinstance(obj, Table) or isinstance(obj, TableAlias) or isinstance(obj, Column) or isinstance(obj, ColumnAlias) for obj in projection):
                raise ValueError("Only columns or column aliases can be retrieved by an 'attribute' query.")
        elif mode == self.AGGREGATE:
            if not all(isinstance(obj, AggregateFunctionAlias) for obj in projection):
                raise ValueError("Only aggregate function aliases can be retrieved by an 'aggregate' query.")
        elif mode == self.ATTRGROUP:
            if not all(isinstance(obj, Column) or isinstance(obj, ColumnAlias) or isinstance(obj, AggregateFunctionAlias) for obj in projection):
                raise ValueError("Only columns, column aliases, or aggregate function aliases can be retrieved by an 'attributegroup' query.")
            if not all(isinstance(obj, Column) or isinstance(obj, ColumnAlias) or isinstance(obj, AggregateFunctionAlias) for obj in group_key):
                raise ValueError("Only column aliases or aggregate function aliases can be used to group an 'attributegroup' query.")
            self._group_key = [obj.projection_name for obj in group_key]

        self._projection = [obj.projection_name for obj in projection]

    @property
    def _path(self):
        assert isinstance(self._r, PathOperator)
        projection = ','.join(self._projection)
        if self._projection_mode == self.ATTRGROUP:
            assert self._group_key
            grouping = ','.join(self._group_key)
            return "%s/%s;%s" % (self._r._path, grouping, projection)
        else:
            return "%s/%s" % (self._r._path, projection)

    @property
    def _mode(self):
        return self._projection_mode


class Link (PathOperator):
    def __init__(self, r, on, as_=None, join_type=''):
        super(Link, self).__init__(r)
        assert isinstance(on, ComparisonPredicate) or isinstance(on, Table) or (
                isinstance(on, ConjunctionPredicate) and on.is_valid_join_condition)
        assert as_ is None or isinstance(as_, TableAlias)
        assert join_type == '' or (join_type in ('left', 'right', 'full') and isinstance(on, Predicate))
        self._on = on
        self._as = as_
        self._join_type = join_type

    @property
    def _path(self):
        assert isinstance(self._r, PathOperator)
        assign = '' if self._as is None else "%s:=" % self._as.uname
        if isinstance(self._on, Table):
            cond = self._on.fqname
        elif isinstance(self._on, ComparisonPredicate):
            cond = str(self._on)
        elif isinstance(self._on, ConjunctionPredicate):
            cond = self._on.as_join_condition
        else:
            raise DataPathException("Invalid join condition: " + str(self._on))
        return "%s/%s%s%s" % (self._r._path, assign, self._join_type, cond)


class Predicate (object):
    """Common base class for all predicate types."""

    def and_(self, other):
        """Returns a conjunction predicate.

        :param other: a predicate object.
        :return: a junction predicate object.
        """
        if not isinstance(other, Predicate):
            raise ValueError("Invalid comparison with object that is not a Predicate instance.")
        return ConjunctionPredicate([self, other])

    __and__ = and_

    def or_(self, other):
        """Returns a disjunction predicate.

        :param other: a predicate object.
        :return: a junction predicate object.
        """
        if not isinstance(other, Predicate):
            raise ValueError("Invalid comparison with object that is not a Predicate instance.")
        return DisjunctionPredicate([self, other])

    __or__ = or_

    def negate(self):
        """Returns a negation predicate.

        This predicate is wrapped in a negation predicate which is returned to the caller.

        :return: a negation predicate object.
        """
        return NegationPredicate(self)

    __invert__ = negate


class ComparisonPredicate (Predicate):
    def __init__(self, lop, op, rop):
        super(ComparisonPredicate, self).__init__()
        assert isinstance(lop, Column)
        assert isinstance(rop, Column) or isinstance(rop, int) or \
            isinstance(rop, float) or isinstance(rop, str) or \
            isinstance(rop, date)
        assert isinstance(op, str)
        self._lop = lop
        self._op = op
        self._rop = rop

    @property
    def is_equality(self):
        return self._op == '='

    @property
    def left(self):
        return self._lop

    @property
    def right(self):
        return self._rop

    def __str__(self):
        if isinstance(self._rop, Column):
            # The only valid circumstance for a Column rop is in a link 'on' predicate for simple key/fkey joins
            return "(%s)=(%s)" % (self._lop.instancename, self._rop.fqname)
        else:
            # All other comparisons are serialized per the usual form
            return "%s%s%s" % (self._lop.instancename, self._op, urlquote(str(self._rop)))


class JunctionPredicate (Predicate):
    def __init__(self, op, operands):
        super(JunctionPredicate, self).__init__()
        assert operands and hasattr(operands, '__iter__') and len(operands) > 1
        assert all(isinstance(operand, Predicate) for operand in operands)
        assert isinstance(op, str)
        self._operands = operands
        self._op = op

    def __str__(self):
        return self._op.join(["(%s)" % operand for operand in self._operands])


class ConjunctionPredicate (JunctionPredicate):
    def __init__(self, operands):
        super(ConjunctionPredicate, self).__init__('&', operands)

    def and_(self, other):
        return ConjunctionPredicate(self._operands + [other])

    @property
    def is_valid_join_condition(self):
        """Tests if this conjunction is a valid join condition."""
        return all(isinstance(o, ComparisonPredicate) and o.is_equality for o in self._operands)

    @property
    def as_join_condition(self):
        """Returns the conjunction in the 'join condition' serialized format."""
        lhs = []
        rhs = []

        for operand in self._operands:
            assert isinstance(operand, ComparisonPredicate) and operand.is_equality
            assert isinstance(operand.left, Column)
            assert isinstance(operand.right, Column)
            lhs.append(operand.left)
            rhs.append(operand.right)

        return "({left})=({right})".format(
            left=",".join(lop.instancename for lop in lhs),
            right=",".join(rop.fqname for rop in rhs)
        )


class DisjunctionPredicate (JunctionPredicate):
    def __init__(self, operands):
        super(DisjunctionPredicate, self).__init__(';', operands)

    def or_(self, other):
        return DisjunctionPredicate(self._operands + [other])


class NegationPredicate (Predicate):
    def __init__(self, child):
        super(NegationPredicate, self).__init__()
        assert isinstance(child, Predicate)
        self._child = child

    def __str__(self):
        return "!(%s)" % self._child


class AggregateFunction (object):
    """Base class of all aggregate functions."""
    def __init__(self, op, operand):
        """Initializes the aggregate function.

        :param op: name of the function per ERMrest specification.
        :param operand: single operand of the function; a Column, Table, or TableAlias object.
        """
        super(AggregateFunction, self).__init__()
        self.op = op
        self.operand = operand

    def __str__(self):
        return "%s(%s)" % (self.op, self.operand)

    @property
    def instancename(self):
        return "%s(%s)" % (self.op, self.operand.instancename)

    def alias(self, alias_name):
        """Returns an (output) alias for this aggregate function instance."""
        return AggregateFunctionAlias(self, alias_name)


class Min (AggregateFunction):
    """Aggregate function for minimum non-NULL value."""
    def __init__(self, operand):
        super(Min, self).__init__('min', operand)


class Max (AggregateFunction):
    """Aggregate function for maximum non-NULL value."""
    def __init__(self, operand):
        super(Max, self).__init__('max', operand)


class Sum (AggregateFunction):
    """Aggregate function for sum of non-NULL values."""
    def __init__(self, operand):
        super(Sum, self).__init__('sum', operand)


class Avg (AggregateFunction):
    """Aggregate function for average of non-NULL values."""
    def __init__(self, operand):
        super(Avg, self).__init__('avg', operand)


class Cnt (AggregateFunction):
    """Aggregate function for count of non-NULL values."""
    def __init__(self, operand):
        super(Cnt, self).__init__('cnt', operand)


class CntD (AggregateFunction):
    """Aggregate function for count of distinct non-NULL values."""
    def __init__(self, operand):
        super(CntD, self).__init__('cnt_d', operand)


class Array (AggregateFunction):
    """Aggregate function for an array containing all values (including NULL)."""
    def __init__(self, operand):
        super(Array, self).__init__('array', operand)


class ArrayD (AggregateFunction):
    """Aggregate function for an array containing distinct values (including NULL)."""
    def __init__(self, operand):
        super(ArrayD, self).__init__('array_d', operand)


class Bin (AggregateFunction):
    """Binning function."""
    def __init__(self, operand, nbins, minval=None, maxval=None):
        """Initialize the bin function.

        If `minval` or `maxval` are not given, they will be set based on the min and/or max values for the column
        (`operand` parameter) as determined by issuing an aggregate query over the current data path.

        :param operand: a column or aliased column instance
        :param nbins: number of bins
        :param minval: minimum value (optional)
        :param maxval: maximum value (optional)
        """
        super(Bin, self).__init__('bin', operand)
        if not (isinstance(operand, Column) or isinstance(operand, ColumnAlias)):
            raise ValueError("Bin operand must be a column or column alias")
        self.nbins = nbins
        self.minval = minval
        self.maxval = maxval

    def __str__(self):
        return "%s(%s;%s;%s;%s)" % (self.op, self.operand, self.nbins, self.minval, self.maxval)

    @property
    def instancename(self):
        return "%s(%s;%s;%s;%s)" % (self.op, self.operand.instancename, self.nbins, self.minval, self.maxval)


class AggregateFunctionAlias (object):
    """Alias for aggregate functions."""
    def __init__(self, fn, alias_name):
        """Initializes the aggregate function alias.

        :param fn: aggregate function instance
        :param alias_name: alias name
        """
        super(AggregateFunctionAlias, self).__init__()
        assert isinstance(fn, AggregateFunction)
        self.fn = fn
        self.name = alias_name

    def __str__(self):
        return str(self.fn)

    @property
    def uname(self):
        return urlquote(self.name)

    @property
    def projection_name(self):
        """In a projection, the object uses this name."""
        return "%s:=%s" % (self.uname, self.fn.instancename)

    @property
    def desc(self):
        """A descending sort modifier based on this alias."""
        return SortDescending(self)


class AttributeGroup (object):
    """A computed attribute group."""
    def __init__(self, source, queryfn, keys):
        """Initializes an attribute group instance.

        :param source: the source object for the group (DataPath, Table, TableAlias)
        :param queryfn: a query function that takes mode, projection, and group_key parameters
        :param keys: an iterable collection of group keys
        """
        super(AttributeGroup, self).__init__()
        assert any(isinstance(source, valid_type) for valid_type in [DataPath, Table, TableAlias])
        assert isinstance(keys, tuple)
        if not keys:
            raise ValueError("No groupby keys.")
        self._source = source
        self._queryfn = queryfn
        self._grouping_keys = list(keys)

    def attributes(self, *attributes):
        """Returns a results set of attributes projected and optionally renamed from this group.

        :param attributes: the columns, aliased columns, and/or aliased aggregate functions to be retrieved for this group.
        :return: a results set of the projected attributes from this group.
        """
        self._resolve_binning_ranges()
        return self._queryfn(mode=Project.ATTRGROUP, projection=list(attributes), group_key=self._grouping_keys)

    def _resolve_binning_ranges(self):
        """Helper method to resolve any unspecified binning ranges."""
        for key in self._grouping_keys:
            if isinstance(key, AggregateFunctionAlias) and isinstance(key.fn, Bin):
                bin = key.fn
                aggrs = []
                if bin.minval is None:
                    aggrs.append(Min(bin.operand).alias('minval'))
                if bin.maxval is None:
                    aggrs.append(Max(bin.operand).alias('maxval'))
                if aggrs:
                    result = self._source.aggregates(*aggrs)[0]
                    bin.minval = result.get('minval', bin.minval)
                    bin.maxval = result.get('maxval', bin.maxval)
                    if (bin.minval is None) or (bin.maxval is None):
                        raise ValueError('Automatic determination of binning bounds failed.')
