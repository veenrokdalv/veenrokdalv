from django.contrib import admin

from apps.shorter import models


@admin.register(models.LinkAlias)
class LinkAliasAdmin(admin.ModelAdmin):
    list_display = ['url', 'alias', 'created_date', 'modified_date']
