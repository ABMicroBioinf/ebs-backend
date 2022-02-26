# Generated by Django 3.1.2 on 2022-02-23 23:58

import apps.seq.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('DateCreated', models.DateTimeField(auto_now=True, verbose_name='date created')),
                ('LastUpdate', models.DateTimeField(auto_now=True, verbose_name='last update')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seqstat',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('rReads', models.IntegerField(blank=True, null=True)),
                ('rYield', models.IntegerField(blank=True, null=True)),
                ('rGeeCee', models.FloatField(blank=True, null=True)),
                ('rMinLen', models.IntegerField(blank=True, null=True)),
                ('rAvgLen', models.IntegerField(blank=True, null=True)),
                ('rMaxLen', models.IntegerField(blank=True, null=True)),
                ('rAvgQual', models.FloatField(blank=True, null=True)),
                ('rErrQual', models.FloatField(blank=True, null=True)),
                ('rAmbiguous', models.FloatField(blank=True, null=True)),
                ('q_Reads', models.IntegerField(blank=True, null=True)),
                ('q_Yield', models.IntegerField(blank=True, null=True)),
                ('q_GeeCee', models.FloatField(blank=True, null=True)),
                ('q_MinLen', models.IntegerField(blank=True, null=True)),
                ('q_AvgLen', models.IntegerField(blank=True, null=True)),
                ('q_MaxLen', models.IntegerField(blank=True, null=True)),
                ('q_AvgQual', models.FloatField(blank=True, null=True)),
                ('q_ErrQual', models.FloatField(blank=True, null=True)),
                ('q_Ambiguous', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('TaxID', models.IntegerField()),
                ('seqtype', models.CharField(blank=True, choices=[('TB', 'mycobacterium tuberculosis'), ('CPO', 'cpo'), ('MG', 'metagenome')], max_length=100, null=True)),
                ('ScientificName', models.CharField(max_length=100)),
                ('Experiment', models.CharField(max_length=100)),
                ('LibraryName', models.CharField(max_length=100)),
                ('LibraryStrategy', models.CharField(blank=True, choices=[('WGA', 'WGA'), ('WGS', 'WGS'), ('WXS', 'WXS'), ('RNA-Seq', 'RNA-Seq'), ('miRNA-Seq', 'miRNA-Seq'), ('WCS', 'WCS'), ('CLONE', 'CLONE'), ('POOLCLONE', 'POOLCLONE'), ('AMPLICON', 'AMPLICON'), ('CLONEEND', 'CLONEEND'), ('FINISHING', 'FINISHING'), ('ChIP-Seq', 'ChIP-Seq'), ('MNase-Seq', 'MNase-Seq'), ('DNase-Hypersensitivity', 'DNase-Hypersensitivity'), ('Bisulfite-Seq', 'Bisulfite-Seq'), ('Tn-Seq', 'Tn-Seq'), ('EST', 'EST'), ('FL-cDNA', 'FL-cDNA'), ('CTS', 'CTS'), ('MRE-Seq', 'MRE-Seq'), ('MeDIP-Seq', 'MeDIP-Seq'), ('MBD-Seq', 'MBD-Seq'), ('Synthetic-Long-Read', 'Synthetic-Long-Read'), ('ATAC-seq', 'ATAC-seq'), ('ChIA-PET', 'ChIA-PET'), ('FAIRE-seq', 'FAIRE-seq'), ('Hi-C', 'Hi-C'), ('ncRNA-Seq', 'ncRNA-Seq'), ('RAD-Seq', 'RAD-Seq'), ('RIP-Seq', 'RIP-Seq'), ('SELEX', 'SELEX'), ('ssRNA-seq', 'ssRNA-seq'), ('Targeted-Capture', 'Targeted-Capture'), ('Tethered Chromatin Conformation Capture', 'Tethered Chromatin Conformation Capture'), ('OTHER', 'OTHER')], max_length=100, null=True)),
                ('LibrarySelection', models.CharField(blank=True, choices=[('RANDOM', 'RANDOM'), ('PCR', 'PCR'), ('RANDOM PCR', 'RANDOM PCR'), ('RT-PCR', 'RT-PCR'), ('HMPR', 'HMPR'), ('MF', 'MF'), ('CF-S', 'CF-S'), ('CF-M', 'CF-M'), ('CF-H', 'CF-H'), ('CF-T', 'CF-T'), ('MDA', 'MDA'), ('MSLL', 'MSLL'), ('cDNA', 'cDNA'), ('ChIP', 'ChIP'), ('MNase', 'MNase'), ('DNAse', 'DNAse'), ('Hybrid Selection', 'Hybrid Selection'), ('Reduced Representation', 'Reduced Representation'), ('Restriction Digest', 'Restriction Digest'), ('5-methylcytidine antibody', '5-methylcytidine antibody'), ('MBD2 protein methyl-CpG binding domain', 'MBD2 protein methyl-CpG binding domain'), ('CAGE', 'CAGE'), ('RACE', 'RACE'), ('size fractionation', 'size fractionation'), ('Padlock probes capture method', 'Padlock probes capture method'), ('other', 'other'), ('unspecified', 'unspecified'), ('cDNA_oligo_dT', 'cDNA_oligo_dT'), ('cDNA_randomPriming', 'cDNA_randomPriming'), ('Inverse rRNA', 'Inverse rRNA'), ('Oligo-dT', 'Oligo-dT'), ('PolyA', 'PolyA'), ('repeat fractionation', 'repeat fractionation')], max_length=100, null=True)),
                ('LibrarySource', models.CharField(blank=True, choices=[('GENOMIC', 'GENOMIC'), ('TRANSCRIPTOMIC', 'TRANSCRIPTOMIC'), ('METAGENOMIC', 'METAGENOMIC'), ('METATRANSCRIPTOMIC', 'METATRANSCRIPTOMIC'), ('SYNTHETIC', 'SYNTHETIC'), ('VIRAL RNA', 'VIRAL RNA'), ('GENOMIC SINGLE CELL', 'GENOMIC SINGLE CELL'), ('TRANSCRIPTOMIC SINGLE CELL', 'TRANSCRIPTOMIC SINGLE CELL'), ('OTHER', 'OTHER')], max_length=100, null=True)),
                ('LibraryLayout', models.CharField(blank=True, choices=[('PAIRED', 'PAIRED'), ('SINGLE', 'SINGLE')], max_length=100, null=True)),
                ('Platform', models.CharField(blank=True, choices=[('_LS454', '_LS454'), ('ABI_SOLID', 'ABI_SOLID'), ('BGISEQ', 'BGISEQ'), ('CAPILLARY', 'CAPILLARY'), ('COMPLETE_GENOMICS', 'COMPLETE_GENOMICS'), ('HELICOS', 'HELICOS'), ('ILLUMINA', 'ILLUMINA'), ('ION_TORRENT', 'ION_TORRENT'), ('OXFORD_NANOPORE', 'OXFORD_NANOPORE'), ('PACBIO_SMRT', 'PACBIO_SMRT')], max_length=100, null=True)),
                ('SequencerModel', models.CharField(blank=True, max_length=100, null=True)),
                ('SampleName', models.CharField(max_length=100)),
                ('CenterName', models.CharField(max_length=100)),
                ('taxName_1', models.CharField(blank=True, max_length=100, null=True)),
                ('taxFrac_1', models.FloatField(blank=True, null=True)),
                ('taxName_2', models.CharField(blank=True, max_length=100, null=True)),
                ('taxFrac_2', models.FloatField(blank=True, null=True)),
                ('taxName_3', models.CharField(blank=True, max_length=100, null=True)),
                ('taxFrac_3', models.FloatField(blank=True, null=True)),
                ('taxName_4', models.CharField(blank=True, max_length=100, null=True)),
                ('taxFrac_4', models.FloatField(blank=True, null=True)),
                ('DateCreated', models.DateTimeField(auto_now=True, verbose_name='date created')),
                ('LastUpdate', models.DateTimeField(auto_now=True, verbose_name='last update')),
                ('Description', models.TextField(blank=True, null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sequences', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sequences', to='seq.project')),
                ('seqstat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='seq.seqstat')),
            ],
        ),
        migrations.CreateModel(
            name='SeqFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('raw_seq_file', models.FileField(upload_to=apps.seq.models.raw_dir)),
                ('qc_seq_file', models.FileField(upload_to=apps.seq.models.qc_dir)),
                ('sequence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seq.sequence')),
            ],
        ),
        migrations.CreateModel(
            name='MetadataFile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('metadata_file', models.FileField(upload_to=apps.seq.models.metadata_dir)),
                ('sequence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seq.sequence')),
            ],
        ),
    ]
