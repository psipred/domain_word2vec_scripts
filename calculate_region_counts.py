import csv
from collections import defaultdict

domain_list = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/final_domains_E.dat"

prots = defaultdict(dict)
count = 0
with open(domain_list, 'r') as dl:
    domreader = csv.reader(dl, delimiter=',', quotechar='|')
    for row in domreader:
        prots[row[0]]['length'] = int(row[8])
        prots[row[0]]['domains'] = 0
        prots[row[0]]['disorder'] = 0
        prots[row[0]]['coiledcoil'] = 0
        prots[row[0]]['gaps'] = 0
        prots[row[0]]['lowcomplexity'] = 0

        # print(row[5])
        if row[5].startswith('PF'):
            prots[row[0]]['domains'] += int(row[7])-int(row[6])
        if row[5].startswith('mobidb-lite'):
            prots[row[0]]['disorder'] += int(row[7])-int(row[6])
        if row[5].startswith('CoiledCoil'):
            prots[row[0]]['coiledcoil'] += int(row[7])-int(row[6])
        if row[5].startswith('LowComplexity'):
            prots[row[0]]['lowcomplexity'] += int(row[7])-int(row[6])


        # count+=1
        # if count==10000:
        #     break
        #print ','.join(row)

for id in prots:
    assigned_total = prots[id]['domains'] + prots[id]['disorder'] + \
                     prots[id]['disorder'] + prots[id]['coiledcoil'] + \
                     prots[id]['lowcomplexity']
    prots[id]['gaps'] = prots[id]['length'] - assigned_total

total_res = 0
total_doms = 0
total_dis = 0
total_cc = 0
total_lc = 0
total_gaps = 0

for id in prots:
    total_res += prots[id]['length']
    total_doms += prots[id]['domains']
    total_dis += prots[id]['disorder']
    total_cc += prots[id]['coiledcoil']
    total_lc += prots[id]['lowcomplexity']
    total_gaps += prots[id]['gaps']


print('Total residues:', total_res)
print('Total domains', total_doms, total_doms/total_res*100)
print('Total disorder ', total_dis, total_dis/total_res*100)
print('Total CC', total_cc, total_cc/total_res*100)
print('Total LC', total_lc, total_lc/total_res*100)
print('Total gaps', total_gaps, total_gaps/total_res*100)
