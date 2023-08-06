import gzip
import gensim
import logging
from gensim.models import doc2vec

class koreanWord2VecManager:

    def __init__(self):
        self.name = 'koreanWord2VecManager'

    def readInput(self, fileName):
        documents = []
        with open(fileName, mode='r',encoding='utf-8') as f:
            for line in f:
                new_doc = []
                toks = line.split()
                for tok in toks:
                    pair = tok.split("/")
                    #pair[0] #word
                    #pair[1] #pos
                    new_doc.append(pair[0])
                documents.append(new_doc)
        return documents

    def train(self, documents, modelFile):
        # build vocabulary and train model
        model = gensim.models.Word2Vec(
            documents,
            size=300,
            window=5,
            sg=1,
            min_count=5,
            workers=10)
        model.train(documents, total_examples=len(documents), epochs=50)
        model.wv.save_word2vec_format(modelFile, binary=True)


if __name__ == '__main__':
    mode = 'train'
    model_file = 'korean_sns_comments_w2v.bin'

    manager = koreanWord2VecManager()
    if mode == 'train':
        file_name = '../wiki_pos_tokenizer_with_taginfo.txt'
        text_data = manager.readInput(file_name)

        print('the number of documents ', len(text_data))

        manager.train(text_data, model_file)