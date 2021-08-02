from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import (
    GenomeViewSet,
    AnnotationViewSet
)

app_name = "basic"
router = DefaultRouter()
router.register(r'genome', GenomeViewSet, basename='genome')
router.register(r'annot', AnnotationViewSet, basename='annot')
urlpatterns = [
    path('', include(router.urls)),
] 