from django.shortcuts import render
from rest_framework import viewsets, permissions
from stashmarksApp import models, serializers


def index(request):
    context_dict = {'msg': "Hello"}
    return render(request, 'stashmarksApp/index.html', context_dict)


# Restricted API
def my_stash(request):
    context_dict = {}
    return render(request, 'stashmarksApp/my_stash.html', context_dict)


def my_stash_add(request):
    context_dict = {}
    return render(request, 'stashmarksApp/my_stash_add.html', context_dict)


def links(request):
    context_dict = {'test1': "Hello"}
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
    paginate_by = 6

    def get_queryset(self):
        return models.Bookmark.objects.filter(public=True)




