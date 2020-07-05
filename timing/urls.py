from django.urls import path
from . import views

app_name = 'timing'
urlpatterns = [
    path('', views.home, name='home_page'),
    path('workouts/', views.WorkoutListView.as_view(), name='show_workouts'),
    path('new-workout/', views.WorkoutCreateView.as_view(), name='new_workout'),
    path('workouts/<int:wrk_id>/', views.WorkoutDetailView.as_view(), name='workout_detail'),
    path('workouts/<int:wrk_id>/update/', views.WorkoutUpdateView.as_view(), name='workout_update'),
    path('workouts/<int:wrk_id>/new/', views.ExerciseCreateView.as_view(), name='new_exercise'),
    path('workouts/<int:wrk_id>/<int:exr_id>/', views.ExerciseDetailView.as_view(), name='exr_detail'),
    path('workouts/<int:wrk_id>/<int:exr_id>/update/', views.ExerciseUpdateView.as_view(), name='exr_update'),
    path('workouts/<int:wrk_id>/del-confirmation/', views.WorkoutDeleteView.as_view(), name='del_workout'),
    path('workouts/<int:wrk_id>/<int:exr_id>/del-confirmation/',
         views.exercise_delete, name='del_exercise'),
    path('workouts/draggy/', views.drag_drop, name='draggy'),
    path('workouts/del-test/', views.del_test, name='del-test'),
    path('test_timer/', views.test_timer, name='test_timer'),
    ]
