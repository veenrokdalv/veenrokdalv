from django.urls import path

from apps.accounts.views.auth_views import SignInByLoginView, SignOutView, SignUpView

app_name = 'accounts'

urlpatterns = (
    path('sign-in/', SignInByLoginView.as_view(), name='sign-in'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
)
