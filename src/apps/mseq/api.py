from gizmos.pagination import CustomPagination
#from gizmos.filter import EbsOrderFilter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .filters import (
    SequenceFilter, 
    SequenceSearchFilter,
    BioSampleFilter,
    BioSampleSearchFilter
)
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import (
    MetadataFile, 
    SeqFile, 
    Sequence, 
    Project, 
    Seqstat,
    BioSample
)

from .serializers import (
    MetadataFileSerializer,
    MyFileSerializer,
    SeqFileSerializer,
    SequenceMetadataSerializer,
    SequenceSerializer,
    ProjectSerializer,
    SeqstatSerializer,
    BioSampleSerializer,
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
        'description',
        'owner__username',
    ]

    #generic filtering only for text, char field
    search_fields = [
        'id',
        'title',
        'description',
        'owner__username',
    ]
    ordering_fields =  [
        'id',
        'title',
        'DateCreated',
        'LastUpdate',
        'owner__username',
    ]
    ordering = ['DateCreated']
 
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class BioSampleViewSet(
    GenericViewSet,  # generic view functionality
    CreateModelMixin,  # handles POSTs
    RetrieveModelMixin,  # handles GETs for 1 Company
    UpdateModelMixin,  # handles PUTs and PATCHes
    ListModelMixin,  # handles GETs for many Companies
    DestroyModelMixin,
):  # handle delete
    
    queryset = BioSample.objects.all()
    serializer_class = BioSampleSerializer
    pagination_class = CustomPagination
    
    filter_backends = (
        #SearchFilter,
        BioSampleSearchFilter,
        OrderingFilter,
        DjangoFilterBackend
        
    )
    
    search_fields = BioSampleSearchFilter.Meta.fields
   
    #ordering_fields = '__all__'
    ordering_fields = BioSampleFilter.Meta.fields
    
    ordering = ['DateCreated']
 
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SeqstatViewSet(
    GenericViewSet,  # generic view functionality
    CreateModelMixin,  # handles POSTs
    RetrieveModelMixin,  # handles GETs for 1 Company
    UpdateModelMixin,  # handles PUTs and PATCHes
    ListModelMixin,  # handles GETs for many Companies
    DestroyModelMixin,
):  # handle delete
    
    queryset = Seqstat.objects.all()
    serializer_class = SeqstatSerializer
    pagination_class = CustomPagination
    #this define nested field
    filterset_class = BioSampleFilter
    
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend
        
    )
    # #equality-based filtering
    # filterset_fields = [
    #     'id',
    #     'title',
    #     'description',
    #     'owner__username',
    # ]

    # #generic filtering only for text, char field
    # search_fields = [
    #     'id',
    #     'title',
    #     'description',
    #     'owner__username',
    # ]
    # ordering_fields =  [
    #     'id',
    #     'title',
    #     'DateCreated',
    #     'LastUpdate',
    #     'owner__username',
    # ]
    # ordering = ['DateCreated']
 
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
        #SearchFilter,
        SequenceSearchFilter,
        OrderingFilter,
        #RelatedOrderingFilter,
        #SequenceOrderingFilter,
        DjangoFilterBackend,
        
    )
    #filterset_fields define equaity based searching, this is defined in SequenceFilter class
    # print("equaity based search fields: *******************************************")
    # print(SequenceSearchFilter.Meta.fields)
    search_fields = SequenceSearchFilter.Meta.fields
   
    #ordering_fields = '__all__'
    ordering_fields = SequenceFilter.Meta.fields
    print(ordering_fields)
    ordering = ['project']
    
    # This method should be overriden
    # if we dont want to modify query set based on current instance attributes
    def get_queryset_0(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        qs = super().get_queryset()
        """ if self.request.user.groups.filter(name='Administrator').exists():
            self.filterset_class = AdminFilterSet """
        self.filterset_class = SequenceFilter
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
       
        return self.filter.qs
    
    @action(detail=False)
    def metadata_0(self, request):
        seq = (
          Sequence.objects.filter(sampleType = request.query_params["sampleType"])
          if "sampleType" in request.GET
          else Sequence.objects.all()
        )
        
        serializer = SequenceMetadataSerializer(seq)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #https://stackoverflow.com/questions/58855861/dynamically-set-filterset-class-in-django-listview
    @action(detail=False)
    def metadata(self, request):
        qs = super().get_queryset()
        self.filterset_class = SequenceFilter
       
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        seq = self.filter.qs
        #get QueryDict
        # q = request.GET
        # seq =  self.queryset.filter(**q.dict())
        serializer = SequenceMetadataSerializer(seq)
        return Response(serializer.data, status=status.HTTP_200_OK)

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