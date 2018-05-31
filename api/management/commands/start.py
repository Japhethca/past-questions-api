from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'start server'

    def handle(self, *args, **options):
        call_command('runserver', 5000)

