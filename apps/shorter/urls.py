from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.shorter.views import RedirectToUrlByAlias, CreateLinkAlias

app_name = 'shorter'
urlpatterns = [
    path('create/', CreateLinkAlias.as_view(), name='link-alias-create'),
    path('<str:alias>/', RedirectToUrlByAlias.as_view(), name='redirect-to-url-by-alias'),
]


