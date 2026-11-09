from typing import TYPE_CHECKING

from django import forms
from django.contrib.auth.models import User

if TYPE_CHECKING:
    from django.forms.fields import Field


def add_placeholder(field: Field, placeholder_val: str) -> None:
    field.widget.attrs["placeholder"] = placeholder_val


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Your username.")
        add_placeholder(self.fields["email"], "Your e-mail.")
        add_placeholder(self.fields["first_name"], "Ex.: Paulo.")
        add_placeholder(self.fields["last_name"], "Ex.: Guina.")

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
