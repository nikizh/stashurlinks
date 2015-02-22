from django.shortcuts import render
from rest_framework import viewsets
from stashmarksApp import models
from stashmarksApp import serializers
from rest_framework import permissions


def index(request):
    context_dict = {'msg': "Hello"}
    return render(request, 'stashmarksApp/index.html', context_dict)


def register(request):
    context_dict = {'page_title': 'Register'}
    return render(request, 'stashmarksApp/register.html', context_dict)


def sign_in(request):
    context_dict = {'page_title': 'Sign In'}
    return render(request, 'stashmarksApp/register.html', context_dict)


# Restricted API


def my_stash(request):
    context_dict = {}
    return render(request, 'stashmarksApp/my_stash.html', context_dict)


def my_stash_add(request):
    context_dict = {}
    return render(request, 'stashmarksApp/my_stash_add.html', context_dict)


def links(request):
    context_dict = {}
    return render(request, 'stashmarksApp/links.html', context_dict)


def sign_out(request):
    context_dict = {}
    return render(request, 'stashmarksApp/links.html', context_dict)


# REST API


class MyTagsViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.order_by('-date_created')
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 10


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_queryset(self):
        user = self.request.user
        return models.Tag.objects.filter(owner=user)


class AllTagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tag.objects.order_by('-date_created')
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 10


class MyBookmarksViewSet(viewsets.ModelViewSet):
    queryset = models.Bookmark.objects.order_by('-date_created')
    serializer_class = serializers.BookmarkSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 10


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_queryset(self):
        user = self.request.user
        return models.Bookmark.objects.filter(owner=user)


class AllBookmarksViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Bookmark.objects.order_by('-date_created')
    serializer_class = serializers.BookmarkSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 10




