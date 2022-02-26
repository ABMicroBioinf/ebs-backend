from djongo import models
from django.conf import settings
from django.utils.text import slugify
from apps.account.models import Account
#from apps.isolate.gbase.models import Assembly
from .common import *
#from apps.common.models import SeqStat


class Project(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(
        Account, related_name="projects", on_delete=models.CASCADE, null=True)
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(verbose_name='last update', auto_now=True)
    
        
    def __str__(self):
        return str(self.id)

class Seqstat(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    r_Reads = models.IntegerField(null=True, blank=True)
    r_Yield = models.IntegerField(null=True, blank=True)
    r_GeeCee = models.FloatField(null=True, blank=True)
    r_MinLen = models.IntegerField(null=True, blank=True)
    r_AvgLen = models.IntegerField(null=True, blank=True)
    r_MaxLen = models.IntegerField(null=True, blank=True)
    r_AvgQual = models.FloatField(null=True, blank=True)
    r_ErrQual = models.FloatField(null=True, blank=True)
    r_Ambiguous = models.FloatField(null=True, blank=True)
    
    q_Reads = models.IntegerField(null=True, blank=True)
    q_Yield = models.IntegerField(null=True, blank=True)
    q_GeeCee = models.FloatField(null=True, blank=True)
    q_MinLen = models.IntegerField(null=True, blank=True)
    q_AvgLen = models.IntegerField(null=True, blank=True)
    q_MaxLen = models.IntegerField(null=True, blank=True)
    q_AvgQual = models.FloatField(null=True, blank=True)
    q_ErrQual = models.FloatField(null=True, blank=True)
    q_Ambiguous = models.FloatField(null=True, blank=True)
    
    owner = models.ForeignKey(
        Account, related_name="seqstats", on_delete=models.CASCADE, null=True)
    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)
    
class Sequence(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    project = models.ForeignKey(
        Project, related_name="sequences", on_delete=models.CASCADE, null=True)
    seqstat = models.OneToOneField(
        Seqstat,
        on_delete=models.CASCADE,
       
    )
   
    TaxID = models.IntegerField()
    seqtype = models.CharField(max_length=100, choices=seqtypes, null=True, blank=True) # WGS
    ScientificName = models.CharField(max_length=100)
    Experiment = models.CharField(max_length=100)
    LibraryName = models.CharField(max_length=100)
    LibraryStrategy = models.CharField(max_length=100, choices=seq_exp_strategies, null=True, blank=True) # WGS
    LibrarySelection = models.CharField(max_length=100, choices=seq_exp_selections, null=True, blank=True) #random
    LibrarySource = models.CharField(max_length=100, choices=seq_exp_sources, null=True, blank=True) # metagenomics
    LibraryLayout = models.CharField(max_length=100, choices=seq_exp_layouts, null=True, blank=True) # paired
    # InsertSize = models.IntegerField()
    # InsertDev = models.FloatField()
    Platform = models.CharField(max_length=100, choices=seq_exp_platforms, null=True, blank=True) #illumina MiSeq
    SequencerModel = models.CharField(max_length=100, null=True, blank=True)
    
    SampleName = models.CharField(max_length=100)
    CenterName = models.CharField(max_length=100)
    
    taxName_1 = models.CharField(max_length=100, null=True, blank=True)
    taxFrac_1 = models.FloatField(null=True, blank=True)
    taxName_2 = models.CharField(max_length=100, null=True, blank=True)
    taxFrac_2 = models.FloatField(null=True, blank=True)
    taxName_3 = models.CharField(max_length=100, null=True, blank=True)
    taxFrac_3 = models.FloatField(null=True, blank=True)
    taxName_4 = models.CharField(max_length=100, null=True, blank=True)
    taxFrac_4 = models.FloatField(null=True, blank=True)
    

    owner = models.ForeignKey(
        Account, related_name="sequences", on_delete=models.CASCADE, null=True)

    """  RawStats = models.EmbeddedField(
        model_container=SeqStat,
        null=True,
        blank= True     
    )
    QcStats = models.EmbeddedField(
        model_container=SeqStat,    
        null=True,
        blank= True
    ) """
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(verbose_name='last update', auto_now=True)

    Description = models.TextField(null=True, blank=True)

    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)


import os

def raw_dir(instance, filename):
    return os.path.join(str(instance.sequence.Projectid), str(instance.sequence.id), 'seqFiles', 'raw', filename)
 
def qc_dir(instance, filename):
    return os.path.join(str(instance.sequence.Projectid), str(instance.sequence.id), 'seqFiles', 'qc', filename)
 

class SeqFile(models.Model):
    id = models.AutoField(primary_key=True)
    raw_seq_file = models.FileField(upload_to=raw_dir, blank=False)
    qc_seq_file = models.FileField(upload_to=qc_dir)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    
def metadata_dir(instance, filename):
    return os.path.join(str(instance.sequence.Projectid), str(instance.sequence.id), 'metadata', filename)

class MetadataFile(models.Model):
    id = models.AutoField(primary_key=True)
    metadata_file = models.FileField(upload_to=metadata_dir, blank=False)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
