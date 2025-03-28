from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import re
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import urllib.parse

app = Flask(__name__)
nltk.download('punkt')
nltk.download('stopwords')

def process_text(text):
    # Clean and tokenize text
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    
    # Split into sentences for trend analysis
    sentences = sent_tokenize(text)
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords
    stopwords = set(nltk.corpus.stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stopwords]
    
    return tokens, sentences

def generate_visualizations(tokens, sentences):
    # Word frequency
    word_freq = Counter(tokens)
    top_words = dict(word_freq.most_common(100))
    
    # Generate trend data
    trends = calculate_word_trends(sentences, list(top_words.keys())[:20])
    
    # Create word cloud data
    word_cloud_data = [{"text": word, "value": freq} for word, freq in top_words.items()]
    
    # Create collocation data
    collocations = get_collocations(tokens)
    
    return {
        'word_frequencies': top_words,
        'word_cloud_data': word_cloud_data,
        'trends': trends,
        'collocations': collocations,
        'total_words': len(tokens),
        'unique_words': len(set(tokens))
    }

def calculate_word_trends(sentences, words):
    trends = {word: [] for word in words}
    chunk_size = max(1, len(sentences) // 10)  # Split into 10 segments
    
    for i in range(0, len(sentences), chunk_size):
        chunk = ' '.join(sentences[i:i+chunk_size])
        chunk_tokens = word_tokenize(chunk.lower())
        chunk_freq = Counter(chunk_tokens)
        
        for word in words:
            trends[word].append(chunk_freq[word])
    
    return trends

def get_collocations(tokens, window_size=5):
    collocations = []
    for i in range(len(tokens) - window_size):
        window = tokens[i:i+window_size]
        for j in range(len(window)):
            for k in range(j+1, len(window)):
                collocations.append((window[j], window[k]))
    return Counter(collocations).most_common(50)
