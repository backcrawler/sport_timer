from django import forms
from .models import Workout


class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ['name', 'warmup_time', 'cooldown_time', 'laps']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

