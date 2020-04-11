from django import forms
from .models import Workout, Exercise


class WorkoutForm(forms.ModelForm):

    class Meta:
        model = Workout
        fields = ['name', 'warmup_time', 'cooldown_time', 'laps']


class ExerciseForm(forms.ModelForm):

    class Meta:
        model = Exercise
        fields = ['name', 'duration', 'preptime']


class MyExerciseForm(forms.Form):
    name = forms.CharField(initial='My Exercise')
    duration = forms.IntegerField(initial=30)
    preptime = forms.IntegerField(initial=0)