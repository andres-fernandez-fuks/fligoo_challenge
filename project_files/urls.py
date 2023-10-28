# Django
from rest_framework.routers import SimpleRouter
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# Project
from tic_tac_toe_api.views import GameViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = SimpleRouter()

router.register(r"games", GameViewSet, basename="games")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),  # To download the swagger.json
]
