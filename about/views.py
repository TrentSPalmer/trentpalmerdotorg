from django.shortcuts import render


def apps(request):
    return render(request, 'about/apps.html')
