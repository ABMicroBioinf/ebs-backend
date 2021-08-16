#from django.db.models.enums import Choices
from djongo import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from apps.account.models import Account


isMigrate = True       #added this line


# Create your models here.
#from django import forms
class Pipeline(models.Model):
    assembler = models.CharField(max_length=100)
    variant_caller = models.CharField(max_length=100)

    class Meta:
        abstract = isMigrate

class GeneCoverage(models.Model):
    gene = models.CharField(max_length=100)
    pct_coverage = models.FloatField()
    class Meta:
        abstract = isMigrate

class Virulome(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    seqtype = models.CharField(max_length=100)
    num_found = models.IntegerField()
    virulome = models.ArrayField(
        model_container = GeneCoverage
    )
    
    owner = models.ForeignKey(
        Account, related_name="virulomes", on_delete=models.CASCADE)
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)

    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)

    Description = models.TextField()

    objects = models.DjongoManager()

    class Meta:
        pass
        # ordering = ['id', 'seqtype', 'num_found', 'gene', 'owner__uername', 'DateCreated', 'LastUpdate']
    
    def __str__(self):
        return str(self.id)

class Resistome(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    seqtype = models.CharField(max_length=100)
    num_found = models.IntegerField()
    resistome = models.ArrayField(
        model_container = GeneCoverage
    )
    owner = models.ForeignKey(
        Account, related_name="resistomes", on_delete=models.CASCADE)
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    Description = models.TextField()

    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)


class Allele(models.Model):
    allele = models.CharField(max_length=100)
    num = models.CharField(max_length=10)
    class Meta:
        abstract = isMigrate
    
class Mlst(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    seqtype = models.CharField(max_length=100)
    scheme = models.CharField(max_length=100)
    st = models.IntegerField()
    alleles = models.ArrayField(
        model_container = Allele
    )
    owner = models.ForeignKey(
        Account, related_name="mlsts", on_delete=models.CASCADE)
    
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    
    Description = models.TextField()

    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)


class Genome(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    seqtype = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField()
    bp = models.IntegerField()
    Ns = models.IntegerField()
    gaps = models.IntegerField()
    min = models.IntegerField()
    max = models.IntegerField()
    avg = models.IntegerField()
    N50 = models.IntegerField()

    owner = models.ForeignKey(
        Account, related_name="genomes", on_delete=models.CASCADE)
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    
    Description = models.TextField()
     
    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)


    
class GffAttr(models.Model):
    tag = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    class Meta:
        abstract = isMigrate
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
        abstract = isMigrate

class Annotation(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    seqtype = models.CharField(max_length=100)
    owner = models.ForeignKey(
        Account, related_name="ganalyses", on_delete=models.CASCADE, null=True)

    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    
    Description = models.TextField()

    gff = models.ArrayField(
        model_container = Gff
    )
    
    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)
