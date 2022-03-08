#!/usr/local/bin/perl

use strict;
use warnings;

open(RUN2BIOSAMPLE, $ARGV[0]);
my %run2biosample = ();

while(<RUN2BIOSAMPLE>){
        next if !/\S/;
        next if/^RUN,/;
        chomp;
        my @l = split(/,/, $_);

        $run2biosample{$l[0]} = $l[1];

}
close(RUN2BIOSAMPLE);

open(FH, "<", $ARGV[1]);
    my $first =  <FH>;
    print $first;

 while (<FH>){
    next if !/\S/;
    s/_contigs.fasta//;
    s/_abricate.tsv//;
    chomp;
    if (/^(\w+)(.*)/){
        
        my $runid = $1;
        if(exists $run2biosample{$runid}){
            print $run2biosample{$runid},$2, "\n";
        }
    }
}


close(FH);