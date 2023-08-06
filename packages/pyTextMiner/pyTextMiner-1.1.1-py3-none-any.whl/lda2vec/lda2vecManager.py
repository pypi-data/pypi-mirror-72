import numpy as np
from sklearn.datasets import fetch_20newsgroups
import torch

import matplotlib.pyplot as plt

# pip install git+https://github.com/DmitryUlyanov/Multicore-TSNE
from MulticoreTSNE import MulticoreTSNE as TSNE

def softmax(x):
    # x has shape [batch_size, n_classes]
    e = np.exp(x)
    n = np.sum(e, 1, keepdims=True)
    return e/n

dataset = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
docs = dataset['data']

# store each document with an initial id
docs = [(i, doc) for i, doc in enumerate(docs)]

# "integer -> word" decoder
decoder = np.load('decoder.npy')[()]

# for restoring document ids, "id used while training -> initial id"
doc_decoder = np.load('doc_decoder.npy')[()]

# original document categories
targets = dataset['target']
target_names = dataset['target_names']
targets = np.array([targets[doc_decoder[i]] for i in range(len(doc_decoder))])


state = torch.load('model_state.pytorch', map_location=lambda storage, loc: storage)
n_topics = 25

doc_weights = state['doc_weights.weight'].cpu().clone().numpy()
topic_vectors = state['topics.topic_vectors'].cpu().clone().numpy()
resulted_word_vectors = state['neg.embedding.weight'].cpu().clone().numpy()

# distribution over the topics for each document
topic_dist = softmax(doc_weights)

# vector representation of the documents
doc_vecs = np.matmul(topic_dist, topic_vectors)

similarity = np.matmul(topic_vectors, resulted_word_vectors.T)
most_similar = similarity.argsort(axis=1)[:, -10:]

for j in range(n_topics):
    topic_words = ' '.join([decoder[i] for i in reversed(most_similar[j])])
    print('topic', j + 1, ':', topic_words)

tsne = TSNE(perplexity=200, n_jobs=4)
X = tsne.fit_transform(doc_vecs.astype('float64'))


def plot(X):
    # X has shape [n_documents, 2]

    plt.figure(figsize=(16, 9), dpi=120);
    cmap = plt.cm.tab20
    number_of_targets = 20

    for i in range(number_of_targets):

        label = target_names[i]
        size = 15.0
        linewidths = 0.5
        edgecolors = 'k'
        color = cmap(i)

        if 'comp' in label:
            marker = 'x'
        elif 'sport' in label:
            marker = 's'
            edgecolors = 'b'
        elif 'politics' in label:
            marker = 'o'
            edgecolors = 'g'
        elif 'religion' in label:
            marker = 'P'
            size = 17.0
        elif 'sci' in label:
            marker = 'o'
            size = 14.0
            edgecolors = 'k'
            linewidths = 1.0
        elif 'atheism' in label:
            marker = 'P'
            size = 18.0
            edgecolors = 'r'
            linewidths = 0.5
        else:
            marker = 'v'
            edgecolors = 'm'

        plt.scatter(
            X[targets == i, 0],
            X[targets == i, 1],
            s=size, c=color, marker=marker,
            linewidths=linewidths, edgecolors=edgecolors,
            label=label
        );

        leg = plt.legend()
        leg.get_frame().set_alpha(0.3)

plot(X)  # learned document vectors

# different colors and markers represent
# ground truth labels of each document

# open this image in new tab to see it better

doc_weights_init = np.load('doc_weights_init.npy')

tsne = TSNE(perplexity=200, n_jobs=4)
Y = tsne.fit_transform(doc_weights_init.astype('float64'))

# to initialize topic assignments for lda2vec algorithm
# I run normal LDA and used output distributions over topics
# of each document

plot(Y)  # distribution over the topics for each document (output of LDA)

# different colors and markers represent
# ground truth labels of each document

# open this image in new tab to see it better

tsne = TSNE(perplexity=200, n_jobs=4)
Z = tsne.fit_transform(topic_dist.astype('float64'))


plot(Z)  # learned distribution over the topics for each document

# these are topic assignments as on the plot above
# but these ones are after the training of lda2vec

# different colors and markers represent
# ground truth labels of each document

# open this image in new tab to see it better

# distribution of nonzero probabilities
dist = topic_dist.reshape(-1)
plt.hist(dist[dist > 0.01], bins=40);

# distribution of probabilities for some random topic
plt.hist(topic_dist[:, 10], bins=40);

# topic assignments for two random topics
plt.scatter(topic_dist[:, 10], topic_dist[:, 20]);

# correlation of topic assignments
corr = np.corrcoef(topic_dist.transpose(1, 0))
plt.imshow(corr);
plt.colorbar();

i = 100 # document id

print('DOCUMENT:')
print([doc for j, doc in docs if j == doc_decoder[i]][0], '\n')

print('DISTRIBUTION OVER TOPICS:')
s = ''
for j, p in enumerate(topic_dist[i], 1):
    s += '{0}:{1:.3f}  '.format(j, p)
    if j%6 == 0:
        s += '\n'
print(s)

print('\nTOP TOPICS:')
for j in reversed(topic_dist[i].argsort()[-3:]):
    topic_words = ' '.join([decoder[i] for i in reversed(most_similar[j])])
    print('topic', j + 1, ':', topic_words)

