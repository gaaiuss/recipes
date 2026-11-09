from typing import TYPE_CHECKING

from django.shortcuts import render

from authors.forms import RegisterForm

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def register_view(request: HttpRequest) -> HttpResponse:
    template_name = "authors/pages/register.html"
    form = RegisterForm(request.POST) if request.POST else RegisterForm()

    return render(
        request=request,
        template_name=template_name,
        context={
            "form": form,
        },
    )
