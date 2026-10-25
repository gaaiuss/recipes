from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views


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
