from djongo import models
from apps.account.models import Account
from apps.seq.models import Run
# Create your models here.

class Lineage(models.Model):
    lin = models.CharField(max_length=100, null=False, blank=False)
    family = models.CharField(max_length=100, null=True, blank=True)
    spoligotype = models.CharField(max_length=100, null=True, blank=True)
    rd = models.CharField(max_length=100, null=True, blank=True)
    frac = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = False
    
class Drug(models.Model):
   
    type = models.CharField(max_length=100)
    drug = models.CharField(max_length=100)
    confidence = models.CharField(max_length=100)
    literature = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = False
    def __str__(self):
        return str(self.drup)


class Resistance(models.Model):
    
    drug = models.CharField(max_length=100)
    mutations = models.CharField(max_length=100)

    class Meta:
        abstract = False
    
class VariantAnnotation(models.Model):
    #desc = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = False

class Variant(models.Model):
    chr = models.CharField(max_length=100)
    genome_pos = models.IntegerField()
    type = models.CharField(max_length=100)
    change = models.CharField(max_length=100)
    freq = models.FloatField()
    nucleotide_change = models.CharField(max_length=100)
    locus_tag = models.CharField(max_length=100)
    gene = models.CharField(max_length=100)
    _internal_change = models.CharField(max_length=100)
    variant_annotations = models.EmbeddedField(
        model_container = VariantAnnotation
    )
    

    class Meta:
        abstract = False
    
    
class DrVariant(Variant):
    drugs = models.ArrayField(
        model_container=Drug,
        
    )
    class Meta:
        abstract = False

class DB_version(models.Model):
    name = models.CharField(max_length=50)
    commit = models.CharField(max_length=50)
    Merge = models.CharField(max_length=50)
    Author = models.CharField(max_length=50)
    Date = models.CharField(max_length=50)

    class Meta:
        abstract = False

class Pipeline(models.Model):
    mapper = models.CharField(max_length=100)
    variant_caller = models.CharField(max_length=100)

    class Meta:
        abstract = False


class Profile(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    main_lin = models.CharField(max_length=100, null=True)
    sublin = models.CharField(max_length=100, null=True)
    drtype = models.CharField(max_length=50)
    num_dr_variants = models.IntegerField()
    num_other_variants = models.IntegerField()
    pct_reads_mapped = models.FloatField()
    num_reads_mapped = models.IntegerField()
    description = models.TextField(max_length=5000, null=True, blank=True)
    owner = models.ForeignKey(
        Account, related_name="profiles", on_delete=models.CASCADE, null=True)

    lineage = models.ArrayField(
        model_container = Lineage
       
    )

    dr_resistances = models.ArrayField(
        model_container = Resistance
    )

    dr_variants = models.ArrayField(
        model_container = DrVariant
    )

    other_variants = models.ArrayField(
        model_container = Variant
    )
    
    db_version = models.EmbeddedField(
        model_container = DB_version
    ) 

    pipeline = models.EmbeddedField(
        model_container = Pipeline
    ) 

    tbprofiler_version = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)
    
