from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView

from users.apps import UsersConfig
from django.urls import path

from users.views import (
    UserCreateView,
    email_verification,
    CustomLoginView,
    UserPasswordResetView,
    NoMailView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("login/", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", UserCreateView.as_view(), name="registration"),
    path("email-confirm/<str:token>", email_verification, name="email-confirm"),
    path("password-reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("no_mail/", NoMailView.as_view(), name="no_mail"),
]
