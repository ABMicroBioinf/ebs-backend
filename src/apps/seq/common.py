
"""
seq module experiment modle variable
Library Layout: whether to expect SINGLE or PAIRED end reads.
Library Source: the type of source material that is being sequenced.
Library Strategy: the sequencing technique intended for the library.
Library Selection: the method used to select and/or enrich the material being sequenced.
"""
seq_exp_strategies = (
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
seq_exp_sources = (
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
    
seq_exp_platforms = (
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

seq_exp_selections = (
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

seq_exp_layouts = (
        ('PAIRED', 'PAIRED'),
        ('SINGLE', 'SINGLE')
    )
sampleTypes = (
    ('TB', 'mycobacterium tuberculosis'),   
    ('CPO', 'cpo'),
    ('MG', 'metagenome')
)