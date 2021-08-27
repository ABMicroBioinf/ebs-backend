from rest_framework import serializers
from .models import Profile, Psummary
from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer
from gizmos.mixins import FlattenMixin

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