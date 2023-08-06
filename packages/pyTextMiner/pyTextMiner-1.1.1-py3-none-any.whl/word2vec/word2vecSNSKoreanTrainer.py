import multiprocessing
from time import time
import gensim
import pyTextMiner as ptm

path = '/usr/local/lib/mecab/dic/mecab-ko-dic'

cores = multiprocessing.cpu_count() # Count the number of cores in a computer

print('Start reading the dataset 1....')
pipeline = ptm.Pipeline(ptm.splitter.KoSentSplitter(),
                        ptm.tokenizer.MeCab(path),
                        ptm.lemmatizer.SejongPOSLemmatizer(),
                        ptm.helper.SelectWordOnly(),
                        ptm.helper.StopwordFilter(file='./stopwords/stopwordsKor.txt'))

corpus1 = ptm.CorpusFromFieldDelimitedFile('/Data/ko_sns_comments/naver_comment_2016_only.txt',1)
corpus2 = ptm.CorpusFromFieldDelimitedFile('/Data/ko_sns_comments/naver_comment_2015_only.txt',1)

corpus = corpus1 + corpus2
result = pipeline.processCorpus(corpus)
documents = []
for doc in result:
    document = []
    for sent in doc:
        document.append(sent.split())
    documents.append(document)

print('Document size for the total dataset: ' + str(len(documents)))

model = gensim.Word2Vec(min_count=5,
                        window=5,
                        size=300,
                        sample=6e-5,
                        alpha=0.03,
                        min_alpha=0.0007,
                        negative=20,
                        workers=cores-1)

modelFile = './korean_sns_comments_w2v.bin'

t = time()
model.build_vocab(documents, progress_per=10000)
print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

model.train(documents, total_examples=model.corpus_count, epochs=30, report_delay=1)
print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

model.wv.save_word2vec_format(modelFile, binary=True)