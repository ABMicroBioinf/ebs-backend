import factory
from factory.django import DjangoModelFactory
from factory import Faker
from seq.models import Study


class StudyFactory(DjangoModelFactory):
    title = Faker('text')
    description = Faker('text')
    
    class Meta:
        model = Study

