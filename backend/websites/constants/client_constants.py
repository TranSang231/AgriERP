from . import WebsiteBuildStatus

client_constants = {
    "website_build_statuses": [{"value": x, "description": y} for x, y in WebsiteBuildStatus.CHOICES]
}