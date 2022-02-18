from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('audio.urls')),
    path('accounts/', include('accounts.urls')),
    path('about/', include('about.urls')),
]
