from re import S
from rest_framework import serializers
from rest_framework.fields import FileField, ReadOnlyField
from rest_framework.relations import PrimaryKeyRelatedField
from apps.account.models import Account
from .models import Study, Sample, Run, SeqFile, MetadataFile
from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer

class StudySerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Study

        fields = '__all__'
        read_only_fields = ['owner']

class RunSerializer(DjongoModelSerializer):
    study = PrimaryKeyRelatedField(queryset=Study.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Run
        
        fields = '__all__'
        read_only_fields = ['owner']

class SeqFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeqFile
        
        fields = (
            'id', 'raw_seq_file', 'qc_seq_file', 'run'
        )

class MetadataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataFile
        fields = (
            'id', 'metadata_file', 'run'
        )

class MyFileSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)