from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
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

    @parameterized.expand(
        [
            ("username", "Username:"),
            ("first_name", "First Name:"),
            ("last_name", "Last Name:"),
            ("password", "Password:"),
            ("password2", "Repeat your password:"),
            ("email", "E-mail:"),
        ],
    )
    def test_fields_label(
        self,
        field_name: str,
        desired: str,
    ):
        form = RegisterForm()
        current = form[field_name].field.label

        if desired != current:
            msg = f"Expected '{desired}', got '{current}'"
            raise AssertionError(msg)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            "username": "user",
            "email": "email@email.com",
            "first_name": "first",
            "last_name": "last",
            "password": "Str0ngPassword1",
            "password2": "Str0ngPassword1",
        }

        return super().setUp()

    @parameterized.expand(
        [
            ("username", "This field is required."),
            ("first_name", "Write your first name."),
            ("last_name", "Write your last name."),
            ("password", "Password must not be empty."),
            ("password2", "Please, repeat your password."),
            ("email", "E-mail is required."),
        ],
    )
    def test_fields_cannot_be_empty(self, field: str, msg: str) -> None:
        self.form_data[field] = ""
        url = reverse("authors:create")

        response = self.client.post(
            url,
            data=self.form_data,
            follow=True,  # When you have a url that redirects you must specify this.
        )
        response_content = response.content.decode("utf-8")
        context_form_errors = response.context["form"].errors.get(field)

        if msg not in response_content:
            error_msg = (
                f"Field '{field}' message '{msg}' not found in response content."
            )
            raise AssertionError(error_msg)

        if msg not in context_form_errors:
            error_msg = (
                f"Field '{field}' message '{msg}' not found in form field errors."
            )
            raise AssertionError(error_msg)
