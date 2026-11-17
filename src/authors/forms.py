from typing import TYPE_CHECKING, Any

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    from django.forms.fields import Field


def add_attr(field: Field, attr_name: str, attr_val: str) -> None:
    existing = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"`{existing} {attr_val}".strip()


def add_placeholder(field: Field, placeholder_val: str) -> None:
    add_attr(field, "placeholder", placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        # Here we are modifying a specific field attribute using custom functions
        add_placeholder(self.fields["username"], "Your username.")
        add_placeholder(self.fields["email"], "Your e-mail.")
        add_placeholder(self.fields["first_name"], "Ex.: Paulo.")
        add_placeholder(self.fields["last_name"], "Ex.: Guina.")
        add_attr(self.fields["username"], "css", "a-css-class")

    # Here we are rewriting the password field with custom parameters and
    # creating a password2 field for password confirmation.
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Your password."}),
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat your password."}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        # exclude = ["first_name"]

        labels = {
            "username": "Username:",
            "first_name": "First Name:",
            "last_name": "Last Name:",
            "password": "Password:",
            "email": "E-mail:",
        }

        # These fields can be modified to rewrite some fields. As we are creating
        # then above, we do not need to use then.

        # help_texts = {
        #     "email": "E-mail must be valid.",
        # }

        # error_messages = {
        #     "username": {
        #         "required": "This field is required.",
        #     },
        # }

        # widgets = {
        #     "password": forms.PasswordInput(
        #         attrs={
        #             "placeholder": "Type your password here.",
        #         },
        #     ),
        # }

    # Validating a single field.
    def clean_password(self) -> str | None:
        data = self.cleaned_data.get("password")

        # Checking if the word attention is in the password field.
        if data is not None and "attention" in data:
            msg = "Password cannot be cleaned because it is in attention status."
            raise ValidationError(msg, code="Invalid")

        return data

    # After Django validates every field like above, it calls the clean() method
    # to validade everything.
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            msg = "Password and password 2 must be equal."
            raise ValidationError(
                {
                    "password": msg,
                    # You can send as many field errors as you want.
                    # "password2": msg,
                    # Or a list as well.
                    # "password2": [msg, "Another error."],
                },
            )

        return cleaned_data
