from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from authors import views

app_name = "authors"

# More specific above, more variable bellow.
urlpatterns = [
    path("register/", views.register, name="register"),
    path(
        "register/create/",  # create will not be directly accessed.
        views.register_create,
        name="register_create",
    ),
    path("login/", views.login, name="login"),
    path(
        "login/create/",  # create will not be directly accessed.
        views.login_create,
        name="login_create",
    ),
    path("logout/", views.logout, name="logout"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
