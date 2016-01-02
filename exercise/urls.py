from django.conf.urls import url

from exercise import views

urlpatterns = [
    url(r'^$', views.exercise_home, name='exercise_home'),
    url(r'^workout_home/$', views.workout_home, name='workout_home'),
    url(r'^my_workouts/$', views.my_workouts, name='my_workouts'),
    url(r'^workout/(?P<pk>[0-9]+)/', views.workout_detail, name='workout_detail'),
    url(r'^create_workout/$', views.create_workout, name='create_workout'),
    url(r'^record_workout/$', views.record_workout, name='record_workout'),
    url(r'^find_workout/$', views.find_workouts, name='find_workout'),

    url(r'^exercises/(?P<muscle_group>\w+)/$', views.list_exercises, name='exercises'),
    url(r'^exercises/(?P<muscle_group>\w+)/(?P<filter>\w+)$', views.list_exercises, name='exercises'),
    url(r'^exercise/(?P<pk>[0-9]+)/', views.exercise_detail, name='exercise_detail'),
    url(r'^create_exercise/$', views.create_exercise, name='create_exercise'),

    url(r'^workout_logs/$', views.workout_logs, name='workout_logs'),

]
