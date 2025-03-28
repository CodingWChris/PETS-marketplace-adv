# from flask import Flask, request, render_template, redirect, url_for
# import pandas as pd
# from collections import Counter
# from nltk.tokenize import word_tokenize, sent_tokenize
# import nltk
# import re
# from wordcloud import WordCloud
# import plotly.express as px
# import plotly.graph_objects as go
# import json
# import requests
# import urllib.parse

# app = Flask(__name__)
# nltk.download('punkt')
# nltk.download('stopwords')

# def process_text(text):
#     # Clean and tokenize text
#     clean = re.compile('<.*?>')
#     text = re.sub(clean, '', text)
    
#     # Split into sentences for trend analysis
#     sentences = sent_tokenize(text)
#     tokens = word_tokenize(text.lower())
    
#     # Remove stopwords
#     stopwords = set(nltk.corpus.stopwords.words('english'))
#     tokens = [word for word in tokens if word.isalnum() and word not in stopwords]
    
#     return tokens, sentences

# def generate_visualizations(tokens, sentences):
#     # Word frequency
#     word_freq = Counter(tokens)
#     top_words = dict(word_freq.most_common(100))
    
#     # Generate trend data
#     trends = calculate_word_trends(sentences, list(top_words.keys())[:20])
    
#     # Create word cloud data
#     word_cloud_data = [{"text": word, "value": freq} for word, freq in top_words.items()]
    
#     # Create collocation data
#     collocations = get_collocations(tokens)
    
#     return {
#         'word_frequencies': top_words,
#         'word_cloud_data': word_cloud_data,
#         'trends': trends,
#         'collocations': collocations,
#         'total_words': len(tokens),
#         'unique_words': len(set(tokens))
#     }

# def calculate_word_trends(sentences, words):
#     trends = {word: [] for word in words}
#     chunk_size = max(1, len(sentences) // 10)  # Split into 10 segments
    
#     for i in range(0, len(sentences), chunk_size):
#         chunk = ' '.join(sentences[i:i+chunk_size])
#         chunk_tokens = word_tokenize(chunk.lower())
#         chunk_freq = Counter(chunk_tokens)
        
#         for word in words:
#             trends[word].append(chunk_freq[word])
    
#     return trends

# def get_collocations(tokens, window_size=5):
#     collocations = []
#     for i in range(len(tokens) - window_size):
#         window = tokens[i:i+window_size]
#         for j in range(len(window)):
#             for k in range(j+1, len(window)):
#                 collocations.append((window[j], window[k]))
#     return Counter(collocations).most_common(50)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return 'No file uploaded', 400
            
#         file = request.files['file']
#         if file.filename.endswith('.csv'):
#             df = pd.read_csv(file)
#             text = ' '.join(df['message'].dropna().tolist())
#         else:
#             text = file.read().decode('utf-8')
        
#         # Encode the text for URL
#         encoded_text = urllib.parse.quote(text)
        
#         # Redirect to Voyant Tools
#         voyant_url = f'http://localhost:8888/?input={encoded_text}'
#         return redirect(voyant_url)
        
#     return render_template('upload.html')

# if __name__ == '__main__':
#     app.run(debug=True, port=5000) 

# import requests
# from flask import Flask, render_template
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Allow all origins

# @app.route("/")
# def index():

#     return render_template("collection.html")

# app.run(port=5001)


import os
import pandas as pd
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "outputs")

@app.route("/")
def index():
    return render_template("collection.html")


# @app.route("/get_csv_data")
# def get_csv_data():
#     file_path = os.path.join(DATA_DIR, "collections.csv")
#     if os.path.exists(file_path):
#         df = pd.read_csv(file_path) 
#         return df.to_json(orient="records")  
#     return jsonify({"error": "File not found"}), 404


# @app.route("/get_json_data")
# def get_json_data():
#     file_path = os.path.join(DATA_DIR, "config.json")
#     if os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as f:
#             data = json.load(f)
#         return jsonify(data)
#     return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(port=5001, debug=True)