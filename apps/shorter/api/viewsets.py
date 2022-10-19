from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.viewsets import ModelViewSet

from apps.shorter.api.serializers import PublicLinkAliasSerializer
from apps.shorter.services import get_all_links, get_link_by_alias


class LinkAliasViewSet(ModelViewSet):
    serializer_class = PublicLinkAliasSerializer
    queryset = get_all_links()
    lookup_field = 'alias'
    lookup_url_kwarg = 'alias'

    def get_object(self):
        try:
            return get_link_by_alias(alias=self.kwargs[self.lookup_url_kwarg])
        except ObjectDoesNotExist:
            raise Http404()
