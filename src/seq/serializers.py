from re import S
from rest_framework import serializers
from rest_framework.fields import FileField, ReadOnlyField
from rest_framework.relations import PrimaryKeyRelatedField
from account.models import Account
from .models import Study, Sample, Run, SeqFile, MetadataFile

from account.serializers import AccountSerializer

class StudySerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Study
        fields = '__all__'
        read_only_fields = ('owner', 'slug')


from rest_meets_djongo.serializers import DjongoModelSerializer
class RunSerializer(DjongoModelSerializer):   
    study = PrimaryKeyRelatedField(queryset=Study.objects.all())
    class Meta:
        model = Run
        fields = (
            'id', 'run_name', 'study', 'sample', 'experiment', 'stats_raw', 'stats_qc'
        )
        

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
