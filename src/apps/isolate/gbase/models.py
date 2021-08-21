#from django.db.models.enums import Choices
from djongo import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from apps.account.models import Account
from apps.seq.models import Sequence


isMigrate = True       #added this line


# Create your models here.
#from django import forms
class Pipeline(models.Model):
    assembler = models.CharField(max_length=100)
    variant_caller = models.CharField(max_length=100)

    class Meta:
        abstract = isMigrate

class Allele(models.Model):
    locus = models.CharField(max_length=50)
    allele = models.CharField(max_length=10)
    class Meta:
        abstract = isMigrate

class Mlst(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    sequence = models.OneToOneField(Sequence, on_delete=models.CASCADE)
    #sequence = models.OneToOneField(Sequence, on_delete=models.CASCADE)
    seqtype = models.CharField(max_length=100)
    scheme = models.CharField(max_length=100)
    st = models.IntegerField(null=True, blank=True)
    profile = models.ArrayField(
        model_container = Allele,       
    )
    owner = models.ForeignKey(
        Account, related_name="mlsts", on_delete=models.CASCADE)
    """ sequence = models.ForeignKey(
        Sequence, related_name="mlsts", on_delete=models.CASCADE) """
    
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    
    Description = models.TextField()
    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)



class Gene(models.Model):
    geneName = models.CharField(max_length=100)
    pctCoverage = models.FloatField()

    class Meta:
        abstract = isMigrate

class Resistance(Gene):
    pass

    class Meta:
        abstract = isMigrate

class Virulence(Gene):
    pass

    class Meta:
        abstract = isMigrate

class Resistome(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    sequence = models.OneToOneField(Sequence, on_delete=models.CASCADE)
    seqtype = models.CharField(max_length=100)
    num_found = models.IntegerField()
    profile = models.ArrayField(
        model_container = Resistance
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


class Virulome(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    sequence = models.OneToOneField(Sequence, on_delete=models.CASCADE)
    seqtype = models.CharField(max_length=100)
    num_found = models.IntegerField()
    profile = models.ArrayField(
        model_container = Virulence
    )
    owner = models.ForeignKey(
        Account, related_name="virulomes", on_delete=models.CASCADE)
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
    sequence = models.OneToOneField(Sequence, on_delete=models.CASCADE)
    seqtype = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    bp = models.IntegerField(null=True, blank=True)
    Ns = models.IntegerField(null=True, blank=True)
    gaps = models.IntegerField(null=True, blank=True)
    min = models.IntegerField(null=True, blank=True)
    max = models.IntegerField(null=True, blank=True)
    avg = models.IntegerField(null=True, blank=True)
    N50 = models.IntegerField(null=True, blank=True)

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

class TagValue(models.Model):
    tag = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        abstract = isMigrate


class Annotation(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    seqid = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    ftype = models.CharField(max_length=100)
    start = models.IntegerField()
    end = models.IntegerField()
    score = models.CharField(max_length=100)
    strand = models.CharField(max_length=1)
    phase = models.CharField(max_length=100)
    attr = models.ArrayField(
        model_container = TagValue
    )
    seqtype = models.CharField(max_length=100)
    sequence = models.OneToOneField(Sequence, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        Account, related_name="annotations", on_delete=models.CASCADE, null=True)
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    Description = models.TextField()

    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)

