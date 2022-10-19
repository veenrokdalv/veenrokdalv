from django.utils.translation import gettext_lazy as _
from django.db import models


class BaseModel(models.Model):
    """Базовая модель"""
    created_date = models.DateTimeField(
        verbose_name=_('Дата и время добавления'),
        db_index=True,
        auto_now_add=True,
    )
    modified_date = models.DateTimeField(
        verbose_name=_('Дата и время изменения'),
        db_index=True,
        auto_now_add=True,
    )

    class Meta:
        abstract = True
