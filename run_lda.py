

import sys

import pandas as pd
import gensim
from gensim import corpora, models

# parameters
doc_thrd_abs = 15
doc_thrd_rel = 0.9
word_keep = 100000

topic_num = 10


data = pd.read_csv('comments.csv', error_bad_lines = False);
comments = data[['comment']]

processed_docs = comments['comment'].map(lambda x : x.split() if not pd.isna(x) else [])
dictionary = gensim.corpora.Dictionary(processed_docs)
dictionary.filter_extremes(
  no_below=doc_thrd_abs, 
  no_above=doc_thrd_rel, 
  keep_n = word_keep
  )
  
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

# LDA using Bag of Words
lda_model = gensim.models.LdaMulticore(
  bow_corpus, 
  num_topics = topic_num,
  id2word = dictionary,
  passes = 10,
  workers = 8
  )
with open('topic_list.txt', 'w') as tfile:
  print('The topics in lda_model using Bag of Words')
  tfile.write('The topics in lda_model using Bag of Words\n')
  for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))
    tfile.write('Topic: {} \nWords: {}'.format(idx, topic) + '\n')
  tfile.write('\n')
  
# LDA using TF-IDF
lda_model_tfidf = gensim.models.LdaMulticore(
  corpus_tfidf,
  num_topics = topic_num,
  id2word = dictionary,
  passes = 10,
  workers = 8
  )
with open('topic_list.txt', 'a') as tfile:
  print('The topics in lda_model using TF-IDF')
  tfile.write('The topics in lda_model using TF-IDF\n')
  for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))
    tfile.write('Topic: {} \nWords: {}'.format(idx, topic) + '\n')
  tfile.write('\n')


cmt_topic = list(map(
  lambda x : 
    sorted(lda_model_tfidf[x], 
      key=lambda tup: -1*tup[1])[0], 
  bow_corpus)
  )
  
data['topic_id'] = [x for x, s in cmt_topic]
data['topic_score'] = [s for x, s in cmt_topic]
data.to_csv('comments_with_topic.csv', index = False)