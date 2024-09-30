import secrets

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordResetView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from config.settings import EMAIL_HOST_USER
from mailing.form import StyleFormMixin
from users.form import UserRegisterForm
from users.models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserPasswordResetView(PasswordResetView, StyleFormMixin):
    form_class = PasswordResetForm
    template_name = "users/password_reset.html"
    success_url = reverse_lazy("users:password_reset_confirm")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            if user:
                password = User.objects.make_random_password(length=10)
                user.set_password(password)
                user.save()
                send_mail(
                    subject="Новый пароль",
                    message=f"Привет, вот твой новый пароль {password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[email],
                )
            return redirect(reverse("users:login"))
        except:
            return redirect(reverse("users:no_mail"))


class NoMailView(TemplateView):
    template_name = "users/no_mail.html"


class CustomLoginView(LoginView):
    model = User
    template_name = "users/login.html"  # путь к вашему шаблону логина
    redirect_authenticated_user = (
        True  # перенаправление аутентифицированных пользователей
    )


@login_required
def viewing_users(request):
    user = request.user
    users = User.objects.exclude(email="admin@example.com").prefetch_related(
        "mailing_set"
    )
    context = {"users_list": users}
    if user.has_perm("users.set_viewing_user"):
        return render(request, "users/users_list.html", context)
    return render(request, "users/no_mail.html", context)


def toggle_activity(request, pk):
    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
    else:
        user_item.is_active = True

    user_item.save()
    return redirect(reverse("users:users_for_manager"))
