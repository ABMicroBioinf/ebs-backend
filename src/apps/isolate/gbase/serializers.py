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

class AssemblySerializer(DjongoModelSerializer):

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
        model = Assembly
        fields = '__all__'
        #fields = [field.name for field in Assembly._meta.fields] + ['sequences', 'sequences1']
        #fields = [field.name for field in Assembly._meta.fields] + ['annotations']
        #fields.append("sequences1")
        read_only_fields = ['owner']

class MlstSerializer(FlattenMixin, DjongoModelSerializer):
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
        model = Mlst
        fields = '__all__'
        
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]


class ResistomeSerializer(FlattenMixin, DjongoModelSerializer):
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
        model = Resistome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]


class VirulomeSerializer(ResistomeSerializer):
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
        model = Virulome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]
       
class AnnotationSerializer(FlattenMixin, DjongoModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')
    project__id = serializers.CharField(source='assembly.sequence.project.id')
    project__title = serializers.CharField(source='assembly.sequence.project.title')
    sequence__id = serializers.CharField(source='assembly.sequence.LibrarySource')
    sequence__LibrarySource = serializers.CharField(source='assembly.sequence.LibrarySource')
    sequence__LibraryLayout = serializers.CharField(source='assembly.sequence.LibraryLayout')
    sequence_SequencerModel = serializers.CharField(source='assembly.sequence.SequencerModel')
    sequence__CenterName = serializers.CharField(source='assembly.sequence.CenterName')
    #genome = GenomeSerializer()
    class Meta:
        model = Annotation
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "attr"
        ]

