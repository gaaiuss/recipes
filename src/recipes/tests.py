from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views


class RecipeURLsTest(TestCase):
    def test_recipe_index_url_is_ok(self) -> None:
        index_url = reverse("recipes:home")

        if index_url != "/":
            msg = f"{index_url} is not '/'"
            raise AssertionError(msg)

    def test_recipe_category_url_is_ok(self) -> None:
        index_url = reverse("recipes:category", kwargs={"category_id": 1})

        if index_url != "/recipes/category/1/":
            msg = f"{index_url} is not '/recipes/category/1/'"
            raise AssertionError(msg)

    def test_recipe_detail_url_is_ok(self) -> None:
        index_url = reverse("recipes:recipe", kwargs={"recipe_id": 1})

        if index_url != "/recipes/recipe/1/":
            msg = f"{index_url} is not '/recipes/recipe/1/'"
            raise AssertionError(msg)


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_is_ok(self) -> None:
        view = resolve(reverse("recipes:home"))

        if view.func is not views.home:
            msg = f"{view.func} is not {views.home}"
            raise AssertionError(msg)

    def test_recipe_category_view_is_ok(self) -> None:
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))

        if view.func is not views.category:
            msg = f"{view.func} is not {views.category}"
            raise AssertionError(msg)

    def test_recipe_recipe_detail_view_is_ok(self) -> None:
        view = resolve(reverse("recipes:recipe", kwargs={"recipe_id": 1}))

        if view.func is not views.recipe_detail:
            msg = f"{view.func} is not {views.recipe_detail}"
            raise AssertionError(msg)
