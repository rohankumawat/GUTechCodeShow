# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk
# nltk.download('punkt')

import warnings
import json
import os
import re

# import data
data = open('data/data_preprocess.txt', mode='r').read()

# bag-of-words
def create_bag_of_words(list_words: list, ngram: int) -> list:
    vec = CountVectorizer(ngram_range=(ngram, ngram),
                          stop_words="english",
                          lowercase=True)
    
    bag_of_words = vec.fit_transform(list_words)
    sum_words = bag_of_words.sum(axis=0)

    return [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]

# tf-idf
def tfidf_vectorizer(documents, total_features: int):
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95,
                                       min_df=2,
                                       max_features=total_features,
                                       stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(documents)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    return tfidf_vectorizer, tfidf, tfidf_feature_names

def count_vectorizer(documents, total_features: int):
    tf_vectorizer = CountVectorizer(max_df=0.95, 
                                    min_df=2,
                                    max_features=total_features,
                                    stop_words='english')
    tf = tf_vectorizer.fit_transform(documents)
    tf_feature_names = tf_vectorizer.get_feature_names()
    return tf_vectorizer, tf, tf_feature_names

total_features = 100000
no_top_words = 20

tfidfvectorizer, tfidf, tfidf_feature_names = tfidf_vectorizer(data,
                                                                total_features)
tf_vectorizer, tf, tf_feature_names = count_vectorizer(data, 
                                                       total_features)

bag_of_words = create_bag_of_words(list_words=data, ngram=1)

def get_top_n_words(bag_of_words, n_elements) -> list:
    return sorted(bag_of_words, key = lambda x: x[1], reverse=True)[:n_elements]

# unigram data analysis
top_20_words = get_top_n_words(bag_of_words, 20)
df_unigram = pd.DataFrame(top_20_words, columns = ['word' , 'count'])
df_unigram.head()

# bigram data analysis
bag_of_words_bigram = create_bag_of_words(data_cleansing, ngram=2)
top_20_words_bigram = get_top_n_words(bag_of_words_bigram, 20)
df_bigram = pd.DataFrame(top_20_words_bigram, columns = ['word' , 'count'])
df_bigram.head()