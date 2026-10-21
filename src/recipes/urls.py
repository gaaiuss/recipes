from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from recipes import views

app_name = "recipes"

urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/<int:recipe_id>/", views.recipe, name="recipe"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
