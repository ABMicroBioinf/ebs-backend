#from django.db.models.enums import Choices
from djongo import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from apps.account.models import Account

# Create your models here.
#from django import forms
class Pipeline(models.Model):
    assembler = models.CharField(max_length=100)
    variant_caller = models.CharField(max_length=100)

    class Meta:
        abstract = True

class SeqStat(models.Model):
    count = models.IntegerField()
    bp = models.IntegerField()
    Ns = models.IntegerField()
    gaps = models.IntegerField()
    min = models.IntegerField()
    max = models.IntegerField()
    avg = models.IntegerField()

    N50 = models.IntegerField()

    class Meta:
        abstract = True


""" class AnnotSummary(models.Model):
    cds = models.IntegerField()
    rrna = models.IntegerField()
    trna = models.IntegerField()
    tmrna = models.IntegerField()

    class Meta:
        abstract = True """

class GffAttr(models.Model):
    tag = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    class Meta:
        abstract = True
class Gff(models.Model):
    seqName = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    feature = models.CharField(max_length=100)
    start = models.IntegerField()
    end = models.IntegerField()
    score = models.CharField(max_length=100)
    strand = models.CharField(max_length=1)
    frame = models.CharField(max_length=100)
    attribute = models.ArrayField( 
        model_container = GffAttr
    )

    class Meta:
        abstract = True

class Annotation(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    owner = models.ForeignKey(
        Account, related_name="ganalyses", on_delete=models.CASCADE, null=True)
    gff = models.ArrayField(
        model_container = Gff
    )

class Virulome(models.Model):
    sequence = models.CharField(max_length=100)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    gene = models.CharField(max_length=100)
    coverage = models.CharField(max_length=100)
    coverage_map = models.CharField(max_length=100)
    gaps = models.CharField(max_length=20)
    database = models.CharField(max_length=50)
    accession = models.CharField(max_length=50)
    product = models.CharField(max_length=100)
    resistance = models.CharField(max_length=100)
    pct_coverage = models.FloatField()
    pct_identity = models.FloatField()

    class Meta:
        abstract = True

class AMR(models.Model):
    sequence = models.CharField(max_length=100)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    gene = models.CharField(max_length=100)
    coverage = models.CharField(max_length=100)
    coverage_map = models.CharField(max_length=100)
    db = models.CharField(max_length=100)
    gaps = models.CharField(max_length=20)
    database = models.CharField(max_length=50)
    accession = models.CharField(max_length=50)
    product = models.CharField(max_length=100)
    resistance = models.CharField(max_length=100)
    pct_coverage = models.FloatField()
    pct_identity = models.FloatField()
    
    class Meta:
        abstract = True


class Genome(models.Model):
    name = models.CharField(max_length=100)
    annotation = models.ForeignKey(
        Annotation, related_name="genomes", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        Account, related_name="genomes", on_delete=models.CASCADE)

    assembly_stats = models.EmbeddedField(
        model_container=SeqStat
    )
    virulome = models.ArrayField(
        model_container = Virulome
    )
    amr = models.ArrayField(
        model_container = AMR
    )

    def __str__(self):
        return str(self.name)
    

    

