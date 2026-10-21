# from inspect import signature
from random import randint
from typing import TYPE_CHECKING

from faker import Faker

if TYPE_CHECKING:
    from datetime import datetime


def rand_ratio() -> tuple[int, int]:
    return randint(840, 900), randint(473, 573)  # noqa: S311


fake = Faker()


def make_recipe() -> dict[str, str | int | datetime | dict[str, str]]:
    return {
        "id": fake.random_number(digits=2, fix_len=True),
        "title": fake.sentence(nb_words=6),
        "description": fake.sentence(nb_words=12),
        "preparation_time": fake.random_number(digits=2, fix_len=True),
        "preparation_time_unit": "Minutes",
        "servings": fake.random_number(digits=2, fix_len=True),
        "servings_unit": "Portions",
        "preparation_steps": fake.text(3000),
        "created_at": fake.date_time(),
        "author": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        },
        "category": {
            "name": fake.word(),
        },
        "cover": {
            "url": "https://picsum.photos//{}/{}/".format(*rand_ratio()),
        },
    }


if __name__ == "__main__":
    from rich import print

    print(make_recipe())
