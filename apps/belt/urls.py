from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^wishes$', views.wishes),
    url(r'^addwish$', views.addwish),
    url(r'^process_wish$', views.process_wish),
    url(r'^view_wish/(?P<id>\d+)$', views.view_wish, name='view_wish'),
    url(r'^join_wish/(?P<id>\d+)$', views.join_wish),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^delete/(?P<id>\d+)$', views.delete),
]
