from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from authors import views

app_name = "authors"

# More specific above, more variable bellow.
urlpatterns = [
    path("register/", views.register_view, name="register"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
