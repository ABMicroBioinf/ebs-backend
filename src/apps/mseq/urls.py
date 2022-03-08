from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    SequenceViewSet,
    BioSampleViewSet,
    ProjectViewSet,
    SeqFileViewSet,
    MetadataFileViewSet,
    MyFileUploadViewSet,
    SequenceMetadataViewSet,
    SeqstatViewSet
)
app_name = "mseq"
router = DefaultRouter()
router.register(r'sequence', SequenceViewSet, basename='sequence')
router.register(r'biosample', BioSampleViewSet, basename='biosample')
router.register(r'project', ProjectViewSet, basename='project')
router.register(r'seqstat', SeqstatViewSet, basename='seqstat')
router.register(r'seqfile', SeqFileViewSet, basename='seqfile')
router.register(r'metadatafile', MetadataFileViewSet, basename='metadatafile')
router.register(r'myfiles', MyFileUploadViewSet, basename='files')
router.register(r'sequence_metadata', SequenceMetadataViewSet, basename='sequence_metadata')

urlpatterns = [
    path('', include(router.urls)),
] 




