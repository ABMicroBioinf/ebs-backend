from rest_framework import serializers
#from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer
from apps.seq.serializers import SequenceSerializer
from apps.seq.models import Sequence
from gizmos.mixins import FlattenMixin
from .models import (
    Assembly,
    Stats,
    Mlst,
    Virulome,
    Resistome,
    Plasmid,
    TbProfile,
    TbProfileSummary
)

from django.db.models import Count
from django.db.models import Max, Min
from djongo import models
from gizmos.util import ObjectIdField


#class AssemblySerializer(DjongoModelSerializer):
class AssemblySerializer(serializers.ModelSerializer):
   
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    # reterieve fields from the related collection
    biosample__sampleType =  serializers.ReadOnlyField(source='biosample.sampleType')
    biosample__ScientificName   =  serializers.ReadOnlyField(source='biosample.ScientificName')
    biosample__project__id =  serializers.ReadOnlyField(source='biosample.project.id')
    biosample__project__title =  serializers.ReadOnlyField(source='biosample.project.title')
    
    class Meta:
        model = Assembly
        fields = '__all__'
        read_only_fields = ['owner']
        ordering = ['biosample__project__id']

class AssemblyMetadataSerializer(serializers.Serializer):
    
    sampleType = serializers.SerializerMethodField(
        "get_distinct_count_for_sampleType"
    )
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
   
    contig_total_count = serializers.SerializerMethodField(
        "get_min_max_for_count"
    )
    contig_total_length = serializers.SerializerMethodField(
        "get_min_max_for_bp"
    )
    
    class Meta:
        model = Assembly
        fields = (
            "contig",
            "total_length",
        
        )
    def get_distinct_count_for_sampleType(self, assembly):
        return assembly.values("biosample__sampleType").annotate(
            total=Count("biosample__sampleType")
            ).order_by("biosample__sampleType")
    
    def get_distinct_count_for_project(self, assembly):
        queryset = assembly.values("biosample__project__id")
        return queryset.annotate(
                total=Count("biosample__project__id", distinct=True)
            ).order_by("biosample__project__id")
        #return queryset
     
    def get_min_max_for_count(self, assembly):
        return assembly.values("count").aggregate(Min("count"), Max("count"))
    
    def get_min_max_for_bp(self, assembly):
        return assembly.values("bp").aggregate(Min("bp"), Max("bp"))
   
   

class StatsSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    assembly__biosample__project__id =  serializers.ReadOnlyField(source='assembly.biosample.project.id')
    assembly__biosample__project__title =  serializers.ReadOnlyField(source='assembly.biosample.project.title')
    biosample__id =  serializers.ReadOnlyField(source='assembly.biosample.id')
    assembly__biosample__sampleType =  serializers.ReadOnlyField(source='assembly.biosample.sampleType')
    class Meta:
        model = Stats
        fields = '__all__'
        read_only_fields = ['owner']
        ordering = ['assembly__biosample__project__id']

class StatsMetadataSerializer(serializers.Serializer):
    sampleType = serializers.SerializerMethodField(
        "get_distinct_count_for_sampleType")
    
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
   
    class Meta:
        model = Stats
        fields = (
            "sampleType",
            "project__id"
        )
        
    def get_distinct_count_for_project(self, stats):
        queryset = stats.values("assembly__biosample__project__id")
        return queryset.annotate(
                total=Count("assembly__biosample__project__id", distinct=True)
            ).order_by("assembly__biosample__project__id")
        #return queryset
        
    def get_distinct_count_for_sampleType(self, stats):
        return stats.values("assembly__biosample__sampleType").annotate(
            total=Count("assembly__biosample__sampleType")).order_by("assembly__biosample__sampleType")
    
#class MlstSerializer(FlattenMixin, DjongoModelSerializer):
class MlstSerializer(FlattenMixin, serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
  
    assembly__biosample__project__id =  serializers.ReadOnlyField(source='assembly.biosample.project.id')
    assembly__biosample__project__title =  serializers.ReadOnlyField(source='assembly.biosample.project.title')
    assembly_biosample__id =  serializers.ReadOnlyField(source='assembly.biosample.id')
    assembly__biosample__sampleType =  serializers.ReadOnlyField(source='assembly.biosample.sampleType')
    
    class Meta:
        model = Mlst
        fields = '__all__'
        ordering = ['assembly__biosample__project__id']

        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]
        

class MlstMetadataSerializer(serializers.Serializer):
    sampleType = serializers.SerializerMethodField(
        "get_distinct_count_for_sampleType")
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
    scheme = serializers.SerializerMethodField("get_distinct_count_for_scheme")
    st = serializers.SerializerMethodField("get_distinct_count_for_st")

    class Meta:
        model = Mlst
        fields = (
            "seqtype",
            "scheme",
            "st"
        )
    def get_distinct_count_for_sampleType(self, stats):
        return stats.values("assembly__biosample__sampleType").annotate(
            total=Count("assembly__biosample__sampleType")).order_by("assembly__biosample__sampleType")
        
    
    def get_distinct_count_for_project(self, stats):
        queryset = stats.values("assembly__biosample__project__id")
        return queryset.annotate(
                total=Count("assembly__biosample__project__id", distinct=True)
            ).order_by("assembly__biosample__project__id")
        #return queryset
        
    def get_distinct_count_for_scheme(self, mlst):
        return mlst.values("scheme").annotate(total=Count("scheme", distinct=True)).order_by("scheme")

    def get_distinct_count_for_st(self, mlst):
        return mlst.values("st").annotate(total=Count("st", distinct=True)).order_by("st")


#class ResistomeSerializer(FlattenMixin, DjongoModelSerializer):
class ResistomeSerializer(FlattenMixin, serializers.ModelSerializer):
    
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    #assembly = serializers.ReadOnlyField(source='assembly.id')

    # reterieve fields from the related collection
    assembly__biosample__project__id =  serializers.ReadOnlyField(source='assembly.biosample.project.id')
    assembly__biosample__project__title =  serializers.ReadOnlyField(source='assembly.biosample.project.title')
    assembly__biosample__id =  serializers.ReadOnlyField(source='assembly.biosample.id')
    assembly__biosample__sampleType =  serializers.ReadOnlyField(source='assembly.biosample.sampleType')
    class Meta:
        model = Resistome
        ordering = ['assembly__biosample__project__id']
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]


class ResistomeMetadataSerializer(serializers.Serializer):
    sampleType = serializers.SerializerMethodField(
        "get_distinct_count_for_sampleType")
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
    num_found = serializers.SerializerMethodField(
        "get_distinct_count_for_num_found")

    class Meta:
        model = Resistome
        fields = (
            "seqtype",
            "num_found"
        )

    def get_distinct_count_for_sampleType(self, stats):
        return stats.values("assembly__biosample__sampleType").annotate(
            total=Count("assembly__biosample__sampleType")).order_by("assembly__biosample__sampleType")

    def get_distinct_count_for_num_found(self, resistome):
        return resistome.values("num_found").annotate(total=Count("num_found")).order_by("num_found")
    def get_distinct_count_for_project(self, resistome):
        queryset = resistome.values("assembly__biosample__project__id")
        return queryset.annotate(
                total=Count("assembly__biosample__project__id", distinct=True)
            ).order_by("assembly__biosample__project__id")

class VirulomeSerializer(ResistomeSerializer):
    #_id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    assembly = serializers.ReadOnlyField(source='assembly.id')

    # reterieve fields from the related collection
    assembly__biosample__project__id =  serializers.ReadOnlyField(source='assembly.biosample.project.id')
    assembly__biosample__project__title =  serializers.ReadOnlyField(source='assembly.biosample.project.title')
    biosample__id =  serializers.ReadOnlyField(source='assembly.biosample.id')
    assembly__biosample__sampleType =  serializers.ReadOnlyField(source='assembly.biosample.sampleType')
    class Meta:
        model = Virulome
        fields = '__all__'
        read_only_fields = ['owner']
        ordering = ['assembly__biosample__project__id']
        flatten = [
            "profile"
        ]

class VirulomeMetadataSerializer(serializers.Serializer):
    sampleType = serializers.SerializerMethodField(
        "get_distinct_count_for_sampleType")
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
    num_found = serializers.SerializerMethodField(
        "get_distinct_count_for_num_found")

    class Meta:
        model = Virulome
        fields = (
            "seqtype",
            "num_found"
        )

    def get_distinct_count_for_sampleType(self, stats):
        return stats.values("assembly__biosample__sampleType").annotate(
            total=Count("assembly__biosample__sampleType")).order_by("assembly__biosample__sampleType")

    def get_distinct_count_for_num_found(self, resistome):
        return resistome.values("num_found").annotate(total=Count("num_found")).order_by("num_found")
    
    def get_distinct_count_for_project(self, virulome):
        queryset = virulome.values("assembly__biosample__project__id")
        return queryset.annotate(
                total=Count("assembly__biosample__project__id", distinct=True)
            ).order_by("assembly__biosample__project__id")

class TbProfileSerializer(FlattenMixin, serializers.ModelSerializer):
    sequence= serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='seq:sequence-detail'
    ) 
    owner = serializers.ReadOnlyField(source='owner.username')
    #reterieve fields from the related collection
    sequence__project__id = serializers.CharField(source='sequence.project.id')
    sequence__project__title = serializers.CharField(source='sequence.project.title')
    sequence__LibrarySource = serializers.CharField(source='sequence.LibrarySource')
    sequence__LibraryLayout = serializers.CharField(source='sequence.LibraryLayout')
    sequence__SequencerModel = serializers.CharField(source='sequence.SequencerModel')
    sequence__CenterName = serializers.CharField(source='sequence.CenterName')

    class Meta:
        model = TbProfile
        fields = '__all__'
       
        flatten = [
            "lineage",
            # "dr_variants",
            # "other_variants",
            # "dr_resistances"

        ]

class PlasmidSerializer(FlattenMixin, serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    assembly = serializers.ReadOnlyField(source='assembly.id')

    # reterieve fields from the related collection
    assembly__biosample__project__id =  serializers.ReadOnlyField(source='assembly.biosample.project.id')
    assembly__biosample__project__title =  serializers.ReadOnlyField(source='assembly.biosample.project.title')
    biosample__id =  serializers.ReadOnlyField(source='assembly.biosample.id')
    assembly__biosample__sampleType =  serializers.ReadOnlyField(source='assembly.biosample.sampleType')
    assembly__count =  serializers.ReadOnlyField(source='assembly.count')
    class Meta:
        model = Plasmid
        fields = '__all__'
        read_only_fields = ['owner']
        ordering = ['assembly__biosample__project__id']
        flatten = [
            "profile"
        ]


class PlasmidMetadataSerializer(serializers.Serializer):
    sampleType = serializers.SerializerMethodField(
        "get_distinct_count_for_sampleType")
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
    
    class Meta:
        model = Plasmid
        # fields = (
        #     "seqtype",
        #     "scheme",
        #     "st"
        # )
    def get_distinct_count_for_sampleType(self, stats):
        return stats.values("assembly__biosample__sampleType").annotate(
            total=Count("assembly__biosample__sampleType")).order_by("assembly__biosample__sampleType")
        
    
    def get_distinct_count_for_project(self, stats):
        queryset = stats.values("assembly__biosample__project__id")
        return queryset.annotate(
                total=Count("assembly__biosample__project__id", distinct=True)
            ).order_by("assembly__biosample__project__id")
        #return queryset
    

              
class TbProfileSummarySerializer(serializers.ModelSerializer):
   
    sequence= serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='seq:sequence-detail'
    ) 
    
    #sequences = SequenceSerializer(many=True)

    owner = serializers.ReadOnlyField(source='owner.username')

    #reterieve fields from the related collection
    sequence__biosample__id =  serializers.ReadOnlyField(source='sequence.biosample.id')
    sequence__project__id =  serializers.ReadOnlyField(source='sequence.project.id')
    
    class Meta:
        model = TbProfileSummary

        fields = '__all__'
        read_only_fields = ['owner']
        

class TbProfileSummaryMetadataSerializer(serializers.ModelSerializer):

    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
    main_lin = serializers.SerializerMethodField(
        "get_distinct_count_for_main_lin")
    sublin = serializers.SerializerMethodField("get_distinct_count_for_sublin")
    num_dr_variants = serializers.SerializerMethodField(
        "get_distinct_count_for_num_dr_variants")
    num_other_variants = serializers.SerializerMethodField(
        "get_distinct_count_for_num_other_variants")
    drtype = serializers.SerializerMethodField("get_distinct_count_for_drtype")

    class Meta:

        model = TbProfileSummary
        fields = (
              "project__id",
            "main_lin",
            "sublin",
            "num_dr_variants",
            "num_other_variants",
            "drtype", 
          
        )

    def get_distinct_count_for_main_lin(self, psummary):
        return (
            psummary.values("main_lin").annotate(
                total=Count("main_lin")).order_by("main_lin")
        )

    def get_distinct_count_for_sublin(self, psummary):
        return (
            psummary.values("sublin").annotate(
                total=Count("sublin")).order_by("sublin")
        )

    def get_distinct_count_for_num_dr_variants(self, psummary):
        return (
            psummary.values("num_dr_variants").annotate(
                total=Count("num_dr_variants")).order_by("num_dr_variants")
        )

    def get_distinct_count_for_num_other_variants(self, psummary):
        return (
            psummary.values("num_other_variants").annotate(
                total=Count("num_other_variants")).order_by("num_other_variants")
        )

    def get_distinct_count_for_drtype(self, psummary):
        return (
            psummary.values("drtype").annotate(
                total=Count("drtype")).order_by("drtype")
        )
    def get_distinct_count_for_project(self, psummary):
        queryset = psummary.values("sequence__project__id")
        return queryset.annotate(
                total=Count("sequence__project__id", distinct=True)
            ).order_by("sequence__project__id")