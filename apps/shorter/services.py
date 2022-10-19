from django.db.models import QuerySet

from apps.shorter.models import LinkAlias


def create_link_alias(*, url: str, alias: str) -> LinkAlias:
    link = LinkAlias(url=url, alias=alias)
    link.full_clean()
    link.save()
    return link


def get_all_links() -> QuerySet[LinkAlias]:
    return LinkAlias.objects.all()


def get_link_by_alias(alias: str) -> LinkAlias:
    return LinkAlias.objects.get(alias=alias)
