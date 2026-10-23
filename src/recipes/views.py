from typing import TYPE_CHECKING

from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe

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
    recipes = get_list_or_404(Recipe, category__id=category_id, is_published=True)

    recipe = recipes[0]

    if recipe.category is not None:
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
    recipe = get_object_or_404(Recipe, pk=recipe_id, is_published=True)
    context = {
        "recipe": recipe,
        "is_detail_page": True,
    }
    return render(request, "recipes/pages/recipe_detail.html", context)
