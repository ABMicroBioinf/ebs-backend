from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import (
    ProfileViewSet
)

app_name = "tb"
router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
urlpatterns = [
    path('', include(router.urls)),
] 