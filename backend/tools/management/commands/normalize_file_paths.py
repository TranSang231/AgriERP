from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Normalize binary_database_files File.name paths: backslashes (\\) -> forward slashes (/)"

    def handle(self, *args, **options):
        # Import here so Django settings are loaded correctly
        from binary_database_files.models import File

        qs = File.objects.filter(name__contains="\\")
        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS("No file paths with backslashes found. Nothing to update."))
            return

        self.stdout.write(f"Found {total} file records with backslashes. Updating...")

        updated = 0
        for f in qs.iterator():
            old_name = f.name
            new_name = old_name.replace("\\", "/")
            if new_name != old_name:
                f.name = new_name
                f.save(update_fields=["name"])
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Updated {updated} file records."))
