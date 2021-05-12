from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(
    #     style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = '__all__'
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    # def save(self):
    #     account = Account(
    #         # email = self.validate_data['email'],
    #         # username = self.validate_data['username'],
    #         # password = self.validate_data['password']
    #     )
    #     # password = self.validate_data['password'],
    #     # password2 = self.validated_data['password2']

    #     # if password != password2:
    #     #     raise serializers.ValidationError({'password': 'Passwords must match.'})
    #     # account.set_password(password)
    #     account.save()
    #     return account