from base.views import BaseViewSet
from rest_framework.permissions import AllowAny
from ..models import ProductCategory
from ..serializers import ProductCategorySerializer

class ProductCategoryViewSet(BaseViewSet):
    queryset = ProductCategory.objects.all()
    search_map = {
        "name__origin": "icontains"
    }
    serializer_class = ProductCategorySerializer
    required_alternate_scopes = {
        "list": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "retrieve": [["ecommerce:products:view"], ["ecommerce:products:edit"]],
        "create": [["ecommerce:products:edit"]],
        "update": [["ecommerce:products:edit"]],
        "destroy": [["ecommerce:products:edit"]]
    }

    def get_permissions(self):
        """Allow public access for listing and viewing product categories."""
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()