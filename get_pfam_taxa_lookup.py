import csv
from collections import defaultdict

clade_assignments = defaultdict(set)
with open("/scratch1/NOT_BACKED_UP/dbuchan/interpro/"
          "protein2ipr_pfam_taxonomy.dat") as pfam_data:
    domainreader = csv.reader(pfam_data, delimiter=",")
    for row in domainreader:
        if "unknown" in row[2]:
            continue
        clade_assignments[row[5]].add(row[2])

for pfam in clade_assignments:
    print(pfam, "".join(sorted(clade_assignments[pfam])), sep=",")
