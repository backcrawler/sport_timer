from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'timing'
urlpatterns = [
    path('', views.home, name='home_page'),
    path('workouts', views.show_workouts, name='show_workouts'),
    path('new-workout', views.WorkoutCreateView.as_view(), name='new_workout'),
    path('thisworkout/(<int:wrk_id>)', views.workout_detail, name='workout_detail'),
    path('thisworkout/(<int:wrk_id>/update)', views.WorkoutUpdateView.as_view(), name='workout_update'),
    path('thisworkout/(<int:wrk_id>)/new', views.new_exercise, name='new_exercise'),
    path('thisworkout/(<int:wrk_id>)/(<int:exr_id>)', views.ExerciseDetailView.as_view(), name='exr_detail'),
    path('thisworkout/(<int:wrk_id>)/(<int:exr_id>)/update', views.ExerciseUpdateView.as_view(), name='exr_update'),
    path('thisworkout/(<int:wrk_id>)/del-confirmation', views.WorkoutDeleteView.as_view(), name='del_workout'),
    path('thisworkout/(<int:wrk_id>)/(<int:exr_id>)/del-confirmation',
         views.exercise_delete, name='del_exercise'),
    ]
