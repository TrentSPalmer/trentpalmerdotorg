from django.urls import path
from . import views

app_name = "about"

urlpatterns = [
    path('apps/', views.apps, name='apps'),
]
