
import gensim

model = gensim.models.Word2Vec.load('ko.bin')

#a=model.wv.most_similar(positive=['강아지','사람'],negative=['어미'],topn=20)
#positive=None, negative=None, topn=10
a=model.wv.most_similar('사람')

print(a)


