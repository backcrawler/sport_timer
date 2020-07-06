from django.contrib import admin
from .models import Exercise, Workout


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'kind']}),
        ('Timings', {'fields': ['duration', 'preptime', ]}),
        ('Workout', {'fields': ['plan']})
    ]


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'laps']}),
        ('Timings', {'fields': ['warmup_time', 'cooldown_time', ]}),
    ]


