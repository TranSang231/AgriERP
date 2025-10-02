from rest_framework import serializers
from base.utils.model_meta import get_field_info, get_unique_fields
import inflect

p = inflect.engine()

class BaseListSerializer(serializers.ListSerializer):
    # def __init__(self, *args, **kwargs):
    #     manager = None
    #     self.manager = kwargs.pop('manager', copy.deepcopy(self.manager))
    #     super().__init__(*args, **kwargs)

    def run_child_validation(self, data):
        id = data.get('id', None)
        if id is not None and self.instance is not None:
            self.child.instance = self.instance.get(pk=id)
        self.child.initial_data = data
        valid_data =  super().run_child_validation(data)
        if id and isinstance(valid_data, dict):
            valid_data.update({'id': id})
        return valid_data
    

class BaseSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        # Replace forward nested data by it instance if the related instance already exist.
        ModelClass = self.Meta.model
        info = get_field_info(ModelClass)
        forward_relations = info.forward_relations
        forward_relation_keys = forward_relations.keys()
        items = data.copy().items()
        for key, value in items:
            if key in forward_relation_keys:
                relation = forward_relations[key]
                RelatedModel = relation.related_model
                unique_fields = get_unique_fields(RelatedModel)
                unique_keys = unique_fields.keys()
                if not relation.to_many and isinstance(value, dict):
                    if len(unique_keys) > 0:
                        for k, v in value.items():
                            if k in unique_keys:
                                try:
                                    related_object = RelatedModel.objects.get(**{k:v})
                                except RelatedModel.DoesNotExist:
                                    related_object = None
                                if related_object is not None:
                                    data.update({f'{key}_id': related_object.id.urn[9:]})
                                    del data[key]
                elif isinstance(value, list):
                    related_ids = []
                    for item in  value:
                        if isinstance(item, dict) and item.get("id",None) is not None:
                            related_ids.append(item.get("id"))

                    data.update({f'{p.singular_noun(key)}_ids': related_ids})
                    del data[key]

        return super().to_internal_value(data)
        