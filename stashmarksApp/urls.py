from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from stashmarksApp import views

router = routers.DefaultRouter()
router.register(r'mytags', views.MyTagsViewSet)
router.register(r'alltags', views.AllTagsViewSet)
router.register(r'mybookmarks', views.MyBookmarksViewSet)
router.register(r'allbookmarks', views.AllBookmarksViewSet)

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^api/', include(router.urls)),
                       url(r'^mystash/$', views.my_stash, name='my_stash'),
                       url(r'^mystash/add/$', views.my_stash_add, name='my_stash_add'),
                       url(r'^links/$', views.links, name='links'),
                       url(r'^settings/$', views.settings, name='settings'),
                       url(r'^api/searchTags/?$', login_required(views.SearchTagsView.as_view()), name='my_rest_view'),)
