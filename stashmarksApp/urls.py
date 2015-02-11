from django.conf.urls import patterns, url
from stashmarksApp import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^signin/$', views.sign_in, name='signin'),
                       url(r'^mystash/$', views.my_stash, name='my_stash'),
                       url(r'^mystash/add/$', views.my_stash_add, name='my_stash_add'),
                       url(r'^links/$', views.links, name='links'),)
