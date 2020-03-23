from builtins import super

from django.shortcuts import render
from django.urls.base import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from .models import Exercise, Workout, Break
from .forms import WorkoutForm


def home(request):
    return render(request, 'timing/index.html')


class WorkoutListView(ListView):
    model = Workout
    template_name = 'timing/workout_list.html'

    def get_queryset(self):
        workouts = Workout.objects.all()
        return workouts

    def get(self, request, *args, **kwargs):
        workouts = self.get_queryset()
        context = {'object_list': workouts}
        return self.render_to_response(context)


def show_workouts(request):
    '''shows all groups available'''
    workouts = Workout.objects.all()
    context = {'workouts': workouts}
    return render(request, 'timing/workout_list.html', context=context)


class WorkoutCreateView(CreateView):
    model = Workout
    template_name = 'timing/new_workout.html'
    #success_url = reverse('timing:show_workouts')
    form_class = WorkoutForm
    ##fields = ['name', 'warmup_time', 'cooldown_time', 'laps']


class ExerciseCreateView(CreateView):
    model = Exercise
    fields = ['name', 'duration', 'exr_type', 'preptime']

