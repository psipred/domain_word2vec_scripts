import gensim
import logging
import itertools
import math
import scipy.spatial
import numpy

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

model = gensim.models.Word2Vec.load('/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/word2vec_E.model')

header = ","
for word in sorted(model.wv.vocab):
    header += word+","
header = header.rstrip(",")
print(header)

dist = 0
for word in sorted(model.wv.vocab):
    line = word+","
    for word2 in sorted(model.wv.vocab):
        sim = model.wv.similarity(word, word2)
        if math.isclose(1.0, sim, rel_tol=1e-8):
            dist = 0
        elif sim > float(1):
            exit()
        else:
            try:
                dist = math.acos(sim)/math.pi
            except Exception as e:
                print("hi")
                print(sim)
                exit()
        line += "%.5f" % dist + ","
    line = line.rstrip(",")
    print(line)


# for word in sorted(model.wv.vocab):
#     line = word+","
#     for word2 in sorted(model.wv.vocab):
#         vec1 = model.wv[word]
#         vec2 = model.wv[word2]
#         cos_dist = scipy.spatial.distance.cosine(vec1, vec2)
#         line += "%.5f" % cos_dist + ","
#     line = line.rstrip(",")
#     print(line)
