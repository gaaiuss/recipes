import pytest
from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)

        desired = "No recipes here..."
        body = self.browser.find_element(By.TAG_NAME, "body")

        if desired not in body.text:
            msg = f"'{desired}' message not found in body text"
            raise AssertionError(msg)
