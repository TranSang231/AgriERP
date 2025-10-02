import io
import tarfile
import json
import hashlib
from django.utils.translation import gettext as _
from django.http import HttpResponse, StreamingHttpResponse
from django.core.files.base import ContentFile
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import NotFound
from common.constants import Http
from ..services.nlp import NLUService
from ..models import Bot, NLUModel


class NLUViewSet(GenericViewSet):
    required_alternate_scopes = {
        "version": [["virtual-assistants:view"], ["virtual-assistants:edit"]],
        "status": [["virtual-assistants:view"], ["virtual-assistants:edit"]]
    }

    @action(detail=False, methods=[Http.HTTP_GET], url_path="version")
    def version(self, request, *args, **kwargs):
        """
        API to get NLU service version
        """
        result = NLUService.get_nlu_version()
        content = result.content
        status = result.status_code
        headers = result.headers
        response = HttpResponse(content=content, status=status)
        for k, v in headers.items():
            if k not in ['connection']:
                response[k] = v
        return response
    
    @action(detail=False, methods=[Http.HTTP_GET], url_path="status")
    def status(self, request, *args, **kwargs):
        """
        API to get NLU service status
        """
        result = NLUService.get_nlu_status()
        content = result.content
        status = result.status_code
        headers = result.headers
        response = HttpResponse(content=content, status=status)
        for k, v in headers.items():
            if k not in ['connection']:
                response[k] = v
        return response

    @action(detail=False, methods=[Http.HTTP_GET], url_path="nlu-host", permission_classes=[AllowAny], authentication_classes=[])
    def nul_host(self, request, *args, **kwargs):
        """
        API to get NLU host
        """
        result = NLUService.get_nlu_host()
        return Response(
            {"host": result},
            status=HTTP_200_OK
        )
    
    @action(detail=False, methods=[Http.HTTP_GET], url_path="models/(?P<model_pk>[^/.]+)", permission_classes=[AllowAny], authentication_classes=[])
    def models(self, request, *args, **kwargs):
        """
        Retrieve model file by model id
        """
        model_pk = kwargs.get('model_pk')
        try:
            model = NLUModel.objects.get(pk=model_pk)
            if model.file:
                with model.file.open('rb') as f:
                    response = StreamingHttpResponse(f, content_type='application/x-tar')
                    response['Content-Disposition'] = f'attachment; filename={model_pk}.tar.gz'
                    response['Content-Length'] = model.file.size
                    response['ETag'] = model.hash
                    response['filename'] =  f'{model.bot.id}.{model.id}.tar.gz'
                    return response
        except NLUModel.DoesNotExist:
            raise ValueError(_("Invalid model id"))
        raise NotFound(_("The model were not found"))

    @action(detail=False, methods=[Http.HTTP_POST], url_path="callback", permission_classes=[AllowAny], authentication_classes=[])
    def callback(self, request, *args, **kwargs):
        """
        API to get NLU host
        """
        #Todo: Limit the host that can call this api
        origin = request.META.get("HTTP_ORIGIN")
        origin = (
            request.META.get("REMOTE_ADDR")
            if origin is None
            else origin
        )
        
        content_type =  request.content_type
        if content_type == 'application/x-tar':
            try:
                # bytes = io.BytesIO(response.content)
                # tar = tarfile.open(fileobj=request._stream.body, mode='r:gz')

                # Stream directly from the stream object
                byte_stream = io.BytesIO(request._request.body)
                with tarfile.open(fileobj=byte_stream, mode='r:gz') as tar:
                    with tar.extractfile('metadata.json') as f:
                        if f: # Check if the file exists in the archive
                            json_data = json.load(f)
                            assistant_id = json_data.get('assistant_id')
                            trained_at = json_data.get('trained_at')
                            model_id = json_data.get('model_id')
                            if assistant_id is not None:
                                bot = Bot.objects.get(pk=assistant_id)
                                if bot is not None:
                                    model_name =  f'{bot.name} - {trained_at}'
                                    file_name = f'{assistant_id}.{model_id}.tar.gz'
                                    file_object = ContentFile(request._request.body, name=file_name)
                                    hasher = hashlib.sha256() # Or hashlib.md5()
                                    file_object.seek(0)  # Ensure the file pointer is at the beginning
                                    for chunk in file_object.chunks():
                                        hasher.update(chunk)
                                    hash = hasher.hexdigest()
                                    model = NLUModel.objects.create(
                                        name=model_name,
                                        hash=hash,
                                        bot=bot
                                    )
                                    model.file.save(file_name, file_object)
                                    model.save()
                                    return Response(
                                        {"message": _('OK')},
                                        status=HTTP_200_OK
                                    )
                        else:
                            raise ValueError(_("File 'metadata.json' not found in the archive."))
            except tarfile.ReadError as e:
                print(f"Error opening tar file: {e}")
                raise ValueError(_("Invalid tar file format."))
            except json.JSONDecodeError:
                raise ValueError(_("Error: Could not decode JSON from 'metadata.json'. The file might not contain valid JSON."))
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        raise ValueError(_("Invalid content."))