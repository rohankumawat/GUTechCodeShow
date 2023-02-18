# Required libraries
import requests
from collections import Counter
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette("coolwarm")
sns.color_palette("ch:start=.2,rot=-.3", as_cmap=True)

# Download the text file
url = 'https://www.gutenberg.org/cache/epub/100/pg100.txt'
response = requests.get(url)
text = response.text

# Define a function to generate n-grams
def generate_ngrams(text, n):
    # Remove stopwords and punctuation from the text
    stop_words = set(['a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 
                      'for', 'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such', 
                      'that', 'the', 'their', 'then', 'there', 'these', 'they', 'this', 'to', 'was', 
                      'will', 'with', 'exeunt', '_exeunt', '_exeunt_', '_exit', 'exit', '_exit_', 
                      'exit_', 'content', 'act', 'acts', 'scene', 'scenes',
                      'project', 'gutenberg', 'literary', 'archive', 'foundation'])
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = [word for word in text.split() if word not in stop_words]
    
    # Generate n-grams of size n
    ngrams = []
    for i in range(len(words)-n+1):
        ngrams.append(' '.join(words[i:i+n]))
    return ngrams

# Define a function to find anagrams
def find_anagrams(ngrams):
    # Create a dictionary to store the anagrams
    anagrams = {}
    
    # Loop through each n-gram and add it to the dictionary with its letters sorted
    for ngram in ngrams:
        sorted_letters = ''.join(sorted(ngram))
        if sorted_letters in anagrams:
            anagrams[sorted_letters].append(ngram)
        else:
            anagrams[sorted_letters] = [ngram]
    
    # Remove any groups of anagrams with only one word
    anagrams = {k:v for k,v in anagrams.items() if len(v) > 1}
    
    return anagrams

# Generate n-grams of length 2, 3, 4 and 5 and count their frequencies
ngram_counts = {}
for n in [2, 3, 4, 5]:
    ngrams = generate_ngrams(text, n)
    ngram_counts[n] = Counter(ngrams)

# Print the top 10 n-grams for each length
for n in [2, 3, 4, 5]:
    print(f'Top 10 {n}-grams:')
    top_ngrams = ngram_counts[n].most_common(10)
    for ngram, count in top_ngrams:
        print(f'{ngram}: {count}')
    print('')

# plot a graph for every n-gram
for n in [2, 3, 4, 5]:
    top_ngrams = ngram_counts[n].most_common(10)
    ngrams, counts = zip(*top_ngrams)
    df = pd.DataFrame({'N-gram': ngrams, 'Frequency': counts})
    plt.figure(figsize=(15,5), facecolor="#f7e4e4")
    ax = plt.axes()
    ax.set_facecolor("#f7e4e4")
    sns.barplot(x='Frequency', y='N-gram', data=df)
    plt.title(f'Top {n}-grams')
    sns.despine(right=True)
    plt.show()