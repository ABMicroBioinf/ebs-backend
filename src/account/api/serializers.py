from rest_framework import serializers

from account.models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    '''
        context = {}
        if request.POST:
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        form.save()
                        email = form.cleaned_data.get('email')
                        raw_password = form.cleaned_data.get('password1')
                        account = authenticate(email=email, password=raw_password)
                        login(request, account)
                        return redirect('home')
                else:
                        context['registration_form'] = form

        else:
                form = RegistrationForm()
                context['registration_form'] = form
        return render(request, 'account/register.html', context
    '''

    # password2 = serializers.CharField(
    #     style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = '__all__'
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def save(self):
        account = Account(
            email=self.validate_data['email'],
            username=self.validate_data['username']
        )
        password = self.validate_data['password'],
        # password2 = self.validated_data['password2']

        # if password != password2:
        #     raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.ModelSerializer):
    '''
        context = {}

        user = request.user
        if user.is_authenticated: 
            return redirect("home")

        if request.POST:
            form = AccountAuthenticationForm(request.POST)
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(email=email, password=password)

                if user:
                    login(request, user)
                    return redirect("home")

        else:
            form = AccountAuthenticationForm()

        context['login_form'] = form

        # print(form)
        return render(request, "account/login.html", context)
    '''

    class Meta:
        model = Account
        fields = '__all__'

    def save(self):
        pass
