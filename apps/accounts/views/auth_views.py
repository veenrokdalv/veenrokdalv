from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import RedirectURLMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView

from apps.accounts.forms.auth_forms import SignInByLoginForm, SignUpForm
from apps.core.mixins.context_mixins import SiteContextDataMixin


class SignInByLoginView(SiteContextDataMixin, SuccessMessageMixin, RedirectURLMixin, FormView):
    site_name = 'Veenrok'
    page_title = 'Вход'
    template_name = 'accounts/auth/sign-in.html'
    form_class = SignInByLoginForm
    success_message = 'Вы успешно вошли в аккаунт!'

    def get_default_redirect_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        user_authenticated = form.get_user_authenticated()
        login(user=user_authenticated, request=self.request)
        return super().form_valid(form=form)


class SignUpView(SiteContextDataMixin, SuccessMessageMixin, RedirectURLMixin, FormView):
    site_name = 'Veenrok'
    page_title = 'Регистрация'
    template_name = 'accounts/auth/sign-up.html'
    form_class = SignUpForm
    success_message = 'Вы успешно зарегистрировались!'
    next_page = reverse_lazy('accounts:sign-up')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SignOutView(RedirectView):

    def post(self, request, *args, **kwargs):
        logout(request=request)
        messages.success(request=request, message='Вы успешно вышли из аккаунта, до встречи!')
        return redirect('home')

    get = post
