from django.urls import path
from . import views

app_name = 'timing'
urlpatterns = [
    path('', views.home, name='home_page'),
    path('workouts', views.WorkoutListView.as_view(), name='show_workouts'),
    path('new_workout', views.WorkoutCreateView.as_view(), name='new_workout'),
    ]