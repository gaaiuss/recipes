from django.urls import resolve, reverse

from recipes import views
from tests.test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self) -> None:
        search_url = reverse("recipes:search")
        resolved = resolve(search_url)

        if resolved.func is not views.search:
            msg = f"{resolved.func} is not {views.search}"
            raise AssertionError(msg)

    def test_recipe_search_loads_correct_template(self) -> None:
        url_path = reverse("recipes:search")
        response = self.client.get(url_path)
        desired_template = "recipes/pages/search.html"

        if response.templates[0].name != desired_template:
            msg = f"{response.templates[0].name} is not {desired_template}"
            raise AssertionError(msg)
