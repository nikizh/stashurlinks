from django.shortcuts import render


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
