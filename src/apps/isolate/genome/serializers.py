from rest_framework import serializers
from .models import Genome, Annotation
from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer
from rest_framework.relations import PrimaryKeyRelatedField

class GenomeSerializer(DjongoModelSerializer):
    annotation = PrimaryKeyRelatedField(queryset=Annotation.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Genome

        fields = '__all__'
        read_only_fields = ['owner']

class AnnotationSerializer(DjongoModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Annotation

        fields = '__all__'
        read_only_fields = ['owner']