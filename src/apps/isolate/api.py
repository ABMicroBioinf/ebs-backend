from .filters import TbProfileFilter, TbProfileSummaryFilter, TbProfileSearchFilter
from .serializers import (
    TbProfileSerializer, 
    TbProfileSummarySerializer, 
    TbProfileSummaryMetadataSerializer,
    PlasmidMetadataSerializer,
    PlasmidSerializer
)
from .models import TbProfile, TbProfileSummary
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters
from gizmos.pagination import CustomPagination
from .models import Assembly, Stats, Virulome, Mlst, Resistome, Plasmid
from .filters import (
    AssemblyFilter,
    AssemblySearchFilter,
    StatsFilter,
    StatsSearchFilter,
    MlstFilter,
    MlstSearchFilter,
    ResistomeFilter,
    ResistomeSearchFilter,
    VirulomeFilter,
    VirulomeSearchFilter,
    PlasmidFilter,
    PlasmidSearchFilter
    

)

from .serializers import (
    AssemblySerializer,
    AssemblyMetadataSerializer,
    StatsSerializer,
    StatsMetadataSerializer,
    VirulomeSerializer,
    VirulomeMetadataSerializer,
    MlstSerializer,
    MlstMetadataSerializer,
    ResistomeSerializer,
    ResistomeMetadataSerializer
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class AssemblyViewSet(GenericViewSet,  # generic view functionality
                      CreateModelMixin,  # handles POSTs
                      RetrieveModelMixin,  # handles GETs for 1 Company
                      UpdateModelMixin,  # handles PUTs and PATCHes
                      ListModelMixin,  # handles GETs for many Companies
                      DestroyModelMixin,):  # handle delete

    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
    filterset_class = AssemblyFilter
    pagination_class = CustomPagination

    filter_backends = (
        #SearchFilter,
        AssemblySearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,

    )

    #define the column for the text search
    search_fields = AssemblySearchFilter.Meta.fields
    print(search_fields)
    

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

       # https://stackoverflow.com/questions/58855861/dynamically-set-filterset-class-in-django-listview
    @action(detail=False)
    def metadata(self, request):
        qs = super().get_queryset()
        self.filterset_class = AssemblyFilter
        dict_params = dict(request.query_params.lists())
        self.filter = self.filterset_class(dict_params, queryset=qs)
        assembly = self.filter.qs
        serializer = AssemblyMetadataSerializer(assembly)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StatsViewSet(GenericViewSet,  # generic view functionality
                   CreateModelMixin,  # handles POSTs
                   RetrieveModelMixin,  # handles GETs for 1 Company
                   UpdateModelMixin,  # handles PUTs and PATCHes
                   ListModelMixin,  # handles GETs for many Companies
                   DestroyModelMixin,):  # handle delete

    queryset = Stats.objects.all()
    serializer_class = StatsSerializer
    filterset_class = StatsFilter
    pagination_class = CustomPagination

    filter_backends = (
        StatsSearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )

    search_fields = StatsSearchFilter.Meta.fields
    
   
    #ordering = ['assembly__sequence__project__id']
    #ordering = ['assembly__biosample__project__id']
  # This method should be overriden
    # if we dont want to modify query set based on current instance attributes
    def get_queryset(self):
        print(self.queryset)
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

       # https://stackoverflow.com/questions/58855861/dynamically-set-filterset-class-in-django-listview
    @action(detail=False)
    def metadata(self, request):
        qs = super().get_queryset()
        self.filterset_class = StatsFilter
       # query_params.get only returs the last occurrence of the parameter
        #self.filter = self.filterset_class(self.request.GET, queryset=qs)

        dict_params = dict(request.query_params.lists())
        self.filter = self.filterset_class(dict_params, queryset=qs)

        stats = self.filter.qs
        serializer = StatsMetadataSerializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def metadata_0(self, request):
        stats = (
            Stats.objects.filter(seqtype=request.query_params["seqtype"])
            if "seqtype" in request.GET
            else Stats.objects.all()
        )
        serializer = StatsMetadataSerializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MlstViewSet(GenericViewSet,  # generic view functionality
                  CreateModelMixin,  # handles POSTs
                  RetrieveModelMixin,  # handles GETs for 1 Company
                  UpdateModelMixin,  # handles PUTs and PATCHes
                  ListModelMixin,  # handles GETs for many Companies
                  DestroyModelMixin,):  # handle delete
    queryset = Mlst.objects.all()
    serializer_class = MlstSerializer
    filterset_class = MlstFilter
    pagination_class = CustomPagination

    filter_backends = (
        # SearchFilter,
        MlstSearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )

    # filterset_fields define equaity based searching, this is defined in SequenceFilter class
    print("equaity based search fields: *******************************************")
    print(MlstFilter.Meta.fields)
    search_fields = MlstFilter.Meta.fields
    
    #ordering_fields = MlstFilter.Meta.fields
    #
    
    # This method should be overriden
    # if we dont want to modify query set based on current instance attributes
    def get_queryset(self):
        print(self.queryset)
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

       # https://stackoverflow.com/questions/58855861/dynamically-set-filterset-class-in-django-listview
    @action(detail=False)
    def metadata(self, request):
        qs = super().get_queryset()
        self.filterset_class = MlstFilter
        # query_params.get only returs the last occurrence of the parameter
        #self.filter = self.filterset_class(self.request.GET, queryset=qs)

        dict_params = dict(request.query_params.lists())
        self.filter = self.filterset_class(dict_params, queryset=qs)

        mlst = self.filter.qs
        serializer = MlstMetadataSerializer(mlst)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def metadata_0(self, request):
        mlst = (
            Mlst.objects.filter(seqtype=request.query_params["seqtype"])
            if "seqtype" in request.GET
            else Mlst.objects.all()
        )
        serializer = MlstMetadataSerializer(mlst)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResistomeViewSet(GenericViewSet,  # generic view functionality
                       CreateModelMixin,  # handles POSTs
                       RetrieveModelMixin,  # handles GETs for 1 Company
                       UpdateModelMixin,  # handles PUTs and PATCHes
                       ListModelMixin,  # handles GETs for many Companies
                       DestroyModelMixin,):  # handle delete

    queryset = Resistome.objects.all()
    serializer_class = ResistomeSerializer
    filterset_class = ResistomeFilter
    pagination_class = CustomPagination
    filter_backends = (
        #SearchFilter,
        ResistomeSearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )
    # filterset_fields define equaity based searching, this is defined in SequenceFilter class
    #print(ResistomeSearchFilter.Meta.fields)
    search_fields = ResistomeSearchFilter.Meta.fields
    

    # This method should be overriden
    # if we dont want to modify query set based on current instance attributes
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

       # https://stackoverflow.com/questions/58855861/dynamically-set-filterset-class-in-django-listview
    @action(detail=False)
    def metadata(self, request):
        qs = super().get_queryset()
        self.filterset_class = ResistomeFilter
        # query_params.get only returs the last occurrence of the parameter
        #self.filter = self.filterset_class(self.request.GET, queryset=qs)

        dict_params = dict(request.query_params.lists())
        self.filter = self.filterset_class(dict_params, queryset=qs)
        resistome = self.filter.qs
        serializer = ResistomeMetadataSerializer(resistome)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VirulomeViewSet(GenericViewSet,  # generic view functionality
                      CreateModelMixin,  # handles POSTs
                      RetrieveModelMixin,  # handles GETs for 1 Company
                      UpdateModelMixin,  # handles PUTs and PATCHes
                      ListModelMixin,  # handles GETs for many Companies
                      DestroyModelMixin,):  # handle delete

    queryset = Virulome.objects.all()
    serializer_class = VirulomeSerializer
    filterset_class = VirulomeFilter
    pagination_class = CustomPagination
    filter_backends = (
        # SearchFilter,
        VirulomeSearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )

    # filterset_fields define equaity based searching, this is defined in SequenceFilter class
    # print("equaity based search fields: *******************************************")
    # print(VirulomeSearchFilter.Meta.fields)
    search_fields = VirulomeSearchFilter.Meta.fields
    #ordering = ['assembly__sequence__project__id']

    # This method should be overriden
    # if we dont want to modify query set based on current instance attributes
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

       # https://stackoverflow.com/questions/58855861/dynamically-set-filterset-class-in-django-listview
    @action(detail=False)
    def metadata(self, request):
        qs = super().get_queryset()
        self.filterset_class = VirulomeFilter
        dict_params = dict(request.query_params.lists())
        self.filter = self.filterset_class(dict_params, queryset=qs)
        viru = self.filter.qs
        serializer = VirulomeMetadataSerializer(viru)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlasmidViewSet(GenericViewSet,  # generic view functionality
                  CreateModelMixin,  # handles POSTs
                  RetrieveModelMixin,  # handles GETs for 1 Company
                  UpdateModelMixin,  # handles PUTs and PATCHes
                  ListModelMixin,  # handles GETs for many Companies
                  DestroyModelMixin,):  # handle delete
    queryset = Plasmid.objects.all()
    serializer_class = PlasmidSerializer
    filterset_class = PlasmidFilter
    pagination_class = CustomPagination

    filter_backends = (
        # SearchFilter,
        PlasmidSearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )

    # filterset_fields define equaity based searching, this is defined in SequenceFilter class
    print("equaity based search fields: *******************************************")
    print(PlasmidFilter.Meta.fields)
    search_fields = PlasmidFilter.Meta.fields
   
    # This method should be overriden
    # if we dont want to modify query set based on current instance attributes
    def get_queryset(self):
        print(self.queryset)
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

       # https://stackoverflow.com/questions/58855861/dynamically-set-filterset-class-in-django-listview
    @action(detail=False)
    def metadata(self, request):
        qs = super().get_queryset()
        self.filterset_class = PlasmidFilter
        dict_params = dict(request.query_params.lists())
        self.filter = self.filterset_class(dict_params, queryset=qs)

        plasmid = self.filter.qs
        serializer = PlasmidMetadataSerializer(plasmid)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TbProfileViewSet(GenericViewSet,  # generic view functionality
                       CreateModelMixin,  # handles POSTs
                       RetrieveModelMixin,  # handles GETs for 1 Company
                       UpdateModelMixin,  # handles PUTs and PATCHes
                       ListModelMixin,  # handles GETs for many Companies
                       DestroyModelMixin,):  # handle delete

    queryset = TbProfile.objects.all()
    serializer_class = TbProfileSerializer
    filterset_class = TbProfileFilter
    pagination_class = CustomPagination
    filter_backends = (
        # SearchFilter,
        TbProfileSearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )
    # filterset_fields define equaity based searching, this is defined in SequenceFilter class
    print("equaity based search fields: *******************************************")
    print(TbProfileFilter.Meta.fields)
    search_fields = TbProfileFilter.Meta.fields
    ordering = ['sequence__project__id']

    # This method should be overriden
    # if we dont want to modify query set based on current instance attributes
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TbProfileSummaryViewSet(GenericViewSet,  # generic view functionality
                              CreateModelMixin,  # handles POSTs
                              RetrieveModelMixin,  # handles GETs for 1 Company
                              UpdateModelMixin,  # handles PUTs and PATCHes
                              ListModelMixin,  # handles GETs for many Companies
                              DestroyModelMixin,):  # handle delete

    queryset = TbProfileSummary.objects.all()
    serializer_class = TbProfileSummarySerializer
    filterset_class = TbProfileSummaryFilter
    pagination_class = CustomPagination
    filter_backends = (
        SearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )

    # filterset_fields define equaity based searching, this is defined in SequenceFilter class
    print("equaity based search fields: *******************************************")
    print(TbProfileSummaryFilter.Meta.fields)
    search_fields = TbProfileSummaryFilter.Meta.fields
    ordering = ['sequence__project__id']

    # This method should be overriden
    # if we dont want to modify query set based on current instance attributes
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

       # https://stackoverflow.com/questions/58855861/dynamically-set-filterset-class-in-django-listview
    @action(detail=False)
    def metadata(self, request):
        qs = super().get_queryset()
        self.filterset_class = TbProfileSummaryFilter
        # query_params.get only returs the last occurrence of the parameter
        #self.filter = self.filterset_class(self.request.GET, queryset=qs)

        dict_params = dict(request.query_params.lists())
        self.filter = self.filterset_class(dict_params, queryset=qs)
        psummary = self.filter.qs
        serializer = TbProfileSummaryMetadataSerializer(psummary)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def metadata_0(self, request):
        psummary = TbProfileSummary.objects.all()
        serializer = TbProfileSummaryMetadataSerializer(psummary)
        return Response(serializer.data, status=status.HTTP_200_OK)
