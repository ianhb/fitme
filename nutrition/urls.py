from django.conf.urls import url

from nutrition import views

urlpatterns = [
    url(r'^$', views.nutrition_home, name='nutrition_home'),
]
