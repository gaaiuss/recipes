from typing import TYPE_CHECKING

from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def register_view(request: HttpRequest) -> HttpResponse:
    template_name = "authors/pages/register.html"
    return render(request=request, template_name=template_name)
