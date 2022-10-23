from pathlib import Path
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.urls import reverse
from django.views.generic import RedirectView, FormView

from apps.shorter.forms import CreateLinkAliasForm
from apps.shorter.services import get_link_by_alias


class RedirectToUrlByAlias(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        try:
            link = get_link_by_alias(alias=self.kwargs['alias'])
        except ObjectDoesNotExist:
            raise Http404()

        return link.url

class CreateLinkAlias(SuccessMessageMixin, FormView):

    form_class = CreateLinkAliasForm
    template_name = 'shortener/link-alias-create.html'
    success_url = '/'

    def get_success_message(self, cleaned_data):
        link = get_link_by_alias(alias=cleaned_data['alias'])
        return f'Скоращенная ссылка: {link.short_url}'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
