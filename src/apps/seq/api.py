from gizmos.pagination import CustomPagination
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
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

    serializer_class = SequenceSerializer
    queryset = Sequence.objects.all()
    
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, OrderingFilter)
   
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
 
 
    def get_queryset_0(self):

        params_dict = self.request.query_params.dict()
        params_dict.pop('page', None)

        for key, value in params_dict.items():
            print(key)
            print(value)
    
        return self.queryset.filter(owner=self.request.user).filter(**params_dict)
    
    def get_queryset_1(self):

        params_dict = self.request.query_params.dict()
        params_dict.pop('page', None)
        params_dict.pop('ordering', None)
        params_dict.pop('search', None)
        for key, value in params_dict.items():
            print(key)
            print(value)
        
        return self.queryset.filter(owner=self.request.user).filter(**params_dict)#.filter(RawStats__startswith={'Reads': 'SRR'})

    def get_queryset(self):

        params_dict = self.request.query_params.dict()
        params_dict.pop('page', None)
        params_dict.pop('ordering', None)
        params_dict.pop('search', None)
        rstats_dict = {}
        qstats_dict = {}
        other_dict = {}
        for key, value in params_dict.items():
            print(key)
            print(value)
            if key.startswith('RawStats'):
                newkey = key[9:]
                rstats_dict[newkey] = value
            elif key.startswith('QcStats'):
                newkey = key[8:]
                qstats_dict[newkey] = value
            else:
                other_dict[key] = value          
        #return self.queryset.filter(owner=self.request.user).filter(**params_dict)
        q = None
        q = self.queryset.filter(owner=self.request.user)
        if other_dict:
            q = q.filter(**other_dict)
        if rstats_dict:
            q = q.filter(RawStats=SeqStat(**rstats_dict))
        if qstats_dict:
            q = q.filter(QcStats=SeqStat(**qstats_dict))
        return q
        #return self.queryset.filter(owner=self.request.user)
 

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