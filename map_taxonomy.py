import csv
import sys
csv.field_size_limit(sys.maxsize)
# parse protein2ipr to output just the pfam domains

name_lookup = {}
# print("Reading TAXA names")
with open('/scratch1/NOT_BACKED_UP/dbuchan/ncbi_taxonomy/names.dmp') as namesfile:
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
with open('/scratch1/NOT_BACKED_UP/dbuchan/ncbi_taxonomy/categories.dmp') as catfile:
    catreader = csv.reader(catfile, delimiter='\t', quotechar='\'')
    for row in catreader:
        if row[1] in name_lookup:
            name_lookup[row[1]]['kingdom'] = row[0]
        if row[2] in name_lookup:
            name_lookup[row[1]]['kingdom'] = row[0]

# print(name_lookup)
uniprot_lookup = {}
# print("Annotating UNIPROT")
with open('/scratch1/NOT_BACKED_UP/dbuchan/uniprot/idmapping_selected.tab') as mapping:
    mappingreader = csv.reader(mapping, delimiter='\t', quotechar='\'')
    for row in mappingreader:
        if row[12] in name_lookup:
            # print(row)
            uniprot_lookup[row[0]] = name_lookup[row[12]]
            uniprot_lookup[row[0]]['taxaid'] = row[12]
            # break

# print("Annotating UNIPROT PFam")

# print(uniprot_lookup)
with open('/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/protein2ipr_pfam.dat') as pfam:
# with open('/scratch1/NOT_BACKED_UP/dbuchan/interpro/masked_regions.dat') as pfam:
#with open('/scratch1/NOT_BACKED_UP/dbuchan/interpro/disorder_regions.dat') as pfam:
    pfamreader = csv.reader(pfam, delimiter=',', quotechar='\'')
    for row in pfamreader:
        if row[0] in uniprot_lookup:
            new_line = [row[0], uniprot_lookup[row[0]]['taxaid'],
                        uniprot_lookup[row[0]]['kingdom'],
                        uniprot_lookup[row[0]]['name']] + row[1:]
            print(",".join(new_line))
            sys.stdout.flush()
