from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth import login, authenticate

from .forms import TimerCreationForm
from .models import Profile
from timing.models import Workout, Exercise


def register(request):
    if request.method != 'POST':
        form = TimerCreationForm()
    else:
        form = TimerCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # new_user.profile = Profile()
            #redirect...
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('news:mainpage'))
    context = {'form': form}
    return render(request, 'users/register.html', context)


def profile_load(request):
    '''Profile for current user'''
    valid_workouts = Workout.objects.filter(owner=request.user)
    valid_exrs = Exercise.objects.filter(plan__owner=request.user)
    context = {'wrk_num': valid_workouts.count(), 'exr_num': valid_exrs.count()}
    return render(request, 'users/userprofile.html', context=context)
