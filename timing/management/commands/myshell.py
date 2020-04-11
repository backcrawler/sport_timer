from django.core.management.base import BaseCommand, CommandError
from timing import utils
import subprocess


class Command(BaseCommand):
    help = 'install a new type of the shell, with extra utility signals'

    def handle(self, *args, **options):
        from timing import utils
        subprocess.call('python manage.py shell')