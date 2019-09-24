import csv

euk_domains = '/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/' \
              'word2vec_input_E.dat'

total_5_tuples = 0
with open(euk_domains, 'r') as fh:
    domreader = csv.reader(fh, delimiter=' ', quotechar='|')
    for row in domreader:
        current_domains = row[1:]
        domain_size = len(current_domains)
        if domain_size >= 3:
            total_5_tuples += (domain_size-3)+1

print(total_5_tuples)
