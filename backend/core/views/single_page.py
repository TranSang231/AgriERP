from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import gettext as _
from django.template.loaders.cached import Loader
from django.template import engines
from websites.models import Site, Build
from common.constants import PublishingStatus
from websites.constants import WebsiteBuildStatus

def reset_template_loader_cache():
    for backend in engines.all():
        if hasattr(backend, 'engine') and hasattr(backend.engine, 'template_loaders'):
            for loader in backend.engine.template_loaders:
                if isinstance(loader, Loader):
                    loader.reset()
    
def get_client_site(domain_name: str):
    """Return `[site_id, context]` of client website if it own that `domain_name`, 
        else return `domain_not_found` if there are none.
    """
    try:
        site = Site.objects.get(domain_name=domain_name)
        site_id = str(site.id)
        if not site.status == PublishingStatus.PUBLISHED:
            return None, {}
        
        ## Get website's latest build.
        build = Build.objects.filter(site_id=site_id, status=WebsiteBuildStatus.DEPLOYED).order_by('-created_at').first()
        ## Check if this build has been loaded to DjangoVite or not. If not, load it.
        # print(client_build, "is register to DjangoVite:", client_build.is_vite_registered())
        if not build.is_vite_registered():
            build.register_site()
            reset_template_loader_cache()
        ## Get website context
        context = { 
            "title": site.title.origin if site.title!=None else _("No title")
        }
        if site.icon is not None: 
            context.update ({"icon": site.icon})
        metadata = []
        if site.keywords != None:
            metadata += [{ "name":"keywords", "content": site.keywords }]
        if site.description is not None:
            if site.description.translates is not None:
                translates = site.description.translates.all()
                for translate in translates:
                    metadata += [{ "name":"description", "lang": translate.language, "content": translate.value }]

        if len(metadata) > 0:
            context.update({ "metadata": metadata})
        return [site_id, context]
    except Exception as e:
        return None, {}
        

@ensure_csrf_cookie
def single_page_view(request):
    host = request.get_host()
    default_host = settings.DEFAULT_HOST
    default_scheme = (
        "http"
        if default_host.startswith("localhost") or default_host.startswith("127.0.0.1")
        else "https"
    )
    apiBase = f"{default_scheme}://{default_host}/api/v1"
    context = { "apiBase": apiBase, "defaultHost": f"{default_scheme}://{default_host}"}
    if host == settings.DEFAULT_HOST:
        return render(request, "index.html", context)
    elif host == settings.BUSINESS_HOST:
        return render(request, "businesses/website/index.html", context)
    else:
        site_id, site_context = get_client_site(host)
        if site_id is not None:
            apiBase = f"{default_scheme}://{default_host}/api/public/v1"
            context.update({"apiBase": apiBase, "siteId": site_id})
            context.update(site_context)
            reponse = render(request, f"{site_id}.html", context)
            reponse.set_cookie('site', site_id)
            return reponse
        return render(request, "domain_not_found.html")