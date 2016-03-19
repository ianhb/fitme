from django.conf.urls import url, include

from nutrition import views

log_urls = [
    url(r'^new/$', views.log_foods, name='log_food'),
    url(r'^day/', views.day_log, name='day_log'),
    url(r'^week/', views.week_log, name='week_log'),
    url(r'^month/', views.month_log, name='month_log')
]

goals_urls = [
    url(r'^view/', views.view_goals, name='view_goals'),
    url(r'^set/', views.set_goals, name='set_goals')
]

urlpatterns = [
    url(r'^$', views.nutrition_home, name='nutrition_home'),
    url(r'^search/$', views.search_foods, name='search_foods'),
    url(r'^log/', include(log_urls)),
    url(r'^goals/', include(goals_urls))
]
