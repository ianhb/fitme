from django.conf.urls import url

from supplementation import views

urlpatterns = [
    url(r'^$', views.supplement_home, name='supplement_home'),
]
