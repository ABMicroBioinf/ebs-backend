from django.db import models

# Create your models here.
class SeqStat(models.Model):
   # id = models.CharField(primary_key=True, max_length=100)
    Reads = models.IntegerField(null=True, blank=True)
    Yield = models.IntegerField(null=True, blank=True)
    GeeCee = models.FloatField(null=True, blank=True)
    MinLen = models.IntegerField(null=True, blank=True)
    AvgLen = models.IntegerField(null=True, blank=True)
    MaxLen = models.IntegerField(null=True, blank=True)
    AvgQual = models.FloatField(null=True, blank=True)
    ErrQual = models.FloatField(null=True, blank=True)
    Ambiguous = models.FloatField(null=True, blank=True)
    
    class Meta:
        abstract = True
        
    def __getitem__(self, name):
        return getattr(self, name)
    
class Pipeline(models.Model):
    assembler = models.CharField(max_length=100)
    variant_caller = models.CharField(max_length=100)

    class Meta:
        abstract = True
        

class Allele(models.Model):
    locus = models.CharField(max_length=50)
    alleleId = models.IntegerField()
    class Meta:
        abstract = True

class Gene(models.Model):
    geneName = models.CharField(max_length=100)
    pctCoverage = models.FloatField()

    class Meta:
        abstract = True

class Amr(models.Model):
    geneName = models.CharField(max_length=25)
    sequenceName = models.CharField(max_length=100)
    scope = models.CharField(max_length=10)
    elementType = models.CharField(max_length=15)
    dclass = models.CharField(max_length=50)
    method = models.CharField(max_length=25)
    pctCoverage = models.FloatField()
    pctIdentity = models.FloatField()
    
    class Meta:
        abstract = True



class TagValue(models.Model):
    tag = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Lineage(models.Model):
    lin = models.CharField(max_length=50)
    frac = models.FloatField()
    family = models.CharField(max_length=100)
    spoligotype = models.CharField(max_length=100)
    rd = models.CharField(max_length=100)
    class Meta:
        abstract = True

class Variant(models.Model):
    chr = models.CharField(max_length=50)
    genome_pos = models.IntegerField()
    type = models.CharField(max_length=20)
    change = models.CharField(max_length=50)
    freq = models.FloatField()
    nucleotide_change = models.CharField(max_length=100)
    locus_tag = models.CharField(max_length=100)
    gene = models.CharField(max_length=50)
    _internal_change = models.CharField(max_length=50)
    class Meta:
        abstract = True

class Resistance(models.Model):
    drug = models.CharField(max_length=50)
    mutations = models.CharField(max_length=20)
    
    class Meta:
        abstract = True

