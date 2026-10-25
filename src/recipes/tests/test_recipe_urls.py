from django.test import TestCase
from django.urls import reverse


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
