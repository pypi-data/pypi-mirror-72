import json
from collections import OrderedDict
from . import urlquote


class AttrDict (dict):
    """Dictionary with optional attribute-based lookup.

       For keys that are valid attributes, self.key is equivalent to
       self[key].
    """
    def __getattr__(self, a):
        try:
            return self[a]
        except KeyError as e:
            raise AttributeError(str(e))

    def __setattr__(self, a, v):
        self[a] = v

    def update(self, d):
        dict.update(self, d)

# convenient enumeration of common annotation tags
tag = AttrDict({
    'generated':          'tag:isrd.isi.edu,2016:generated',
    'immutable':          'tag:isrd.isi.edu,2016:immutable',
    'display':            'tag:misd.isi.edu,2015:display',
    'visible_columns':    'tag:isrd.isi.edu,2016:visible-columns',
    'visible_foreign_keys': 'tag:isrd.isi.edu,2016:visible-foreign-keys',
    'foreign_key':        'tag:isrd.isi.edu,2016:foreign-key',
    'table_display':      'tag:isrd.isi.edu,2016:table-display',
    'table_alternatives': 'tag:isrd.isi.edu,2016:table-alternatives',
    'column_display':     'tag:isrd.isi.edu,2016:column-display',
    'asset':              'tag:isrd.isi.edu,2017:asset',
    'bulk_upload':        'tag:isrd.isi.edu,2017:bulk-upload',
    'export':             'tag:isrd.isi.edu,2016:export',
    'chaise_config':      'tag:isrd.isi.edu,2019:chaise-config',
})

def presence_annotation(tag_uri):
    """Decorator to establish property getter/setter/deleter for presence annotations.

       Usage example:

          @presence_annotation(tag.generated)
          def generated(self): pass

       The stub method will be discarded.
    """
    def helper(ignore):
        docstr = "Convenience property for managing presence of annotation %s" % tag_uri

        def getter(self):
            return tag_uri in self.annotations

        def setter(self, present):
            if present:
                self.annotations[tag_uri] = None
            else:
                self.annotations.pop(tag_uri, None)

        def deleter(self):
            self.annotations.pop(tag_uri, None)

        return property(getter, setter, deleter, docstr)

    return helper

def object_annotation(tag_uri):
    """Decorator to establish property getter/setter/deleter for object annotations.

       Usage example:

          @presence_annotation(tag.display)
          def display(self): pass

       The stub method will be discarded.
    """
    def helper(ignore):
        docstr = "Convenience property for managing content of object annotation %s" % tag_uri

        def getter(self):
            if tag_uri not in self.annotations:
                self.annotations[tag_uri] = AttrDict({})
            return self.annotations[tag_uri]

        def setter(self, value):
            if not isinstance(value, (dict, AttrDict)):
                raise TypeError('Unexpected object type %s for annotation %s' % (type(value), tag_uri))
            self.annotations[tag_uri] = AttrDict(value)

        def deleter(self):
            self.annotations.pop(tag_uri, None)

        return property(getter, setter, deleter, docstr)

    return helper

def equivalent(doc1, doc2, method=None):
    """Determine whether two dict/array/literal documents are structurally equivalent."""
    if method == 'acl_binding':
        # fill in defaults to avoid some false negatives on acl binding comparison
        if not isinstance(doc1, dict):
            return False
        def canonicalize(d):
            if not isinstance(d, dict):
                return d
            def helper(b):
                if not isinstance(b, dict):
                    return b
                return {
                    'projection': b['projection'],
                    'projection_type': b.get('projection_type'), # we can't provide default w/o type inference!
                    'types': b['types'],
                    'scope_acl': b.get('scope_acl', ['*']), # this is a common omission...
                }
            return {
                binding_name: helper(binding)
                for binding_name, binding in d.items()
            }
        return equivalent(canonicalize(doc1), canonicalize(doc2))
    elif isinstance(doc1, dict) and isinstance(doc2, dict):
        return equivalent(sorted(doc1.items()), sorted(doc2.items()))
    elif isinstance(doc1, (list, tuple)) and isinstance(doc2, (list, tuple)):
        if len(doc1) != len(doc2):
            return False
        for e1, e2 in zip(doc1, doc2):
            if not equivalent(e1, e2):
                return False
        return True
    return doc1 == doc2

class NodeConfig (object):
    """Generic model document node configuration management.

       annotations: map of annotations for node by key
       comment: comment string or None (if supported by sub-class)

       Convenience access for common annotations:
         self.display: access mutable tag.display object
         self.generated: treat tag.generated as a boolean
         self.immutable: treat tag.immutable as a boolean
    """
    def __init__(self, node_doc):
        self.annotations = dict(node_doc.get('annotations', {}))
        self._supports_comment = True
        self._comment = node_doc.get('comment')

    @property
    def catalog(self):
        raise NotImplementedError('derived classes MUST define self.catalog property')

    @property
    def uri_path(self):
        """URI to this model resource."""
        raise NotImplementedError('Subclasses need their own URI path properties.')

    @property
    def update_uri_path(self):
        """URI to use as base for sub-resources ./comment ./annotation etc."""
        # normally this is the same as uri_path, but a subclass may need to override
        return self.uri_path

    def apply(self, existing=None):
        """Apply configuration to corresponding node in catalog unless existing already matches.

        :param existing: An instance comparable to self, or None to apply configuration unconditionally.

        The configuration in self.comment and self.annotations will be
        applied to the remote model node corresponding to self, unless
        existing node configuration is supplied and is equivalent.
        """
        if self._supports_comment:
            if existing is None or not equivalent(self._comment, existing._comment):
                if self._comment is not None:
                    self.catalog.put('%s/comment' % self.update_uri_path, data=self._comment)
                else:
                    self.catalog.delete('%s/comment' % self.update_uri_path)
        if existing is None or not equivalent(self.annotations, existing.annotations):
            try:
                self.catalog.put(
                    '%s/%s' % (self.update_uri_path, 'annotation'),
                    json=self.annotations
                )
            except TypeError as e:
                raise TypeError('Bad %s/annotation' % (self.update_uri_path, self.annotations)) from e

    def clear(self, clear_comment=False):
        """Clear existing annotations on node, also clearing comment if clear_comment is True.

        NOTE: as a backwards-compatible heuristic, comments are
        retained by default so that a typical configuration-management
        client does not strip useful documentation from existing models.

        """
        self.annotations.clear()
        if clear_comment and self._supports_comment:
            self.comment = None

    def prejson(self):
        """Produce a representation of configuration as generic Python data structures"""
        d = dict()
        if self.annotations:
            d["annotations"] = self.annotations
        return d

    @property
    def comment(self):
        """Comment on this node in model, if supported.

        Raises TypeError if accessed when unsupported, e.g. on top-level catalog objects.
        """
        if self._supports_comment:
            return self._comment
        else:
            raise TypeError('%r does not support comment management.' % type(self).__name__)

    @comment.setter
    def comment(self, value):
        """Comment on this node in model, if supported.

        Raises TypeError if accessed when unsupported, e.g. on top-level catalog objects.
        """
        if self._supports_comment:
            self._comment = value
        else:
            raise TypeError('%r does not support comment management.' % type(self).__name__)

    @presence_annotation(tag.immutable)
    def immutable(self): pass

    @presence_annotation(tag.generated)
    def generated(self): pass

    @object_annotation(tag.display)
    def display(self): pass

class NodeConfigAcl (NodeConfig):
    """Generic model acl-bearing document node configuration management.

       acls: map of acls for node by key
       annotations: map of annotations for node by key
       comment: comment string or None (if supported by sub-class)

       Convenience access for common annotations:
         self.display: access mutable tag.display object
         self.generated: treat tag.generated as a boolean
         self.immutable: treat tag.immutable as a boolean
    """
    def __init__(self, node_doc):
        NodeConfig.__init__(self, node_doc)
        self.acls = AttrDict(node_doc.get('acls', {}))

    def apply(self, existing=None):
        """Apply configuration to corresponding node in catalog unless existing already matches.

        :param existing: An instance comparable to self, or None to apply configuration unconditionally.

        The configuration in self.comment, self.annotations, and
        self.acls will be applied to the remote model node
        corresponding to self, unless existing node configuration is
        supplied and is equivalent.

        """
        NodeConfig.apply(self, existing)
        if existing is None or not equivalent(self.acls, existing.acls):
            self.catalog.put(
                '%s/%s' % (self.update_uri_path, 'acl'),
                json=self.acls
            )

    def clear(self):
        """Clear existing acls and annotations on node."""
        NodeConfig.clear(self)
        self.acls.clear()

    def prejson(self):
        """Produce a representation of configuration as generic Python data structures"""
        d = NodeConfig.prejson(self)
        if self.acls:
            d["acls"] = self.acls
        return d


class NodeConfigAclBinding (NodeConfigAcl):
    """Generic model acl_binding-bearing document node configuration management.

       acl_bindings: map of acl bindings for node by key
       acls: map of acls for node by key
       annotations: map of annotations for node by key
       comment: comment string or None (if supported by sub-class)

       Convenience access for common annotations:
         self.display: access mutable tag.display object
         self.generated: treat tag.generated as a boolean
         self.immutable: treat tag.immutable as a boolean
    """
    def __init__(self, node_doc):
        NodeConfigAcl.__init__(self, node_doc)
        self.acl_bindings = AttrDict(node_doc.get('acl_bindings', {}))

    def apply(self, existing=None):
        """Apply configuration to corresponding node in catalog unless existing already matches.

        :param existing: An instance comparable to self, or None to apply configuration unconditionally.

        The configuration in self.comment, self.annotations,
        self.acls, and self.acl_bindings will be applied to the remote
        model node corresponding to self, unless existing node
        configuration is supplied and is equivalent.

        """
        NodeConfigAcl.apply(self, existing)
        if existing is None or not equivalent(self.acl_bindings, existing.acl_bindings, method='acl_binding'):
            self.catalog.put(
                '%s/%s' % (self.update_uri_path, 'acl_binding'),
                json=self.acl_bindings
            )

    def clear(self):
        """Clear existing acl_bindings, acls, and annotations on node."""
        NodeConfigAcl.clear(self)
        self.acl_bindings.clear()

    def prejson(self):
        """Produce a representation of configuration as generic Python data structures"""
        d = NodeConfigAcl.prejson(self)
        if self.acl_bindings:
            d["acl_bindings"] = self.acl_bindings
        return d

class CatalogConfig (NodeConfigAcl):
    """Top-level catalog configuration management.

       acls: catalog-level ACL configuration
       annotations: catalog-level annotations
       schemas: all schemas in catalog, by name
    """
    def __init__(self, catalog, model_doc, **kwargs):
        self._catalog = catalog
        NodeConfigAcl.__init__(self, model_doc)
        self._supports_comment = False
        self._pseudo_fkeys = {}
        self.schemas = {
            sname: kwargs.get('schema_class', CatalogSchema)(self, sname, sdoc, **kwargs)
            for sname, sdoc in model_doc.get('schemas', {}).items()
        }
        self.digest_fkeys()

    def digest_fkeys(self):
        """Finish second-pass digestion of foreign key definitions using full model w/ all schemas and tables.
        """
        for schema in self.schemas.values():
            for referer in schema.tables.values():
                for fkey in list(referer.foreign_keys):
                    try:
                        fkey.digest_referenced_columns(self)
                    except KeyError:
                        del referer.foreign_keys[fkey.name]

    @property
    def catalog(self):
        return self._catalog

    @property
    def uri_path(self):
        """URI to this model resource."""
        return "/schema"

    @property
    def update_uri_path(self):
        """URI to use as base for sub-resources ./acl ./annotation etc."""
        # we get whole catalog schema at /schema
        # but we get whole catalog sub-resources at /acl etc.
        return ""

    @classmethod
    def fromcatalog(cls, catalog):
        """Retrieve catalog config as a CatalogConfig management object."""
        return cls(catalog, catalog.get("/schema").json())

    @classmethod
    def fromfile(cls, catalog, schema_file):
        """Deserialize a JSON schema file as a CatalogConfig management object."""
        with open(schema_file) as sf:
            schema = sf.read()

        return cls(catalog, json.loads(schema, object_pairs_hook=OrderedDict))

    def apply(self, existing=None):
        """Apply catalog configuration to catalog unless existing already matches.

        :param existing: An instance comparable to self.

        The configuration in self will be applied recursively to the
        corresponding model nodes in schema. For each node, the
        comment, annotations, acls, and/or acl_bindings will be
        applied where applicable.

        If existing is not provided (default), the current whole
        configuration will be retrieved from the catalog and used
        automatically to determine whether the configuration goals
        under this CatalogConfig instance are already met or need to
        be remotely applied.

        """
        if existing is None:
            existing = self.fromcatalog(self.catalog)
        NodeConfigAcl.apply(self, existing)
        for sname, schema in self.schemas.items():
            schema.apply(existing.schemas[sname])

    def clear(self):
        """Clear all configuration in catalog and children."""
        NodeConfigAcl.clear(self)
        for schema in self.schemas.values():
            schema.clear()

    def table(self, sname, tname):
        """Return table configuration for table with given name."""
        return self.schemas[sname].tables[tname]

    def column(self, sname, tname, cname):
        """Return column configuration for column with given name."""
        return self.table(sname, tname).column_definitions[cname]

    def fkey(self, constraint_name_pair):
        """Return configuration for foreign key with given name pair.

        Accepts (schema_name, constraint_name) pairs as found in many
        faceting annotations and (schema_obj, constraint_name) pairs
        as found in fkey.name fields.

        """
        sname, cname = constraint_name_pair
        if isinstance(sname, CatalogSchema):
            if self.schemas[sname.name] is sname:
                return sname._fkeys[cname]
            else:
                raise ValueError('schema object %s is not from same model tree' % (sname,))
        elif sname is None or sname == '':
            return self._pseudo_fkeys[cname]
        else:
            return self.schemas[sname]._fkeys[cname]

    @object_annotation(tag.bulk_upload)
    def bulk_upload(self): pass

    def prejson(self, prune=True):
        """Produce a representation of configuration as generic Python data structures"""
        d = NodeConfigAcl.prejson(self)
        d["schemas"] = {
            sname: schema.prejson()
            for sname, schema in self.schemas.items()
        }
        return d

class CatalogSchema (NodeConfigAcl):
    """Schema-level configuration management.

       acls: schema-level ACL configuration
       annotations: schema-level annotations
       comment: schema-level comment string
       tables: all tables in schema, by name

       Convenience access for common annotations:
         self.display: access mutable tag.display object
    """
    def __init__(self, model, sname, schema_doc, **kwargs):
        NodeConfigAcl.__init__(self, schema_doc)
        self.model = model
        self.name = sname
        self._fkeys = {}
        self.tables = {
            tname: kwargs.get('table_class', CatalogTable)(self, tname, tdoc, **kwargs)
            for tname, tdoc in schema_doc.get('tables', {}).items()
        }

    @property
    def catalog(self):
        return self.model.catalog

    @property
    def uri_path(self):
        """URI to this model resource."""
        return "/schema/%s" % urlquote(self.name)

    def apply(self, existing=None):
        """Apply schema configuration to catalog unless existing already matches.

        :param existing: An instance comparable to self.

        The configuration in self will be applied recursively to the
        corresponding model nodes in catalog. For each node, the
        comment, annotations, acls, and/or acl_bindings will be
        applied where applicable unless existing value is equivalent.

        """
        NodeConfigAcl.apply(self, existing)
        for tname, table in self.tables.items():
            table.apply(existing.tables[tname] if existing else None)

    def clear(self):
        """Clear all configuration in schema and children."""
        NodeConfigAcl.clear(self)
        for table in self.tables.values():
            table.clear()

    def prejson(self, prune=True):
        """Produce a representation of configuration as generic Python data structures"""
        d = NodeConfigAcl.prejson(self)
        d["schema_name"] = self.name
        d["tables"] = {
            tname: table.prejson()
            for tname, table in self.tables.items()
        }
        return d

class KeyedList (list):
    """Keyed list."""
    def __init__(self, l):
        list.__init__(self, l)
        self.elements = {
            e.name: e
            for e in l
        }

    def __getitem__(self, idx):
        """Get element by key or by list index or slice."""
        if isinstance(idx, (int, slice)):
            return list.__getitem__(self, idx)
        else:
            return self.elements[idx]

    def __delitem__(self, idx):
        """Delete element by key or by list index or slice."""
        if isinstance(idx, int):
            victim = list.__getitem__(self, idx)
            list.__delitem__(self, idx)
            del self.elements[victim.name]
        elif isinstance(idx, slice):
            victims = [list.__getitem__(self, idx)]
            list.__delslice__(self, idx)
            for victim in victims:
                del self.elements[victim.name]
        else:
            victim = self.elements[idx]
            list.__delitem__(self, self.index(victim))
            del self.elements[victim.name]

    def append(self, e):
        """Append element to list and record its key."""
        if e.name in self.elements:
            raise ValueError('Element name %s already exists.' % (e.name,))
        list.append(self, e)
        self.elements[e.name] = e

class CatalogTable (NodeConfigAclBinding):
    """Table-level configuration management.

       acl_bindings: table-level dynamic ACL bindings
       acls: table-level ACL configuration
       annotations: table-level annotations
       column_definitions: columns in table
       comment: table-level comment string

       Convenience access to common annotations:
         self.alternatives: tag.table_alternatives object
         self.display: tag.display object
         self.generated: treat tag.generated as a boolean
         self.immutable: treat tag.immutable as a boolean
         self.table_display: tag.table_display object
         self.visible_columns: tag.visible_columns object
         self.visible_foreign_keys: tag.visible_foreign_keys object
    """

    def __init__(self, schema, tname, table_doc, **kwargs):
        NodeConfigAclBinding.__init__(self, table_doc)
        self.schema = schema
        self.name = tname
        self.column_definitions = KeyedList([
            kwargs.get('column_class', CatalogColumn)(self, cdoc, **kwargs)
            for cdoc in table_doc.get('column_definitions', [])
        ])
        self.keys = KeyedList([
            kwargs.get('key_class', CatalogKey)(self, kdoc, **kwargs)
            for kdoc in table_doc.get('keys', [])
        ])
        self.foreign_keys = KeyedList([
            kwargs.get('foreign_key_class', CatalogForeignKey)(self, fkdoc, **kwargs)
            for fkdoc in table_doc.get('foreign_keys', [])
        ])
        self.referenced_by = KeyedList([])

    @property
    def columns(self):
        """Sugared access to self.column_definitions"""
        return self.column_definitions

    @property
    def catalog(self):
        return self.schema.model.catalog

    @property
    def uri_path(self):
        """URI to this model element."""
        return "%s/table/%s" % (self.schema.uri_path, urlquote(self.name))

    def apply(self, existing=None):
        """Apply table configuration to catalog unless existing already matches.

        :param existing: An instance comparable to self.

        The configuration in self will be applied recursively to the
        corresponding model nodes in catalog. For each node, the
        comment, annotations, acls, and/or acl_bindings will be
        applied where applicable unless existing is supplied and is
        equivalent.

        """
        NodeConfigAclBinding.apply(self, existing)
        for col in self.column_definitions:
            col.apply(existing.column_definitions[col.name] if existing else None)
        for key in self.keys:
            key.apply(existing.keys[key.name_in_model(existing.schema.model)] if existing else None)
        for fkey in self.foreign_keys:
            fkey.apply(existing.foreign_keys[fkey.name_in_model(existing.schema.model)] if existing else None)

    def clear(self):
        """Clear all configuration in table and children."""
        NodeConfigAclBinding.clear(self)
        for col in self.column_definitions:
            col.clear()
        for key in self.keys:
            key.clear()
        for fkey in self.foreign_keys:
            fkey.clear()

    def prejson(self, prune=True):
        """Produce a representation of configuration as generic Python data structures"""
        d = NodeConfigAclBinding.prejson(self)
        d.update({
            "schema_name": self.schema.name,
            "table_name": self.name,
            "column_definitions": [
                c.prejson()
                for c in self.column_definitions
            ],
            "keys": [
                key.prejson()
                for key in self.keys
            ],
            "foreign_keys": [
                fkey.prejson()
                for fkey in self.foreign_keys
            ]
        })
        return d

    def _own_column(self, column):
        if isinstance(column, CatalogColumn):
            if self.column_definitions[column.name] is column:
                return column
            raise ValueError('column %s object is not from this table object' % (column,))
        elif column in self.column_definitions.elements:
            return self.column_definitions[column]
        raise ValueError('value %s does not name a defined column in this table' % (column,))

    def key_by_columns(self, unique_columns, raise_nomatch=True):
        """Return key from self.keys with matching unique columns.

        unique_columns: iterable of column instances or column names
        raise_nomatch: for True, raise KeyError on non-match, else return None
        """
        cset = { self._own_column(c) for c in unique_columns }
        for key in self.keys:
            if cset == { c for c in key.unique_columns }:
                return key
        if raise_nomatch:
            raise KeyError(cset)

    def fkeys_by_columns(self, from_columns, partial=False, raise_nomatch=True):
        """Iterable of fkeys from self.foreign_keys with matching columns.

        from_columns: iterable of referencing column instances or column names
        partial: include fkeys which cover a superset of from_columns
        raise_nomatch: for True, raise KeyError on empty iterable
        """
        cset = { self._own_column(c) for c in from_columns }
        if not cset:
            raise ValueError('from_columns must be non-empty')
        to_table = None
        for fkey in self.foreign_keys:
            fkey_cset = set(fkey.foreign_key_columns)
            if cset == fkey_cset or partial and cset.issubset(fkey_cset):
                raise_nomatch = False
                yield fkey
        if raise_nomatch:
            raise KeyError(cset)

    def fkey_by_column_map(self, from_to_map, raise_nomatch=True):
        """Return fkey from self.foreign_keys with matching {referencing: referenced} column mapping.

        from_to_map: dict-like mapping with items() method yielding (from_col, to_col) pairs
        raise_nomatch: for True, raise KeyError on non-match, else return None
        """
        colmap = {
            self._own_column(from_col): to_col
            for from_col, to_col in from_to_map.items()
        }
        if not colmap:
            raise ValueError('column mapping must be non-empty')
        to_table = None
        for c in colmap.values():
            if to_table is None:
                to_table = c.table
            elif to_table is not c.table:
                raise ValueError('to-columns must all be part of same table')
        for fkey in self.foreign_keys:
            if colmap == fkey.column_map:
                return fkey
        if raise_nomatch:
            raise KeyError(from_to_map)

    def is_association(self, min_arity=2, max_arity=2, unqualified=True, pure=True, no_overlap=True):
        """Return (truthy) integer arity if self is a matching association, else False.

        min_arity: minimum number of associated fkeys (default 2)
        max_arity: maximum number of associated fkeys (default 2) or None
        unqualified: reject qualified associations when True (default True)
        pure: reject impure assocations when True (default True)
        no_overlap: reject overlapping associations when True (default True)

        The default behavior with no arguments is to test for pure,
        unqualified, non-overlapping, binary assocations.

        An association is comprised of several foreign keys which are
        covered by a non-nullable composite row key. This allows
        specific combinations of foreign keys to appear at most once.

        The arity of an association is the number of foreign keys
        being associated. A typical binary association has arity=2.

        An unqualified association contains *only* the foreign key
        material in its row key. Conversely, a qualified association
        mixes in other material which means that a specific
        combination of foreign keys may repeat with different
        qualifiers.

        A pure association contains *only* row key
        material. Conversely, an impure association includes
        additional metadata columns not covered by the row key. Unlike
        qualifiers, impure metadata merely decorates an association
        without augmenting its identifying characteristics.

        A non-overlapping association does not share any columns
        between multiple foreign keys. This means that all
        combinations of foreign keys are possible. Conversely, an
        overlapping association shares some columns between multiple
        foreign keys, potentially limiting the combinations which can
        be represented in an association row.

        These tests ignore the five ERMrest system columns and any
        corresponding constraints.

        """
        if min_arity < 2:
            raise ValueError('An assocation cannot have arity < 2')
        if max_arity is not None and max_arity < min_arity:
            raise ValueError('max_arity cannot be less than min_arity')

        # TODO: revisit whether there are any other cases we might
        # care about where system columns are involved?
        non_sys_cols = {
            col
            for col in self.column_definitions
            if col.name not in {'RID', 'RCT', 'RMT', 'RCB', 'RMB'}
        }
        non_sys_key_colsets = {
            frozenset(key.unique_columns)
            for key in self.keys
            if set(key.unique_columns).issubset(non_sys_cols)
            and len(key.unique_columns) > 1
        }

        if not non_sys_key_colsets:
            # reject: not association
            return False

        # choose longest compound key (arbitrary choice with ties!)
        row_key = sorted(non_sys_key_colsets, key=lambda s: len(s), reverse=True)[0]
        covered_fkeys = {
            fkey
            for fkey in self.foreign_keys
            if set(fkey.foreign_key_columns).issubset(row_key)
        }
        covered_fkey_cols = set()

        if len(covered_fkeys) < min_arity:
            # reject: not enough fkeys in association
            return False
        elif max_arity is not None and len(covered_fkeys) > max_arity:
            # reject: too many fkeys in association
            return False

        for fkey in covered_fkeys:
            fkcols = set(fkey.foreign_key_columns)
            if no_overlap and fkcols.intersection(covered_fkey_cols):
                # reject: overlapping fkeys in association
                return False
            covered_fkey_cols.update(fkcols)

        if unqualified and row_key.difference(covered_fkey_cols):
            # reject: qualified association
            return False

        if pure and non_sys_cols.difference(row_key):
            # reject: impure association
            return False

        # return (truthy) arity
        return len(covered_fkeys)

    @object_annotation(tag.table_alternatives)
    def alternatives(self): pass

    @object_annotation(tag.table_display)
    def table_display(self): pass

    @object_annotation(tag.visible_columns)
    def visible_columns(self): pass

    @object_annotation(tag.visible_foreign_keys)
    def visible_foreign_keys(self): pass

class CatalogColumn (NodeConfigAclBinding):
    """Column-level configuration management.

       acl_bindings: column-level dynamic ACL bindings
       acls: column-level ACL configuration
       annotations: column-level annotations
       comment: column-level comment string
       name: name of column

       Convenience access to common annotations:
         self.asset: tag.asset object
         self.column_display:: tag.column_display object
         self.display: tag.display object
         self.generated: treat tag.generated as a boolean
         self.immutable: treat tag.immutable as a boolean
    """

    def __init__(self, table, column_doc, **kwargs):
        cname = column_doc['name']
        NodeConfigAclBinding.__init__(self, column_doc)
        self.table = table
        self.name = cname

    @property
    def catalog(self):
        return self.table.schema.model.catalog

    @property
    def uri_path(self):
        """URI to this model resource."""
        return "%s/column/%s" % (self.table.uri_path, urlquote(self.name))

    def prejson_colref(self):
        return {
            "schema_name": self.table.schema.name,
            "table_name": self.table.name,
            "column_name": self.name,
        }

    def prejson(self, prune=True):
        """Produce a representation of configuration as generic Python data structures"""
        d = NodeConfig.prejson(self)
        d["name"] = self.name
        return d

    @object_annotation(tag.asset)
    def asset(self): pass

    @object_annotation(tag.column_display)
    def column_display(self): pass

def _constraint_name_parts(constraint, doc):
    # modern systems should have 0 or 1 names here
    names = doc.get('names', [])[0:1]
    if not names:
        raise ValueError('Unexpected constraint without any name.')
    if names[0][0] == '':
        constraint_schema = None
    elif names[0][0] == constraint.table.schema.name:
        constraint_schema = constraint.table.schema
    else:
        raise ValueError('Unexpected schema name in constraint %s' % (names[0],))
    constraint_name = names[0][1]
    return (constraint_schema, constraint_name)

class CatalogKey (NodeConfig):
    """Key-level configuration management.

       annotations: column-level annotations
       comment: key-level comment string
       name: (self.schema, name_str) pair of key constraint
    """
    def __init__(self, table, key_doc, **kwargs):
        NodeConfig.__init__(self, key_doc)
        self.table = table
        try:
            self.constraint_schema, self.constraint_name = _constraint_name_parts(self, key_doc)
        except ValueError:
            self.constraint_schema, self.constraint_name = None, str(hash(self))
        self.unique_columns = KeyedList([
            table.column_definitions[cname]
            for cname in key_doc['unique_columns']
        ])

    @property
    def columns(self):
        """Sugared access to self.unique_columns"""
        return self.unique_columns

    @property
    def catalog(self):
        return self.table.schema.model.catalog

    @property
    def uri_path(self):
        """URI to this model resource."""
        return '%s/key/%s' % (
            self.table.uri_path,
            ','.join([ urlquote(c.name) for c in self.unique_columns ])
        )

    @property
    def name(self):
        """Constraint name (schemaobj, name_str) used in API dictionaries."""
        return (self.constraint_schema, self.constraint_name)

    def name_in_model(self, model):
        """Constraint name (schemaobj, name_str) used in API dictionaries fetching schema from model.

        While self.name works as a key within the same model tree,
        self.name_in_model(dstmodel) works in dstmodel tree by finding
        the equivalent schemaobj in that model via schema name lookup.

        """
        return (
            model.schemas[self.constraint_schema.name] if self.constraint_schema else None,
            self.constraint_name
        )

    @property
    def names(self):
        """Constraint names field as seen in JSON document."""
        return [ [self.constraint_schema.name if self.constraint_schema else '', self.constraint_name] ]

    def prejson(self, prune=True):
        """Produce a representation of configuration as generic Python data structures"""
        d = NodeConfig.prejson(self)
        d.update({
            'unique_columns': [
                c.name
                for c in self.unique_columns
            ],
            'names': self.names,
        })
        return d

class CatalogForeignKey (NodeConfigAclBinding):
    """Foreign key-level configuration management.

       acl_bindings: foreign key-level acl-bindings
       acls: foreign key-level acls
       annotations: foreign key-level annotations
       comment: foreign key-level comment string
       name: (self.schema, name_str) pair of foreign key constraint
    """
    def __init__(self, table, fkey_doc, **kwargs):
        refcols = fkey_doc['referenced_columns']
        NodeConfigAclBinding.__init__(
            self,
            fkey_doc
        )
        self.table = table
        self.pk_table = None
        try:
            self.constraint_schema, self.constraint_name = _constraint_name_parts(self, fkey_doc)
        except ValueError:
            self.constraint_schema, self.constraint_name = None, str(hash(self))
        if self.constraint_schema:
            self.constraint_schema._fkeys[self.constraint_name] = self
        else:
            self.table.schema.model._pseudo_fkeys[self.constraint_name] = self
        self.foreign_key_columns = KeyedList([
            table.column_definitions[coldoc['column_name']]
            for coldoc in fkey_doc['foreign_key_columns']
        ])
        self._referenced_columns_doc = fkey_doc['referenced_columns']
        self.referenced_columns = None

    def digest_referenced_columns(self, model):
        """Finish construction deferred until model is known with all tables."""
        if self.referenced_columns is None:
            pk_sname = self._referenced_columns_doc[0]['schema_name']
            pk_tname = self._referenced_columns_doc[0]['table_name']
            self.pk_table = model.schemas[pk_sname].tables[pk_tname]
            self.referenced_columns = KeyedList([
                self.pk_table.column_definitions[coldoc['column_name']]
                for coldoc in self._referenced_columns_doc
            ])
            self._referenced_columns_doc = None
            self.pk_table.referenced_by.append(self)

    @property
    def column_map(self):
        """Mapping of foreign_key_columns elements to referenced_columns elements."""
        return {
            fk_col: pk_col
            for fk_col, pk_col in zip(self.foreign_key_columns, self.referenced_columns)
        }

    @property
    def columns(self):
        """Sugared access to self.column_definitions"""
        return self.foreign_key_columns

    @property
    def catalog(self):
        return self.table.schema.model.catalog

    @property
    def uri_path(self):
        """URI to this model resource."""
        return '%s/foreignkey/%s/reference/%s:%s/%s' % (
            self.table.uri_path,
            ','.join([ urlquote(c.name) for c in self.foreign_key_columns ]),
            urlquote(self.pk_table.schema.name),
            urlquote(self.pk_table.name),
            ','.join([ urlquote(c.name) for c in self.referenced_columns ]),
        )

    @property
    def name(self):
        """Constraint name (schemaobj, name_str) used in API dictionaries."""
        return (self.constraint_schema, self.constraint_name)

    def name_in_model(self, model):
        """Constraint name (schemaobj, name_str) used in API dictionaries fetching schema from model.

        While self.name works as a key within the same model tree,
        self.name_in_model(dstmodel) works in dstmodel tree by finding
        the equivalent schemaobj in that model via schema name lookup.

        """
        return (
            model.schemas[self.constraint_schema.name] if self.constraint_schema else None,
            self.constraint_name
        )

    @property
    def names(self):
        """Constraint names field as seen in JSON document."""
        return [ [self.constraint_schema.name if self.constraint_schema else '', self.constraint_name] ]

    def prejson(self, prune=True):
        """Produce a representation of configuration as generic Python data structures"""
        def expand(c):
            c['schema_name'] = self.sname
            c['table_name'] = self.tname
            return c
        d = NodeConfig.prejson(self)
        d.update({
            'foreign_key_columns': [
                c.prejson_colref()
                for c in self.foreign_key_columns
            ],
            'referenced_columns': [
                c.prejson_colref()
                for c in self.referenced_columns
            ],
            'names': self.names,
        })
        return d

    @object_annotation(tag.foreign_key)
    def foreign_key(self): pass
