#!/usr/bin/perl

  use strict;
  use warnings;
  use Text::CSV;
  use Getopt::Long;

  my ($srafile, $raw_stat_file, $qc_stat_file, $study_id);
  &GetOptions(
    "s=s"       => \$srafile,
	  "r=s" =>\$raw_stat_file,
    "q=s" =>\$qc_stat_file,
    "i=s" =>\$study_id
  );

($srafile && $raw_stat_file && $qc_stat_file) or die "\nusage: $0 \n 
        -s  <sra table file downloaded from sra run selector> 
        -r  <raw sequence stats file> 
        -q  <quality controlled sequence stats file>\n";

  
  my %summary = ();
  my @sra_header = ();

  open my $fh, "<", $srafile or die "$srafile: $!";
  my $csv = Text::CSV->new ({
      binary    => 1, # Allow special character. Always set this
      auto_diag => 1, # Report irregularities immediately
      });

  my %sample_fields = (
    #"BioSample" => -1,
    "Organism"  => -1,
    "Sample Name"  => -1,
    "strain"  => -1
  );
  my %exp_fields = (
    "Library Name"  => -1,
    "Instrument"  => -1,
    "Library Name"  => -1,
    "LibraryLayout"  => -1,
    "LibrarySource"  => -1,
    "LibrarySelection" => -1,
    "Platform"  => -1
  );

  my $i = 0;
  my %index2samplefield = ();
  my %index2expfield = ();
  foreach my $item (@{$csv->getline ($fh)}){
    if(exists $sample_fields{$item}){
      $sample_fields{$item} = $i;
      $index2samplefield{$i} = $item;
    }
    elsif(exists $exp_fields{$item}){
      $exp_fields{$item} = $i;
      $index2expfield{$i} = $item;
    }
    $i++;
  }

  my $dbid = 1;
  while (my $row = $csv->getline ($fh)) {
      
      my %sfields = ();
      my %efields = ();  
      my $runid = @$row[0];
      my $i = 0;
      foreach my $item (@$row){
        #print STDERR "****************** $item\n";
        if(exists $index2samplefield{$i}){
          my $field = lcfirst($index2samplefield{$i});
          $field =~ s/\s+//;
          $sfields{$field} = $item;
          #print STDERR "******************$index2samplefield{$i}, $item\n"
        }
        elsif(exists $index2expfield{$i}){
          my $field = lcfirst($index2expfield{$i});
          $field =~ s/\s+//;
          $efields{$field} = $item;
        }
        $i++;
      }
      $summary{$runid}->{id} = $dbid++;
      $summary{$runid}->{run_name} = $runid;
      $summary{$runid}->{study_id} = $study_id;

      $summary{$runid}->{sample} = \%sfields;
      $summary{$runid}->{experiment} = \%efields;

  }
  close $fh;

  open $fh, "<", $raw_stat_file or die "$raw_stat_file:$!";
  
  my @header = split(/,/, "Seqfile,seqtype,reads,total_bp,geecee,minLen,avgLen,maxLen,avgQual,errQual,ambiguous");

  my %col2header = ();
  $i = 0;
  shift @header;
  shift @header;

  foreach (@header){
    
    $col2header{$i} = $_;
    #print $_, "****************$i\n";
   
    $i++;
  }

  $csv->getline($fh);
  while(my $row = $csv->getline($fh)){
    my $c = 0;
    my %mystats = ();
    my $seqfile = shift @$row;
    shift @$row;

    foreach my $col (@$row){
      $mystats{$col2header{$c++}} = 1 * $col;
    } 
    $summary{$seqfile}->{stats_raw} = \%mystats
  } 
  close $fh;

  open $fh, "<", $qc_stat_file or die "$qc_stat_file:$!";
  $csv->getline($fh);
  while(my $row = $csv->getline($fh)){
    
    my $c = 0;
    my %mystats = ();
    my $seqfile = shift @$row;
    shift @$row;
    foreach my $col (@$row){
      $mystats{$col2header{$c++}} = 1 * $col;
    } 
    $summary{$seqfile}->{stats_qc} = \%mystats
  } 
  close $fh;

  #use Data::Dumper;

#print Dumper(%summary);

use JSON;
my $json = JSON->new->allow_nonref;
#my $json = new JSON::XS;
 
my $pretty_printed = $json->pretty->encode(\%summary);
#my $json = encode_json \%summary;
print $pretty_printed;