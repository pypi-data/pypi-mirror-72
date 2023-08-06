from random import sample

import pandas as pd
import numpy as np
import nltk
import re

from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
from nltk import word_tokenize, PorterStemmer

# Load the model
from nltk.corpus import stopwords

model = Doc2Vec.load('tmp/1569388658926_pv_dma_dim=100_window=5_epochs=20/doc2vec.model')


def default_clean(text):
    #text = filter(lambda x: x in string.printable, text)
    if not (pd.isnull(text)):
        bad_chars = set(
        ["@", "+", '/', "'", '"', '\\', '(', ')', '', '\\n', '', '?', '#', ',', '.', '[', ']', '%', '$', '&', ';', '!',
         ';', ':', "*", "_", "=", "}", "{"])
    for char in bad_chars:
        text = text.replace(char, " ")
    text = re.sub('\d+', "", text)
    return text


def stop_and_stem(text, stem=True, stemmer=PorterStemmer()):
    '''
    Removes stopwords and does stemming
    '''
    stoplist = stopwords.words('english')
    if stem:
        text_stemmed = [stemmer.stem(word) for word in word_tokenize(text) if word not in stoplist and len(word) > 3]
    else:
        text_stemmed = [word for word in word_tokenize(text) if word not in stoplist and len(word) > 3]
        text = ' '.join(text_stemmed)
        return text


def test_predict():
    test_sample = '한국 경제가 위기에 처하다'
    # Convert the sample document into a list and use the infer_vector method to get a vector representation for it
    new_doc_words = test_sample.split()
    new_doc_vec = model.infer_vector(new_doc_words, steps=50, alpha=0.25)

    # use the most_similar utility to find the most similar documents.
    similars = model.docvecs.most_similar(positive=[new_doc_vec])
    for sim in similars:
        print(str(sim))


test_predict()