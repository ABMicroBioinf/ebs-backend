from django.db.models import Count
from django.db.models.aggregates import Max, Min
from gizmos.mixins import FlattenMixin
from rest_framework import serializers
from rest_framework.compat import distinct
from django.db.models.functions import TruncDate

from .models import (
    Sequence, 
    SeqFile, 
    MetadataFile, 
    Project, 
    Seqstat,
    BioSample
)

from gizmos.util import ObjectIdField

class ProjectSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    #sequences = serializers.StringRelatedField(many=True)
    sequences = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='seq:sequence-detail'
    )
    
    class Meta:
        model = Project
        fields = "__all__"
        #fields = ['id', 'owner', 'title', 'description', 'DateCreated', 'LastUpdate', 'sequences']
#class ProjectSerializer(DjongoModelSerializer):
class BioSampleSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    project__id =  serializers.ReadOnlyField(source='project.id')
    project__title =  serializers.ReadOnlyField(source='project.title')
    
    owner = serializers.ReadOnlyField(source="owner.username")
    sequences = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='seq:sequence-detail'
    )
    
    class Meta:
        model = BioSample
        fields = "__all__"
        #fields = ['id', 'owner', 'title', 'description', 'DateCreated', 'LastUpdate', 'sequences']

#class ProjectSerializer(DjongoModelSerializer):
class SeqstatSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    class Meta:
        model = Seqstat
        fields = "__all__"
        
class SequenceSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    
    owner = serializers.ReadOnlyField(source="owner.username")
    project__id = serializers.CharField(source='project.id')
    project__title = serializers.CharField(source='project.title')
    
    biosample__id = serializers.CharField(source='biosample.id')
    biosample__ScientificName = serializers.CharField(source='biosample.ScientificName')
    
    seqstat__id = serializers.CharField(source='seqstat.id')
    seqstat__r_Reads = serializers.IntegerField(source='seqstat.r_Reads')
    seqstat__r_Yield = serializers.CharField(source='seqstat.r_Yield')
    seqstat__r_GeeCee = serializers.CharField(source='seqstat.r_GeeCee')
    seqstat__r_MinLen = serializers.CharField(source='seqstat.r_MinLen')
    seqstat__r_AvgLen = serializers.CharField(source='seqstat.r_AvgLen')
    seqstat__r_MaxLen = serializers.CharField(source='seqstat.r_MaxLen')
    seqstat__r_AvgQual = serializers.CharField(source='seqstat.r_AvgQual')
    seqstat__r_ErrQual = serializers.CharField(source='seqstat.r_ErrQual')
    seqstat__r_Ambiguous = serializers.CharField(source='seqstat.r_Ambiguous')
    
    seqstat__q_Reads = serializers.CharField(source='seqstat.q_Reads')
    seqstat__q_Yield = serializers.CharField(source='seqstat.q_Yield')
    seqstat__q_GeeCee = serializers.CharField(source='seqstat.q_GeeCee')
    seqstat__q_MinLen = serializers.CharField(source='seqstat.q_MinLen')
    seqstat__q_AvgLen = serializers.CharField(source='seqstat.q_AvgLen')
    seqstat__q_MaxLen = serializers.CharField(source='seqstat.q_MaxLen')
    seqstat__q_AvgQual = serializers.CharField(source='seqstat.q_AvgQual')
    seqstat__q_ErrQual = serializers.CharField(source='seqstat.q_ErrQual')
    seqstat__q_Ambiguous = serializers.CharField(source='seqstat.q_Ambiguous')
    
    class Meta:
        model = Sequence
        fields = "__all__"
       
        
class SeqFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeqFile
        
        fields = (
            'id', 'raw_seq_file', 'qc_seq_file', 'sequence'
        )

class MetadataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataFile
        fields = (
            'id', 'metadata_file', 'sequence'
        )

class MyFileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)

class SequenceMetadataSerializer(serializers.Serializer):
    
   
    sampleType= serializers.SerializerMethodField(
        "get_distinct_count_for_sampleType"
    )
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
    LibraryLayout = serializers.SerializerMethodField(
        "get_distinct_count_for_library_layout"
    )
    Platform = serializers.SerializerMethodField(
        "get_distinct_count_for_platform"
    )
    SequencerModel = serializers.SerializerMethodField(
        "get_distinct_count_for_sequencer_model"
    )
    CenterName = serializers.SerializerMethodField(
        "get_distinct_count_for_center_name"
    )
    DateCreated = serializers.SerializerMethodField(
        "get_distinct_count_for_date_created"
    )
    LastUpdate = serializers.SerializerMethodField(
        "get_distinct_count_for_last_update"
    )
    
   
    """ 
    LibraryStrategy = serializers.SerializerMethodField(
        "get_distinct_count_for_library_strategy"
    )
    LibrarySelection = serializers.SerializerMethodField(
        "get_distinct_count_for_library_selection"
    )
    LibrarySource = serializers.SerializerMethodField(
        "get_distinct_count_for_library_source"
    ) """
    
    
    """  ScientificName = serializers.SerializerMethodField(
        "get_distinct_count_for_scientific_name"
    ) """
    
    
    
    
    # DateCreated = serializers.SerializerMethodField(
    #     "get_min_max_for_date_created"
    # )
    # LastUpdate = serializers.SerializerMethodField(
    #     "get_min_max_for_last_update"
    # )

    class Meta:
        model: Sequence
        fields = (
            # "LibraryStrategy",
            # "LibrarySelection",
            # "LibrarySource",
            # "LibraryLayout",
            "Platform",
            "ScientificName",
            "CenterName",
            "SequencerModel",
        )
        
    def get_distinct_count_for_sampleType(self, seq):
        return seq.values("sampleType").annotate(total=Count("sampleType")).order_by("sampleType")
    
    def get_distinct_count_for_library_strategy(self, seq):
        return seq.values("LibraryStrategy").annotate(total=Count("LibraryStrategy")).order_by('LibraryStrategy')

    def get_distinct_count_for_library_selection(self, seq):
        return seq.values("LibrarySelection").annotate(total=Count("LibrarySelection")).order_by('LibrarySelection')

    def get_distinct_count_for_library_source(self, seq):
        return seq.values("LibrarySource").annotate(total=Count("LibrarySource")).order_by('LibrarySource')

    def get_distinct_count_for_library_layout(self, seq):
        return seq.values("LibraryLayout").annotate(total=Count("LibraryLayout")).order_by('LibraryLayout')
    
    def get_distinct_count_for_platform(self, seq):
        return seq.values("Platform").annotate(total=Count("Platform")).order_by('Platform')

    def get_distinct_count_for_scientific_name(self, seq):
        return seq.values("ScientificName").annotate(total=Count("ScientificName")).order_by('ScientificName')

    def get_distinct_count_for_center_name(self, seq):
        return seq.values("CenterName").annotate(total=Count("CenterName")).order_by('CenterName')

    def get_distinct_count_for_sequencer_model(self, seq):
        return seq.values("SequencerModel").annotate(total=Count("SequencerModel")).order_by('SequencerModel')
    
    def get_distinct_count_for_project(self, seq):
        return seq.values("project__id").annotate(total=Count("project__id")).order_by('project__id')
    
    def get_distinct_count_for_date_created(self, seq):
        return seq.values("DateCreated").annotate(total=Count("DateCreated")).order_by('DateCreated')
    
    def get_distinct_count_for_last_update(self, seq):
        return seq.values("LastUpdate").annotate(total=Count("LastUpdate")).order_by('LastUpdate')
    
    def get_min_max_for_date_created(self, seq):
        return(
            seq.values("DateCreated")
            .aggregate(Min("DateCreated"), Max("DateCreated"))
        )
    def get_min_max_for_last_update(self, seq):
        return(
            seq.values("LastUpdate")
            .aggregate(Min("LastUpdate"), Max("LastUpdate"))
        )

    # Example of distinct count for nested field when 'JOIN' issue occurs
    # def get_count_for_library_source(self, run):
    #     experiments = run.values("experiment")
    #     source = []
    #     for sourceObj in experiments:
    #         source.append(sourceObj["experiment"].librarySource)
    #     return dict(zip(Counter(source).keys(), Counter(source).values()))