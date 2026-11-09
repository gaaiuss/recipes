from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password", "email"]
        # exclude = ["first_name"]

        labels = {
            "username": "Username:",
            "first_name": "First Name:",
            "last_name": "Last Name:",
            "password": "Password:",
            "email": "E-mail:",
        }

        help_texts = {
            "email": "E-mail must be valid.",
        }

        error_messages = {
            "username": {
                "required": "This field is required.",
            },
        }

        widgets = {
            "password": forms.PasswordInput(
                attrs={
                    "placeholder": "Type your password here.",
                },
            ),
        }
