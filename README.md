# Source Data

uniprot_trembl and id mappings from uniprot May 2017
interpro 63

## Files:
/scratch0/NOT_BACKED_UP/dbuchan/projects/interpro_word2vec/
/scratch1/NOT_BACKED_UP/dbuchan/interpro/

1) run pfilt for CC and LC over all of uniprot
parse_masked_regions.py : parse the fasta files which have been masked for lc
                          and cc sequence and output dummy interpro-like
                          domain regions maskedregions.dat
                          PRODUCES: masked_regions.dat
2) retrieve the disorder region assignments from interpro
parse_match_complete.py : parse the interpro match_complete.xml to extract all
                          the MOBIDB disorder regions
                          PRODUCES: disorder_regions.dat
3) retrieve the pfam assignments from interpro
get_pf_ipr_assignments.py : parse the interpro file to remove only the pfam
                            PRODUCES: protein2ipr_pfam.dat
4) assign the NCBI taxonomy information to the uniprot IDs
map_taxonomy.py: open the uniprot and ncbi tax data and add the taxa_id and
              kingdom to the pfam assignments
              PRODUCES: protein2ipr_pfam_taxonomy.dat also protein2ipr_pfam_taxonomy_withipr.dat
                        disorder_regions_taxonomy.dat
                        masked_regions_taxonomy.dat

5) Use domain, masked and disorder regions to extract only eukaryotic proteins.
  extract_eukaryotic_proteins.py
    PRODUCES: protein2ipr_pfam_taxonomy_E.dat
              disorder_regions_taxonomy_E.dat
              masked_regions_taxonomy_E.dat
              
6) Build the word2vec strings
combine_domains.py: read disorder_regions_taxonomy.dat and
                    masked_regions_taxonomy.dat then interleave these with
                    protein2ipr_pfam_taxonomy.dat
                    PRODUCES: combined_domains_E.dat (29,277,053 annoated segments)
winnow_domains.py: reads the combined_domains_E.dat and outputs a smaller
                   file which resolves any overlaps.
                   Pfam domains take precedence over disorder, lc and cc regions
                   Disorder is kept in favour of lc and cc
                   cc is kept in favour of lc
                   If Pfam domains conflict the longer one is kept.
                   PRODUCES: final_domains_E.dat (25,776,649 annotated segments)
construct_word2vec_strings.py: Run through the final_domains_E.dat and produce
                               the word2 vec strings
                               PRODUCES: word2vec_input_E.dat
                                         (9,030,650 sentences)
7) Build embedding
build_vectors_word2vec.py: read the word2vec_input.dat sentences and train
                           word2vec
    word2vec training min_count=0
                  size=x? default 100
                        PRODUCES: word2vec.model

8) get distances
get_distance.py: read the gensim model and output the distance matrix produced
                  PRODUCES: word2vev_E.similarity - cosine similarity matrix
9) annotate the pfam stuff
annotate_pfam_go.py: read in interpro2go to get ipr to GO mapping. Read in
                     protein2ipr to map uniprot to go via ipr lastly read
                     final_domains_E.dat to work out which GO terms can be
                     associated with which pfam domains
                     PRODUCES: pfam_go_mapping.csv

# Analysis

7) get the pfam domain list and extract the DUFs
used grep to produce
/scratch1/NOT_BACKED_UP/dbuchan/pfam/DUF_list.txt
/scratch1/NOT_BACKED_UP/dbuchan/pfam/PfamID_list.txt
8) Select 1,000 NON-duf domains
select_random_pfams.py takes the lists and outputs 1,000 pfam domains.
/scratch1/NOT_BACKED_UP/dbuchan/pfam/pfam_random_list.txt
9) score what the accuracy would be if we didn't know their GO goterms on a gensims nearest neighbour basis
scrub final_domains_E.dat for all possible EUK pfam domains that COULD be predicted


calculate_nn_accuracy.py - aggregates data and calculates the precision, and hit rate
summarise_accuracy.R - total the accuracy scores we counted up


10) Annotate DUFs
annotate_dufs.py takes the distance matrix and finds the nearest neighbour to each duf and
outputs the putative annotations K=1
produces duf_annotations.csv

11) Do vector algebra
takes the model outputs and finds some pfam top twenty minus VECTOR which result
in possibly interesting
allgebra_output.csv - list of domain, minus domain that results in a 3rd domain and the distance


12) Test algebra output.
Takes the allgebra_output.csv and test if the GO term bags makes sense with
regards sets of GO terms domain1 -domain2 = domain3 therefor, to what extent
is GoSet1 - GoSet2 = GoSet3?
When GOSet2 and GoSet3 are greater than 0 subtracting domains typically goes to a a domain that has little GO overlap with domain1 or domain2

13) test algebra transforms
take 2 vectors A and B, find the vector C that maps A to B (B-A). If A and B have mutually exclusive GO go_terms are
the vectors C that do the mapping similar?
Cellular component
Nucleus -> Cytoplasm
GO:0005634 -> GO:0005737

Intracellular -> extracellular
GO:0005622 -> GO:0005615

Transmembrane -> cytoplasmic
GO:0009279 -> GO:0005737

outputs transform_angles.csv: contains all against all angles of the vectors for the closest transform from type A to B


14) search_good_low_angle_examples.py
Take transform_angles.csv find examples with very low angles (< 1). Then search domain corpus to see if we
can find two proteins that have those two domains. IDEALLY with the other domains being the same.


# Ancillary/Analysis

1) calculate gap distribution over the uniprot pfam assignments information
used in construct_word2vec_strings.py
calculate_gaps.py: protein2ipr_pfam_taxonomy.dat protein assignments and
                   output a list of the gap lengths

2) build look up of which pfam domain to which clade
get_pfam_taxa_lookup.py: parse protein2ipr_pfam_taxonomy.dat outputs PF to clade lookup
        PRODUCES: Pfam2clade.csv
3) parse the uniprot_trembl.dat to get a list of uniprot IDS to goterms and
their evidence codes
4) Get the OBO and GOA file that (probably) matches our interpro release
run.
get the: goa_uniprot_all.gaf.164
goa_euk_only.py: removes all archaea and bacterial entries from our GOA gaf file
                 PRODUCES: /scratch1/NOT_BACKED_UP/dbuchan/GO/goa_uniprot_all.gaf.164_euk
5)
Install fastsemsim to python2, use it to generate all the semantic similarities
for all pairs of eukaryotci GOA terms. based on interpro2go file @ 2017/03/07
Which are the annotations from quick go which map to

source /scratch0/NOT_BACKED_UP/dbuchan/python2/bin/activate
 
http://viewvc.geneontology.org/viewvc/GO-SVN/ontology-releases/2017-03-07/
fastsemsim --ontology_type GeneOntology --ontology_file /scratch1/NOT_BACKED_UP/dbuchan/GO/gene_ontology.obo --query_ss_type term --tss Lin --query_input ontology --remove_nan --cut 0.0001  --output_file euk_go_pfam_ss.txt --ac_file /scratch1/NOT_BACKED_UP/dbuchan/GO/goa_uniprot_all.gaf.164_euk

6) calculate distribution of # of domains with x many GO terms
$ go_count_distribution.py
read in the /scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/pfam_go_mapping.csv
output counts

7) calculate average semantic similarity bew
/scratch1/NOT_BACKED_UP/dbuchan/GO/euk_go_pfam_ss.txt

8) summary_stats.py
calcualte the number of euk proteins, GO terms and PFam domains we see

---

# AFTER REVIEWERS Comments. Redoing the following steps

1) calculate_region_counts.py - fraction of interpro sequences which are gap, domain, etc...
    outputs: assignment_statistics.csv
2) count_gap_classes.py - total up the number of proteins that have at least one of X gap count_gap_classes
    outputs: gap_class_populations.csv
3) count_go_distribution - read the pfam to go assignments and spit out
      go_counts.txt
   draw_go_counts.R - outputs histogram or less than 250
4) calculate_average_depth.pl. Take the DUF assignments we made and calculate the distance from root for each term (for histogram) and the average depth.  Also edit_obo.py to output a version of the obo where MF has no 'relationship: part_of' links to BP. Produces: duf_annotation_depths.csv > duf_annotation_depths_list.csv
draw_depth_histogram.R - calcualtes the mean depth and the distribution

5) calculate_transition_table.py - calculate markov chain transitions outputs
  first_order_tranistion_counts.csv - counts of all the transitions
  first_order_transition_probs.csv - probabilities of the transitions
7) calculate_markov_distances.py - opens markov probability matrices and calculates distances between pairs of domains.
   domain_markov_distance_matrix.csv
8) repurpose calculate_nn_accuracy.py to output stats for markov process.
    e.g: python3 calculate_nn_accuracy.py 1 molecular_function > nn1_markov_accuracy_mf.csv
      etc...
   repurpose summarise_accuracy.R - total the accuracy scores we counted up
