from rest_framework import serializers


class RecursiveSerializer(serializers.Serializer):
    def __init__(self, source_class=None, **kwargs):
        self.source_class = source_class
        kwargs.pop('source_class', None)
        super().__init__(**kwargs)

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
        
    def to_internal_value(self, data):
        root_serializer = self.root
        child_serializer = self.root.child if hasattr(self.root, "child") else None
        serializer = (
            child_serializer 
            if not isinstance(data, list) and child_serializer
            else root_serializer
        )
        return serializer.to_internal_value(data)