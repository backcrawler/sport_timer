from builtins import super

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer

from .models import Exercise, Workout
from .forms import WorkoutForm, ExerciseForm, MyExerciseForm


def home(request):
    '''Shows homepage'''
    return render(request, 'timing/home.html')


class WorkoutListView(LoginRequiredMixin, ListView):
    """Shows all Workouts"""
    model = Workout
    template_name = 'timing/workout_list.html'

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        super().setup(request, *args, **kwargs)

    def get_queryset(self):
        workouts = self.model.objects.filter(owner=self.user).order_by('-date_added')
        return workouts


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    '''shows students for each group, shadows group_details'''
    template_name = "timing/workout_plan.html"
    model = Workout
    pk_url_kwarg = "wrk_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = context.get('workout')
        if workout.owner != self.request.user:
            raise Http404
        context['exercises'] = workout.exercise_set.order_by('order')
        return context


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    '''Creates a Workout instance'''
    template_name = 'timing/new_workout.html'
    success_url = reverse_lazy('timing:show_workouts')
    model = Workout
    fields = ['name', 'warmup_time', 'cooldown_time']

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    '''Updates Workout instance'''
    model = Workout
    fields = ['name', 'warmup_time', 'cooldown_time', 'laps']
    pk_url_kwarg = 'wrk_id'
    template_name = 'timing/update_workout.html'
    success_url = '..'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = context.get('workout')
        if workout.owner != self.request.user:
            raise Http404
        return context


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    '''Deletes this Workout instance'''
    template_name = 'timing/workout_deletion.html'
    success_url = reverse_lazy('timing:show_workouts')
    pk_url_kwarg = 'wrk_id'
    model = Workout

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = context.get('workout')
        if workout.owner != self.request.user:
            raise Http404
        return context


class ExerciseDetailView(LoginRequiredMixin, DetailView):
    '''Shows details for current Exercise'''
    template_name = "timing/exr_details.html"
    model = Exercise
    pk_url_kwarg = "exr_id"

    def get(self, request, *args, **kwargs):
        self.wrk_id = kwargs["wrk_id"]
        self.user = request.user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        workout = get_object_or_404(Workout, id=self.wrk_id)
        if workout.owner != self.user:
            raise Http404
        context['workout'] = workout
        return context


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    '''Creates an Exercise instance, uses custom logic inside the model'''
    template_name = 'timing/new_exercise.html'
    success_url = '..'
    form_class = ExerciseForm
    pk_url_kwarg = 'wrk_id'

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        self.workout = get_object_or_404(Workout, id=kwargs[self.pk_url_kwarg])
        if self.workout.owner != self.user:
            raise Http404
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout'] = self.workout
        print(context)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.plan = self.workout
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ExerciseUpdateView(LoginRequiredMixin, UpdateView):
    '''Updates Exercise instance'''
    model = Exercise
    pk_url_kwarg = 'exr_id'
    fields = ['name', 'duration', 'preptime', 'kind']
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


@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def drag_drop(request):
    if request.method != 'POST':
        raise Http404
    ids = tuple(map(lambda x: int(x), request.POST.getlist('exrs[]')))
    print('IDS:',ids)
    selected_posts = Exercise.objects.filter(id__in=ids)
    response_data = {}
    ownage_checked = all(map(lambda x: x.plan.owner == request.user, selected_posts))
    if len(ids) == selected_posts.count() and ownage_checked:
        response_data['result'] = 'Success'
        mapping = {id_: order for order, id_ in enumerate(ids)}
        for exr in selected_posts:
            exr.order = mapping[exr.id]
            exr.save()
            print('DONE')
    else:
        response_data['result'] = 'Failure'
    return Response(data=response_data)
    # return HttpResponse(
    #     json.dumps(response_data),
    #     content_type="application/json"
    # )


def del_test(request):
    if request.method != 'POST':
        raise Http404
    print('RECEIVED:', request.POST)
    name = request.POST.get('name')
    print(name)
    return HttpResponseRedirect(redirect_to='/')
