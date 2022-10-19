from django.contrib import admin

from apps.accounts import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', models.User.USERNAME_FIELD, 'first_name', 'last_name', 'date_registered')
    search_fields = ('id', models.User.USERNAME_FIELD)
