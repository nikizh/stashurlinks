from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from stashmarksApp import models, serializers
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status


def index(request):
    context_dict = {}

    if request.user.is_authenticated():
        return redirect('my_stash')

    return render(request, 'stashmarksApp/index.html', context_dict)


@login_required
def my_stash(request):
    context_dict = {}
    return render(request, 'stashmarksApp/my_stash.html', context_dict)


@login_required
def my_stash_add(request):
    context_dict = {}
    return render(request, 'stashmarksApp/my_stash_add.html', context_dict)


@login_required
def links(request):
    context_dict = {}
    return render(request, 'stashmarksApp/links.html', context_dict)


@login_required
def settings(request):
    context_dict = {}
    return render(request, 'stashmarksApp/settings.html', context_dict)


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


class SearchTagsView(APIView):

    def get(self, request, *args, **kw):
        query = request.query_params["q"]
        result = models.Tag.objects.filter(name__startswith=query).values_list('name', flat=True).distinct()
        serializedResult = [{'name':x} for x in result]
        return Response(serializedResult, status=status.HTTP_200_OK)


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
    paginate_by = 6

    def get_queryset(self):
        if "tags" in self.request.query_params:
            tags = self.request.query_params["tags"].split(",")
            return models.Bookmark.objects.filter(public=True, tags__name__in=tags)
        elif "q" in self.request.query_params:
            query = self.request.query_params["q"]
            return models.Bookmark.objects.filter(public=True, title__contains=query)
        else:
            return models.Bookmark.objects.filter(public=True).order_by('-date_created')
