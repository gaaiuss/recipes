from django.test import TestCase
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ("username", "Your username."),
            ("email", "Your e-mail."),
            ("first_name", "Ex.: Paulo."),
            ("last_name", "Ex.: Guina."),
            ("password", "Your password."),
            ("password2", "Repeat your password."),
        ],
    )
    def test_fields_placeholder(
        self,
        field_name: str,
        desired: str,
    ):
        form = RegisterForm()
        current = form[field_name].field.widget.attrs["placeholder"]

        if desired != current:
            msg = f"Expected '{desired}', got '{current}'"
            raise AssertionError(msg)

    @parameterized.expand(
        [
            (
                "username",
                (
                    "Required. 150 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."
                ),
            ),
            ("email", "E-mail must be valid. Ex: pauloguina@email.com"),
            (
                "password",
                (
                    "Password must contain at least 8 characters, uppercase and "
                    "lowercase strings and a number."
                ),
            ),
        ],
    )
    def test_fields_help_text(
        self,
        field_name: str,
        desired: str,
    ):
        form = RegisterForm()
        current = form[field_name].field.help_text

        if desired != current:
            msg = f"Expected '{desired}', got '{current}'"
            raise AssertionError(msg)
