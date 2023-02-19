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
import re

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

################################################################

# preprocessing

def remove_unnecessary_text(str_shakespeare_full: str, int_last_line: int):
    """
    Remove:
        -> the first lines
        -> the last lines
        -> the poems
        -> This piece:
            '<<THIS ELECTRONIC VERSION OF THE COMPLETE WORKS OF WILLIAM
                SHAKESPEARE IS COPYRIGHT 1990-1993 BY WORLD LIBRARY, INC., AND IS
                PROVIDED BY PROJECT GUTENBERG ETEXT OF ILLINOIS BENEDICTINE COLLEGE
                WITH PERMISSION.  ELECTRONIC AND MACHINE READABLE COPIES MAY BE
                DISTRIBUTED SO LONG AS SUCH COPIES (1) ARE FOR YOUR OR OTHERS
                PERSONAL USE ONLY, AND (2) ARE NOT DISTRIBUTED OR USED
                COMMERCIALLY.  PROHIBITED COMMERCIAL DISTRIBUTION INCLUDES BY ANY
                SERVICE THAT CHARGES FOR DOWNLOAD TIME OR FOR MEMBERSHIP.>>'
    """    
    str_pre_clean = re.sub("<(.+)\n(.+)\n(.+)\n(.+)\n(.+)\n(.+)\n(.+)\n(.+)",
                           '',
                           str_shakespeare_full)
    
    slines = str_pre_clean.splitlines(keepends=True)[1:int_last_line]
    author_count = 0
    start_line = 1
    
    for i, row in enumerate(slines):        
        # under the title always appears "by William Shakespeare"
        if 'by William Shakespeare' in row: 
            author_count += 1
        
        # position where the first play starts
        if author_count == 2:
            start_line = i - 5
            break
    
    return slines[(start_line + 2):]

dataPreClean = remove_unnecessary_text(str_shakespeare_full=text, int_last_line=122343)

dataClean = [x.lstrip() for x in dataPreClean]

newText = " ".join(str(x) for x in dataClean)

with open('data/data_preprocess.txt', mode='w') as w:
    w.write(str(newText))