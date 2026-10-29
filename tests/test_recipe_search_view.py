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
        url_path = reverse("recipes:search") + "?q=test"
        response = self.client.get(url_path)
        desired_template = "recipes/pages/search.html"

        if desired_template not in [t.name for t in response.templates]:
            msg = f"Template '{desired_template}' not found in 'response.templates'"
            raise AssertionError(msg)

    def test_recipe_search_raises_404_if_no_search_term(self) -> None:
        url_path = reverse("recipes:search")
        response = self.client.get(url_path)
        code = 404

        if response.status_code != code:
            msg = (
                f"Recipe search did not returned {code} when no search term "
                f"was sent, got {response.status_code}"
            )
            raise AssertionError(msg)
