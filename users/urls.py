from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    CustomLoginView,
    NoMailView,
    UserPasswordResetView,
    UserRegisterView,
    email_verification,
    toggle_activity,
    viewing_users,
)

app_name = UsersConfig.name


urlpatterns = [
    path("login/", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", UserRegisterView.as_view(), name="registration"),
    path("email-confirm/<str:token>", email_verification, name="email-confirm"),
    path("password-reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("no_mail/", NoMailView.as_view(), name="no_mail"),
    path("users/", viewing_users, name="users_for_manager"),
    path("activity/<int:pk>/", toggle_activity, name="toggle_activity"),
]
