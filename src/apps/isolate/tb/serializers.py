from rest_framework import serializers
from .models import Profile
from rest_meets_djongo.serializers import DjongoModelSerializer
from apps.account.serializers import AccountSerializer

#class ProfileSerializer(serializers.ModelSerializer):
class ProfileSerializer(DjongoModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Profile

        fields = '__all__'
        read_only_fields = ['owner']