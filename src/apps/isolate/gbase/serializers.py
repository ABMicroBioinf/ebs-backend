from rest_framework import serializers
from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer
from apps.seq.serializers import SequenceSerializer
from gizmos.mixins import FlattenMixin
from .models import (
    Genome, 
    Annotation, 
    Mlst, 
    Virulome, 
    Resistome
)


class MlstSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    Projectid = serializers.CharField(source='sequence.Projectid')
    class Meta:
        model = Mlst
        fields = '__all__'
        
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]


class ResistomeSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    Projectid = serializers.CharField(source='sequence.Projectid')
    class Meta:
        model = Resistome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]


class VirulomeSerializer(ResistomeSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    Projectid = serializers.CharField(source='sequence.Projectid')
    class Meta:
        model = Virulome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "profile"
        ]
       
class AnnotationSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    Projectid = serializers.CharField(source='sequence.Projectid')
    class Meta:
        model = Annotation
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "attr"
        ]


class GenomeSerializer(DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    Projectid = serializers.CharField(source='sequence.Projectid')
    class Meta:
        model = Genome
        fields = '__all__'
        read_only_fields = ['owner']
