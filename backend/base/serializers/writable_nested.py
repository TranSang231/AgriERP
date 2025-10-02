from django.db import transaction
from django.db.models.fields.related_descriptors import (
    ManyToManyDescriptor,
    ForwardManyToOneDescriptor,
    ReverseManyToOneDescriptor,
    ForwardOneToOneDescriptor,
    ReverseOneToOneDescriptor
)
from rest_framework.fields import empty
from rest_framework.serializers import ListSerializer
from base.utils.model_meta import get_field_info
from rest_framework import serializers
import inflect
import copy

p = inflect.engine()

related_descriptors = [
    ManyToManyDescriptor,
    ForwardManyToOneDescriptor,
    ReverseManyToOneDescriptor,
    ForwardOneToOneDescriptor,
    ReverseOneToOneDescriptor
]


class WritableNestedSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        self.forward_relationships_data = {}
        self.reverse_relationships_data = {}
        super().__init__(instance,data,**kwargs)

    @transaction.atomic
    def create(self, validated_data):
        nested_create_fields = self.get_nested_create_fields()
         # Save forward relationship data
        relationship_data = {}
        for key, value in self.forward_relationships_data.items():
            if key in nested_create_fields:
                i, source, related_data = self.save_relationship(key, value)
                if i is not None:
                    validated_data.update({key: i})
                elif related_data is not None:
                    relationship_data.update({key: value.copy()})
        # self.forward_relationships_data.clear()

        # Create object
        m2m_fields = {}
        for key, value in validated_data.copy().items():
            if isinstance(value, list):
                m2m_fields.update({key: value})
                del validated_data[key]
        instance = self.Meta.model.objects.create(**validated_data)
        for key, value in m2m_fields.items():
            getattr(instance, key).set(value)

        # Save many to many relationship data
        if len(relationship_data.keys()) > 0:
            for key, value in relationship_data.items():
                self.save_relationship(key, value, instance)
                    
        if(len(self.reverse_relationships_data.keys()) == 0):
            return instance

         # Save reverse relationship data
        for key, value in self.reverse_relationships_data.items():
            if key in nested_create_fields:
                self.save_relationship(key, value, instance)
        # self.reverse_relationships_data.clear()

        return instance
    
    @transaction.atomic
    def update(self, instance, validated_data):
        nested_update_fields = self.get_nested_update_fields()
       
       # Save forward relationship data
        source_map = {}
        for key, value in self.forward_relationships_data.items():
            if key in nested_update_fields:
                i, source, related_data = self.save_relationship(key, value, instance)
                source_map.update({key: source});
                if i is not None:
                    validated_data.update({key: i})
        # self.forward_relationships_data.clear()

        # Save object
        if(len(validated_data.keys()) > 0):
            m2m_fields = {}
            for key, value in validated_data.copy().items():
                if isinstance(value, list):
                    m2m_fields.update({key: value})
                    del validated_data[key]
            instance = super().update(instance, validated_data)
            for key, value in m2m_fields.items():
                source = source_map.get(key,None)
                if source is not None:
                    getattr(instance, source).set(value)
                else:
                    getattr(instance, key).set(value)

        if(len(self.reverse_relationships_data.keys()) == 0):
            return instance
        
        # Save reverse relationship data
        for key, value in self.reverse_relationships_data.items():
            if key in nested_update_fields:
                self.save_relationship(key, value, instance)
        # self.reverse_relationships_data.clear()

        return instance
    
    def save_relationship(self, key, value, instance=None):
        """
        Save the nested relationship data.
        Parameters
        ----------
        key: str
            The attribute name.
        value: object
            The data for this attribute.
        instance: Model
            The model instnace that you want to set attribute.
        Returns
        -------
        instance: Model or list[model] or None
            The instance of list of instance to be set to the attribute.
        source: str
            The attribute on the model instance that acturly data come from.
        """
        many = value.get('many',False)
        source = value.get('source', None)
        removed_items = value.get('removed_items', [])
        related_serializer_class =  value.get('related_serializer_class')
        target_serializer_class = value.get('target_serializer_class')
        target_model = value.get('target_model')
        source_attname = value.get('source_attname')
        m2m_name  = value.get('m2m_name')
        related_data = value.get('related_data', [])
        if many:
            instances = []
            if source == key:
                # Update the exist data
                exist_target_data = value.get('exist_target_data',[])
                exist_target_ids = [item.get('id') for item in exist_target_data]
                target_queryset = (
                    getattr(instance, source).filter(pk__in=exist_target_ids)
                    if instance is not None
                    else target_model.objects.filter(pk__in=exist_target_ids)
                )
                target_serializer_data = copy.deepcopy(exist_target_data)
                exist_target_serializer = target_serializer_class(target_queryset, data=target_serializer_data, many=many)
                if exist_target_serializer.is_valid(raise_exception=True):
                    if not exist_target_serializer.__class__ == ListSerializer:
                        exist_target_serializer.save()
                        instances.extend(exist_target_serializer.instance)
                    else:
                        item_serializer_class = exist_target_serializer.child.__class__
                        for index, item in enumerate(exist_target_serializer.instance):
                            data = (
                                exist_target_data[index]
                                if index < len(exist_target_data)
                                else None
                            )
                            if data is not None:
                                item_serializer = item_serializer_class(item, data=data)
                                if item_serializer.is_valid():
                                    item_serializer.save()
                                    instances.append(item_serializer.instance)
                # Add new data
                new_target_data = value.get('new_target_data')
                if m2m_name is None and new_target_data is not None:
                    for item in new_target_data:
                        if item.get(source_attname) is None:
                            item.update({source_attname: instance.id.urn[9:]})
                new_target_serializer = (
                    target_serializer_class(data=new_target_data, many=many)
                    if new_target_data is not None
                    else None
                )
                if new_target_serializer is not None and new_target_serializer.is_valid(raise_exception=True):
                    if not new_target_serializer.__class__ == ListSerializer:
                        new_target_serializer.save()
                        instances.extend(new_target_serializer.instance)
                    else:
                        item_serializer_class = new_target_serializer.child.__class__
                        for item in new_target_data:
                            item_serializer = item_serializer_class(data=item)
                            if item_serializer.is_valid():
                                    item_serializer.save()
                                    instances.append(item_serializer.instance)
                if instance is not None:
                    if len(instances) > 0 or len(removed_items) > 0:
                        getattr(instance, key).set(instances)
                return instances, source, None
            elif instance is not None:
                related_serializer_class = value.get('related_serializer_class')
                related_descriptor = getattr(instance, source)
                target_descriptor = getattr(instance, key)
                related_queryset = related_descriptor.get_queryset()
                # Update and add new data
                for item in related_data:
                    foreign_key = value.get(source_attname)
                    foreign_object = value.get(m2m_name)
                    if foreign_key is None and foreign_object is None:
                        item.update({source_attname: instance.id.urn[9:]})
                    id = item.get('id')
                    i = (
                        related_queryset.get(pk=id)
                        if id is not None and related_queryset is not None
                        else None
                    )
                    item_serializer = (
                        related_serializer_class(i, data=item)
                        if i is not None
                        else related_serializer_class(data=item)
                    )
                    if item_serializer.is_valid():
                        item_serializer.save()
                        instances.append(item_serializer.instance)
                # Remove old data:
                m2m_reverse_name  = value.get('m2m_reverse_name')
                if removed_items is not None and len(removed_items) > 0:
                    old_ids = [obj.pk for obj in removed_items if isinstance(obj, related_descriptor.model)]
                    removed_target_ids = [getattr(obj, m2m_reverse_name).id.urn[9:] for obj in removed_items]
                    if len (old_ids) > 0:
                        related_descriptor._remove_prefetched_objects()
                        related_descriptor.filter(pk__in=old_ids).delete()
                if len(instances) > 0 or len(removed_items) > 0:
                    target_queryset = target_descriptor.get_queryset()
                    target_instances = (
                        [getattr(i, m2m_reverse_name) for i in instances]
                        if len(instances) > 0
                        else target_queryset.exclude(pk__in=removed_target_ids)
                    )
                    target_descriptor.set(target_instances)
                return instances, source, None
            else:
                return None, source, related_data
        else:
            # Update reference for reverse relationship
            if source_attname is not None and instance is not None:
                related_data.update({source_attname: instance.id.urn[9:]})
            related_data_id = related_data.get('id')
            try:
                related_current_instance = (
                    getattr(instance, key)
                    if instance is not None
                    else None
                )
            except:
                related_current_instance = None
            related_intance = (
                related_current_instance
                if related_current_instance and related_current_instance.id.urn[9:] == related_data_id
                else None
            )
            target_serializer = (
                target_serializer_class(related_intance, data=related_data)
                if related_intance is not None
                else  target_serializer_class(data=related_data)
            )
            if target_serializer.is_valid(raise_exception=True):
                target_serializer.save()
                if instance is not None:
                    setattr(instance, key, target_serializer.instance)
                return target_serializer.instance, source, None
        return None, None, None   
    
    def get_related_serializer_info(self, fieldName):
        related_field = self.fields.fields.get(fieldName, None)
        source = (
            related_field.source
            if related_field.source is not None
            else None
        ) 
        try:
            many = related_field.many
        except:
            many = False
        model_class = (
            self.Meta.model
            if self.Meta is not None and self.Meta.model is not None
            else self.child.Meta.model
        )
        related_descriptor = (
            getattr(model_class, source)
            if model_class is not None and source is not None
            else None
        )
        target_descriptor = (
            getattr(model_class, fieldName)
            if model_class is not None
            else None
        )
        target_model = (
            target_descriptor.field.related_model
            if isinstance(target_descriptor, ForwardManyToOneDescriptor)
            else target_descriptor.related.related_model
                if isinstance(target_descriptor, ReverseOneToOneDescriptor)
                else target_descriptor.rel.related_model
        )
        m2m_name = (
            target_descriptor.field.m2m_field_name()
            if target_descriptor is not None and isinstance(target_descriptor, ManyToManyDescriptor)
            else None
        )
        m2m_reverse_name = (
            target_descriptor.field.m2m_reverse_field_name()
            if target_descriptor is not None and isinstance(target_descriptor, ManyToManyDescriptor)
            else None
        )
        source_attname = (
            related_descriptor.field.attname
            if related_descriptor is not None and isinstance(related_descriptor, ReverseManyToOneDescriptor)
            else related_descriptor.related.field.attname
                if related_descriptor is not None and isinstance(related_descriptor, ReverseOneToOneDescriptor)
                else None
        )
        related_queyset = (
            getattr(self.instance, source).get_queryset()
            if many and self.instance is not None and source is not None
            else None
        )
        related_serializer_class = (
            related_field.child.__class__
            if many
            else related_field.__class__
        )
        target_field = (
            related_field.child.fields.fields.get(m2m_name)
            if source != fieldName and many
            else related_field
        )
        target_serializer_class = (
            related_serializer_class
            if source == fieldName
            else target_field.__class__
        )

        return (
            many,
            source,
            related_serializer_class,
            related_queyset,
            target_serializer_class,
            target_model,
            m2m_name,
            m2m_reverse_name,
            source_attname
        )
    
    def get_nested_create_fields(self):
        try:
            nested_create_fields = (
                self.Meta.nested_create_fields 
                if self.Meta is not None and self.Meta.nested_create_fields is not None
                else list()
            )
        except:
            nested_create_fields = list()
        return nested_create_fields
    
    def get_nested_update_fields(self):
        try:
            nested_update_fields = (
                self.Meta.nested_update_fields 
                if self.Meta is not None and self.Meta.nested_update_fields is not None
                else list()
            )
        except:
            nested_update_fields = list()
        return nested_update_fields;

    def convert_nested_data(self, data, key, value):
        if isinstance(value, dict):
            related_id = value.get("id", None)
            if related_id is not None:
                data.update({f'{key}_id': related_id})
            del data[key]
        elif isinstance(value, list):
            related_ids = [item.get('id') for item in value if item.get('id') is not None]
            data.update({f'{p.singular_noun(key)}_ids': related_ids})
            del data[key]
    
    def to_internal_value(self, data):
        if not isinstance(data, dict) and not isinstance(data, list):
            return super().to_internal_value(data)
        # extract nested data
        ModelClass = self.Meta.model
        nested_create_fields = self.get_nested_create_fields()
        nested_update_fields = self.get_nested_update_fields()
        nested_fields = nested_create_fields + list((set(nested_update_fields)-set(nested_create_fields)))
        info = get_field_info(ModelClass)
        relations = info.relations
        relation_keys = relations.keys()
        forward_relations = info.forward_relations
        forward_relation_keys = forward_relations.keys()
        reverse_relations =  info.reverse_relations
        reverse_relation_keys = reverse_relations.keys()
        copy_data = data.copy()
        items = copy_data.items()
        for key, value in items:
            if key.endswith('_deleted_ids') and len(value) > 0:
                origin_key = key[:-12]
                removed_field = {
                    'many': True
                }
                if copy_data.get(origin_key) is None and self.instance is not None:
                    origin_field = self.fields.fields.get(origin_key, None)
                    origin_source = (
                        origin_field.source
                        if origin_field is not None
                        else None
                    )
                    descriptor = (
                        getattr(self.instance, origin_source)
                        if origin_source is not None
                        else None
                    )
                    if descriptor is not None:
                        values = []
                        for v in value:
                            try:
                                i = descriptor.get(pk=v)
                                values.append(i)
                            except Exception as e:
                                print(e)
                        if len(values) > 0:
                            removed_field.update({
                                'removed_items': values,
                                'source': origin_source,
                                'm2m_reverse_name': getattr(self.instance, origin_key).target_field_name
                            })
                            if origin_key in forward_relation_keys:
                                self.forward_relationships_data.update({origin_key: removed_field})
                            elif origin_key in reverse_relation_keys:
                                self.reverse_relationships_data.update({origin_key: removed_field})
        
        for key, value in items:
            if key in relation_keys:
                if key in nested_fields:
                    # Prevent creating/updating the nested field that was not allowed. 
                    if self.instance is None and key not in nested_create_fields:
                        self.convert_nested_data(data, key, value)
                    elif self.instance is not None and key not in nested_update_fields:
                        self.convert_nested_data(data, key, value)
                    else:
                        (
                            many,
                            source,
                            related_serializer_class,
                            related_queyset,
                            target_serializer_class,
                            target_model,
                            m2m_name,
                            m2m_reverse_name,
                            source_attname
                        ) = self.get_related_serializer_info(key)
                        relationship = {
                            'many': many,
                            'source': source,
                            'related_serializer_class': related_serializer_class,
                            'target_serializer_class': target_serializer_class,
                            'target_model': target_model,
                            'source_attname': source_attname,
                        }
                        if many:
                            exist_ids = [item.get('id') for item in value]
                            removed_items = (
                                [item for item in related_queyset if item.id.urn[9:] not in exist_ids]
                                if self.instance is not None
                                else None
                            )

                            if removed_items is not None and len(removed_items) > 0:
                                relationship.update({ 'removed_items': removed_items })
                            if source != key:
                                relationship.update( {
                                    'related_data': value.copy(),
                                    'source': source,
                                    'm2m_name': m2m_name,
                                    'm2m_reverse_name': m2m_reverse_name
                                })
                            else:
                                target_data = value.copy()
                                exist_target = [item for item in target_data if item.get('id') is not None]
                                if exist_target is not None and len(exist_target) > 0:
                                    relationship.update({ 'exist_target_data': exist_target })
                                
                                new_target_data = [item for item in target_data if item.get('id') is None]
                                if self.instance is not None and source == key:
                                    instance_id = self.instance.id.urn[9:]
                                    for item in new_target_data:
                                        item.update({source_attname: instance_id})
                                
                                if new_target_data is not None and len(new_target_data) > 0:
                                    relationship.update( {
                                        'new_target_data': new_target_data
                                    })
                            
                            if key in forward_relation_keys:
                                self.forward_relationships_data.update({ key: relationship })
                            elif key in reverse_relation_keys:
                                self.reverse_relationships_data.update({ key: relationship })
                        elif value is not None:
                            relationship.update( {
                                'related_data': value.copy(),
                                'source': source
                            })
                            if key in forward_relation_keys:
                                self.forward_relationships_data.update({ key: relationship })
                            elif key in reverse_relation_keys:
                                self.reverse_relationships_data.update({ key: relationship })
                        del data[key]
                else:
                    self.convert_nested_data(data, key, value)
        valid_data = super().to_internal_value(data)
        return valid_data

