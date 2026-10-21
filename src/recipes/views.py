from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "recipes/pages/index.html")


def recipe(request: HttpRequest, recipe_id: int) -> HttpResponse:
    return render(request, "recipes/pages/recipe_detail.html")
