import pytest
from django.core.exceptions import ValidationError
from parameterized import parameterized

from tests.test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self) -> Recipe:
        recipe = Recipe(
            title="Recipe title",
            description="Recipe description",
            slug="recipe-slug",
            preparation_time=10,
            preparation_time_unit="minutes",
            servings=10,
            servings_unit="portions",
            preparation_steps="Recipe preparation steps",
            category=self.make_category(name="Meat"),
            author=self.make_author(username="gaaiuss"),
        )
        recipe.full_clean()
        recipe.save()

        return recipe

    @parameterized.expand(
        [
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
        ],
    )
    def test_recipe_fields_max_length(self, field: str, max_length: int) -> None:
        setattr(self.recipe, field, "A" * (max_length + 1))

        with pytest.raises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self) -> None:
        recipe = self.make_recipe_no_defaults()

        if recipe.preparation_steps_is_html is not False:
            msg = "Recipe 'preparation_steps_is_html' is not False"
            raise AssertionError(msg)

    def test_recipe_is_published_is_false_by_default(self) -> None:
        recipe = self.make_recipe_no_defaults()

        if recipe.is_published is not False:
            msg = "Recipe 'is_published' is not False"
            raise AssertionError(msg)
