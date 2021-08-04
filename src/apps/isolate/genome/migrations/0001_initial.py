# Generated by Django 2.2.22 on 2021-07-30 20:55

import apps.isolate.genome.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('gff', djongo.models.fields.ArrayField(model_container=apps.isolate.genome.models.Gff)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ganalyses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('assembly_stats', djongo.models.fields.EmbeddedField(model_container=apps.isolate.genome.models.SeqStat, null=True)),
                ('virulome', djongo.models.fields.ArrayField(model_container=apps.isolate.genome.models.Virulome)),
                ('amr', djongo.models.fields.ArrayField(model_container=apps.isolate.genome.models.AMR)),
                ('annotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genomes', to='genome.Annotation')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genomes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]