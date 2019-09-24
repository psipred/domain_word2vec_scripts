#!/usr/bin/perl

# $Id: ancestors.pl,v 1.7 2007/11/15 18:30:47 sherlock Exp $

# License information (the MIT license)

# Copyright (c) 2003, 2007 Gavin Sherlock; Stanford University

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

use strict;
use diagnostics;
use warnings;
use Try::Tiny;

use GO::OntologyProvider::OboParser;

my ($ontologyFile) = @ARGV;

&Usage("You must provide an obo file")                  if (!$ontologyFile);
&Usage("Your obo file does not exist")                  if (!-e $ontologyFile);
&Usage("Your obo file does not have a .obo extension")  if (!-e $ontologyFile);

my $ontologies = {
      'P' => GO::OntologyProvider::OboParser->new(ontologyFile => $ontologyFile,
                                                  aspect       => 'P'),
      'C' => GO::OntologyProvider::OboParser->new(ontologyFile => $ontologyFile,
                                                      aspect       => 'C'),
      'F' => GO::OntologyProvider::OboParser->new(ontologyFile => $ontologyFile,
                                                    aspect       => 'F'),
};

sub return_shortest_path{
   my ($goid, $ontologiesd) = @_;
   my $node;
   foreach my $aspect (keys %$ontologies)
   {
     # print $aspect, "\n";
     # print $ontologies->{$aspect}, "\n";
     $node = $ontologies->{$aspect}->nodeFromId($goid);
     if(defined $node)
     {
       last;
     }
   }

   my @pathsToRoot = $node->pathsToRoot;

   my $path_depth = 0;
   my $shortest = 100000000000000;
   foreach my $path (@pathsToRoot){
       if(scalar(@{$path}) < $shortest)
       {
         $shortest = scalar(@{$path});
       }
       # print scalar(@{$path}), "\n";
   }
   return $shortest;
}


my $duf_file = 'duf_annotations.csv';
open(my $fh, $duf_file) or die "File can't be opened";
my $all_depths = '';
while( my $line = <$fh>)
{
  chomp $line;
  my @entries = split(/,/, $line);
  my $out_line = shift @entries;
  $out_line .= ",";
  foreach my $goid (@entries){
    my $len = "-";
    try{
        $len = return_shortest_path($goid, \$ontologies);
    }
    catch{};
    $out_line.=$len.",";
    $all_depths.=$len.",";
  }
  chop $out_line;
  print $out_line, "\n";
}
chop $all_depths;
print $all_depths, "\n";

sub Usage{

    my $message = shift;

    print $message, ".\n\n";

    print "Usage :

ancestors.pl  <obo_file>

Where aspect is P, C or F.  Note, the provided GOID must be for a GO term in the aspect that you provide.\n\n";

    exit;

}
