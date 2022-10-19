from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.shorter.api.viewsets import LinkAliasViewSet

router = DefaultRouter()

router.register('link', LinkAliasViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
