from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_index_url_is_ok(self) -> None:
        index_url = reverse("recipes:home")
        desired_url = "/"

        if index_url != desired_url:
            msg = f"{index_url} is not {desired_url}"
            raise AssertionError(msg)

    def test_recipe_category_url_is_ok(self) -> None:
        category_url = reverse("recipes:category", kwargs={"category_id": 1})
        desired_url = "/recipes/category/1/"

        if category_url != desired_url:
            msg = f"{category_url} is not {desired_url}"
            raise AssertionError(msg)

    def test_recipe_detail_url_is_ok(self) -> None:
        recipe_detail_url = reverse("recipes:recipe", kwargs={"recipe_id": 1})
        desired_url = "/recipes/recipe/1/"

        if recipe_detail_url != desired_url:
            msg = f"{recipe_detail_url} is not {desired_url}"
            raise AssertionError(msg)

    def test_recipe_search_url_is_ok(self) -> None:
        search_url = reverse("recipes:search")
        desired_url = "/recipes/search/"

        if search_url != desired_url:
            msg = f"{search_url} is not {desired_url}"
            raise AssertionError(msg)
