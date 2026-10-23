from typing import TYPE_CHECKING

from django.http import Http404
from django.shortcuts import render

from recipes.models import Recipe
from utils import recipe_factory

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")
    context = {
        "recipes": recipes,
        "title": "Home",
        # "recipes": [recipe_factory.make_recipe() for _ in range(12)],
    }
    return render(request, "recipes/pages/index.html", context)


def category(request: HttpRequest, category_id: int) -> HttpResponse:
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
    ).order_by("-id")

    recipe = recipes.first()

    if recipe is not None and recipe.category is not None:
        category_name = f"{recipe.category.name} - Category"
    else:
        msg = "Category does not exists"
        raise Http404(msg)

    context = {
        "recipes": recipes,
        "title": category_name,
    }

    return render(request, "recipes/pages/category.html", context)


def recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    context = {
        "recipe": recipe_factory.make_recipe(),
        "is_detail_page": True,
    }
    return render(request, "recipes/pages/recipe_detail.html", context)
