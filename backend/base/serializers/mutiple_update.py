from rest_framework import serializers

class MutipleUpdateListSerializer(serializers.ListSerializer):
    def run_child_validation(self, data):
        id = data.get('id', None)
        if id:
            self.child.instance = self.instance.get(pk=id)
        self.child.initial_data = data
        valid_data =  super().run_child_validation(data)
        if id and isinstance(valid_data, dict):
            valid_data.update({'id': id})
        return valid_data


    def create(self, validated_data):
        ModelClass = self.child.Meta.model
        instances = [ModelClass(**item) for item in validated_data]
        return ModelClass._default_manager.bulk_create(instances)
    
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        instance_mapping = {item.id.urn[9:]: item for item in instance}
        new_data = [item for item in validated_data if item.get('id') is None]
        
        data_mapping = {item['id']: item for item in validated_data if item.get('id') is not None}

        # Perform creations and updates.
        ModelClass = self.child.Meta.model
        ret = []
        if new_data:
            new_items  = self.create(new_data)
            ret.extend(new_items)
        
        for item_id, data in data_mapping.items():
            item = instance_mapping.get(item_id, None)
            if item is not None:
                ret.append(self.child.update(item, data))

        # Perform deletions.
        delete_ids = []
        for item_id, item in instance_mapping.items():
            if item_id not in data_mapping:
                delete_ids.append(item_id)
        if delete_ids:
            ModelClass._default_manager.filter(id__in=delete_ids).delete()

        return ret
        