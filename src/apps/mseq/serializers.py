from django.db.models import Count
from django.db.models.aggregates import Max, Min
from gizmos.mixins import FlattenMixin
from rest_framework import serializers
from rest_framework.compat import distinct
#from rest_meets_djongo.serializers import DjongoModelSerializer

from .models import Sequence, SeqFile, MetadataFile, Project

from gizmos.util import ObjectIdField


#class ProjectSerializer(DjongoModelSerializer):
class ProjectSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    #sequences = serializers.StringRelatedField(many=True)
    msequences = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='seq:sequence-detail'
    )
    
    class Meta:
        model = Project
        fields = "__all__"
        #fields = ['id', 'owner', 'title', 'description', 'DateCreated', 'LastUpdate', 'sequences']

    
#class SequenceSerializer(FlattenMixin, DjongoModelSerializer):
class SequenceSerializer_org(serializers.Serializer):
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    project__id = serializers.CharField(source='project.id')
    project__title = serializers.CharField(source='project.title')
    class Meta:
        model = Sequence
        fields = "__all__"
        read_only_fields = ["owner"]

        flatten = [
            "RawStats",
            "QcStats",
        ]
    
class SequenceSerializer(FlattenMixin, serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    project__id = serializers.CharField(source='project.id')
    project__title = serializers.CharField(source='project.title')
    class Meta:
        model = Sequence
        fields = "__all__"
        read_only_fields = ["owner"]
        flatten = [
            "RawStats",
            "QcStats",
        ]
        
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
    
    """  seqtype = serializers.SerializerMethodField(
        "get_distinct_count_for_seqtype"
    ) """
    
    project__id = serializers.SerializerMethodField(
        "get_distinct_count_for_project"
    )
    Platform = serializers.SerializerMethodField(
        "get_distinct_count_for_platform"
    )
    LibraryStrategy = serializers.SerializerMethodField(
        "get_distinct_count_for_library_strategy"
    )
    LibrarySelection = serializers.SerializerMethodField(
        "get_distinct_count_for_library_selection"
    )
    LibrarySource = serializers.SerializerMethodField(
        "get_distinct_count_for_library_source"
    )
    LibraryLayout = serializers.SerializerMethodField(
        "get_distinct_count_for_library_layout"
    )
    
    """  ScientificName = serializers.SerializerMethodField(
        "get_distinct_count_for_scientific_name"
    ) """
    CenterName = serializers.SerializerMethodField(
        "get_distinct_count_for_center_name"
    )
    SequencerModel = serializers.SerializerMethodField(
        "get_distinct_count_for_sequencer_model"
    )
    
    DateCreated = serializers.SerializerMethodField(
        "get_min_max_for_date_created"
    )
    LastUpdate = serializers.SerializerMethodField(
        "get_min_max_for_last_update"
    )

    class Meta:
        model: Sequence
        fields = (
            "LibraryStrategy",
            "LibrarySelection",
            "LibrarySource",
            "LibraryLayout",
            "Platform",
            "ScientificName",
            "CenterName",
            "SequencerModel",
        )
    def get_distinct_count_for_seqtype(self, seq):
        return seq.values("seqtype").annotate(total=Count("seqtype")).order_by("seqtype")
    
    def get_distinct_count_for_library_strategy(self, seq):
        return seq.values("LibraryStrategy").annotate(total=Count("LibraryStrategy")).order_by('total')

    def get_distinct_count_for_library_selection(self, seq):
        return seq.values("LibrarySelection").annotate(total=Count("LibrarySelection")).order_by('total')

    def get_distinct_count_for_library_source(self, seq):
        return seq.values("LibrarySource").annotate(total=Count("LibrarySource")).order_by('total')

    def get_distinct_count_for_library_layout(self, seq):
        return seq.values("LibraryLayout").annotate(total=Count("LibraryLayout")).order_by('total')

    def get_distinct_count_for_platform(self, seq):
        return seq.values("Platform").annotate(total=Count("Platform")).order_by('total')

    def get_distinct_count_for_scientific_name(self, seq):
        return seq.values("ScientificName").annotate(total=Count("ScientificName")).order_by('total')

    def get_distinct_count_for_center_name(self, seq):
        return seq.values("CenterName").annotate(total=Count("CenterName")).order_by('total')

    def get_distinct_count_for_sequencer_model(self, seq):
        return seq.values("SequencerModel").annotate(total=Count("SequencerModel")).order_by('total')
    def get_distinct_count_for_project(self, seq):
        return seq.values("project__id").annotate(total=Count("project__id")).order_by('total')
    
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