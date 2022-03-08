from rest_framework import serializers
from .models import Account
from gizmos.util import ObjectIdField

class AccountSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
     
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

    class Meta:
        model = Account
        fields = ('email', 'username', 'password', '_id', 'projects', 'biosamples')
        extra_kwargs = {
            'password': {'write_only': True}
        }

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print("xiaoli login..................................................................token")
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
