from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^user$',views.user),
    url(r'^edit/(?P<id>\d+)$',views.edit),
    url(r'^update/(?P<id>\d+)$',views.update),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^delete/(?P<id>\d+)$',views.delete),
    url(r'^add$',views.add)
]