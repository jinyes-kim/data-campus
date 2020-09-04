import gensim
from pprint import pprint

""""
초기 모델 확인에 사용한 영문 샘플 데이터

#import gensim.downloader as api
#dataset = api.load("text8")
#data = [d for d in dataset]
"""


def tagged_document(list_of_list_of_words):
    for i, list_of_words in enumerate(list_of_list_of_words):
        yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])


data = []
with open('sample_text.txt', encoding='utf-8-sig') as file:
    for line in file:
        word = line.split()
        data.append(word)


data_for_training = list(tagged_document(data))

model = gensim.models.doc2vec.Doc2Vec(vector_size=40, min_count=2, epochs=30)
model.build_vocab(data_for_training)
model.train(data_for_training, total_examples=model.corpus_count, epochs=model.epochs)

save_as = './model/doc2vec_kr.model'
word2vec_file = save_as + ".word2vec_format"

model.save(save_as)
model.save_word2vec_format(word2vec_file, binary=False)

