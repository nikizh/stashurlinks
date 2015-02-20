from django.conf.urls import patterns, url, include
from rest_framework import routers
from stashmarksApp import views

router = routers.DefaultRouter()
router.register(r'tags', views.TagsViewSet)

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^api/', include(router.urls)),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^signin/$', views.sign_in, name='signin'),
                       url(r'^mystash/$', views.my_stash, name='my_stash'),
                       url(r'^mystash/add/$', views.my_stash_add, name='my_stash_add'),
                       url(r'^links/$', views.links, name='links'),)
