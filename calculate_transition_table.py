import numpy as np
import csv
from collections import defaultdict
import sys
from collections import Counter

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


euk_domains = '/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/' \
              'word2vec_input_E.dat'

domain_list = set()
domain_transitions = defaultdict(list)
count = 0
eprint("Gathering Transition Counts")
with open(euk_domains, 'r') as fh:
    domreader = csv.reader(fh, delimiter=' ', quotechar='|')
    for row in domreader:
        current_domains = row[1:]
        for domain in current_domains:
            domain_list.add(domain)
        for i, domain in enumerate(current_domains):
            if i+1 == len(current_domains):
                break
            domain_transitions[domain].append(current_domains[i+1])

        count += 1
        if count == 1000000:
             print("million")
        if count == 2000000:
             print("2million")
        if count == 3000000:
             print("3million")
        if count == 4000000:
             print("4million")
        if count == 5000000:
             print("5million")
        if count == 6000000:
             print("6million")
        if count == 7000000:
             print("7million")
        if count == 8000000:
             print("8million")
        if count == 9000000:
             print("9million")


eprint("Transitions Gathered")

eprint("Sorting Domains")
domain_list = sorted(domain_list)
# print(domain_list)
# print(domain_transitions)
eprint("Printing files")
counts_out = open("markov_first_order_counts.csv", "w")
probs_out = open("markov_first_order_probs.csv", "w")
title = "DOMAINS,"
for domain in domain_list:
    title += domain+","
title = title.rstrip(",")
counts_out.write(title+"\n")
probs_out.write(title+"\n")

for domain in domain_list:
    eprint(domain)
    eprint(len(domain_transitions[domain]))
    count_line = domain+","
    prob_line = domain+","
    if domain in domain_transitions:
        line_total = 0
        cnt = Counter(domain_transitions[domain])
        for domain2 in domain_list:
            count_line += str(cnt[domain2])+","
            line_total += cnt[domain2]
        for domain2 in domain_list:
            try:
                prob_line += str(cnt[domain2]/line_total)+","
            except:
                prob_line += "0.0,"
    else:
        for domain in domain_list:
            count_line += "0,"
            prob_line += "0.0,"
    count_line = count_line.rstrip(",")
    prob_line = prob_line.rstrip(",")
    counts_out.write(count_line+"\n")
    probs_out.write(prob_line+"\n")
    counts_out.flush()
    probs_out.flush()

counts_out.close()
probs_out.close()
