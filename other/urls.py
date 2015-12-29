from django.conf.urls import url
from django.contrib.auth.views import login, logout

from other import views

urlpatterns = [
    url(r'^$', views.account_home, name='account_home'),
    url(r'^login/$', login, {'template_name': 'other/login.html'}, name='login'),
    url(r'^create/', views.create_account, name='create_account'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^update_weight', views.new_weight, name='new_weight'),
    url(r'^update_body_fat', views.new_bf, name='new_bf'),
    url(r'^logout/$', logout, name='logout'),
]
