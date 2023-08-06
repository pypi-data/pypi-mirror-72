# imports needed and logging
from __future__ import unicode_literals
import gzip
import gensim
import logging
from gensim.models import Word2Vec

class word2vecManager:
    def __init__(self):
        name = "word2vecManager"

    def read_input(self, input_file):
        """This method reads the input file which is in gzip format"""
        logging.info("reading file {0}...this may take a while".format(input_file))
        with gzip.open(input_file, 'rb') as f:
            for i, line in enumerate(f):
                if (i % 10000 == 0):
                    logging.info("read {0} reviews".format(i))
                # do some pre-processing and return list of words for each review
                # text
                yield gensim.utils.simple_preprocess(line)


    def train(self, documents, modelFile):
        # build vocabulary and train model
        model = gensim.models.Word2Vec(
            documents,
            size=150,
            window=10,
            sg=0,
            min_count=1,
            workers=10)
        model.train(documents, total_examples=len(documents), epochs=50)
        model.wv.save_word2vec_format(modelFile, binary=True)

    def load(self, modelFile):
        model = gensim.models.KeyedVectors.load_word2vec_format(modelFile, binary=True, unicode_errors='ignore')
        return model


if __name__ == '__main__':
    import pyTextMiner as ptm
    import io
    import nltk

    corpus = ptm.CorpusFromFile('../donald.txt')
    pipeline = ptm.Pipeline(ptm.splitter.NLTK(), ptm.tokenizer.Komoran(),
                            ptm.helper.POSFilter('NN*'),
                            ptm.helper.SelectWordOnly(),
                            ptm.helper.StopwordFilter(file='../stopwordsKor.txt'),
                            ptm.ngram.NGramTokenizer(3))

    result = pipeline.processCorpus(corpus)

    text_data = []
    for doc in result:
        new_doc = []
        for sent in doc:
            for _str in sent:
                if len(_str) > 0:
                    new_doc.append(_str)
        text_data.append(new_doc)

    mode = 'test'
    model_file = 'w2v.model'
    if mode == 'train':
        word2vecManager().train(text_data, model_file)
    else:
        model = word2vecManager().load(model_file)
        # Some predefined functions that show content related information for given words
        try:
            print(model.most_similar(positive=['이재명'], topn=5))
            print(model.similar_by_word('이재명'))
            #print("distance " + model.distance('이재명', '문재인'))

        except:
            print('not found')

