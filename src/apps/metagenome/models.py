#from django.db.models.enums import Choices
from djongo import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from seq.models import SeqStat, Run

# Create your models here.
#from django import forms

class Classification(models.Model):
    tool_name = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=100, null=True)
    class Meta:
        abstract = True

class Analysis(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    input_sequences = models.ArrayReferenceField(
        to=Run
    )
    
    classify = models.EmbeddedField(
        model_container=Classification
    )
   
    def __str__(self):
        return self.name
