import re
from typing import TYPE_CHECKING

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
