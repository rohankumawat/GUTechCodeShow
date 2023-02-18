# Required libraries
import requests
from collections import Counter
import re
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette("coolwarm")
sns.color_palette("ch:start=.2,rot=-.3", as_cmap=True)


# Fetch the data from the URL and decode it as text
url = 'https://www.gutenberg.org/cache/epub/100/pg100.txt'
response = requests.get(url)
text = response.text

# Tokenize the text by splitting on whitespace and punctuation
words = text.split()
for i in range(len(words)):
    words[i] = words[i].lower().strip('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')

# Remove stop words
stopwords = stopwords.words('english')
newStopWords = ["thou", "thy", "thee", "shall", "_", "would", "us", "tis", "therefore", "ever", "_exit", "could", "though", "till", "whose", "done"]
stopwords.extend(newStopWords)

# Find all words in the text
words = re.findall(r'\b\w+\b', text.lower())

# Count word frequencies
word_counts = Counter(words)
for word in list(word_counts):
    if word in stopwords:
        del word_counts[word]

# Retrieve the top 100 most frequent words and their frequencies
top_100 = word_counts.most_common(100)
for word, count in top_100:
    print(f'{word}: {count}')

# Plot the top 10 words
plt.figure(figsize=(8,5), facecolor="#f7e4e4")
ax = plt.axes()
ax.set_facecolor("#f7e4e4")
sns.barplot(x=[x[0] for x in top_100[0:10]], y=[x[1] for x in top_100[0:10]])

# set plot title and axis labels
plt.title("Frequency of Words")
plt.xlabel("Word")
plt.ylabel("Frequency")
sns.despine(right=True)
# show the plot
plt.show()