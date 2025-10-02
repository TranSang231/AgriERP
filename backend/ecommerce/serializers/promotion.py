from base.serializers import WritableNestedSerializer
from ..models import Promotion
from .promotion_item import PromotionItemSerializer

class PromotionSerializer(WritableNestedSerializer):
    promotion_items = PromotionItemSerializer(
        many=True,
        required=False
    )
    
    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "start",
            "end",
            "type",
            "discount",
            "promotion_items",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'name': {'required': False},
            'start': {'required': False},
            'end': {'required': False},
            'type': {'required': False},
            'discount': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["promotion_items"]
        nested_update_fields = ["promotion_items"]