from django.contrib.auth.forms import UserCreationForm, UsernameField

from django.contrib.auth.models import User


class TimerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")