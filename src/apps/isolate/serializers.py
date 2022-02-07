from rest_framework import serializers
#from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer
from apps.seq.serializers import SequenceSerializer
from gizmos.mixins import FlattenMixin
from .models import (
    Assembly,
    Stats,
    Annotation,
    Mlst,
    Virulome,
    Resistome,
    TbProfile,
    TbProfileSummary
)

from django.db.models import Count
from django.db.models import Max, Min
from djongo import models
from gizmos.util import ObjectIdField


#class AssemblySerializer(DjongoModelSerializer):
class AssemblySerializer(serializers.ModelSerializer):
    print("********************************** serializer")
    _id = ObjectIdField(read_only=True)
    sequence = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='seq:sequence-detail'
    )
    
    #sequences = SequenceSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    # reterieve fields from the related collection
    sequence__project__id = serializers.CharField(source='sequence.project.id')
    sequence__project__title = serializers.CharField(
        source='sequence.project.title')

    sequence__LibrarySource = serializers.CharField(
        source='sequence.LibrarySource')
    sequence__LibraryLayout = serializers.CharField(
        source='sequence.LibraryLayout')
    sequence__SequencerModel = serializers.CharField(
        source='sequence.SequencerModel')
    sequence__CenterName = serializers.CharField(source='sequence.CenterName')
    
    
    class Meta:
        model = Assembly
        fields = '__all__'
        read_only_fields = ['owner']

class AssemblyMetadataSerializer(serializers.Serializer):
    # contig = serializers.SerializerMethodField("get_max_for_count")
    # total_length = serializers.SerializerMethodField("get_min_max_for_bp")
    
    seqtype = serializers.SerializerMethodField(
        "get_distinct_count_for_seqtype"
    )
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
    count_range = serializers.SerializerMethodField(
        "get_count_bins"
    )
    bp_range = serializers.SerializerMethodField(
        "get_bp_bins"
    )
    class Meta:
        model = Assembly
        fields = (
            "contig",
            "total_length",
        
        )
    def get_distinct_count_for_seqtype(self, assembly):
        return assembly.values("seqtype").annotate(total=Count("seqtype")).order_by("seqtype")
    
    def get_distinct_count_for_project(self, assembly):
        queryset = assembly.values("sequence__project__id")
        return queryset.annotate(
                total=Count("sequence__project__id", distinct=True)
            ).order_by("sequence__project__id")
        #return queryset
        

    def get_distinct_count_for_sequencer_model(self, assembly):
        # queryset = assembly.values("sequence__SequencerModel")
        # print(queryset)
        # return queryset
        return(
            assembly.values(sequence__SequenceModel)
            .annotate(total=Count("sequence__SequenceModel"))
            .order_by("total")
        )

    def get_max_for_count(self, assembly):
        return assembly.values("count").aggregate(Max("count"))

    def get_min_max_for_bp(self, assembly):
        return assembly.values("bp").aggregate(Min("bp"), Max("bp"))
   
   
    def get_count_bins(self, assembly):
        dict = assembly.values("count").aggregate(Min("count"), Max("count"))
        print(dict)
        min = dict["count__min"]
        max = dict["count__max"]
        print(min)
        print(max)
        step = 100
        myList = list(range(min, max+step, step))
        #print(myList)
        start = -1
        bins = []
        for i in myList:
            #print (i)
            if start == -1:
                start = i
                continue
            end = i
            num = assembly.values("count").filter(count__range=(start, end)).count()
            bins.append({ "count_range": str(start) + "," + str(end), "total": num})
            #print(query)
            start = end
        #print(bins)
        return bins
    
    def get_bp_bins(self, assembly):
        dict = assembly.values("bp").aggregate(Min("bp"), Max("bp"))
        #print(dict)
        min = dict["bp__min"]
        max = dict["bp__max"]
        print(min)
        print(max)
        step = 100000
        myList = list(range(min, max+step, step))
        #print(myList)
        start = -1
        bins = []
        for i in myList:
            #print (i)
            if start == -1:
                start = i
                continue
            end = i
            num = assembly.values("bp").filter(bp__range=(start, end)).count()
            bins.append({ "bp_range": str(start) + ","  + str(end), "total": num})
            #print(query)
            start = end
        #print(bins)
        return bins

class StatsSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    assembly = serializers.ReadOnlyField(source='assembly.id')
    # reterieve fields from the related collection
    assembly__sequence__project__id = serializers.CharField(
        source='assembly.sequence.project.id')
    assembly__sequence__project__title = serializers.CharField(
        source='assembly.sequence.project.title')

    assembly__sequence__LibrarySource = serializers.CharField(
        source='assembly.sequence.LibrarySource')
    assembly__sequence__LibraryLayout = serializers.CharField(
        source='assembly.sequence.LibraryLayout')
    assembly__sequence__SequencerModel = serializers.CharField(
        source='assembly.sequence.SequencerModel')
    assembly__sequence__CenterName = serializers.CharField(
        source='assembly.sequence.CenterName')

    class Meta:
        model = Stats
        fields = '__all__'
        read_only_fields = ['owner']

class StatsMetadataSerializer(serializers.Serializer):
    seqtype = serializers.SerializerMethodField(
        "get_distinct_count_for_seqtype")
    
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
    CDS_range = serializers.SerializerMethodField(
        "get_CDS_bins"
    )
    class Meta:
        model = Stats
        fields = (
            "seqtype",
            "project__id"
        )
        
    def get_distinct_count_for_project(self, stats):
        queryset = stats.values("assembly__sequence__project__id")
        return queryset.annotate(
                total=Count("assembly__sequence__project__id", distinct=True)
            ).order_by("assembly__sequence__project__id")
        #return queryset
        
    def get_distinct_count_for_seqtype(self, stats):
        return stats.values("seqtype").annotate(total=Count("seqtype")).order_by("seqtype")
    
    def get_CDS_bins(self, assembly):
        dict = assembly.values("CDS").aggregate(Min("CDS"), Max("CDS"))
        #print(dict)
        min = dict["CDS__min"]
        max = dict["CDS__max"]
        print(min)
        print(max)
        step = 200
        myList = list(range(min, max+step, step))
        #print(myList)
        start = -1
        bins = []
        for i in myList:
            #print (i)
            if start == -1:
                start = i
                continue
            end = i
            num = assembly.values("CDS").filter(CDS__range=(start, end)).count()
            bins.append({ "CDS_range": str(start) + ","  + str(end), "total": num})
            #print(query)
            start = end
        #print(bins)
        return bins
#class MlstSerializer(FlattenMixin, DjongoModelSerializer):
class MlstSerializer(FlattenMixin, serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    # is not working
    # assembly = serializers.HyperlinkedRelatedField(
    #     many=False,
    #     read_only=True,
    #     view_name='isolate.gbase:assembly-detail'
    # )

    #sequences = SequenceSerializer(many=True)

    owner = serializers.ReadOnlyField(source='owner.username')
    assembly = serializers.ReadOnlyField(source='assembly.id')
    # reterieve fields from the related collection
    assembly__sequence__project__id = serializers.CharField(
        source='assembly.sequence.project.id')
    assembly__sequence__project__title = serializers.CharField(
        source='assembly.sequence.project.title')

    assembly__sequence__LibrarySource = serializers.CharField(
        source='assembly.sequence.LibrarySource')
    assembly__sequence__LibraryLayout = serializers.CharField(
        source='assembly.sequence.LibraryLayout')
    assembly__sequence__SequencerModel = serializers.CharField(
        source='assembly.sequence.SequencerModel')
    assembly__sequence__CenterName = serializers.CharField(
        source='assembly.sequence.CenterName')
    
    class Meta:
        model = Mlst
        fields = '__all__'

        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]
        

class MlstMetadataSerializer(serializers.Serializer):
    seqtype = serializers.SerializerMethodField(
        "get_distinct_count_for_seqtype")
    scheme = serializers.SerializerMethodField("get_distinct_count_for_scheme")
    st = serializers.SerializerMethodField("get_distinct_count_for_st")

    class Meta:
        model = Mlst
        fields = (
            "seqtype",
            "scheme",
            "st"
        )

    def get_distinct_count_for_seqtype(self, mlst):
        return mlst.values("seqtype").annotate(total=Count("seqtype")).order_by("seqtype")

    def get_distinct_count_for_scheme(self, mlst):
        return mlst.values("scheme").annotate(total=Count("scheme", distinct=True)).order_by("scheme")

    def get_distinct_count_for_st(self, mlst):
        return mlst.values("st").annotate(total=Count("st", distinct=True)).order_by("st")


#class ResistomeSerializer(FlattenMixin, DjongoModelSerializer):
class ResistomeSerializer(FlattenMixin, serializers.ModelSerializer):
    
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    assembly = serializers.ReadOnlyField(source='assembly.id')

    # reterieve fields from the related collection
    assembly__sequence__project__id = serializers.CharField(
        source='assembly.sequence.project.id')
    assembly__sequence__project__title = serializers.CharField(
        source='assembly.sequence.project.title')

    assembly__sequence__LibrarySource = serializers.CharField(
        source='assembly.sequence.LibrarySource')
    assembly__sequence__LibraryLayout = serializers.CharField(
        source='assembly.sequence.LibraryLayout')
    assembly__sequence__SequencerModel = serializers.CharField(
        source='assembly.sequence.SequencerModel')
    assembly__sequence__CenterName = serializers.CharField(
        source='assembly.sequence.CenterName')

    class Meta:
        model = Resistome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]


class ResistomeMetadataSerializer(serializers.Serializer):
    seqtype = serializers.SerializerMethodField(
        "get_distinct_count_for_seqtype")
    num_found = serializers.SerializerMethodField(
        "get_distinct_count_for_num_found")

    class Meta:
        model = Resistome
        fields = (
            "seqtype",
            "num_found"
        )

    def get_distinct_count_for_seqtype(self, resistome):
        return resistome.values("seqtype").annotate(total=Count("seqtype")).order_by("seqtype")

    def get_distinct_count_for_num_found(self, resistome):
        return resistome.values("num_found").annotate(total=Count("num_found")).order_by("num_found")


class VirulomeSerializer(ResistomeSerializer):
    #_id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    assembly = serializers.ReadOnlyField(source='assembly.id')

    # reterieve fields from the related collection
    assembly__sequence__project__id = serializers.CharField(
        source='assembly.sequence.project.id')
    assembly__sequence__project__title = serializers.CharField(
        source='assembly.sequence.project.title')

    assembly__sequence__LibrarySource = serializers.CharField(
        source='assembly.sequence.LibrarySource')
    assembly__sequence__LibraryLayout = serializers.CharField(
        source='assembly.sequence.LibraryLayout')
    assembly__sequence__SequencerModel = serializers.CharField(
        source='assembly.sequence.SequencerModel')
    assembly__sequence__CenterName = serializers.CharField(
        source='assembly.sequence.CenterName')

    class Meta:
        model = Virulome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]

class VirulomeMetadataSerializer(serializers.Serializer):
    seqtype = serializers.SerializerMethodField(
        "get_distinct_count_for_seqtype")
    num_found = serializers.SerializerMethodField(
        "get_distinct_count_for_num_found")

    class Meta:
        model = Virulome
        fields = (
            "seqtype",
            "num_found"
        )

    def get_distinct_count_for_seqtype(self, virulome):
        return virulome.values("seqtype").annotate(total=Count("seqtype")).order_by("seqtype")

    def get_distinct_count_for_num_found(self, resistome):
        return resistome.values("num_found").annotate(total=Count("num_found")).order_by("num_found")

#class AnnotationSerializer(FlattenMixin, DjongoModelSerializer):
class AnnotationSerializer(FlattenMixin, serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    assembly = serializers.ReadOnlyField(source='assembly.id')

    # reterieve fields from the related collection
    assembly__sequence__project__id = serializers.CharField(
        source='assembly.sequence.project.id')
    assembly__sequence__project__title = serializers.CharField(
        source='assembly.sequence.project.title')

    assembly__sequence__LibrarySource = serializers.CharField(
        source='assembly.sequence.LibrarySource')
    assembly__sequence__LibraryLayout = serializers.CharField(
        source='assembly.sequence.LibraryLayout')
    assembly__sequence__SequencerModel = serializers.CharField(
        source='assembly.sequence.SequencerModel')
    assembly__sequence__CenterName = serializers.CharField(
        source='assembly.sequence.CenterName')

    class Meta:
        model = Annotation
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "attr"
        ]



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
            # "lineage",
            # "dr_variants",
            # "other_variants",
            # "dr_resistances"

        ]
        
class TbProfileSummarySerializer(serializers.ModelSerializer):
   
    sequence= serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='seq:sequence-detail'
    ) 
    
    #sequences = SequenceSerializer(many=True)

    owner = serializers.ReadOnlyField(source='owner.username')

    #reterieve fields from the related collection
    project__id = serializers.CharField(source='sequence.project.id')
    project__title = serializers.CharField(source='sequence.project.title')

    
    sequence__LibrarySource = serializers.CharField(source='sequence.LibrarySource')
    sequence__LibraryLayout = serializers.CharField(source='sequence.LibraryLayout')
    sequence__SequencerModel = serializers.CharField(source='sequence.SequencerModel')
    sequence__CenterName = serializers.CharField(source='sequence.CenterName')
    
    class Meta:
        model = TbProfileSummary

        fields = '__all__'
        read_only_fields = ['owner']
        

class TbProfileSummaryMetadataSerializer(serializers.ModelSerializer):

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
            "main_lin",
            "sublin",
            "num_dr_variants",
            "num_other_variants",
            "drtype"
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