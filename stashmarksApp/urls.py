from django.conf.urls import patterns, url, include
from rest_framework import routers
from stashmarksApp import views

router = routers.DefaultRouter()
router.register(r'alltags', views.AllTagsViewSet)
router.register(r'mybookmarks', views.MyBookmarksViewSet)
router.register(r'allbookmarks', views.AllBookmarksViewSet)

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^api/', include(router.urls)),
                       url(r'^api/rating/(?P<bookmarkId>[0-9]+)/$', views.RateBookmark.as_view()),
                       url(r'^mystash/$', views.my_stash, name='my_stash'),
                       url(r'^mystash/add/title/(?P<title>.*)/url/(?P<url>.*)$', views.my_stash_add, name='my_stash_add'),
                       url(r'^links/$', views.links, name='links'),
                       url(r'^settings/$', views.settings, name='settings'),)
