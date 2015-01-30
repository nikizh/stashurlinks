from django.shortcuts import render

def index(request):
    context_dict = {'msg': "Hello"}

    return render(request, 'stashmarksApp/index.html', context_dict)
