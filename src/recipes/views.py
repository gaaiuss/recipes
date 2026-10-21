from typing import TYPE_CHECKING

from django.shortcuts import render

from utils import recipe_factory

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    context = {
        "recipes": [recipe_factory.make_recipe() for _ in range(10)],
    }
    return render(request, "recipes/pages/index.html", context)


def recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    context = {
        "recipe": recipe_factory.make_recipe(),
    }
    return render(request, "recipes/pages/recipe_detail.html", context)
