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
    
    owner = serializers.ReadOnlyField(source='owner.username')
    project_id = serializers.CharField(source='sequence.project.id')
    project_title = serializers.CharField(source='sequence.project.title')
    sequence_LibrarySource = serializers.CharField(source='sequence.LibrarySource')
    sequence_LibraryLayout = serializers.CharField(source='sequence.LibraryLayout')
    sequence_SequencerModel = serializers.CharField(source='sequence.SequencerModel')

    class Meta:
        model = Assembly
        fields = '__all__'
        read_only_fields = ['owner']

class MlstSerializer(FlattenMixin, DjongoModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')
    project_id = serializers.CharField(source='sequence.project.id')
    project_title = serializers.CharField(source='sequence.project.title')
    sequence_LibrarySource = serializers.CharField(source='sequence.LibrarySource')
    sequence_LibraryLayout = serializers.CharField(source='sequence.LibraryLayout')
    sequence_SequencerModel = serializers.CharField(source='sequence.SequencerModel')
    #genome = GenomeSerializer()
    class Meta:
        model = Mlst
        fields = '__all__'
        
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]


class ResistomeSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    project_id = serializers.CharField(source='sequence.project.id')
    project_title = serializers.CharField(source='sequence.project.title')
    sequence_LibrarySource = serializers.CharField(source='sequence.LibrarySource')
    sequence_LibraryLayout = serializers.CharField(source='sequence.LibraryLayout')
    sequence_SequencerModel = serializers.CharField(source='sequence.SequencerModel')
    #genome = GenomeSerializer()
    class Meta:
        model = Resistome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]


class VirulomeSerializer(ResistomeSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    project_id = serializers.CharField(source='sequence.project.id')
    project_title = serializers.CharField(source='sequence.project.title')
    sequence_LibrarySource = serializers.CharField(source='sequence.LibrarySource')
    sequence_LibraryLayout = serializers.CharField(source='sequence.LibraryLayout')
    sequence_SequencerModel = serializers.CharField(source='sequence.SequencerModel')
    #genome = GenomeSerializer()
    class Meta:
        model = Virulome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]
       
class AnnotationSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    project_id = serializers.CharField(source='sequence.project.id')
    project_title = serializers.CharField(source='sequence.project.title')
    sequence_LibrarySource = serializers.CharField(source='sequence.LibrarySource')
    sequence_LibraryLayout = serializers.CharField(source='sequence.LibraryLayout')
    sequence_SequencerModel = serializers.CharField(source='sequence.SequencerModel')
    #genome = GenomeSerializer()
    class Meta:
        model = Annotation
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "attr"
        ]

