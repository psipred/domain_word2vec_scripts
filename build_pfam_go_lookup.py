import csv
from collections import defaultdict

uniprot_pfam = defaultdict(set)
pf_2_go = defaultdict(set)
with open("/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/"
          "protein2ipr_pfam_taxonomy.dat") as pfam_data:
#          "prot2ipd_test.dat") as pfam_data:
    domainreader = csv.reader(pfam_data, delimiter=",")
    for row in domainreader:
        uniprot_pfam[row[0]].add(row[5])

with open("/scratch1/NOT_BACKED_UP/dbuchan/uniprot/"
#          "idmapping_selected_test.tab") as pfam_data:
          "idmapping_selected.tab") as pfam_data:
    idreader = csv.reader(pfam_data, delimiter="\t")
    try:
        for row in idreader:
            if row[0] in uniprot_pfam:
                go_list = row[6].split("; ")
                if len(go_list) == 1 and len(go_list[0]) == 0:
                    go_list = []
                for go in go_list:
                    for pfam in uniprot_pfam[row[0]]:
                        pf_2_go[pfam].add(go)
    except Exception as e:
        pass
        # print("Unparseable line")

for pfam in pf_2_go:
    for go in pf_2_go[pfam]:
        print(pfam, go)
