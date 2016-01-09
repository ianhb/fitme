from django.conf.urls import url

from supplementation import views

urlpatterns = [
    url(r'^$', views.supplement_home, name='supplement_home'),
    url(r'^log/$', views.log_supplement_list, name='choose_supplement_to_log'),
    url(r'^log/(?P<pk>[0-9]+)/', views.log_supplement, name='log_supplement'),
    url(r'^my_supplements/$', views.my_supplements, name='my_supplements'),

    url(r'^end/(?P<pk>[0-9]+)/', views.end_log_set, name='supplement_set_log_end'),

    url(r'^search/$', views.search_supplements, name='search_supplements'),
    url(r'^list/$', views.supplement_list, name='supplement_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.supplement_detail, name='supplement_detail'),
    url(r'^categories/(?P<pk>[0-9]+)/', views.supplement_category_detail, name='supplement_category_detail')
]
