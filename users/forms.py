from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser
from .validators import (
    validate_confusables,
    validate_confusables_email,
    validate_reserved_name,
)


class UserAdminForm(forms.ModelForm):
    def clean_username(self):

        username = self.data.get("username")

        validate_confusables(value=username, exception_class=ValidationError)

        validate_reserved_name(value=username, exception_class=ValidationError)

        return self.cleaned_data["username"]

    def clean_email(self):

        email = self.data.get("email")

        local_part, domain = self.data.get("email")

        validate_confusables_email(
            local_part=local_part, domain=domain, exception_class=ValidationError
        )

        validate_reserved_name(value=email, exception_class=ValidationError)

        return self.cleaned_data["email"]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
