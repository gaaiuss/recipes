from django.urls import resolve, reverse

from recipes import views
from tests.test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_is_ok(self) -> None:
        view = resolve(reverse("recipes:recipe", kwargs={"recipe_id": 1}))

        if view.func is not views.recipe_detail:
            msg = f"{view.func} is not {views.recipe_detail}"
            raise AssertionError(msg)

    def test_detail_view_returns_404_if_no_recipes_found(self) -> None:
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"recipe_id": 1000}),
        )
        code = 404

        if response.status_code != code:
            msg = f"Status code not 404, got {response.status_code}"
            raise AssertionError(msg)

    def test_recipe_detail_template_loads_the_correct_recipe(self) -> None:
        title = "Recipe detail page - It loads one recipe"
        recipe = self.make_recipe(title=title)
        response = self.client.get(reverse("recipes:recipe", kwargs={"recipe_id": 1}))
        content = response.content.decode("utf-8")

        if recipe.title not in content:
            msg = f"{recipe.title} not found in response content"
            raise AssertionError(msg)

    def test_recipe_detail_template_do_not_loads_recipes_not_published(self) -> None:
        recipe = self.make_recipe(is_published=False)
        recipe_id = recipe.id  # type: ignore
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"recipe_id": recipe_id}),
        )
        code = 404

        if response.status_code != code:
            msg = f"Status code not 404, got {response.status_code}"
            raise AssertionError(msg)
