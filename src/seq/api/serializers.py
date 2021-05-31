from re import S
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework.relations import PrimaryKeyRelatedField
from account.models import Account
from seq.models import Study, Sample, Run, SeqFile, MetadataFile

from account.api.serializers import AccountSerializer

class StudySerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Study
        fields = (
            'id', 'title', 'description', 'slug', 'owner'
        )
        read_only_fields = ('owner', 'slug')


from rest_meets_djongo.serializers import DjongoModelSerializer
#class RunSerializer(serializers.ModelSerializer):
class RunSerializer(DjongoModelSerializer):   
    study = PrimaryKeyRelatedField(queryset=Study.objects.all())
    #sample = serializers.SerializerMethodField()
    #sample = SampleSerializer()
    class Meta:
        model = Run
        fields = (
            'id', 'run_name', 'study', 'sample', 'experiment'
        )
        
    """ def get_sample(self, obj):
        return_data = None
        if type(obj.sample) == list:
            embedded_list = []
            for item in obj.sample:
                embedded_dict = item.__dict__
                for key in list(embedded_dict.keys()):
                    if key.startswith('_'):
                        embedded_dict.pop(key)
                embedded_list.append(embedded_dict)
            return_data = embedded_list
        else:
            embedded_dict = obj.sample
            for key in list(embedded_dict.keys()):
                if key.startswith('_'):
                    embedded_dict.pop(key)
            return_data = embedded_dict
        return return_data """
    

class SeqFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeqFile
        fields = (
            'id', 'raw_seq_file', 'qc_seq_file', 'run_id'
        )

class MetadataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetadataFile
        fields = (
            'id', 'metadata_file', 'run_id'
        )
