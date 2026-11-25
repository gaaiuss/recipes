from typing import TYPE_CHECKING

from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import RegisterForm

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def register(request: HttpRequest) -> HttpResponse:
    """
    This is the view responsible to render the form.
    """
    template_path = "authors/pages/register.html"
    register_form_data = request.session.get("register_form_data")
    form = RegisterForm(register_form_data)

    return render(
        request=request,
        template_name=template_path,
        context={
            "form": form,
            "form_action": reverse("authors:register_create"),
        },
    )


def register_create(request: HttpRequest) -> HttpResponseRedirect:
    """
    This view is responsible to redirect back to the form if the page is reloaded.
    """
    if not request.POST:
        raise Http404

    request.session["register_form_data"] = request.POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        # Before we save the form we must criptograph the user password.
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        msg = "Your user was created successfully, please log in."
        messages.success(request=request, message=msg)

        del request.session["register_form_data"]

        # You can edit data after validating your form as shown bellow.
        # data = form.save(commit=False)
        # data.another_field = "another value"

    return redirect("authors:register")


def login(request: HttpRequest) -> HttpResponse:
    template_path = "authors/pages/login.html"

    return render(request, template_path)


def login_create(request: HttpRequest) -> HttpResponse:
    template_path = "authors/pages/login.html"

    return render(request, template_path)
