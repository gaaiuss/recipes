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

        if response.templates[0].name != "recipes/pages/index.html":
            msg = f"{response.templates[0].name} is not 'recipes/pages/index.html'"
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
