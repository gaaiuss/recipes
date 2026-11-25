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
                    "At least 4 up to 150 characters required. Letters, digits "
                    "and @/./+/-/_ only."
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

    def test_username_char_min_length_must_be_4(self) -> None:
        self.form_data["username"] = "cai"
        url = reverse("authors:create")

        response = self.client.post(
            url,
            data=self.form_data,
            follow=True,  # When you have a url that redirects you must specify this.
        )

        response_content = response.content.decode("utf-8")
        context_form_errors = response.context["form"].errors.get("username")

        msg = "At least 4 up to 150 characters required."

        if msg not in response_content:
            error_msg = f"Username message '{msg}' not found in response content."
            raise AssertionError(error_msg)

        if msg not in context_form_errors:
            error_msg = f"Username message '{msg}' not found in username errors."
            raise AssertionError(error_msg)

    def test_username_char_max_length_must_be_150(self) -> None:
        self.form_data["username"] = "C" * 151
        url = reverse("authors:create")

        response = self.client.post(
            url,
            data=self.form_data,
            follow=True,  # When you have a url that redirects you must specify this.
        )

        response_content = response.content.decode("utf-8")
        context_form_errors = response.context["form"].errors.get("username")

        msg = "At least 4 up to 150 characters required."

        if msg not in response_content:
            error_msg = f"Username message '{msg}' not found in response content."
            raise AssertionError(error_msg)

        if msg not in context_form_errors:
            error_msg = f"Username message '{msg}' not found in username errors."
            raise AssertionError(error_msg)

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data["password"] = "abc123"  # noqa: S105
        url = reverse("authors:create")

        response = self.client.post(
            url,
            data=self.form_data,
            follow=True,  # When you have a url that redirects you must specify this.
        )

        response_content = response.content.decode("utf-8")
        context_form_errors = response.context["form"].errors.get("password")

        msg = (
            "Password must contain at least 8 characters, uppercase and "
            "lowercase strings and a number."
        )

        if msg not in response_content:
            error_msg = f"Password message '{msg}' not found in response content."
            raise AssertionError(error_msg)

        if msg not in context_form_errors:
            error_msg = f"Password message '{msg}' not found in password errors."
            raise AssertionError(error_msg)

        # Test if password is in context form errors

        self.form_data["password"] = "@A123abc123"  # noqa: S105
        url = reverse("authors:create")

        response = self.client.post(
            url,
            data=self.form_data,
            follow=True,
        )

        context_form_errors = response.context["form"].errors.get("password")

        if msg in context_form_errors:
            error_msg = f"Password message '{msg}' not found in password errors."
            raise AssertionError(error_msg)

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data["password"] = "@A123abc123"  # noqa: S105
        self.form_data["password2"] = "@A123abc1234"

        url = reverse("authors:create")

        response = self.client.post(
            url,
            data=self.form_data,
            follow=True,  # When you have a url that redirects you must specify this.
        )

        response_content = response.content.decode("utf-8")
        context_form_errors = response.context["form"].errors.get("password")

        msg = "Password and password 2 must match."

        if msg not in response_content:
            error_msg = f"Password message '{msg}' not found in response content."
            raise AssertionError(error_msg)

        if msg not in context_form_errors:
            error_msg = f"Password message '{msg}' not found in password errors."
            raise AssertionError(error_msg)

        # Test when passwords are equal

        self.form_data["password"] = "@A123abc123"  # noqa: S105
        self.form_data["password2"] = "@A123abc123"

        url = reverse("authors:create")

        response = self.client.post(
            url,
            data=self.form_data,
            follow=True,  # When you have a url that redirects you must specify this.
        )

        response_content = response.content.decode("utf-8")

        if msg in response_content:
            error_msg = f"Password message '{msg}' found in response content."
            raise AssertionError(error_msg)

    def test_send_get_request_to_register_create_view_returns_404(self) -> None:
        url = reverse("authors:create")
        response = self.client.get(url)
        status_404 = 404

        if response.status_code != status_404:
            msg = "Response did not returned 404."
            raise AssertionError(msg)

    def test_if_email_is_already_in_use(self):
        self.form_data["email"] = "email@email.com"

        url = reverse("authors:create")

        # Creating a user twice with the same data.
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        email_error_msgs = response.context["form"].errors.get("email")
        response_content = response.content.decode("utf-8")

        msg = "E-mail already in use."

        if msg not in email_error_msgs:
            error_msg = (
                f"Email message '{msg}' not found in email error messages "
                f"{email_error_msgs}"
            )
            raise AssertionError(error_msg)

        if msg not in response_content:
            error_msg = (
                f"Email message '{msg}' not found in response content "
                f"{response_content}"
            )
            raise AssertionError(error_msg)
