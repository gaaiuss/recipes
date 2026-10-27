from django.contrib.auth.models import User
from django.test import TestCase

from recipes.models import Category, Recipe


class RecipeTestBase(TestCase):
    def make_category(self, name: str = "Category") -> Category:
        return Category.objects.create(name=name)

    def make_author(
        self,
        username: str = "user",
        email: str = "user@email.com",
        password: str = "123456",
        first_name: str = "user",
        last_name: str = "last name",
    ) -> User:
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

    def make_recipe(
        self,
        title: str = "Recipe title",
        description: str = "Recipe description",
        slug: str = "recipe-slug",
        preparation_time: int = 10,
        preparation_time_unit: str = "minutes",
        servings: int = 10,
        servings_unit: str = "portions",
        preparation_steps: str = "Recipe preparation steps",
        preparation_steps_is_html: bool = False,
        is_published: bool = True,
        category: Category | None = None,
        author: User | None = None,
    ) -> Recipe:
        if category is None:
            category = self.make_category()

        if author is None:
            author = self.make_author()

        return Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            category=category,
            author=author,
        )
