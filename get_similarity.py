import gensim
import logging
import itertools

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

model = gensim.models.Word2Vec.load('/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/word2vec.model')


header = ","
for word in sorted(model.wv.vocab):
    header += word+","
header = header.rstrip(",")
print(header)

for word in sorted(model.wv.vocab):
    line = word+","
    for word2 in sorted(model.wv.vocab):
        sim = model.wv.similarity(word, word2)
        line += "%.5f" % sim + ","
    line = line.rstrip(",")
    print(line)
# for word, word2 in itertools.combinations(model.wv.vocab, 2):
#     sim = model.wv.similarity(word, word2)
#     print(word, word2, sim)
