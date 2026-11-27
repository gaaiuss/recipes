from typing import TYPE_CHECKING

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement


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

        form.find_element(By.NAME, "email").send_keys("dummy@email.com")

    def test_empty_first_name_error_message(self) -> None:
        self.browser.get(self.live_server_url + "/authors/register/")

        form = self.browser.find_element(
            By.XPATH,
            "/html/body/main/div[2]/form",
        )

        self.fill_form_dummy_data(form)

        first_name_field = self.get_web_element_by_placeholder(form, "Ex.: Paulo.")
        first_name_field.send_keys(" ")
        first_name_field.send_keys(Keys.ENTER)

        # Here we must reselect the form as after we pressed enter all the elements
        # in the page are new.
        form = self.browser.find_element(
            By.XPATH,
            "/html/body/main/div[2]/form",
        )

        desired_text = "Write your first name."

        if desired_text not in form.text:
            msg = f"'{desired_text}' not found in form '{form.text}'"
            raise AssertionError(msg)
