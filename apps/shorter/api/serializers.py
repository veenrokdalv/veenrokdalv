from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.shorter.models import LinkAlias


class PublicLinkAliasSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(
        label=_('Короткая ссылка'),
        read_only=True,
    )

    class Meta:
        model = LinkAlias
        fields = ['url', 'alias', 'short_url', 'created_date']
        read_only_fields = ['short_url', 'created_date']
