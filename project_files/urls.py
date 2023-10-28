# Django
from rest_framework.routers import SimpleRouter
from django.contrib import admin
from django.urls import include, path

# Project
from tic_tac_toe_api.views import GameViewSet


router = SimpleRouter()

router.register(r"games", GameViewSet, basename="games")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
