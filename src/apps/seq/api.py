from gizmos.pagination import CustomPagination

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .filters import SequenceFilter, CustomSearchFilter

from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.seq.models import MetadataFile, SeqFile, Sequence, Project

from .serializers import (
    MetadataFileSerializer,
    MyFileSerializer,
    SeqFileSerializer,
    SequenceMetadataSerializer,
    SequenceSerializer,
    ProjectSerializer
)

class ProjectViewSet(
    GenericViewSet,  # generic view functionality
    CreateModelMixin,  # handles POSTs
    RetrieveModelMixin,  # handles GETs for 1 Company
    UpdateModelMixin,  # handles PUTs and PATCHes
    ListModelMixin,  # handles GETs for many Companies
    DestroyModelMixin,
):  # handle delete
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend
        
    )
    #equality-based filtering
    filterset_fields = [
        'id',
        'title',
        'owner__username',
        'description'
    ]

    #generic filtering only for text, char field
    search_fields = [
        'id',
        'title',
        'owner__username',
        'description'
    ]
    ordering_fields =  [
        'id',
        'title',
        'owner__username',
        'DateCreated',
        'LastUpdate',
    ]
    ordering = ['DateCreated']

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SequenceViewSet(
    GenericViewSet,  # generic view functionality
    CreateModelMixin,  # handles POSTs
    RetrieveModelMixin,  # handles GETs for 1 Company
    UpdateModelMixin,  # handles PUTs and PATCHes
    ListModelMixin,  # handles GETs for many Companies
    DestroyModelMixin,
):  # handle delete
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer

    #this define nested field
    filterset_class = SequenceFilter
    pagination_class = CustomPagination
    filter_backends = (
        # SearchFilter,
        CustomSearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    )
    filterset_fields = [f.name for f in Sequence._meta.get_fields()]
    #equality-based filtering
    filterset_fields = [
        "seqtype",
        "id",
        "owner__username",
        "TaxID",
        "ScientificName",
        "Experiment",
        "LibraryName",
        "LibraryStrategy",
        "LibrarySelection",
        "LibrarySource",
        "LibraryLayout",
        "Platform",
        "SequencerModel",
        "project__id",
        "project__title",
        "SampleName",
        "CenterName",
        "DateCreated",
        "LastUpdate",
        "Description",
        "taxName_1",
        "taxFrac_1",
        "taxName_2",
        "taxFrac_2",
        "taxName_3",
        "taxFrac_3",
        "taxName_4",
        "taxFrac_4",
        "RawStats__Reads",
        "RawStats__Yield",
        "RawStats__GeeCee",
        "RawStats__MinLen",
        "RawStats__AvgLen",
        "RawStats__MaxLen",
        "RawStats__AvgQual",
        "RawStats__ErrQual",
        "RawStats__Ambiguous",
        "QcStats__Reads",
        "QcStats__Yield",
        "QcStats__GeeCee",
        "QcStats__MinLen",
        "QcStats__AvgLen",
        "QcStats__MaxLen",
        "QcStats__AvgQual",
        "QcStats__ErrQual",
        "QcStats__Ambiguous",
    ]

    #searchFilter will only be applied if the view has search_fields
    #search fields should be a list of names of test type fields such as CharField, TextField
    search_fields = [
        # "owner",
        "seqtype",
        "id",
        "owner__username",
        "project__id",
        "project__title",
        "TaxID",
        "ScientificName",
        "Experiment",
        "LibraryName",
        "LibraryStrategy",
        "LibrarySelection",
        "LibrarySource",
        "LibraryLayout",
        "Platform",
        "SequencerModel",
        "SampleName",
        "CenterName",
        "DateCreated",
        "LastUpdate",
        "Description",
        "taxName_1",
        "taxFrac_1",
        "taxName_2",
        "taxFrac_2",
        "taxName_3",
        "taxFrac_3",
        "taxName_4",
        "taxFrac_4",
        "RawStats__Reads",
        "RawStats__Yield",
        "RawStats__GeeCee",
        "RawStats__MinLen",
        "RawStats__AvgLen",
        "RawStats__MaxLen",
        "RawStats__AvgQual",
        "RawStats__ErrQual",
        "RawStats__Ambiguous",
        "QcStats__Reads",
        "QcStats__Yield",
        "QcStats__GeeCee",
        "QcStats__MinLen",
        "QcStats__AvgLen",
        "QcStats__MaxLen",
        "QcStats__AvgQual",
        "QcStats__ErrQual",
        "QcStats__Ambiguous",
    ]

    ordering_fields = "__all__"
    ordering = ['DateCreated']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False)
    def metadata(self, request):
        seqtype = request.query_params["seqtype"]
        seq = Sequence.objects.filter(seqtype=seqtype)
        serializer = SequenceMetadataSerializer(seq)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SequenceViewSet_0(
    GenericViewSet,  # generic view functionality
    CreateModelMixin,  # handles POSTs
    RetrieveModelMixin,  # handles GETs for 1 Company
    UpdateModelMixin,  # handles PUTs and PATCHes
    ListModelMixin,  # handles GETs for many Companies
    DestroyModelMixin,
):  # handle delete
    
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer
    filterset_class = SequenceFilter
    pagination_class = CustomPagination
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
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
        "project",
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
        return self.queryset.filter(owner=self.request.user)
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