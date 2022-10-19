from django.urls import reverse_lazy
from django.views.generic import RedirectView


class HomeView(RedirectView):

    url = reverse_lazy('shorter:link-alias-create')
