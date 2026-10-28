import pytest
from django.core.exceptions import ValidationError
from parameterized import parameterized

from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

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
