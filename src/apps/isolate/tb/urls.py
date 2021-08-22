from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import (
    ProfileViewSet,
    PsummaryViewSet
)

app_name = "tb"
router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'summary', PsummaryViewSet, basename='summary')
urlpatterns = [
    path('', include(router.urls)),
] 