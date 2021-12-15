from rest_framework import serializers
from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer
from apps.seq.serializers import SequenceSerializer
from gizmos.mixins import FlattenMixin
from .models import (
    Assembly,
    Annotation,
    Mlst,
    Virulome,
    Resistome
)
from django.db.models import Count
from django.db.models import Max, Min

class AssemblySerializer(DjongoModelSerializer):

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
    contig = serializers.SerializerMethodField("get_max_for_count")
    total_length = serializers.SerializerMethodField("get_min_max_for_bp")

    class Meta:
        model = Assembly
        fields = (
            "contig",
            "total_length"
        )

    def get_distinct_count_for_project(self, assembly):
        queryset = assembly.values("sequence__project__id")
        # return queryset.annotate(
        #         total=Count("sequence__project__id", distinct=True)
        #     ).order_by("total")
        return queryset

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


class MlstSerializer(FlattenMixin, DjongoModelSerializer):

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
    st = serializers.SerializerMethodField("get_distinct_count_for_strand")

    class Meta:
        model = Mlst
        fields = (
            "seqtype",
            "scheme",
            "st"
        )

    def get_distinct_count_for_seqtype(self, mlst):
        return mlst.values("seqtype").annotate(total=Count("seqtype")).order_by("total")

    def get_distinct_count_for_scheme(self, mlst):
        return mlst.values("scheme").annotate(total=Count("scheme", distinct=True)).order_by("total")

    def get_distinct_count_for_strand(self, mlst):
        return mlst.values("st").annotate(total=Count("st", distinct=True)).order_by("total")


class ResistomeSerializer(FlattenMixin, DjongoModelSerializer):

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
        return resistome.values("seqtype").annotate(total=Count("seqtype")).order_by("total")

    def get_distinct_count_for_num_found(self, resistome):
        return resistome.values("num_found").annotate(total=Count("num_found")).order_by("total")


class VirulomeSerializer(ResistomeSerializer):
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
        return virulome.values("seqtype").annotate(total=Count("seqtype")).order_by("total")

    def get_distinct_count_for_num_found(self, resistome):
        return resistome.values("num_found").annotate(total=Count("num_found")).order_by("total")

class AnnotationSerializer(FlattenMixin, DjongoModelSerializer):

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
