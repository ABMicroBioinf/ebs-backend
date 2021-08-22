from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import (
    AssemblyViewSet,
    MlstViewSet,
    ResistomeViewSet,
    VirulomeViewSet,
    AnnotationViewSet
)

app_name = "basic"
router = DefaultRouter()
router.register(r'assembly', AssemblyViewSet, basename='assembly')
router.register(r'mlst', MlstViewSet, basename='mlst')
router.register(r'resistome', ResistomeViewSet, basename='resistome')
router.register(r'virulome', VirulomeViewSet, basename='virulome')
router.register(r'annot', AnnotationViewSet, basename='annot')
urlpatterns = [
    path('', include(router.urls)),
] 