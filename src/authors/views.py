from typing import TYPE_CHECKING

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render

from authors.forms import RegisterForm

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def register(request: HttpRequest) -> HttpResponse:
    """
    This is the view responsible to render the form.
    """
    template_name = "authors/pages/register.html"
    register_form_data = request.session.get("register_form_data")
    form = RegisterForm(register_form_data)

    return render(
        request=request,
        template_name=template_name,
        context={
            "form": form,
        },
    )


def create(request: HttpRequest) -> HttpResponseRedirect:
    """
    This view is responsible to redirect back to the form if the page is reloaded.
    """
    if not request.POST:
        raise Http404

    request.session["register_form_data"] = request.POST
    # form = RegisterForm(request.POST)

    return redirect("authors:register")
