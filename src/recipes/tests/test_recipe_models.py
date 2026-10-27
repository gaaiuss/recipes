import pytest
from django.core.exceptions import ValidationError

from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_with_more_than_65_chars_raises_exception(self) -> None:
        self.recipe.title = "A" * 70
        with pytest.raises(ValidationError):
            self.recipe.full_clean()
