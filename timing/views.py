from builtins import super

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView

from .models import Exercise, Workout
from .forms import WorkoutForm, ExerciseForm, MyExerciseForm


def home(request):
    '''Shows homepage'''
    return render(request, 'timing/index.html')


class WorkoutListView(LoginRequiredMixin, ListView):  # TODO: date_added proper filtering
    """Shows all Workouts"""
    model = Workout
    template_name = 'timing/workout_list.html'

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        super().setup(request, *args, **kwargs)

    def get_queryset(self):
        workouts = Workout.objects.filter(owner=self.user).order_by('date_added')
        return workouts


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    '''Creates a Workout instance'''
    template_name = 'timing/new_workout.html'
    success_url = '/workouts'
    form_class = WorkoutForm
    ##fields = ['name', 'warmup_time', 'cooldown_time', 'laps']

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    '''Creates an Exercise instance, uses custom logic inside the model'''
    template_name = 'timing/new_exercise.html'
    success_url = '..'
    form_class = ExerciseForm
    pk_url_kwarg = 'wrk_id'

    def setup(self, request, *args, **kwargs):
        self.workout = Workout.objects.get(id=kwargs['wrk_id'])
        if self.workout.owner != request.user:
            raise Http404
        self.wrk_id = kwargs['wrk_id']
        super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.form = MyExerciseForm()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout'] = self.workout
        return context

    def post(self, request, *args, **kwargs):
        self.form = MyExerciseForm(request.POST)
        if self.form.is_valid():
            params = {'plan': self.workout}
            for fieldname in self.form.fields:
                params[fieldname] = self.form.cleaned_data[fieldname]
            Exercise.add_exr(**params)
            return HttpResponseRedirect(reverse('timing:workout_detail', args=[self.wrk_id]))
        else:
            super().form_invalid(self.form)


@login_required
def new_exercise(request, wrk_id):
    '''Creates an Exercise instance, uses custom logic inside the model'''
    workout = Workout.objects.get(id=wrk_id)
    if workout.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = MyExerciseForm()
    else:
        # POST
        form = MyExerciseForm(request.POST)
        if form.is_valid():
            params = {'plan': workout}
            for fieldname in form.fields:
                params[fieldname] = form.cleaned_data[fieldname]
            Exercise.add_exr(**params)
            return HttpResponseRedirect(reverse('timing:workout_detail', args=[wrk_id]))
    context = {'form': form, 'workout': workout}
    return render(request, 'timing/new_exercise.html', context)


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    '''Updates Workout instance'''
    model = Workout
    pk_url_kwarg = 'wrk_id'
    fields = ['name', 'warmup_time', 'cooldown_time', 'laps']
    template_name = 'timing/update_workout.html'
    success_url = '..'

    def setup(self, request, *args, **kwargs):
        wrk_id = kwargs['wrk_id']
        workout = get_object_or_404(Workout, id=wrk_id)
        if workout.owner != request.user:
            raise Http404
        super().setup(request, *args, **kwargs)


class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    '''Updates Exercise instance'''
    model = Exercise
    pk_url_kwarg = 'exr_id'
    fields = ['name', 'duration', 'preptime']
    template_name = 'timing/update_exercise.html'
    success_url = '..'

    def setup(self, request, *args, **kwargs):
        wrk_id = kwargs['wrk_id']
        self.workout = get_object_or_404(Workout, id=wrk_id)
        if self.workout.owner != request.user:
            raise Http404
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['workout'] = self.workout
        return context_data


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    '''Deletes this Workout instance'''
    template_name = 'timing/workout_deletion.html'
    success_url = '/workouts'
    pk_url_kwarg = 'wrk_id'
    model = Workout

    def setup(self, request, *args, **kwargs):
        wrk_id = kwargs['wrk_id']
        workout = get_object_or_404(Workout, id=wrk_id)
        if workout.owner != request.user:
            raise Http404
        super().setup(request, *args, **kwargs)


@login_required
def exercise_delete(request, wrk_id, exr_id):
    '''Deletes this Exercise instance, uses custom logic inside the model'''
    exercise = get_object_or_404(Exercise, id=exr_id)
    workout = get_object_or_404(Workout, id=wrk_id)
    if workout.owner != request.user:
        raise Http404
    if request.method == 'POST':
        exercise.del_exr()
        return HttpResponseRedirect(reverse('timing:workout_detail', args=[wrk_id]))
    context = {'exercise': exercise, 'workout': workout}
    return render(request, 'timing/exercise_deletion.html', context)


@login_required
def workout_detail(request, wrk_id):
    '''Shows details for current Workout'''
    workout = get_object_or_404(Workout, id=wrk_id)
    if workout.owner != request.user:
        raise Http404
    exr_ids = workout.exrs
    exercises = []
    for idn in exr_ids:
        obj = Exercise.objects.get(id=idn)
        exercises.append(obj)
    context = {'workout': workout, 'exercises': exercises}
    return render(request, 'timing/workout_plan.html', context)


class ExerciseDetailView(LoginRequiredMixin, DetailView):
    '''Shows details for current Exercise'''
    template_name = "timing/exr_details.html"
    model = Exercise
    pk_url_kwarg = "exr_id"

    def get(self, request, *args, **kwargs):
        self.exr_id = kwargs["exr_id"]
        self.wrk_id = kwargs["wrk_id"]
        self.user = request.user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercise'] = get_object_or_404(Exercise, id=self.exr_id)
        workout = get_object_or_404(Workout, id=self.wrk_id)
        if workout.owner != self.user:
            raise Http404
        context['workout'] = workout
        return context