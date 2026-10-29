from typing import TYPE_CHECKING

from django.db.models import Q
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


def recipe_detail(request: HttpRequest, recipe_id: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe, pk=recipe_id, is_published=True)
    context = {
        "recipe": recipe,
        "is_detail_page": True,
    }
    return render(request, "recipes/pages/recipe_detail.html", context)


def search(request: HttpRequest) -> HttpResponse:
    template_name = "recipes/pages/search.html"
    search_term = request.GET.get("q", "").strip()

    if not search_term:
        msg = f"Term {search_term} not found in template {template_name} url"
        raise Http404(msg)

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | Q(description__icontains=search_term),
        ),
        is_published=True,
    ).order_by("-id")

    context = {
        "title": f"Search for {search_term}",
        "search_term": search_term,
        "recipes": recipes,
    }

    return render(request=request, template_name=template_name, context=context)
