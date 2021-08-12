from rest_framework import serializers
from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer
from gizmos.mixins import FlattenMixin
from .models import Genome, Annotation, Mlst, Virulome, Resistome

class GenomeSerializer(DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Genome
        fields = '__all__'
        read_only_fields = ['owner']
        
class VirulomeSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Virulome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "virulome"
        ]



class ResistomeSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Resistome
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "resistome"
        ]

class MlstSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Mlst
        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "alleles"
        ]

class AnnotationSerializer(FlattenMixin, DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Annotation

        fields = '__all__'
        read_only_fields = ['owner']
        flatten = [
            "gff"
        ]