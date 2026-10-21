import os
import sys
from pathlib import Path
from random import choice

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 12

sys.path.append(str(DJANGO_BASE_DIR))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
settings.USE_TZ = False

django.setup()

if __name__ == "__main__":
    import faker

    from recipes.models import Category, Recipe

    Recipe.objects.all().delete()
    Category.objects.all().delete()

    fake = faker.Faker("en")
    categories = [
        "Meat",
        "Vegan",
        "Breakfast",
    ]

    django_categories = [Category(name=name) for name in categories]

    for category in django_categories:
        category.save()

    django_recipes: list[Recipe] = []

    for _ in range(NUMBER_OF_OBJECTS):
        title = fake.catch_phrase()
        description = fake.text(max_nb_chars=50)
        slug = fake.text(max_nb_chars=100)
        preparation_time = fake.random_number(2)
        preparation_time_unit = fake.text(max_nb_chars=10)
        servings = fake.random_number(2)
        servings_unit = fake.text(max_nb_chars=10)
        preparation_steps = fake.text(max_nb_chars=2000)
        preparation_steps_is_html = fake.boolean()
        is_published = True
        cover = fake.image_url()
        category = choice(django_categories)  # noqa: S311

        django_recipes.append(
            Recipe(
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
            ),
        )

    if len(django_recipes) > 0:
        Recipe.objects.bulk_create(django_recipes)
