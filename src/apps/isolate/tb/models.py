from djongo import models
from apps.account.models import Account
# Create your models here.


class Profile(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    Description = models.TextField(max_length=1000, null=True, blank=True)
    owner = models.ForeignKey(
        Account, related_name="profiles", on_delete=models.CASCADE, null=True)
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
    
