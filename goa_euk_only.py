from __future__ import print_function
import csv
import sys

'''
Open protein2ipr file with taxonomy data and get all the uniprot IDS for
Eukaryotic proteins Then run through goa_file to throw away the eukarytotic
proteins
'''


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


taxonomy_names = "/scratch1/NOT_BACKED_UP/dbuchan/ncbi_taxonomy/names.dmp"
taxonomy_categories = "/scratch1/NOT_BACKED_UP/dbuchan/ncbi_taxonomy/categories.dmp"
goa_file = "/scratch1/NOT_BACKED_UP/dbuchan/GO/goa_uniprot_all.gaf.164"

name_lookup = {}
# print("Reading TAXA names")
with open(taxonomy_names) as namesfile:
    namesreader = csv.reader(namesfile, delimiter='|', quotechar='\'')
    for row in namesreader:
        clean_row = [x.rstrip().lstrip() for x in row]
        if 'scientific name' in clean_row[3]:
            # print(clean_row)
            clean_row[1] = clean_row[1].replace(',', '')
            name_lookup[clean_row[0]] = {}
            name_lookup[clean_row[0]]['name'] = clean_row[1]
            name_lookup[clean_row[0]]['kingdom'] = 'unknown'


# print("Reading TAXA categories")
with open(taxonomy_categories) as catfile:
    catreader = csv.reader(catfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    for row in catreader:
        if row[1] in name_lookup:
            name_lookup[row[1]]['kingdom'] = row[0]
        if row[2] in name_lookup:
            name_lookup[row[1]]['kingdom'] = row[0]

euk_lookup = {}
for taxaid in name_lookup:
    if name_lookup[taxaid]['kingdom'] is "E":
        euk_lookup[taxaid] = name_lookup[taxaid]

# print(euk_lookup)
with open(goa_file) as goa_file:
    for i in range(1, 9):
        print(goa_file.next().rstrip())
    csv.field_size_limit(sys.maxsize)
    goreader = csv.reader(goa_file, delimiter='\t', quoting=csv.QUOTE_NONE)
    for row in goreader:
        try:
            if row[11] == 'protein':
                if row[12].split(':')[1] in euk_lookup:
                    print("\t".join(row))
        except Exception as e:
            eprint(row)
