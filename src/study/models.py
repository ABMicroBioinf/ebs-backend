from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

class Study(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=5000, null=True, blank=True)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="date created")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

def pre_save_project_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.owner.username + "-" + instance.title)

pre_save.connect(pre_save_project_receiver, sender=Study)


class Sample(models.Model):
    title = models.CharField(max_length=100)
    taxon_id = models.CharField(max_length=100, null=True, blank=True)
    scientific_name = models.CharField(max_length=100, null=True, blank=True)
    common_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    study = models.ForeignKey(
        Study, related_name = 'samples', on_delete=models.CASCADE)
    
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="date created")

    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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

    title = models.CharField(max_length=100)
    library_name = models.CharField(max_length=100)
    platform = models.CharField(max_length=100, choices=platforms) #illumina MiSeq
    instrument_model = models.CharField(max_length=100, null=True, blank=True)
    library_strategy = models.CharField(max_length=100, choices=strategies) # WGS
    library_source = models.CharField(max_length=100, choices=sources) # metagenomics
    library_layout = models.CharField(max_length=100, choices=layouts) # paired
    library_selection = models.CharField(max_length=100, choices=selections) #random
    description = models.CharField(max_length=100, null=True, blank=True)
    #created = models.DateTimeField(auto_now_add=True)
    #seqfile = models.FileField(upload_to='seqs/', null=True, blank=True)
    sample = models.ForeignKey(Sample, related_name='experiments', on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="date created")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Run(models.Model):
    name = models.CharField(max_length=100)
    date_run = models.DateTimeField(blank=True, null=True)
    experiment = models.ForeignKey(Experiment, related_name='runs', on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name="date created")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Seq(models.Model):
    study = models.ForeignKey(
        Study, related_name = 'runs', on_delete=models.CASCADE)
    seqfile = models.FileField(upload_to='seqs/', null=True, blank=True)
    #seqfile_name = seqfile.name 
    avg_length = models.IntegerField()
    bases = models.IntegerField()
    count = models.IntegerField()
    date_added = models.DateTimeField(
        auto_now_add=True, verbose_name="date created")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")


