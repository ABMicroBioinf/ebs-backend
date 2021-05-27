import factory
from factory.django import DjangoModelFactory
from factory import Faker
from sandbox.models import Company


class CompanyFactory(DjangoModelFactory):
    name = Faker('company')
    description = Faker('text')
    website = Faker('url')
    street_line_1 = Faker('street_address')
    city = Faker('city')
    state = Faker('state_abbr')
    zipcode = Faker('zipcode')

    class Meta:
        model = Company


from django.contrib.auth.hashers import make_password
#from django.contrib.auth.models import User
from account.models import Account

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    username = 'bob'
    email = 'bob@example.com'
    