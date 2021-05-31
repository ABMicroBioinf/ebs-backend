from rest_framework import serializers

from account.models import Account
#from seq.models import Study

class AccountSerializer(serializers.ModelSerializer):
    #studies = serializers.PrimaryKeyRelatedField(many=True, queryset=Study.objects.all())

    class Meta:
        model = Account
        fields = ('email', 'password', 'username', )
