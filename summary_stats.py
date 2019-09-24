import csv

domains = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/final_domains_E.dat"
pfam_go_mappings = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/pfam_go_mapping.csv"

euk_list = {}
pf_list = {}
go_list = {}
with open(domains) as doms:
    domData = csv.reader(doms, delimiter=',', quotechar='\'')
    for row in domData:
        euk_list[row[0]] = 1
        pf_list[row[5]] = 1

with open(pfam_go_mappings) as mappings:
    mapData = csv.reader(mappings, delimiter=',', quotechar='\'')
    for row in mapData:
        if row[0] in pf_list:
            entries = row[1:]
            for entry in entries:
                go_list[entry] = 1

print(len(euk_list))
print(len(pf_list))
print(len(go_list))
