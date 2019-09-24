import csv
from collections import defaultdict


angles = "/home/dbuchan/Code/domain_word2vec/transform_angles.csv"
corpus = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/word2vec_input_E.dat"
summary = "/home/dbuchan/Code/domain_word2vec/word2_vec_summary.dat"

coherent_pairs = defaultdict(dict)
domain_list = set([])
with open(angles) as angles_file:
    angle_reader = csv.reader(angles_file, delimiter=',')
    angle_reader.__next__()
    for row in angle_reader:
        if float(row[5]) < 0.5 and row[0] == 'intracellular':
            coherent_pairs[row[1]]['target']=row[2]
            coherent_pairs[row[1]]['coherent']=[row[3], row[4]]
            domain_list.add(row[1])
            domain_list.add(row[2])
            domain_list.add(row[3])
            domain_list.add(row[4])

# print(coherent_pairs)

# with open(corpus) as corpus_file:
#     corpus_reader = csv.reader(corpus_file, delimiter=' ')
#     for row in corpus_reader:
#         for domain in row[1:]:
#             if domain in domain_list and len(row[1:]) > 1:
#                 print(*row, sep=",")
protein_data = {}
with open(summary) as summary_file:
    summary_reader = csv.reader(summary_file, delimiter=',')
    for row in summary_reader:
        protein_data[row[0][:-1]] = row[1:]

for domain in coherent_pairs:
    for protID in protein_data:
        if domain in protein_data[protID]:
            for protID2 in protein_data:
                if protID == protID2:
                    continue
                # print(domain)
                if coherent_pairs[domain]['target'] in protein_data[protID2]:
                    first_set = set([x for x in protein_data[protID] if x != domain])
                    second_set = set([x for x in protein_data[protID2] if x != coherent_pairs[domain]['target']])
                    if first_set.issubset(second_set):
                        p_found = False
                        for domainthis in first_set:
                            if domainthis.startswith('P'):
                                p_found = True
                        if p_found:
                            print(protID, domain, first_set, protID2, coherent_pairs[domain]['target'], second_set)
