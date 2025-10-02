from . import AccessMode

client_constants = {
    "access_modes": [{"value": x, "description": y} for x, y in AccessMode.CHOICES]
}