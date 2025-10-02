from collections import namedtuple

from rest_framework.utils.model_meta import (
    FieldInfo,
    _get_pk,
    _get_fields,
    _get_to_field,
    _get_forward_relationships,
    _get_reverse_relationships,
    _merge_fields_and_pk,
    _merge_relationships
)

RelationInfo = namedtuple('RelationInfo', [
    'model_field',
    'related_model',
    'to_many',
    'to_field',
    'has_through_model',
    'reverse',
    'field_name'
])

def get_field_info(model):
    """
    Given a model class, returns a `FieldInfo` instance, which is a
    `namedtuple`, containing metadata about the various field types on the model
    including information about their relationships.
    """
    opts = model._meta.concrete_model._meta

    pk = _get_pk(opts)
    fields = _get_fields(opts)
    forward_relations = _get_forward_relationships(opts)
    reverse_relations = _get_reverse_relationships(opts)
    fields_and_pk = _merge_fields_and_pk(pk, fields)
    relationships = _merge_relationships(forward_relations, reverse_relations)

    return FieldInfo(pk, fields, forward_relations, reverse_relations,
                     fields_and_pk, relationships)

def get_unique_fields(model):
    """
    Given a model class, returns a dictionary of unique fields.
    """
    unique_fields = {}
    meta = getattr(model, '_meta', None)
    if meta is not None:
        fields = getattr(meta, 'fields', None)
        if fields is not None:
            for field in fields:
                if field.unique:
                    unique_fields[field.name] =  field
    return unique_fields

def _get_reverse_relationships(opts):
    """
    Returns a dict of field names to `RelationInfo`.
    """
    reverse_relations = {}
    all_related_objects = [r for r in opts.related_objects if not r.field.many_to_many]
    for relation in all_related_objects:
        accessor_name = relation.get_accessor_name()
        reverse_relations[accessor_name] = RelationInfo(
            model_field=None,
            related_model=relation.related_model,
            to_many=relation.field.remote_field.multiple,
            to_field=_get_to_field(relation.field),
            has_through_model=False,
            reverse=True,
            field_name=relation.field.name
        )

    # Deal with reverse many-to-many relationships.
    all_related_many_to_many_objects = [r for r in opts.related_objects if r.field.many_to_many]
    for relation in all_related_many_to_many_objects:
        accessor_name = relation.get_accessor_name()
        reverse_relations[accessor_name] = RelationInfo(
            model_field=None,
            related_model=relation.related_model,
            to_many=True,
            # manytomany do not have to_fields
            to_field=None,
            has_through_model=(
                (getattr(relation.field.remote_field, 'through', None) is not None) and
                not relation.field.remote_field.through._meta.auto_created
            ),
            reverse=True,
            field_name=relation.field.name
        )

    return reverse_relations