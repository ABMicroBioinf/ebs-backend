from django.db.models import Count
from gizmos.mixins import FlattenMixin
from rest_framework import serializers
from rest_framework.compat import distinct
from rest_meets_djongo.serializers import DjongoModelSerializer

from .models import Sequence, SeqFile, MetadataFile

class SequenceSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

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
    Platform = serializers.SerializerMethodField(
        "get_distinct_count_for_platform"
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
    Projectid = serializers.SerializerMethodField(
        "get_distinct_count_for_projectid"
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
    def get_distinct_count_for_projectid(self, seq):
        return seq.values("Projectid").annotate(total=Count("Projectid")).order_by('total')

    # Example of distinct count for nested field when 'JOIN' issue occurs
    # def get_count_for_library_source(self, run):
    #     experiments = run.values("experiment")
    #     source = []
    #     for sourceObj in experiments:
    #         source.append(sourceObj["experiment"].librarySource)
    #     return dict(zip(Counter(source).keys(), Counter(source).values()))