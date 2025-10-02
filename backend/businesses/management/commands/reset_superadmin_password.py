from ...models import User
from core.settings.base import (
    SECRET_KEY,
    SUPER_ADMIN_EMAIL,
    SUPER_ADMIN_PASSWORD
)
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Reset passsword superadmin"

    def handle(self, *args, **options):
        superadmin = User.objects.filter(email=SUPER_ADMIN_EMAIL).first()
        if not superadmin:
            raise CommandError("superadmin not found")

        superadmin.password = make_password(
            SUPER_ADMIN_PASSWORD,
            salt=SECRET_KEY
        )
        superadmin.save()

        self.stdout.write(self.style.SUCCESS("Reset passsword successfully"))
