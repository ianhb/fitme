from django.conf.urls import url, include

from exercise.views.exercise_views import *
from exercise.views.log_views import *
from exercise.views.routine_views import *
from exercise.views.views import exercise_home
from exercise.views.workout_views import *

exercise_list_urls = [
    url(r'^(?P<filter_type>\w+)/(?P<filter_main>\w+)/$', list_exercises, name='list_exercises'),
    url(r'^(?P<filter_type>\w+)/(?P<filter_main>\w+)/(?P<second_filter>\w+)/$',
        list_exercises, name='list_exercises'),
]

routines_urls = [
    url(r'^my/$', my_routines, name='my_routines'),
    url(r'^followed/$', followed_routines, name='followed_routines'),
    url(r'^(?P<pk>[0-9]+)/', routine_detail, name='routine_detail'),
    url(r'^search/', search_routines, name='routine_search'),
    url(r'^create/', create_routine, name='create_routine'),
    url(r'^follow/(?P<pk>[0-9]+)/', follow_routine, name='routine_follow'),
    url(r'^unfollow/(?P<pk>[0-9]+)/', unfollow_routine, name='routine_unfollow'),
]

workout_urls = [
    url(r'^my/$', my_workouts, name='my_workouts'),
    url(r'^(?P<pk>[0-9]+)/', workout_detail, name='workout_detail'),
    url(r'^create/$', create_workout, name='create_workout'),
    url(r'^record/$', record_workout, name='choose_workout_to_log'),
    url(r'^record/(?P<pk>[0-9]+)/', record_workout, name='record_workout'),
    url(r'^search/$', search_workout, name='workout_search'),
    url(r'^add/(?P<pk>[0-9]+)/', add_to_workout, name='add_to_workout'),
    url(r'^move_up/(?P<pk>[0-9]+)/', move_exercise_up, name='move_up'),
    url(r'^link/(?P<pk>[0-9]+)/', link, name='link'),
    url(r'^unlink/(?P<pk>[0-9]+)/', unlink, name='unlink'),
    url(r'^remove/(?P<pk>[0-9]+)/', remove_from_workout, name='remove_from_workout'),
]


urlpatterns = [
    url(r'^$', exercise_home, name='exercise_home'),

    url(r'^workout/', include(workout_urls)),

    url(r'^list/', include(exercise_list_urls)),
    url(r'^search/exercise/', search_exercises, name='exercise_search'),
    url(r'^exercise/(?P<pk>[0-9]+)/', exercise_detail, name='exercise_detail'),
    url(r'^create_exercise/$', create_exercise, name='create_exercise'),

    url(r'^workout_logs/$', log_list, name='workout_logs'),
    url(r'^workout_logs/(?P<pk>[0-9]+)/', log_detail, name='workout_log_detail'),

    url(r'^routines/', include(routines_urls))

]
