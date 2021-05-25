#from django.db.models.enums import Choices
from djongo import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from seq.models import SeqStat, Run

# Create your models here.
#from django import forms

class Assembly(models.Model):
    tool_name = models.CharField(max_length=100, null=True)
    contig_stats = models.EmbeddedField(
        model_container=SeqStat
    )
    class Meta:
        abstract = True

class Annotation(models.Model):
    tool_name = models.CharField(max_length=100, null=True)
    cds = models.IntegerField()
    rrna = models.IntegerField()
    trna = models.IntegerField()
    tmrna = models.IntegerField()
    quality = models.IntegerField()
    
    class Meta:
        abstract = True
    
class Allele(models.Model):
    gene = models.CharField(max_length=50)
    type = models.IntegerField()
    class Meta:
        abstract = True

class Mlst(models.Model):  
    tool_name = models.CharField(max_length=100, null=True)
    schema = models.CharField(max_length=100)
    sequenceType = models.IntegerField()
    alleles = models.ArrayField(
        model_container=Allele
    )
    quality = models.IntegerField(default=0)
   
    class Meta:
        abstract = True
    def __str__(self):
        return self.name
 
"""
FILE     SEQUENCE     START   END     STRAND GENE     COVERAGE     COVERAGE_MAP     GAPS  %COVERAGE  %IDENTITY  DATABASE  ACCESSION  PRODUCT        RESISTANCE
#6159.fna  NC_017338.1  39177   41186   +      mecA_15  1-2010/2010  ===============  0/0   100.00     100.000    ncbi      AB505628   n/a	     FUSIDIC_ACID
6159.fna  NC_017338.1  727191  728356  -      norA_1   1-1166/1167  ===============  0/0   99.91      92.367     ncbi      M97169     n/a            FOSFOMYCIN
6159.fna  NC_017339.1  10150   10995   +      blaZ_32  1-846/846    ===============  0/0   100.00     100.000    ncbi      AP004832   betalactamase  BETA-LACTAM;PENICILLIN
"""
class Feature(models.Model):
    tool_name = models.CharField(max_length=100, null=True)
    contigid = models.CharField(max_length=100)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=100)
    # AMR gene name
    gene = models.CharField(max_length=100)

    # What proportion of the gene is in our sequence
    coverage = models.CharField(max_length=100)

    # A visual represenation of the hit. ==aligned, .=unaligned, /=has_gaps
    coverage_map = models.CharField(max_length=100)

    # Openings / gaps in subject and query - possible psuedogene?
    gaps = models.CharField(max_length=100)

    # Proportion of gene covered
    percent_coverage = models.FloatField()

    # Proportion of exact nucleotide matches
    percent_identity = models.FloatField()

    # The database this sequence comes from
    database = models.CharField(max_length=100)

    # The genomic source of the sequence
    accession = models.CharField(max_length=100)

    # Gene product (if available)
    product = models.CharField(max_length=100)

    # putative antibiotic resistance phenotype, ;-separated
    resistance = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Analysis(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    input_sequences = models.ArrayReferenceField(
        to=Run
    )
    assembly = models.EmbeddedField(
        model_container=Assembly
    )
    annotation = models.EmbeddedField(
        model_container=Annotation
    )
    mlst = models.EmbeddedField(
        model_container=Mlst
    )
    resistome = models.ArrayField(
        model_container=Feature
    )
    virulome = models.ArrayField(
        model_container=Feature
    )
    def __str__(self):
        return self.title

class ComparisonAnalysis(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    input_sequences = models.ArrayReferenceField(
        to=Run
    )
    input_analyses = models.ArrayReferenceField(
        to=Analysis
    )
    
    def __str__(self):
        return self.title
