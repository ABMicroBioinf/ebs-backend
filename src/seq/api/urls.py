from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudyViewSet, RunViewSet, SeqFileViewSet, MetadataFileViewSet
app_name = "seq"
router = DefaultRouter()
router.register(r'study', StudyViewSet, basename='study')
router.register(r'run', RunViewSet, basename='run')
router.register(r'seqfile', SeqFileViewSet, basename='seqfile')
router.register(r'metadatafile', MetadataFileViewSet, basename='metadatafile')

urlpatterns = [
    path('', include(router.urls)),
] 