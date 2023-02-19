# import libraries
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk
# nltk.download('punkt')

import warnings
import json
import os

#################################################################

# Fetch the data from the URL and decode it as text
url = 'https://www.gutenberg.org/cache/epub/100/pg100.txt'
response = requests.get(url)
text = response.text

count_rows = text.count('\n')
unique_char = sorted(set(text))
list_word_tokens = word_tokenize(text)

print(f'Total Rows: {count_rows}')
print(f'Total Tokens: {len(list_word_tokens)}')
print(f'Total Characters: {len(text)}')
print(f'Total Unique Character: {len(unique_char)}')
print(f'\nSample:\n{text[:500]}')