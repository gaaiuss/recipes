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

    def test_recipe_search_term_is_on_page_title_and_escaped(self) -> None:
        url_path = reverse("recipes:search") + '?q="<Test>"'
        response = self.client.get(url_path)
        content = response.content.decode("utf-8")
        expected_escaped_title = "Search for &quot;&lt;Test&gt;&quot;"

        if expected_escaped_title not in content:
            msg = f"{expected_escaped_title} not found in content"
            raise AssertionError(msg)

    def test_recipe_search_can_find_recipe_by_title(self) -> None:
        title1 = "This is recipe 1"
        title2 = "This is recipe 2"

        author1 = self.make_author("one")
        author2 = self.make_author("two")

        recipe1 = self.make_recipe(
            slug="one",
            title=title1,
            author=author1,
        )

        recipe2 = self.make_recipe(
            slug="two",
            title=title2,
            author=author2,
        )

        search_url = reverse("recipes:search")

        path1 = search_url + f"?q={title1}"
        response1 = self.client.get(path1)

        path2 = search_url + f"?q={title2}"
        response2 = self.client.get(path2)

        path_both = search_url + "?q=this"
        response_both = self.client.get(path_both)

        # ------------------------- test response 1 --------------------------

        if recipe1 not in response1.context["recipes"]:
            msg = f"'{recipe1}' not found in '{response1.context['recipes']}'"
            raise AssertionError(msg)

        if recipe2 in response1.context["recipes"]:
            msg = f"'{recipe2}' found '{response1.context['recipes']}'"
            raise AssertionError(msg)

        # ------------------------- test response 2 --------------------------

        if recipe2 not in response2.context["recipes"]:
            msg = f"'{recipe2}' not found in '{response2.context['recipes']}'"
            raise AssertionError(msg)

        if recipe1 in response2.context["recipes"]:
            msg = f"'{recipe1}' found '{response2.context['recipes']}'"
            raise AssertionError(msg)

        # ----------------------- test both responses ------------------------

        if recipe1 not in response_both.context["recipes"]:
            msg = f"'{recipe1}' not found in '{response_both.context['recipes']}'"
            raise AssertionError(msg)

        if recipe2 not in response_both.context["recipes"]:
            msg = f"'{recipe2}' not found '{response_both.context['recipes']}'"
            raise AssertionError(msg)
