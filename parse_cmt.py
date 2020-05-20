
import time

import json
import string
import csv
import re

import nltk
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

datafile = open('total.json', 'r')
resfile = open('comments-8.csv', 'w', newline='')
cmtwriter = csv.writer(resfile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
cmtwriter.writerow(['host_id', 'create_time', 'comment', 'rating', 'guest_id']) # host_id, data time, comment
table = str.maketrans(string.punctuation, ' '*len(string.punctuation))

data = json.load(datafile)

rev_count = 0
tmp_id = ""
words = set(nltk.corpus.words.words())
# stop_words = [w for w in stopwords.words('english') if not w in ['not', 'nor', 'no']] + ['us', ]
stop_words = stopwords.words('english')

lmtizer = WordNetLemmatizer()
sno = nltk.stem.SnowballStemmer('english')

# sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

clean_cmt = []

def prep(cmt):
  tk_list = [w.lower() for w in nltk.word_tokenize(cmt) if w.lower() in words] 
  # tk_list = [w for w in tk_list if (not w in stop_words) and (w in words) ] # if w in words]
  
  '''
  # comments-1.csv
  # only lemmatize with default type
  # elimate words in stopwords
  # lt_list = [lmtizer.lemmatize(word) for word in tk_list]
  # comments-5.csv
  # use stem
  lt_list = [sno.stem(word) for word in tk_list]
  '''
  
  '''
  # comments-2.csv
  # filter of NN and NNS, then lemmatize
  # remove stopwords
  lt_list = []
  for word, tag in pos_tag(tk_list):
    if tag == 'NN' or tag == 'NNS':
      pos = 'n'
    else:
      continue
    # lt_list.append(lmtizer.lemmatize(word, pos))
    lt_list.append(sno.stem(word))
  # comments-6.csv
  '''
  
  '''
  # comments-3.csv
  # NN, NNS, JJ and RB, with lemmatization
  # remove stopwords
  lt_list = []
  for word, tag in pos_tag(tk_list):
    if tag == 'NN' or tag == 'NNS':
      pos = 'n'
    elif tag.startswith('JJ') or \
      tag.startswith('RB'):
      pos = 'a'
    else:
      continue
    # lt_list.append(lmtizer.lemmatize(word, pos))
    lt_list.append(sno.stem(word))
  # comments-7.csv
  '''
  
  
  # comments-4.csv
  # norn, verb, ad. with lemmatization
  # remove stopwords
  lt_list = []
  for word, tag in pos_tag(tk_list):
    if tag == 'NN' or tag == 'NNS':
      pos = 'n'
    elif tag.startswith('VB'):
      pos = 'v'
    elif tag.startswith('JJ') or \
          tag.startswith('RB'):
      pos = 'a'
    else:
      continue    
    # lt_list.append(lmtizer.lemmatize(word, 'v')) # sno.stem
    lt_list.append(sno.stem(word))
  # comments-8.csv
  
  return [w for w in lt_list if (not w in stop_words)] # and w in words]
  

for host_data in data:
  reviews = json.loads(host_data['res'])['reviews']
  for review in reviews:
    if review['language'] != 'en':
      continue
    t_review = prep(review['comments'])
    clean_cmt.append(t_review)
  # print(time.ctime())
    
fdist = nltk.FreqDist([x for wl in clean_cmt for x in wl])
# print(fdist.most_common())
word_list = [w for w, f in fdist.most_common() if f > 1]
  

for host_data in data:
  host_id = host_data['host_id']
  reviews = json.loads(host_data['res'])['reviews']
  if tmp_id != host_id:
    # rev_count += json.loads(host_data['res'])['metadata']['reviews_count']
    tmp_id = host_id
  for review in reviews:
    # cmt = re.sub('[,\.!?]', ' ', review['comments'])
    if review['language'] != 'en':
      continue
    creattime = review['created_at']
    cmtwriter.writerow([host_id, creattime, 
            " ".join([w for w in prep(review['comments']) if w in word_list]), review['rating'],
            review['author']['id']]) 
    # review['comments'].translate(table)
    rev_count += 1
  
datafile.close()
resfile.close()

print(rev_count)


# LDA section

# documents['comment'].map(lambda x : x.split() if not pd.isna(x) else [])
