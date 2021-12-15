from rest_framework import serializers
from .models import Profile, Psummary
from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer
from gizmos.mixins import FlattenMixin
from django.db.models import Count
class ProfileSerializer(FlattenMixin, DjongoModelSerializer):
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
        model = Profile
        fields = '__all__'
       
        flatten = [
            # "lineage",
            # "dr_variants",
            # "other_variants",
            # "dr_resistances"

        ]
        
class PsummarySerializer(DjongoModelSerializer):
   
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
        model = Psummary

        fields = '__all__'
        read_only_fields = ['owner']
        

class PsummaryMetadataSerializer(serializers.Serializer):

    main_lin = serializers.SerializerMethodField(
        "get_distinct_count_for_main_lin")
    sublin = serializers.SerializerMethodField("get_distinct_count_for_sublin")
    num_dr_variants = serializers.SerializerMethodField(
        "get_distinct_count_for_num_dr_variants")
    num_other_variants = serializers.SerializerMethodField(
        "get_distinct_count_for_num_other_variants")
    drtype = serializers.SerializerMethodField("get_distinct_count_for_drtype")

    class Meta:

        model = Psummary
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
                total=Count("main_lin")).order_by("total")
        )

    def get_distinct_count_for_sublin(self, psummary):
        return (
            psummary.values("sublin").annotate(
                total=Count("sublin")).order_by("total")
        )

    def get_distinct_count_for_num_dr_variants(self, psummary):
        return (
            psummary.values("num_dr_variants").annotate(
                total=Count("num_dr_variants")).order_by("total")
        )

    def get_distinct_count_for_num_other_variants(self, psummary):
        return (
            psummary.values("num_other_variants").annotate(
                total=Count("num_other_variants")).order_by("total")
        )

    def get_distinct_count_for_drtype(self, psummary):
        return (
            psummary.values("drtype").annotate(
                total=Count("drtype")).order_by("total")
        )
