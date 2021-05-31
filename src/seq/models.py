#from django.db.models.enums import Choices
from djongo import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
# Create your models here.
#from django import forms
from account.models import Account

class Study(models.Model):
    id = models.BigAutoField(primary_key=True)
    #_id = models.ObjectIdField()
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=5000, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    #owner = models.ForeignKey(
        #settings.AUTH_USER_MODEL, related_name="studies", on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(
        Account, related_name="studies", on_delete=models.CASCADE, null=True)
  
    def __str__(self):
        return self.title

def pre_save_study_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.owner.username + "-" + instance.title)

pre_save.connect(pre_save_study_receiver, sender=Study)



class Sample(models.Model):
    title = models.CharField(max_length=100, unique=True)
    taxon_id = models.CharField(max_length=100, null=True, blank=True)
    scientific_name = models.CharField(max_length=100, null=True, blank=True)
    common_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = False

    def __str__(self):
        return self.title

"""
Library Layout: whether to expect SINGLE or PAIRED end reads.
Library Source: the type of source material that is being sequenced.
Library Strategy: the sequencing technique intended for the library.
Library Selection: the method used to select and/or enrich the material being sequenced.
"""
class Experiment(models.Model):

    strategies = (
        ('WGA', 'WGA'),
        ('WGS', 'WGS'),
        ('WXS', 'WXS'),
        ('RNA-Seq', 'RNA-Seq'),
        ('miRNA-Seq', 'miRNA-Seq'),
        ('WCS', 'WCS'),
        ('CLONE', 'CLONE'),
        ('POOLCLONE', 'POOLCLONE'),
        ('AMPLICON', 'AMPLICON'),
        ('CLONEEND', 'CLONEEND'),
        ('FINISHING', 'FINISHING'),
        ('ChIP-Seq', 'ChIP-Seq'),
        ('MNase-Seq', 'MNase-Seq'),
        ('DNase-Hypersensitivity', 'DNase-Hypersensitivity'),
        ('Bisulfite-Seq', 'Bisulfite-Seq'),
        ('Tn-Seq', 'Tn-Seq'),
        ('EST', 'EST'),
        ('FL-cDNA', 'FL-cDNA'),
        ('CTS', 'CTS'),
        ('MRE-Seq', 'MRE-Seq'),
        ('MeDIP-Seq', 'MeDIP-Seq'),
        ('MBD-Seq', 'MBD-Seq'),
        ('Synthetic-Long-Read', 'Synthetic-Long-Read'),
        ('ATAC-seq', 'ATAC-seq'),
        ('ChIA-PET', 'ChIA-PET'),
        ('FAIRE-seq', 'FAIRE-seq'),
        ('Hi-C', 'Hi-C'),
        ('ncRNA-Seq', 'ncRNA-Seq'),
        ('RAD-Seq', 'RAD-Seq'),
        ('RIP-Seq', 'RIP-Seq'),
        ('SELEX', 'SELEX'),
        ('ssRNA-seq', 'ssRNA-seq'),
        ('Targeted-Capture', 'Targeted-Capture'),
        ('Tethered Chromatin Conformation Capture', 'Tethered Chromatin Conformation Capture'),
        ('OTHER', 'OTHER'),
    )
    sources = (
        ('GENOMIC', 'GENOMIC'),
        ('TRANSCRIPTOMIC', 'TRANSCRIPTOMIC'),
        ('METAGENOMIC', 'METAGENOMIC'),
        ('METATRANSCRIPTOMIC', 'METATRANSCRIPTOMIC'),
        ('SYNTHETIC', 'SYNTHETIC'),
        ('VIRAL RNA', 'VIRAL RNA'),
        ('GENOMIC SINGLE CELL', 'GENOMIC SINGLE CELL'),
        ('TRANSCRIPTOMIC SINGLE CELL', 'TRANSCRIPTOMIC SINGLE CELL'),
        ('OTHER', 'OTHER'),
    )
    platforms = (
        ('_LS454', '_LS454'),
        ('ABI_SOLID', 'ABI_SOLID'),
        ('BGISEQ', 'BGISEQ'),
        ('CAPILLARY', 'CAPILLARY'),
        ('COMPLETE_GENOMICS', 'COMPLETE_GENOMICS'),
        ('HELICOS', 'HELICOS'),
        ('ILLUMINA', 'ILLUMINA'),
        ('ION_TORRENT', 'ION_TORRENT'),
        ('OXFORD_NANOPORE', 'OXFORD_NANOPORE'),
        ('PACBIO_SMRT', 'PACBIO_SMRT'),

    )
    selections = (
        ('RANDOM', 'RANDOM'),
        ('PCR', 'PCR'),
        ('RANDOM PCR', 'RANDOM PCR'),
        ('RT-PCR', 'RT-PCR'),
        ('HMPR', 'HMPR'),
        ('MF', 'MF'),
        ('CF-S', 'CF-S'),
        ('CF-M', 'CF-M'),
        ('CF-H', 'CF-H'),
        ('CF-T', 'CF-T'),
        ('MDA', 'MDA'),
        ('MSLL', 'MSLL'),
        ('cDNA', 'cDNA'),
        ('ChIP', 'ChIP'),
        ('MNase', 'MNase'),
        ('DNAse', 'DNAse'),
        ('Hybrid Selection', 'Hybrid Selection'),
        ('Reduced Representation', 'Reduced Representation'),
        ('Restriction Digest', 'Restriction Digest'),
        ('5-methylcytidine antibody', '5-methylcytidine antibody'),
        ('MBD2 protein methyl-CpG binding domain', 'MBD2 protein methyl-CpG binding domain'),
        ('CAGE', 'CAGE'),
        ('RACE', 'RACE'),
        ('size fractionation', 'size fractionation'),
        ('Padlock probes capture method', 'Padlock probes capture method'),
        ('other', 'other'),
        ('unspecified', 'unspecified'),
        ('cDNA_oligo_dT', 'cDNA_oligo_dT'),
        ('cDNA_randomPriming', 'cDNA_randomPriming'),
        ('Inverse rRNA', 'Inverse rRNA'),
        ('Oligo-dT', 'Oligo-dT'),
        ('PolyA', 'PolyA'),
        ('repeat fractionation', 'repeat fractionation'),
    )
    layouts = (
        ('PAIRED', 'PAIRED'),
        ('SINGLE', 'SINGLE')
    )

    title = models.CharField(max_length=100, unique=True)
    library_name = models.CharField(max_length=100, null=True, blank=True)
    platform = models.CharField(max_length=100, choices=platforms, null=True, blank=True) #illumina MiSeq
    instrument_model = models.CharField(max_length=100, null=True, blank=True)
    library_strategy = models.CharField(max_length=100, choices=strategies, null=True, blank=True) # WGS
    library_source = models.CharField(max_length=100, choices=sources, null=True, blank=True) # metagenomics
    library_layout = models.CharField(max_length=100, choices=layouts, null=True, blank=True) # paired
    library_selection = models.CharField(max_length=100, choices=selections, null=True, blank=True) #random
    description = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        abstract = False
    def __str__(self):
        return self.title

class SeqStat(models.Model):
    count = models.IntegerField(null=True, blank=True)
    bp = models.IntegerField(null=True, blank=True)
    ns = models.IntegerField(null=True, blank=True)
    gaps = models.IntegerField(null=True, blank=True)
    minLen = models.IntegerField(null=True, blank=True)
    avgLen = models.FloatField(null=True, blank=True)
    maxLen = models.IntegerField(null=True, blank=True)
    n50 = models.IntegerField(null=True, blank=True)
    class Meta:
        abstract = True

import os

def raw_dir(instance, filename):
    return os.path.join(str(instance.run.study.id), str(instance.run.id), 'seqFiles', 'raw', filename)
 
def qc_dir(instance, filename):
    return os.path.join(str(instance.run.study.id), str(instance.run.id), 'seqFiles', 'qc', filename)
 

class MyRawSeqFile(models.Model):
    id = models.AutoField(primary_key=True)
    raw_seq_file = models.FileField(upload_to=raw_dir, blank=False)
    raw_stats = models.EmbeddedField(
        model_container=SeqStat
    )
    

class Run(models.Model):
    id = models.BigAutoField(primary_key=True)
    run_name = models.CharField(max_length=100, unique=True)
    study = models.ForeignKey(
        Study, related_name="runs", on_delete=models.CASCADE)
    sample = models.EmbeddedField(
        model_container=Sample
    )
    
    experiment = models.EmbeddedField(
        model_container=Experiment
    )
    """raw_seq = models.ArrayField(
        model_container=MyRawSeqFile
    )
    
    raw_stats = models.EmbeddedField(
        model_container=SeqStat
    )
    qc_stats = models.EmbeddedField(
        model_container=SeqStat
    ) """
    
    objects = models.DjongoManager()
    
    def __str__(self):
        return self.run_name



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
    
