import os
from typing import TYPE_CHECKING

from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from dotenv import load_dotenv

from recipes.models import Recipe
from utils.pagination import make_pagination

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

load_dotenv()

PER_PAGE = int(os.environ.get("PER_PAGE", "6"))


def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")

    page_object, pagination_range = make_pagination(
        request=request,
        queryset=recipes,
        per_page=PER_PAGE,
    )

    messages.success(request, "Home view loaded successful.")

    context = {
        "recipes": page_object,
        "pagination_range": pagination_range,
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

    page_object, pagination_range = make_pagination(
        request=request,
        queryset=recipes,
        per_page=PER_PAGE,
    )

    context = {
        "recipes": page_object,
        "pagination_range": pagination_range,
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

    page_object, pagination_range = make_pagination(
        request=request,
        queryset=recipes,
        per_page=PER_PAGE,
    )

    context = {
        "title": f"Search for {search_term}",
        "search_term": search_term,
        "recipes": page_object,
        "pagination_range": pagination_range,
        "additional_url_query": f"&q={search_term}",
    }

    return render(request=request, template_name=template_name, context=context)
