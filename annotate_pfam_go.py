import csv
import re
from collections import defaultdict
'''read in interpro2go to get ipr to GO mapping. Read in
                     protein2ipr to map uniprot to go via ipr lastly read
                     final_domains_E.dat to work out which GO terms can be
                     associated with which pfam domains'''

interpro2go = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/interpro2go"
protein2ipr = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/protein2ipr_pfam_taxonomy_withipr.dat"
euk_domains = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/final_domains_E.dat"

ipr2go_lookup = defaultdict(list)
# {ipr : [GO, GO, GO]}
with open(interpro2go) as go_data:
    for line in go_data:
        if line.startswith("!"):
            continue
        line = line.rstrip()
        initial_split = line.split(" > ")
        first_section = initial_split[0].split(" ")
        iprsplit = first_section[0].split(':')
        last_section = initial_split[1].split(" ; ")
        ipr2go_lookup[iprsplit[1]].append(last_section[1])


prot2ipr_lookup = defaultdict(list)
# {uniprot: [IPR, IPR, IPR]}
with open(protein2ipr) as prot_data:
    protreader = csv.reader(prot_data, delimiter=",")
    for row in protreader:
        if row[2] == 'E':
            prot2ipr_lookup[row[0]].append(row[4])

# print(ipr2go_lookup)
# print(prot2ipr_lookup)

# {pfam: [go, go, go]}
pfam_assigns = defaultdict(list)
with open(euk_domains) as euk_data:
    eukreader = csv.reader(euk_data, delimiter=",")
    for row in eukreader:
        if row[0] in prot2ipr_lookup:
            for ipr in prot2ipr_lookup[row[0]]:
                if ipr in ipr2go_lookup:
                    for go in ipr2go_lookup[ipr]:
                        pfam_assigns[row[5]].append(go)

for domain in pfam_assigns:
    line = domain+","
    pfam_assigns[domain] = list(set(pfam_assigns[domain]))
    for go in pfam_assigns[domain]:
        line += go+","
    print(line.rstrip(","))
