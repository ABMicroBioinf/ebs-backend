from djongo import models
from django.conf import settings
from django.utils.text import slugify
from apps.account.models import Account
from .common import *

# Create your models here.
class Study(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True, null=False, blank=False)
    data_type = models.CharField(max_length=100, null=False, blank=False)
    abstract = models.TextField(max_length=5000, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    date_created = models.DateTimeField(
        verbose_name='date created', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='last update', auto_now=True)
    owner = models.ForeignKey(
        Account, related_name="studies", on_delete=models.CASCADE, null=True)
  
    def __str__(self):
        return str(self.title)

class Sample(models.Model):
    sampleName = models.CharField(max_length=100)
    organism = models.CharField(max_length=100, null=True, blank=True)
    strain = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        abstract = True
    def __str__(self):
        return str(self.sampleName)


class Experiment(models.Model):
    libraryName = models.CharField(max_length=100)
    platform = models.CharField(max_length=100, choices=seq_exp_platforms, null=True, blank=True) #illumina MiSeq
    instrument = models.CharField(max_length=100, null=True, blank=True)
    library_strategy = models.CharField(max_length=100, choices=seq_exp_strategies, null=True, blank=True) # WGS
    librarySource = models.CharField(max_length=100, choices=seq_exp_sources, null=True, blank=True) # metagenomics
    libraryLayout = models.CharField(max_length=100, choices=seq_exp_layouts, null=True, blank=True) # paired
    librarySelection = models.CharField(max_length=100, choices=seq_exp_selections, null=True, blank=True) #random
    description = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        abstract = True
    def __str__(self):
        return str(self.libraryName)

class SeqStat(models.Model):
    reads = models.IntegerField(null=True, blank=True)
    total_bp = models.IntegerField(null=True, blank=True)
    minLen = models.IntegerField(null=True, blank=True)
    avgLen = models.FloatField(null=True, blank=True)
    maxLen = models.IntegerField(null=True, blank=True)
    avgQual = models.FloatField(null=True, blank=True)
    errQual = models.FloatField(null=True, blank=True)
    geecee = models.FloatField(null=True, blank=True)
    ambiguous = models.FloatField(null=True, blank=True)
    class Meta:
        abstract = True

class Run(models.Model):
    id = models.BigAutoField(primary_key=True)
    run_name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    study = models.ForeignKey(
        Study, related_name="runs", on_delete=models.CASCADE)
    sample = models.EmbeddedField(
        model_container=Sample
    )
    
    experiment = models.EmbeddedField(
        model_container=Experiment
    )
    
    stats_raw = models.EmbeddedField(
        model_container=SeqStat,
        null=True
        
    )
    stats_qc = models.EmbeddedField(
        model_container=SeqStat,
        null=True
    )

    date_created = models.DateTimeField(
        verbose_name='date created', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='last update', auto_now=True)
    owner = models.ForeignKey(
        Account, related_name="runs", on_delete=models.CASCADE, null=True)

    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.run_name)

import os

def raw_dir(instance, filename):
    return os.path.join(str(instance.run.study.id), str(instance.run.id), 'seqFiles', 'raw', filename)
 
def qc_dir(instance, filename):
    return os.path.join(str(instance.run.study.id), str(instance.run.id), 'seqFiles', 'qc', filename)
 

class SeqFile(models.Model):
    id = models.AutoField(primary_key=True)
    raw_seq_file = models.FileField(upload_to=raw_dir, blank=False)
    qc_seq_file = models.FileField(upload_to=qc_dir)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    
def metadata_dir(instance, filename):
    return os.path.join(str(instance.run.study.id), str(instance.run.id), 'metadata', filename)

class MetadataFile(models.Model):
    id = models.AutoField(primary_key=True)
    metadata_file = models.FileField(upload_to=metadata_dir, blank=False)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
