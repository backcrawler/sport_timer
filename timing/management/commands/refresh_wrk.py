from django.core.management.base import BaseCommand, CommandError
from timing.models import Workout


class Command(BaseCommand):
    help = 'clears all Workouts at once'

    def handle(self, *args, **options):
        Workout.objects.all().delete()
        print('INFO: All Workout objects have been cleared')