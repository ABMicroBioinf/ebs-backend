#from django.db.models.enums import Choices
from djongo import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from apps.account.models import Account
from apps.seq.models import Sequence
from apps.common.models import (
    Allele,
    TagValue,
    Lineage,
    Variant,
    Gene,
    Amr
)


class Assembly(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    # sequence = models.ForeignKey(
    #     Sequence, related_name="assemblies", on_delete=models.CASCADE, null=True)
    sequence = models.OneToOneField(
        Sequence,
        on_delete=models.CASCADE,
        #primary_key=True,
    )
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

class Stats(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    assembly = models.OneToOneField(
        Assembly,
        on_delete=models.CASCADE,
    )
    seqtype = models.CharField(max_length=100, null=True, blank=True)
    CDS = models.IntegerField(null=True, blank=True)
    CRISPR = models.IntegerField(null=True, blank=True)
    ncRNA = models.IntegerField(null=True, blank=True)
    oriC = models.IntegerField(null=True, blank=True)
    rRNA = models.IntegerField(null=True, blank=True)
    region = models.IntegerField(null=True, blank=True)
    regulatory_region = models.IntegerField(null=True, blank=True)
    tRNA = models.IntegerField(null=True, blank=True)
    tmRNA = models.IntegerField(null=True, blank=True)

    owner = models.ForeignKey(
        Account, related_name="stats", on_delete=models.CASCADE)
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    
    Description = models.TextField()
     
    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)

class Mlst(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    seqtype = models.CharField(max_length=100)
    scheme = models.CharField(max_length=100)
    #st = models.IntegerField(null=True, blank=True)
    st =  models.CharField(max_length=10)
    profile = models.ArrayField(
        model_container = Allele,       
    )
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    
    Description = models.TextField()
    assembly = models.OneToOneField(
        Assembly,
        on_delete=models.CASCADE,
    )
    owner = models.ForeignKey(
        Account, related_name="mlsts", on_delete=models.CASCADE)
    
    objects = models.DjongoManager()
    
    def __str__(self):
        return str(self.id)



class Resistome(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    
    assembly = models.OneToOneField(
        Assembly,
        on_delete=models.CASCADE,
    )
    seqtype = models.CharField(max_length=100)
    num_found = models.IntegerField()
    profile = models.ArrayField(
        model_container = Amr
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
    assembly = models.OneToOneField(
        Assembly,
        on_delete=models.CASCADE,
    )
    seqtype = models.CharField(max_length=100)
    num_found = models.IntegerField()
    profile = models.ArrayField(
        model_container = Gene
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
    assembly = models.ForeignKey(Assembly, related_name='annotations', on_delete=models.CASCADE)
    
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


class TbProfileSummary(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    sequence = models.OneToOneField(
        Sequence,
        on_delete=models.CASCADE,
        #primary_key=True,
    )
    Description = models.TextField(max_length=1000, null=True, blank=True)
    owner = models.ForeignKey(
        Account, related_name="profileSummaries", on_delete=models.CASCADE, null=True)
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    pct_reads_mapped = models.FloatField()
    num_reads_mapped = models.IntegerField()
    main_lin = models.CharField(max_length=100, null=True)
    sublin = models.CharField(max_length=100, null=True)
    num_dr_variants = models.IntegerField()
    num_other_variants = models.IntegerField()
    drtype = models.CharField(max_length=50)
    #drugs
    rifampicin = models.CharField(max_length=150)
    isoniazid = models.CharField(max_length=150)
    pyrazinamide = models.CharField(max_length=150)
    ethambutol = models.CharField(max_length=150)
    streptomycin = models.CharField(max_length=150)
    fluoroquinolones = models.CharField(max_length=150)
    moxifloxacin = models.CharField(max_length=150)
    ofloxacin = models.CharField(max_length=150)
    levofloxacin = models.CharField(max_length=150)
    ciprofloxacin = models.CharField(max_length=150)
    aminoglycosides = models.CharField(max_length=150)
    amikacin = models.CharField(max_length=150)
    kanamycin = models.CharField(max_length=150)
    capreomycin = models.CharField(max_length=150)
    ethionamide = models.CharField(max_length=150)
    para_aminosalicylic_acid = models.CharField(max_length=150)
    cycloserine = models.CharField(max_length=150)
    linezolid = models.CharField(max_length=150)
    bedaquiline = models.CharField(max_length=150)
    clofazimine = models.CharField(max_length=150)
    delamanid = models.CharField(max_length=150)

    objects = models.DjongoManager()

    def __str__(self):
        return str(self.id)

# "chr": "Chromosome",
# "genome_pos": 4408156,
# "type": "missense",
# "change": "p.Leu16Arg",
# "freq": 1.0,
# "nucleotide_change": "4408156A>C",
# "variant_annotations": {

# },
# "locus_tag": "Rv3919c",
# "gene": "gid",
# "_internal_change": "16L>16R"



class TbProfile(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    sequence = models.OneToOneField(
        Sequence,
        on_delete=models.CASCADE,
        #primary_key=True,
    )
    pct_reads_mapped = models.FloatField()
    num_reads_mapped = models.IntegerField()
    main_lin = models.CharField(max_length=100, null=True)
    sublin = models.CharField(max_length=100, null=True)
    num_dr_variants = models.IntegerField()
    num_other_variants = models.IntegerField()
    drtype = models.CharField(max_length=50)
    
    lineage = models.ArrayField(
        model_container = Lineage
    )
    
    dr_resistances = models.ArrayField(
        model_container = Gene
    )
    
    dr_variants = models.ArrayField(
        model_container = Variant
    )

    other_variants = models.ArrayField(
        model_container = Variant
    )

    owner = models.ForeignKey(
        Account, related_name="profiles", on_delete=models.CASCADE, null=True)
    DateCreated = models.DateTimeField(
        verbose_name='date created', auto_now=True)
    LastUpdate = models.DateTimeField(
        verbose_name='last update', auto_now=True)
    Description = models.TextField(max_length=1000, null=True, blank=True)
    objects = models.DjongoManager()

    def __str__(self):
        return str(self.id)
