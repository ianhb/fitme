from django.conf.urls import url

from exercise import views

urlpatterns = [
    url(r'^$', views.exercise_home, name='exercise_home'),
]
