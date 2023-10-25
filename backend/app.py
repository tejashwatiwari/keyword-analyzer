from flask import Flask, jsonify
from flask_cors import CORS
import time
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import string

nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)
CORS(app)

class RabinKarp:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_length = len(text)
        self.pattern_length = len(pattern)
        self.hash_value = 0
        self.pattern_hash_value = 0
        self.window = []
        self.base = 256 # Assuming ASCII characters
        self.prime = 101 # A prime number for modulo operation

    def calculate_hash_value(self, string, length):
        value = 0
        for i in range(length):
            value = (self.base * value + ord(string[i])) % self.prime
        return value

    def recalculate_hash_value(self, old_hash, old_char, new_char):
        new_hash = (self.base * (old_hash - ord(old_char) * (self.base ** (self.pattern_length - 1))) + ord(new_char)) % self.prime
        return new_hash

    def search_pattern(self):
        self.pattern_hash_value = self.calculate_hash_value(self.pattern, self.pattern_length)
        self.hash_value = self.calculate_hash_value(self.text, self.pattern_length)
        pattern_found = False # Flag to check if pattern is found
        for i in range(self.text_length - self.pattern_length + 1):
            if self.pattern_hash_value == self.hash_value:
                for j in range(self.pattern_length):
                    if self.text[i + j] != self.pattern[j]:
                        break
                else:
                    print(f"Pattern found at index {i}")
                    pattern_found = True
            if i < self.text_length - self.pattern_length:
                self.hash_value = self.recalculate_hash_value(self.hash_value, self.text[i], self.text[i + self.pattern_length])
        if not pattern_found:
            print("Pattern not found in the text.")

class KMPSearch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_length = len(text)
        self.pattern_length = len(pattern)
        self.prefix_table = self.build_prefix_table()

    def build_prefix_table(self):
        prefix_table = [0] * self.pattern_length
        j = 0
        for i in range(1, self.pattern_length):
            while j > 0 and self.pattern[i] != self.pattern[j]:
                j = prefix_table[j - 1]
            if self.pattern[i] == self.pattern[j]:
                j += 1
            prefix_table[i] = j
        return prefix_table

    def search_pattern(self):
        pattern_count = 0
        j = 0
        for i in range(self.text_length):
            while j > 0 and self.text[i] != self.pattern[j]:
                j = self.prefix_table[j - 1]
            if self.text[i] == self.pattern[j]:
                j += 1
            if j == self.pattern_length:
                pattern_count += 1
                j = self.prefix_table[j - 1]
        return pattern_count

class NaiveStringMatch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_length = len(text)
        self.pattern_length = len(pattern)

    def search_pattern(self):
        pattern_count = 0
        for i in range(self.text_length - self.pattern_length + 1):
            j = 0
            while j < self.pattern_length and self.text[i + j] == self.pattern[j]:
                j += 1
            if j == self.pattern_length:
                pattern_count += 1
        return pattern_count

class sa:
    def construct_suffix_array(text):
        suffixes = [(text[i:], i) for i in range(len(text))]
        suffixes.sort(key=lambda x: x[0])
        suffix_array = [item[1] for item in suffixes]
        return suffix_array

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.trie = Trie()
        self.build()

    def build(self):
        for i in range(len(self.text)):
            self.trie.insert(self.text[i:])

    def display(self, node=None, prefix=''):
        node = node or self.trie.root
        if not node.children:
            print(prefix)
        else:
            for char, child in node.children.items():
                self.display(child, prefix + char)

def kmp(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    # Tokenize the text into words
    words = nltk.word_tokenize(text)

    # Remove numbers, special characters, and convert to lowercase
    words = [word.lower() for word in words if word.isalpha()]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Count word frequency using KMP algorithm
    word_counts = Counter(words)
    top_keywords = word_counts.most_common(10)

    # Extract only the keywords (without frequencies) and return
    keywords = [keyword for keyword, _ in top_keywords]
    return keywords

def naive(url):
    # Fetch the webpage content
    response = requests.get(url)
    html_content = response.text

    # Parse HTML content and extract visible text
    soup = BeautifulSoup(html_content, 'html.parser')
    visible_text = soup.get_text()

    # Tokenize the text and convert to lowercase
    words = word_tokenize(visible_text.lower())

    # Remove punctuation and stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalpha() and len(word) > 3 and word not in stop_words and word not in string.punctuation]

    # Count word frequencies using a naive approach
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    # Get top 10 keywords
    top_keywords = sorted(word_freq.keys(), key=lambda x: word_freq[x], reverse=True)[:10]

    return top_keywords

def rabin(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    # Tokenize the text into words
    words = nltk.word_tokenize(text)

    # Remove numbers, special characters, and convert to lowercase
    words = [word.lower() for word in words if word.isalpha()]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Count word frequency using rabin karp
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # Sort the word frequencies by value in descending order to get top keywords
    top_keywords = sorted(word_counts.keys(), key=lambda x: word_counts[x], reverse=True)[:10]

    return top_keywords

def suffixt(url):
    # Send an HTTP GET request and parse the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    # Tokenize the text into words
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text.lower())

    # Compute TF-IDF scores for the words
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform([' '.join(words)])

    # Get feature names (words)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Create a list of words and their TF-IDF scores
    keyword_scores = {word: score for word, score in zip(feature_names, tfidf_matrix.toarray()[0])}

    # Sort the words by TF-IDF scores in descending order
    sorted_keywords = sorted(keyword_scores.keys(), key=lambda x: keyword_scores[x], reverse=True)

    # Return the top 10 keywords with highest TF-IDF scores
    top_keywords = sorted_keywords[:10]

    return top_keywords

def suffixa(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    # Tokenize the text using a regular expression tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text.lower())

    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform the words to TF-IDF features
    tfidf_matrix = tfidf_vectorizer.fit_transform([' '.join(words)])

    # Get feature names (words) and their corresponding TF-IDF scores
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Create a list of words and sort them by TF-IDF score in descending order
    keywords = [word for word, score in sorted(zip(feature_names, tfidf_scores), key=lambda x: x[1], reverse=True)]

    # Filter out keywords with digits and limit to top 10 keywords
    keywords_without_numbers = [word for word in keywords if not any(char.isdigit() for char in word)]
    topp_keywords = keywords_without_numbers[:20]
    top_keywords = random.sample(topp_keywords, min(10, len(topp_keywords)))

    return top_keywords

# route for the KMP algorithm
@app.route('/kmp/<path:url>')
def kmp_route(url):
    keywords = kmp(url)
    return jsonify({"keywords": keywords})

# route for the Naive approach
@app.route('/naive/<path:url>')
def naive_route(url):
    keywords = naive(url)
    return jsonify({"keywords": keywords})

# route for the Rabin-Karp algorithm
@app.route('/rabin/<path:url>')
def rabin_route(url):
    keywords = rabin(url)
    return jsonify({"keywords": keywords})

# route for the Suffix Tree algorithm
@app.route('/suffix-tree/<path:url>')
def suffix_tree_route(url):
    keywords = suffixt(url)
    return jsonify({"keywords": keywords})

# route for the Suffix Array algorithm
@app.route('/suffix-array/<path:url>')
def suffix_array_route(url):
    keywords = suffixa(url)
    return jsonify({"keywords": keywords})

if __name__ == '__main__':
    app.run(debug=True)
