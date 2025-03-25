import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk
import re

# Ensure you have the necessary NLTK resources
nltk.download('punkt')


def get_job_details():
    root = os.getenv('ROOT_FOLDER', '')
    """Reads in metadata information about assets used by the algo"""
    job = dict()
    job['dids'] = json.loads(os.getenv('DIDS', None))
    job['metadata'] = dict()
    job['files'] = dict()
    job['algo'] = dict()
    job['secret'] = os.getenv('secret', None)
    algo_did = os.getenv('TRANSFORMATION_DID', None)
    if job['dids'] is not None:
        for did in job['dids']:
            job['files'][did] = list()
            # Just one file for DID with name "0"
            job['files'][did].append(root + '/data/inputs/' + did + '/0')
    if algo_did is not None:
        job['algo']['did'] = algo_did
        job['algo']['ddo_path'] = root + '/data/ddos/' + algo_did
    return job


def voyant2_data_analysis_visualization(job_details):
    """Analyze Enron email dataset, tokenize words, and create a static visualization"""
    first_did = job_details['dids'][0]
    filename = job_details['files'][first_did][0]
    
    # Read the email dataset
    try:
        df = pd.read_csv(filename)
        
        # Combine all email bodies into a single text
        all_text = ' '.join(df['message'].dropna().tolist())
        

        # Tokenize the text
        tokens = tokenize_text(clean_email_text(all_text))
        
        # Count word occurrences
        word_counts = Counter(tokens)
        
        # Create a DataFrame from the word counts
        word_count_df = pd.DataFrame(word_counts.items(), columns=['word', 'count'])
        
        # Sort by count
        word_count_df = word_count_df.sort_values(by='count', ascending=False).head(20)  # Top 20 words
        
        # Plotting
        plt.figure(figsize=(12, 6))
        plt.barh(word_count_df['word'], word_count_df['count'], color='skyblue')
        plt.xlabel('Count')
        plt.title('Top 20 Most Frequent Words in Enron Emails')
        plt.gca().invert_yaxis()  # Invert y-axis to have the highest count on top
        plt.savefig('/data/outputs/enron_email_word_counts.png')  # Save the figure
        plt.close()  # Close the plot to free memory
        
        # Save word counts to a JSON file
        word_count_df.to_json('/data/outputs/enron_email_word_counts.json', orient='records', lines=True)
        
    except Exception as e:
        error_message = f"Error analyzing dataset: {str(e)}"
        with open("/data/outputs/error.txt", "w") as f:
            f.write(error_message)
        raise Exception(error_message)




def clean_email_text(text):
    """Clean email text by removing HTML tags and other non-text content"""
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)



def tokenize_text(text):
    """Tokenize text into words"""
    return word_tokenize(text.lower())



def local_text_voyant(filename):
    df = pd.read_csv(filename)
        
    # Combine all email bodies into a single text
    all_text = ' '.join(df['message'].dropna().tolist())
    

    # Tokenize the text
    tokens = tokenize_text(clean_email_text(all_text))
    
    # Count word occurrences
    word_counts = Counter(tokens)
    
    # Create a DataFrame from the word counts
    word_count_df = pd.DataFrame(word_counts.items(), columns=['word', 'count'])
    
    # Sort by count
    word_count_df = word_count_df.sort_values(by='count', ascending=False).head(20)  # Top 20 words
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.barh(word_count_df['word'], word_count_df['count'], color='skyblue')
    plt.xlabel('Count')
    plt.title('Top 20 Most Frequent Words in Enron Emails')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest count on top
    plt.savefig('/data/outputs/enron_email_word_counts.png')  # Save the figure
    plt.close()  # Close the plot to free memory



if __name__ == '__main__':
    # voyant2_data_analysis_visualization(get_job_details())
    local_text_voyant('../data/inputs/enron/enron_subset.csv')
