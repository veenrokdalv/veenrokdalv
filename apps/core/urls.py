from django.contrib import admin
from django.urls import path, include

from apps.core.views import HomeView

urlpatterns = [
    path('', HomeView.as_view()),
    path('', include('apps.shorter.urls')),
]
