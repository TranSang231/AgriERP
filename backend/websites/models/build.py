from django.db import models
from base.models.timestamped import TimeStampedModel
from websites.models import Site
from ..constants import WebsiteBuildStatus
from os import path
from zipfile import ZipFile
from traceback import print_exception
from django_vite.core.asset_loader import DjangoViteAssetLoader
from core.settings.base import BASE_DIR

def website_archive_path(instance, filename):
    return "\\".join(['webstites', str(instance.site.id), 'builds', filename])

def website_static_path(instance):
    return path.join(BASE_DIR, "client-sites", "static", str(instance.site.id))

def website_template_path():
    return path.join(BASE_DIR, "client-sites", "templates")

class Build(TimeStampedModel):
    site = models.ForeignKey(Site, blank=True, on_delete=models.CASCADE, related_name="builds")
    archive = models.FileField(upload_to=website_archive_path, max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(choices=WebsiteBuildStatus.CHOICES, default=WebsiteBuildStatus.OPEN, blank=True)
    info = models.JSONField(null=True, blank=True)
    config = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "websites_builds"

    def extract_build(self):
        """Extract build_zip to storage"""
        with ZipFile(self.archive) as zip:
            # zip.extractall(path=deploy_folder)
            for file in zip.namelist():
                if file.startswith('client'):
                    zip.extract(file, path=website_static_path(self))
                if file.endswith('.html'):
                    zip.extract(file, path=website_template_path())
            ## TODO: hot reload server, to make new static files available

    def register_site(self):
        """Register build config to DjangoVite module"""
        try:
            site_id = str(self.site.id)
            vite_config = self.config
            if vite_config != None:
                DjangoViteAssetLoader.add_new_app(site_id, vite_config)
            else:
                raise ValueError(f'Build {self.id}: vite_config is None')
        except Exception as e:
            raise e
        
    def is_vite_registered(self):
        """If build config has been registered to DjangoVite, return True, else return False"""
        site_id = str(self.site.id)
        return DjangoViteAssetLoader.is_loaded_app(site_id)

    def deploy(self):
        """Call after finished build pipeline, save deploy config to DB"""
        try:
            ## extract files
            self.extract_build()
            ## DjangoVite app config
            static_folder = website_static_path(self)
            site_id = str(self.site.id)
            vite_config = {
                # "dev_server_host": "localhost",
                # "dev_server_port": 3009,
                "manifest_path": path.join(static_folder, "client.manifest", f"{site_id}.manifest.json"),
                "static_url_prefix": f"{site_id}/client/_nuxt",
                "ws_client_url": "@vite/client",
                "react_refresh_url": "@react-refresh",
            }
            self.config = vite_config
            self.status = WebsiteBuildStatus.DEPLOYED
            self.save()
        except Exception as e:
            print_exception(e)
            raise e