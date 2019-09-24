from __future__ import print_function
import csv
from collections import defaultdict
import pandas
import numpy as np
import sys
import math
import re


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# 1) read in gensim distance matrix
# 2) read in pfam go goterms
# 3) read in random_list
# 4) for each in random list, find nearest neighbour from gensim transfer GO, score how oftern it is rights


k_neighbours = int(sys.argv[1])
# molecular_function
# biological_process
# cellular_component
ontology = None
if len(sys.argv) == 3:
    ontology = sys.argv[2]

distance_matrix = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/word2vec_E.similarity"
go_mapping = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/pfam_go_mapping.csv"
pfam_sample = "/scratch1/NOT_BACKED_UP/dbuchan/pfam/pfam_random_list.txt"
final_pfam_domains = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/final_domains_E.dat"
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

pfam_set = []
with open(pfam_sample) as pfamlist:
    for line in pfamlist:
        pfam_set.append(line.rstrip()[0:7])

all_pfam_domains = set([])
with open(final_pfam_domains) as domain_list:
    domain_reader = csv.reader(domain_list, delimiter=',')
    for row in domain_reader:
        all_pfam_domains.add(row[5])

possible_pfam_go_predictions = set([])
for domain in all_pfam_domains:
    if domain in go_terms:
        for go in go_terms[domain]:
            if ontology:
                if ontology in go_namespace[go]:
                    possible_pfam_go_predictions.add(go)
            else:
                possible_pfam_go_predictions.add(go)

#eprint(len(possible_pfam_go_predictions))
#exit()

distances = pandas.read_csv(open(distance_matrix, "rb"),
                            delimiter=",", header=0, index_col=0)
distances = distances.replace(0.0, np.NaN)
# closest_distance = distances.idxmin(axis=1)
# https://stackoverflow.com/questions/45193131/return-n-smallest-indexes-by-column-using-pandas
row_names = list(distances.index)
pfam_set = defaultdict(list)
for name in row_names:
    if name.startswith('PF'):
        sorted = distances[name].sort_values()
        i = 0
        completed = 0
        while True:
            # print(sorted.index[i])
            if sorted.index[i].startswith('PF'):
                pfam_set[name].append(sorted.index[i])
                completed += 1
            if completed == k_neighbours:
                break
            i += 1
        # for element in distances[name]:
        #     print(type(element))
        # print(pfam_set)
        # break


def print_accuracy(pfam_set, go_terms, go_namespace, k_neighbours, ontology):
    print("ID,Closest,No. True,No. Prediction,TP,FN,FP,TN,Precision,Accuracy,Recall,Hit Rate,MCC,No. Consensus Prediction,Consensus TP,Consensus FN,Consensus FP,Consensus TN,Consensus Precision,Consensus Accuracy,Consensus Recall,Consensus Hit Rate,Consensus MCC")
    # TP: number shared between Truth and Prediction
    # FN: Number in Truth but not in Prediction - low bound estimate
    # FP: Number in Prediction but not in Truth - low bound estimate
    # tn_list: number of things in possible_pfam_domain_predictions that are not in pred_set
    # TN: Not in Prediction set and Not in Truth set
    for pfamID in pfam_set:
        try:
            true_set = []
            if ontology:
                for term in go_terms[pfamID]:
                    if term in go_namespace:
                        if ontology in go_namespace[term]:
                            true_set.append(term)
            else:
                true_set = go_terms[pfamID]
            pred_set = set([])
            consensus_set = defaultdict(int)
            for term in pfam_set[pfamID]:
                if ontology:
                    for go_term in go_terms[term]:
                        # print("Ontology set", term)
                        if go_term in go_namespace:
                            # print("term in namespace", go_namespace[go_term])
                            if ontology in go_namespace[go_term]:
                                # print("found")
                                pred_set.add(go_term)
                                consensus_set[go_term] += 1
                else:
                    pred_set.update(go_terms[term])
                    for go_term in go_terms[term]:
                        consensus_set[go_term] += 1
            # print(true_set)
            # print(pred_set)
            # print(consensus_set)

            consensus_set = {k: v for k, v in consensus_set.items() if v > (k_neighbours/2)}
            tp = set(true_set).intersection(set(pred_set))
            fn = set(true_set).difference(set(pred_set))
            fp = set(pred_set).difference(set(true_set))
            tn_list = set(possible_pfam_go_predictions).difference(set(pred_set))
            tn = set(tn_list).difference(set(true_set))
            precision = 0
            try:
                precision = len(tp)/(len(tp)+len(fp))
            except Exception as e:
                pass
            accuracy = 0
            try:
                accuracy = (len(tp)+len(tn))/(len(tp)+len(fn)+len(fp)+len(tn))
            except Exception as e:
                # print(str(e))
                pass
            recall = 0
            try:
                recall = len(tp)/(len(tp)+len(fn))
            except Exception as e:
                pass
            hit_rate = 0
            try:
                hit_rate = len(tp)/len(true_set)
            except Exception as e:
                pass
            mcc = 0
            try:
                mcc = ((len(tp)*len(tn))-(len(fp)*len(fn)))/math.sqrt((len(tp)+len(fp))*(len(tp)+len(fn))*(len(tn)+len(fp))*(len(tn)+len(fn)))
            except Exception as e:
                pass

            cons_tp = set(true_set).intersection(set(consensus_set))
            cons_fn = set(true_set).difference(set(consensus_set))
            cons_fp = set(consensus_set).difference(set(true_set))
            cons_tn_list = set(possible_pfam_go_predictions).difference(set(consensus_set))
            cons_tn = set(cons_tn_list).difference(set(true_set))
            cons_precision = 0
            try:
                cons_precision = len(cons_tp)/(len(cons_tp)+len(cons_fp))
            except Exception as e:
                pass
            cons_recall = 0
            try:
                cons_recall = len(cons_tp)/(len(cons_tp)+len(cons_fn))
            except Exception as e:
                pass
            cons_hit_rate = 0
            try:
                cons_hit_rate = len(cons_tp)/len(true_set)
            except Exception as e:
                pass
            cons_accuracy = 0
            try:
                cons_accuracy = (len(cons_tp)+len(cons_tn))/(len(cons_tp)+len(cons_fn)+len(cons_fp)+len(cons_tn))
            except Exception as e:
                pass
            cons_mcc = 0
            try:
                cons_mcc = ((len(cons_tp)*len(cons_tn))-(len(cons_fp)*len(cons_fn)))/math.sqrt((len(cons_tp)+len(cons_fp))*(len(cons_tp)+len(cons_fn))*(len(cons_tn)+len(cons_fp))*(len(cons_tn)+len(cons_fn)))
            except Exception as e:
                pass

            close_str = ''
            for id in pfam_set[pfamID]:
                close_str += id+":"
            close_str = close_str.rstrip(':')
            print(pfamID, close_str, len(true_set),
                  len(pred_set), len(tp), len(fn), len(fp), len(tn),
                  round(precision, 2), round(accuracy, 2), round (recall, 2), round(hit_rate, 2),
                  round(mcc, 2),
                  len(consensus_set), len(cons_tp), len(cons_fn), len(cons_fp),
                  len(cons_tn),
                  round(cons_precision, 2), round(cons_accuracy, 2), round(cons_recall, 2),
                  round(cons_hit_rate, 2), round(cons_mcc, 2), sep=",")
        except Exception as e:
            eprint(str(e))


print_accuracy(pfam_set, go_terms, go_namespace, k_neighbours, ontology)
