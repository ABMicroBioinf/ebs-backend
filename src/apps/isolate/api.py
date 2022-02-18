from .filters import TbProfileFilter, TbProfileSummaryFilter, TbProfileSearchFilter
from .serializers import TbProfileSerializer, TbProfileSummarySerializer, TbProfileSummaryMetadataSerializer
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
from .models import Assembly, Stats, Annotation, Virulome, Mlst, Resistome
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
    AnnotationFilter,
    AnnotationSearchFilter

)

from .serializers import (
    AssemblySerializer,
    AssemblyMetadataSerializer,
    StatsSerializer,
    StatsMetadataSerializer,
    AnnotationSerializer,
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
        SearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,

    )

    #define the column for the text search
    search_fields = AssemblySearchFilter.Meta.fields
    print(search_fields)
    
    ordering = ['sequence__project__id']
    
    """ def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
      
      def get(self, request, format=None, **kwargs):
        dict_params = dict(request.query_params.lists())
        filter = AssemblyFilter(dict_params, queryset=Assembly.objects.all())
        return filter.queryset """

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # print("I am in perform_create...................................")
        # print(self.queryset)
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
    ordering = ['assembly__sequence__project__id']
  # This method should be overriden
    # if we dont want to modify query set based on current instance attributes

    def get_queryset(self):
        print(self.queryset)
        return self.queryset.filter(owner=self.request.user)
    # This method should be overriden
    # if we dont want to modify query set based on current instance attributes

    def get_queryset_1(self):
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
    
    ordering = ['assembly__sequence__project__id']
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
    #filterset_class = ResistomeFilter
    pagination_class = CustomPagination
    filter_backends = (
        #SearchFilter,
        ResistomeSearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )
    # filterset_fields define equaity based searching, this is defined in SequenceFilter class
    print("Resistome equaity based search fields: *******************************************")
    print(ResistomeFilter.Meta.fields)
    search_fields = ResistomeFilter.Meta.fields
    
    ordering = ['assembly__sequence__project__id']

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

    @action(detail=False)
    def metadata_0(self, request):
        resistome = (
            Resistome.objects.filter(seqtype=request.query_params["seqtype"])
            if "seqtype" in request.GET
            else Resistome.objects.all()
        )
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
    print("equaity based search fields: *******************************************")
    print(VirulomeFilter.Meta.fields)
    search_fields = VirulomeFilter.Meta.fields
    ordering = ['assembly__sequence__project__id']

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
        # query_params.get only returs the last occurrence of the parameter
        #self.filter = self.filterset_class(self.request.GET, queryset=qs)

        dict_params = dict(request.query_params.lists())
        self.filter = self.filterset_class(dict_params, queryset=qs)
        viru = self.filter.qs
        serializer = VirulomeMetadataSerializer(viru)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False)
    def metadata_0(self, request):
        virulome = (
            Virulome.objects.filter(seqtype=request.query_params["seqtype"])
            if "seqtype" in request.GET
            else Virulome.objects.all()
        )
        serializer = VirulomeMetadataSerializer(virulome)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnnotationViewSet(GenericViewSet,  # generic view functionality
                        CreateModelMixin,  # handles POSTs
                        RetrieveModelMixin,  # handles GETs for 1 Company
                        UpdateModelMixin,  # handles PUTs and PATCHes
                        ListModelMixin,  # handles GETs for many Companies
                        DestroyModelMixin,):  # handle delete

    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    filterset_class = AnnotationFilter
    pagination_class = CustomPagination
    filter_backends = (
        # SearchFilter,
        AnnotationSearchFilter,
        OrderingFilter,
        filters.DjangoFilterBackend,
    )

    # filterset_fields define equaity based searching, this is defined in SequenceFilter class
    print("equaity based search fields: *******************************************")
    print(AnnotationFilter.Meta.fields)
    search_fields = AnnotationFilter.Meta.fields
    ordering = ['DateCreated']

    # This method should be overriden
    # if we dont want to modify query set based on current instance attributes
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
