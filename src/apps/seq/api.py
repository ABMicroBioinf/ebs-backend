from gizmos.pagination import CustomPagination

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters

from .filters import SequenceFilter

from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.seq.models import MetadataFile, SeqFile, Sequence, SeqStat

from .serializers import (
    MetadataFileSerializer,
    MyFileSerializer,
    SeqFileSerializer,
    SequenceMetadataSerializer,
    SequenceSerializer,
)

class SequenceViewSet(
    GenericViewSet,  # generic view functionality
    CreateModelMixin,  # handles POSTs
    RetrieveModelMixin,  # handles GETs for 1 Company
    UpdateModelMixin,  # handles PUTs and PATCHes
    ListModelMixin,  # handles GETs for many Companies
    DestroyModelMixin,
):  # handle delete
    
    #queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer
    filterset_class = SequenceFilter
    pagination_class = CustomPagination
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )
    # search_fields = "__all__"
    # ordering_fields = "__all__" 
    search_fields = [
        "DateCreated",
        "Experiment",
        "LastUpdate",
        "LibraryLayout",
        "LibrarySelection",
        "LibrarySource",
        "LibraryStrategy",
        "Platform", 
        "Projectid",
        "ScientificName",
        "SequencerModel",
        "TaxID",
        "id",
        "seqtype",
        "taxName_1", 
        "taxName_2", 
        "taxName_3", 
        "taxName_4",
        "owner__username",
        
        ] 

    ordering_fields = [
        "DateCreated",
        "Experiment",
        "LastUpdate",
        "LibraryLayout",
        "LibrarySelection",
        "LibrarySource",
        "LibraryStrategy",
        "Platform", 
        "Projectid",
        "ScientificName",
        "SequencerModel",
        "TaxID",
        "id",
        "seqtype",
        "taxName_1", 
        "taxName_2", 
        "taxName_3", 
        "taxName_4",
        "owner__username",
       
        ] 
 
 
    def get_queryset(self):
        return Sequence.objects.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SeqFileViewSet(
    GenericViewSet,  # generic view functionality
    CreateModelMixin,  # handles POSTs
    RetrieveModelMixin,  # handles GETs for 1 Company
    UpdateModelMixin,  # handles PUTs and PATCHes
    ListModelMixin,  # handles GETs for many Companies
    DestroyModelMixin,
):  # handle delete
    serializer_class = SeqFileSerializer
    queryset = SeqFile.objects.all()


class MetadataFileViewSet(
    GenericViewSet,  # generic view functionality
    CreateModelMixin,  # handles POSTs
    RetrieveModelMixin,  # handles GETs for 1 Company
    UpdateModelMixin,  # handles PUTs and PATCHes
    ListModelMixin,  # handles GETs for many Companies
    DestroyModelMixin,
):  # handle delete

    serializer_class = MetadataFileSerializer
    queryset = MetadataFile.objects.all()


class MyFileUploadViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer_class = MyFileSerializer(data=request.data)
        if "file" not in request.FILES or not serializer_class.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # Single File
            # handle_uploaded_file(request.FILES['file'])

            # Multiple Files
            files = request.FILES.getlist("file")
            for f in files:
                handle_uploaded_file(f)

            return Response(status=status.HTTP_201_CREATED)


def handle_uploaded_file(f):
    with open(f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# jongil
class SequenceMetadataViewSet(viewsets.ModelViewSet):
    serializer_class = SequenceMetadataSerializer
    @action(detail=False)
    def count(self, request):
        seq = Sequence.objects.all()
        serializer = SequenceMetadataSerializer(seq)
        return Response(serializer.data, status=status.HTTP_200_OK)