from django.contrib.auth.forms import UserCreationForm

from mailing.form import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


# class UserLoginForm(StyleFormMixin, UserLoginView):
#     class Meta:
#         model = User
#         fields = ("email", "password")
