from unittest.mock import patch

import pytest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch("recipes.views.PER_PAGE", new=4)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)

        desired = "No recipes here..."
        body = self.browser.find_element(By.TAG_NAME, "body")

        if desired not in body.text:
            msg = f"'{desired}' message not found in body text"
            raise AssertionError(msg)

    @patch("recipes.views.PER_PAGE", new=4)
    def test_recipe_search_input_finds_correct_recipe(self):
        recipes = self.make_recipe_in_batch(20)

        desired_title = "Desired Title"

        recipes[0].title = desired_title
        recipes[0].save()

        # User opens the page
        self.browser.get(self.live_server_url)

        # Sees a input field "Search for a recipe..."
        search_input = self.browser.find_element(
            By.XPATH,
            "//input[@placeholder='Search for a recipe...']",
        )

        # Clicks the input and types the search term to find the respective recipe.
        search_input.send_keys(desired_title)
        search_input.send_keys(Keys.ENTER)

        body_text = self.browser.find_element(By.TAG_NAME, "body").text

        if desired_title not in body_text:
            msg = f"'{desired_title}' not found in body text: {body_text}"
            raise AssertionError(msg)
