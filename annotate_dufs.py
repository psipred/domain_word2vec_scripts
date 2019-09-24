import re
import sys
import random
import pandas
import numpy as np
import csv
from collections import defaultdict

def read_accessions(file):
    ac = re.compile("#=GF\s+AC\s+(.+)\.")

    accs = []
    with open(file) as file_list:
        for line in file_list:
            match = ac.search(line)
            if match:
                accs.append(match.group(1))
    return(accs)

ontology = None
if len(sys.argv) == 1:
    ontology = sys.argv[0]

go_mapping = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/pfam_go_mapping.csv"
obo = "/scratch1/NOT_BACKED_UP/dbuchan/GO/gene_ontology.obo"

go_namespace = {}
id = ''
namespace = ''
with open(obo) as obo_file:
    for line in obo_file:
        line = line.rstrip()
        if line.startswith('id: GO'):
            id = line[4:]
        if line.startswith('namespace: '):
            namespace = line[11:]
            if 'external' not in namespace:
                go_namespace[id] = namespace


go_terms = defaultdict(list)
with open(go_mapping) as go_file:
    go_reader = csv.reader(go_file, delimiter=',')
    for row in go_reader:
        go_terms[row[0]] = row[1:]


duf_list = "/scratch1/NOT_BACKED_UP/dbuchan/pfam/DUF_list.txt"
dufs = read_accessions(duf_list)
distance_matrix = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/word2vec_E.similarity"
distances = pandas.read_csv(open(distance_matrix, "rb"),
                            delimiter=",", header=0, index_col=0)
distances = distances.replace(0.0, np.NaN)
# print(distances)
pfam_set = defaultdict(list)
k_neighbours = 1

for name in dufs:
    if name in distances:
        sorted = distances[name].sort_values()
        i = 0
        completed = 0
        while True:
            # print(sorted.index[i])jjj
            if sorted.index[i].startswith('PF'):
                pfam_set[name].append(sorted.index[i])
                completed += 1
            if completed == k_neighbours:
                break
            i += 1

for duf in pfam_set:
    if len(go_terms[pfam_set[duf][0]]) > 0:
        out_str = duf+","
        for go in go_terms[pfam_set[duf][0]]:
            out_str += go+","
        out_str = out_str.rstrip(',')
        print(out_str)
