from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import (
    AssemblyViewSet,
    StatsViewSet,
    MlstViewSet,
    ResistomeViewSet,
    VirulomeViewSet,
    TbProfileViewSet,
    TbProfileSummaryViewSet,
    PlasmidViewSet,
)

app_name = "isolate"
router = DefaultRouter()
router.register(r'assembly', AssemblyViewSet, basename='assembly')
router.register(r'stats', StatsViewSet, basename='stats')
router.register(r'mlst', MlstViewSet, basename='mlst')
router.register(r'resistome', ResistomeViewSet, basename='resistome')
router.register(r'virulome', VirulomeViewSet, basename='virulome')
router.register(r'plasmid', PlasmidViewSet, basename='plasmid')
router.register(r'tbprofile', TbProfileViewSet, basename='tbprofile')
router.register(r'tbprofilesummary', TbProfileSummaryViewSet, basename='tbprofilesummary')
urlpatterns = [
    path('', include(router.urls)),
] 