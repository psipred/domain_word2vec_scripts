import sys
from collections import defaultdict


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def read_dat_file(path, dat):
    with open(path) as data:
        for line in data:
            entries = line.split(",")
            dat[entries[0]].append(line)
    return(dat)


accessions = defaultdict(list)
accessions = read_dat_file("/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/"
                           "masked_regions_taxonomy_E.dat", accessions)
accessions = read_dat_file("/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/"
                           "disorder_regions_taxonomy_E.dat", accessions)
# accessions = read_dat_file("/scratch1/NOT_BACKED_UP/dbuchan/interpro/"
#                            "test_disorder.dat", accessions)

previous_uniprot = "XXX"
line_cache = []
with open("/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/"
          "protein2ipr_pfam_taxonomy_E.dat") as pfam:
#          "test_pfam.dat") as pfam:
    first_line = pfam.readline()
    entries = first_line.split(",")
    line_cache.append(first_line)
    previous_uniprot = entries[0]

    for line in pfam:
        entries = line.split(",")
        if entries[0] not in previous_uniprot:
            # process previous
            for line2 in line_cache:
                print(line2.rstrip())
            line_cache = []
            line_cache.append(line)

            if previous_uniprot in accessions:
                for line2 in accessions[previous_uniprot]:
                    print(line2.rstrip())
            previous_uniprot = entries[0]
        else:
            line_cache.append(line)


for line in line_cache:
    print(line.rstrip())
    if previous_uniprot in accessions:
        for line2 in accessions[previous_uniprot]:
            print(line2.rstrip())
