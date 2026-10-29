from django.urls import resolve, reverse

from recipes import views
from tests.test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_is_ok(self) -> None:
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1000}))

        if view.func is not views.category:
            msg = f"{view.func} is not {views.category}"
            raise AssertionError(msg)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self) -> None:
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000}),
        )
        code = 404

        if response.status_code != code:
            msg = f"Status code not 404, got {response.status_code}"
            raise AssertionError(msg)

    def test_recipe_category_template_loads_recipes(self) -> None:
        recipe = self.make_recipe(title="Category test")
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1}),
        )
        content = response.content.decode("utf-8")

        if recipe.title not in content:
            msg = f"{recipe.title} not found in response content"
            raise AssertionError(msg)

    def test_recipe_category_template_do_not_loads_recipes_not_published(self) -> None:
        recipe = self.make_recipe(is_published=False)
        category_id = recipe.category.id  # type: ignore
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": category_id}),
        )
        code = 404

        if response.status_code != code:
            msg = f"Status code not 404, got {response.status_code}"
            raise AssertionError(msg)
