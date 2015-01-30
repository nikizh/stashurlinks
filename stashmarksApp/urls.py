from django.conf.urls import patterns, url
from stashmarksApp import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        )
