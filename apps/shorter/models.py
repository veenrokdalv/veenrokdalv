from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.core.models import BaseModel


class LinkAlias(BaseModel):
    """Псевдоним ссылки"""
    url = models.URLField(
        verbose_name=_('Url адресс'),
    )
    alias = models.CharField(
        verbose_name=_('Псевдоним'),
        unique=True,
        max_length=32,
    )

    class Meta:
        verbose_name = _('Сокращенная ссылка')
        verbose_name_plural = _('Сокращенные ссылки')

    def __str__(self):
        return f'{self.url} ({self.alias})'

    @property
    def short_url(self):
        kwargs = {'alias': self.alias}
        url = reverse('shorter:redirect-to-url-by-alias', kwargs=kwargs)
        return f'http://{settings.DOMAIN}{url}'
