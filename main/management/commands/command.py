from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This is a help string"

    def handle(self, *args, **options):
        self.stdout.write("Starting")
