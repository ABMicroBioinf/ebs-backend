from rest_framework import serializers
from .models import Profile, Psummary
from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer
from gizmos.mixins import FlattenMixin

class ProfileSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    project_id = serializers.CharField(source='sequence.project.id')
    project_title = serializers.CharField(source='sequence.project.title')
    sequence_LibrarySource = serializers.CharField(source='sequence.LibrarySource')
    sequence_LibraryLayout = serializers.CharField(source='sequence.LibraryLayout')
    sequence_SequencerModel = serializers.CharField(source='sequence.SequencerModel')

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
    owner = serializers.ReadOnlyField(source='owner.username')
    project_id = serializers.CharField(source='sequence.project.id')
    project_title = serializers.CharField(source='sequence.project.title')
    sequence_LibrarySource = serializers.CharField(source='sequence.LibrarySource')
    sequence_LibraryLayout = serializers.CharField(source='sequence.LibraryLayout')
    sequence_SequencerModel = serializers.CharField(source='sequence.SequencerModel')

    class Meta:
        model = Psummary

        fields = '__all__'
        read_only_fields = ['owner']