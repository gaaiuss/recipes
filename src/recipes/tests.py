from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_index_is_ok(self) -> None:
        index_url = reverse("recipes:home")
        if index_url != "/":
            raise ValueError
