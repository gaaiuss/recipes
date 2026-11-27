from typing import TYPE_CHECKING

import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest

if TYPE_CHECKING:
    from collections.abc import Callable

    from selenium.webdriver.remote.webelement import WebElement


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    def get_web_element_by_placeholder(
        self,
        web_element: WebElement,
        placeholder: str,
    ) -> WebElement:
        return web_element.find_element(
            By.XPATH,
            f"//input[@placeholder='{placeholder}']",
        )

    def fill_form_dummy_data(self, form: WebElement) -> None:
        fields = form.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)

    def get_form(self) -> WebElement:
        return self.browser.find_element(
            By.XPATH,
            "/html/body/main/div[2]/form",
        )

    def form_fields_test_with_callback(
        self,
        callback: Callable[[WebElement], None],
    ):
        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()
        self.fill_form_dummy_data(form)

        form.find_element(By.NAME, "email").send_keys("dummy@email.com")

        callback(form)

        return form

    def test_empty_first_name_error_message(self) -> None:
        def callback(form: WebElement) -> None:
            first_name_field = self.get_web_element_by_placeholder(form, "Ex.: Paulo.")
            first_name_field.send_keys(" ")
            first_name_field.send_keys(Keys.ENTER)

            # Here we must reselect the form as after we pressed enter all the elements
            # in the page are new.
            form = self.get_form()

            error_message = "Write your first name."

            if error_message not in form.text:
                msg = f"'{error_message}' not found in form '{form.text}'"
                raise AssertionError(msg)

        self.form_fields_test_with_callback(callback)

    def test_empty_last_name_error_message(self) -> None:
        def callback(form: WebElement) -> None:
            last_name_field = self.get_web_element_by_placeholder(form, "Ex.: Guina.")
            last_name_field.send_keys(" ")
            last_name_field.send_keys(Keys.ENTER)

            # Here we must reselect the form as after we pressed enter all the elements
            # in the page are new.
            form = self.get_form()

            error_message = "Write your last name."

            if error_message not in form.text:
                msg = f"'{error_message}' not found in form '{form.text}'"
                raise AssertionError(msg)

        self.form_fields_test_with_callback(callback)

    def test_empty_username_error_message(self) -> None:
        def callback(form: WebElement) -> None:
            username_field = self.get_web_element_by_placeholder(
                form,
                "Your username.",
            )
            username_field.send_keys(" ")
            username_field.send_keys(Keys.ENTER)

            # Here we must reselect the form as after we pressed enter all the elements
            # in the page are new.
            form = self.get_form()

            error_message = "This field is required."

            if error_message not in form.text:
                msg = f"'{error_message}' not found in form '{form.text}'"
                raise AssertionError(msg)

        self.form_fields_test_with_callback(callback)

    def test_invalid_email_error_message(self) -> None:
        def callback(form: WebElement) -> None:
            email_field = self.get_web_element_by_placeholder(
                form,
                "Your e-mail.",
            )
            email_field.send_keys("email@invalid")
            email_field.send_keys(Keys.ENTER)

            # Here we must reselect the form as after we pressed enter all the elements
            # in the page are new.
            form = self.get_form()

            error_message = "E-mail must be valid. Ex: pauloguina@email.com"

            if error_message not in form.text:
                msg = f"'{error_message}' not found in form '{form.text}'"
                raise AssertionError(msg)

        self.form_fields_test_with_callback(callback)

    def test_passwords_do_not_match(self) -> None:
        def callback(form: WebElement) -> None:
            password1 = self.get_web_element_by_placeholder(
                form,
                "Your password.",
            )
            password1.send_keys("Abc123456")

            password2 = self.get_web_element_by_placeholder(
                form,
                "Repeat your password.",
            )
            password2.send_keys("Abc1234567")

            password2.send_keys(Keys.ENTER)

            # Here we must reselect the form as after we pressed enter all the elements
            # in the page are new.
            form = self.get_form()

            error_message = "Password and password 2 must match."

            if error_message not in form.text:
                msg = f"'{error_message}' not found in form '{form.text}'"
                raise AssertionError(msg)

        self.form_fields_test_with_callback(callback)

    def test_user_registered_successfully_with_valid_data(self) -> None:
        self.browser.get(self.live_server_url + "/authors/register/")

        form = self.get_form()

        self.get_web_element_by_placeholder(form, "Your username.").send_keys(
            "pauloguina",
        )
        self.get_web_element_by_placeholder(form, "Ex.: Paulo.").send_keys("Paulo")
        self.get_web_element_by_placeholder(form, "Ex.: Guina.").send_keys("Guina")
        self.get_web_element_by_placeholder(form, "Your e-mail.").send_keys(
            "pauloguina@email.com",
        )
        self.get_web_element_by_placeholder(form, "Your password.").send_keys(
            "Oco!@123",
        )
        self.get_web_element_by_placeholder(form, "Repeat your password.").send_keys(
            "Oco!@123",
        )

        form.submit()

        body_text = self.browser.find_element(By.TAG_NAME, "body").text

        success_message = "Your user was created successfully, please log in."

        if success_message not in body_text:
            msg = f"'{success_message}' not found in body text: {body_text}"
            raise AssertionError(msg)
