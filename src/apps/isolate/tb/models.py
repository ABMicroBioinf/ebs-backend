from djongo import models
from apps.account.models import Account
from apps.seq.models import Sequence
# Create your models here.


class Psummary(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    sequence = models.ForeignKey(
        Sequence, related_name="Psummaries", on_delete=models.CASCADE, null=True)
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

class Lineage(models.Model):
    lin = models.CharField(max_length=50)
    frac = models.FloatField()
    family = models.CharField(max_length=100)
    spoligotype = models.CharField(max_length=100)
    rd = models.CharField(max_length=100)
    class Meta:
        abstract = True


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

class Variant(models.Model):
    chr = models.CharField(max_length=50)
    genome_pos = models.FloatField()
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

class Profile(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    sequence = models.ForeignKey(
        Sequence, related_name="profiles", on_delete=models.CASCADE, null=True)
    
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
        model_container = Resistance
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