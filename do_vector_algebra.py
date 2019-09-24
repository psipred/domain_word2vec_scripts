from __future__ import print_function
import gensim
import logging
import itertools
import math
import scipy.spatial
import numpy as np
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# most common pfam domains less the one that isn't in Eukaryotes (only 19)
top_twenty = ['PF00400', 'PF00005', 'PF00069', 'PF07690', 'PF00072',
              'PF12796', 'PF00528', 'PF02518', 'PF13855', 'PF00076', 'PF00271',
              'PF13041', 'PF00153', 'PF00041', 'PF00501', 'PF07679', 'PF00106',
              'PF01535', 'PF00512', ]



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

model = gensim.models.Word2Vec.load('/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/word2vec_E.model')
vocab = sorted(model.wv.vocab)
print("domain1,domain2,domain result,cosine distance")
for domain in top_twenty:
    vector1 = model.wv[domain]
    for domain2 in vocab:
        if domain == domain2:
            continue
        eprint(domain, domain2)
        out_str = domain+","+domain2
        vector2 = model.wv[domain2]
        alt_vec_1 = np.subtract(vector1, vector2)
        alt_vec_2 = np.subtract(vector2, vector1)
        nearest_set_1 = model.wv.similar_by_vector(alt_vec_1, topn=1)
        nearest_set_2 = model.wv.similar_by_vector(alt_vec_2, topn=1)
        if (nearest_set_1[0][0] != domain and nearest_set_1[0][0] != domain2) and nearest_set_1[0][1] < 0.3:
            print(out_str,  nearest_set_1[0][0], nearest_set_1[0][1], sep=",")
        if (nearest_set_2[0][0] != domain and nearest_set_2[0][0] != domain2) and nearest_set_2[0][1] < 0.3:
            print(out_str,  nearest_set_2[0][0], nearest_set_2[0][1], sep=",")
