import os
from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from stashmarksApp import models, serializers
from django.contrib.auth.decorators import login_required
from allauth.account.forms import ChangePasswordForm
from django.views.decorators.clickjacking import xframe_options_exempt
from urllib import parse


def index(request):
    context_dict = {}

    if request.user.is_authenticated():
        return redirect('my_stash')

    return render(request, 'stashmarksApp/index.html', context_dict)


@login_required
def my_stash(request):
    context_dict = {}
    return render(request, 'stashmarksApp/my_stash.html', context_dict)


@xframe_options_exempt
def my_stash_add(request, title, url):

    # Escape quote
    escaped_title = title.replace("'", "\\'")

    context_dict = {
        'title': escaped_title,
        'url': parse.unquote(url),
    }

    print(context_dict['title'])
    return render(request, 'stashmarksApp/my_stash_add.html', context_dict)


@login_required
def links(request):
    context_dict = {}
    return render(request, 'stashmarksApp/links.html', context_dict)


@login_required
def settings(request):
    context_dict = {}

    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('account_login')
        else:
            context_dict['error'] = True
    else:
        form = ChangePasswordForm(user=request.user)

    context_dict['form'] = form

    return render(request, 'stashmarksApp/settings.html', context_dict)


# REST API
class AllTagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if "q" in self.request.query_params:
            query = self.request.query_params["q"]
            return models.Tag.objects.filter(name__startswith=query).distinct()
        else:
            return models.Tag.objects.all()


class MyBookmarksViewSet(viewsets.ModelViewSet):
    queryset = models.Bookmark.objects.order_by('-date_created')
    serializer_class = serializers.BookmarkSerializer
    permission_classes = (permissions.IsAuthenticated,)
    paginate_by = 10

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        bookmarksQuery = models.Bookmark.objects.filter(owner=user)
        if "visibility" in self.request.query_params:
            visibility = True if self.request.query_params["visibility"] == "pub" else False
            bookmarksQuery = bookmarksQuery.filter(public=visibility)
        if "tags" in self.request.query_params:
            tags = self.request.query_params["tags"].split(",")
            bookmarksQuery = bookmarksQuery.filter(owner=user, tags__name__in=tags)
        elif "q" in self.request.query_params:
            query = self.request.query_params["q"]
            bookmarksQuery = bookmarksQuery.filter(owner=user, title__contains=query)

        return bookmarksQuery.order_by('-date_created')

    def perform_destroy(self, instance):
        from stashmarksProj import settings

        if instance.thumb and instance.thumb is not 'placeholder.png':
            thumb_file = os.path.join(settings.THUMBS_PATH, instance.thumb)

            if os.path.isfile(thumb_file):
                os.remove(thumb_file)

        super().perform_destroy(instance)


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
