from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views
from tests.test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_home_view_is_ok(self) -> None:
        view = resolve(reverse("recipes:home"))

        if view.func is not views.home:
            msg = f"{view.func} is not {views.home}"
            raise AssertionError(msg)

    def test_home_view_returns_status_code_200_ok(self) -> None:
        response = self.client.get(reverse("recipes:home"))
        code = 200

        if response.status_code != code:
            msg = f"Status code not 200, got {response.status_code}"
            raise AssertionError(msg)

    def test_home_view_loads_correct_template(self) -> None:
        response = self.client.get(reverse("recipes:home"))
        desired_template = "recipes/pages/index.html"

        if desired_template not in [t.name for t in response.templates]:
            msg = f"'{desired_template}' not found in 'response.templates'"
            raise AssertionError(msg)

    def test_recipe_home_template_shows_no_recipes_if_no_recipes_were_found(
        self,
    ) -> None:
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")

        if "<h1>No recipes here...</h1>" not in content:
            msg = "text '<h1>No recipes here...</h1>' not found int index.html"
            raise AssertionError(msg)

    def test_recipe_home_template_loads_recipes(self) -> None:
        recipe = self.make_recipe()  # needs a recipe for this test
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")

        # checks if a recipe exists
        if recipe.title not in content:
            msg = f"{recipe.title} not found in response content"
            raise AssertionError(msg)

    def test_recipe_home_template_do_not_loads_recipes_not_published(self) -> None:
        self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode("utf-8")
        no_recipe_content = "<h1>No recipes here...</h1>"

        if no_recipe_content not in content:
            msg = f"{no_recipe_content} not found int index.html"
            raise AssertionError(msg)

    def test_recipe_home_is_paginated(self) -> None:
        total_of_recipes = 9

        for i in range(total_of_recipes):
            author = self.make_author(username=f"u{i}")
            slug = f"s{i}"
            self.make_recipe(author=author, slug=slug)

        with patch("recipes.views.PER_PAGE", new=3):
            response = self.client.get(reverse("recipes:home"))
            recipes = response.context["recipes"]
            paginator = recipes.paginator

            number_of_elements_per_page = 3

            if paginator.num_pages != number_of_elements_per_page:
                msg = (
                    f"The number of pages '{paginator.num_pages}' is not "
                    f"equal to the intended value of '{number_of_elements_per_page}'."
                )
                raise AssertionError(msg)

            number_of_elements = len(paginator.get_page(1))

            if number_of_elements != number_of_elements_per_page:
                msg = (
                    f"The number of elements in page '{number_of_elements}' is not "
                    f"equal to the intended value of '{number_of_elements_per_page}'."
                )
                raise AssertionError(msg)

            number_of_elements = len(paginator.get_page(2))

            if number_of_elements != number_of_elements_per_page:
                msg = (
                    f"The number of elements in page '{number_of_elements}' is not "
                    f"equal to the intended value of '{number_of_elements_per_page}'."
                )
                raise AssertionError(msg)

            number_of_elements = len(paginator.get_page(3))

            if number_of_elements != number_of_elements_per_page:
                msg = (
                    f"The number of elements in page '{number_of_elements}' is not "
                    f"equal to the intended value of '{number_of_elements_per_page}'."
                )
                raise AssertionError(msg)
