from django import forms
from django.forms.utils import ValidationError

from .models import Workout, Exercise


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'warmup_time', 'cooldown_time']

    def clean(self):
        cleaned = self.cleaned_data
        if cleaned['laps'] <= 0:
            raise ValidationError('Number of laps cannot be less than 1')
        return super().clean()


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'duration', 'preptime', 'kind']


class MyExerciseForm(forms.Form):
    name = forms.CharField()
    duration = forms.IntegerField(initial=30)
    preptime = forms.IntegerField(initial=0)