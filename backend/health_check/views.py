from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse(content="The service is up and healthy.")
