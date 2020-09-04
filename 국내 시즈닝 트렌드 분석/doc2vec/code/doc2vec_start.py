import gensim
from pprint import pprint

model = gensim.models.Doc2Vec.load("./model/doc2vec_kr.model")
pprint(model.most_similar(u'시즈닝', topn=10))