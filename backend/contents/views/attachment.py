from rest_framework import status
from rest_framework.response import Response
from base.views.base import BaseViewSet
from contents.models import Attachment
from contents.serializers import AttachmentSerializer

# Create your views here.
class AttachmentViewSet(BaseViewSet):
    queryset = Attachment.objects.all() 
    serializer_class= AttachmentSerializer
    required_alternate_scopes = {
        "create": [["admin:contents:edit"]],
        "retrieve": [["admin:contents:view"], ["admin:contents:edit"]],
        "update": [["admin:contents:edit"]],
        "destroy": [["admin:contents:edit"]],
        "list": [["admin:contents:view"], ["admin:contents:edit"]],
    }

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        long_content_pk = kwargs.get('long_content_pk')
        if long_content_pk is not None:
            data['long_content_id'] = long_content_pk
        file = file_name = request.FILES['file']
        file_name = file.name
        data['original_name'] = file_name
        data['mine_type'] = file.content_type
        data['path'] = "/".join(['attachments', str(file_name)])
        serializer = self.serializer_class(data=data, context=self.get_parser_context(request))
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = serializer.data
                return Response(response, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)