import numpy as np
import csv
from scipy.spatial import distance
from sklearn.metrics.pairwise import euclidean_distances

file = 'markov_first_order_probs.csv'

domain_list = []
prob_list = []
count = 0
with open(file, "r") as probs:
    domreader = csv.reader(probs, delimiter=',', quotechar='|')
    for row in domreader:
        if count == 0:
            count += 1
            continue
        domain_list.append(row[0])
        probs = row[1:]
        probs = [float(i) for i in probs]
        prob_list.append(probs)
        count += 1
        # if count == 11:
        #     break

prob_mat = np.array(prob_list)

row_distances = euclidean_distances(prob_mat, prob_mat)
prob_mat_t = prob_mat.transpose()
col_distances = euclidean_distances(prob_mat_t, prob_mat_t)
distance_mat = np.add(row_distances, col_distances)

title = "DOMAIN,"
for domain in domain_list:
    title += domain+","
title = title.rstrip(',')
print(title)

for i, row in enumerate(distance_mat):
    line = domain_list[i]+","
    for element in row:
        line += str(element)+','
    line = line.rstrip(',')
    print(line)
