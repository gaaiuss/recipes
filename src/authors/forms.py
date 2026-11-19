import re
from typing import TYPE_CHECKING, Any

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

if TYPE_CHECKING:
    from django.forms.fields import Field


def add_attr(field: Field, attr_name: str, attr_val: str) -> None:
    existing = field.widget.attrs.get(attr_name, "")
    field.widget.attrs[attr_name] = f"{existing} {attr_val}".strip()


def add_placeholder(field: Field, placeholder_val: str) -> None:
    add_attr(field, "placeholder", placeholder_val)


def strong_password(password: str) -> None:
    regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$")

    if not regex.match(password):
        msg = (
            "Password must contain at least 8 characters, uppercase and "
            "lowercase strings and a number."
        )
        raise ValidationError(msg, code="Invalid")


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore # noqa: ANN002, ANN003
        super().__init__(*args, **kwargs)
        # Here we are modifying a specific field attribute using custom functions
        add_placeholder(self.fields["username"], "Your username.")
        add_placeholder(self.fields["email"], "Your e-mail.")
        add_placeholder(self.fields["first_name"], "Ex.: Paulo.")
        add_placeholder(self.fields["last_name"], "Ex.: Guina.")
        add_placeholder(self.fields["password"], "Your password.")
        add_placeholder(self.fields["password2"], "Repeat your password.")

    # Here we are rewriting the password field with custom parameters and
    # creating a password2 field for password confirmation.
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[strong_password],
        help_text=(
            "Password must contain at least 8 characters, uppercase and "
            "lowercase strings and a number."
        ),
        label="Password:",
        error_messages={"required": "Password must not be empty."},
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[strong_password],
        label="Repeat your password:",
        error_messages={"required": "Please, repeat your password."},
    )

    first_name = forms.CharField(
        label="First Name:",
        error_messages={"required": "Write your first name."},
    )

    last_name = forms.CharField(
        label="Last Name:",
        error_messages={"required": "Write your last name."},
    )

    email = forms.EmailField(
        label="E-mail:",
        error_messages={"required": "E-mail is required."},
        help_text="E-mail must be valid. Ex: pauloguina@email.com",
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        # exclude = ["first_name"]

        labels = {
            "username": "Username:",
        }

        # These fields can be modified to rewrite some fields. As we are creating
        # then above, we do not need to use then.

        help_texts = {
            "username": (
                "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
            ),
        }

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
    # def clean_password(self) -> str | None:
    #     data = self.cleaned_data.get("password")

    #     # Checking if the word attention is in the password field.
    #     if data is not None and "attention" in data:
    #         msg = "Password cannot be cleaned because it is in attention status."
    #         raise ValidationError(msg, code="Invalid")

    #     return data

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
