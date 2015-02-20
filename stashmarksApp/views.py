from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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


class TagsViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_queryset(self):
        user = self.request.user
        return models.Tag.objects.filter(owner=user)
