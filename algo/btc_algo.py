# algorithm written in Python, based on Python v3.9

import pandas as pd
import numpy as np
import os
import time
import json

# def get_job_details():
#     """Reads in metadata information about assets used by the algo"""
#     job = dict()
#     job['dids'] = json.loads(os.getenv('DIDS', None))
#     job['metadata'] = dict()
#     job['files'] = dict()
#     job['algo'] = dict()
#     job['secret'] = os.getenv('secret', None)
#     algo_did = os.getenv('TRANSFORMATION_DID', None)
#     if job['dids'] is not None:
#         for did in job['dids']:
#             # get the ddo from disk
#             filename = '/data/ddos/' + did
#             print(f'Reading json from {filename}')
#             with open(filename) as json_file:
#                 ddo = json.load(json_file)
#                 # search for metadata service
#                 for service in ddo['service']:
#                     if service['type'] == 'metadata':
#                         job['files'][did] = list()
#                         index = 0
#                         for file in service['attributes']['main']['files']:
#                             job['files'][did].append(
#                                 '/data/inputs/' + did + '/' + str(index))
#                             index = index + 1
#     if algo_did is not None:
#         job['algo']['did'] = algo_did
#         job['algo']['ddo_path'] = '/data/ddos/' + algo_did
#     return job

def get_job_details():
    root = os.getenv('ROOT_FOLDER', '')
    print('ROOT_FOLDER:', root)
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
            # local path to the file
            # Just one file for DID with name in the last ''  -> in this case "BTC_trend.json"
            job['files'][did].append(root + '/data/inputs/' + did + '/BTC_trend.json')
    if algo_did is not None:
        job['algo']['did'] = algo_did
        job['algo']['ddo_path'] = root + '/data/ddos/' + algo_did
    return job


def data_average(job_details):
    """Executes the line counter based on inputs"""
    print('Starting compute job with the following input information:')
    print(json.dumps(job_details, sort_keys=True, indent=4))

    """ Now, count the lines of the first file in first did """
    first_did = job_details['dids'][0]
    filename = job_details['files'][first_did][0]

    print("====================================")
    print('Reading JSON from:', filename)

    non_blank_count = 0
    with open(filename) as infp:
        for line in infp:
            if line.strip():
                non_blank_count += 1
    print ('number of non-blank lines found %d' % non_blank_count)

    # Read JSON data into DataFrame
    df = pd.read_json(filename)
    
    """ Calculate average of numeric column """
    avg_open = df['open'].mean() if 'open' in df.columns else None
    avg_high = df['high'].mean() if 'high' in df.columns else None
    avg_low = df['low'].mean() if 'low' in df.columns else None
    avg_close = df['close'].mean() if 'close' in df.columns else None

    sd_open = df['open'].std() if 'open' in df.columns else None
    sd_high = df['high'].std() if 'high' in df.columns else None
    sd_low = df['low'].std() if 'low' in df.columns else None
    sd_close = df['close'].std() if 'close' in df.columns else None

    skew_open = df['open'].skew() if 'open' in df.columns else None
    skew_high = df['high'].skew() if 'high' in df.columns else None
    skew_low = df['low'].skew() if 'low' in df.columns else None
    skew_close = df['close'].skew() if 'close' in df.columns else None

    print('Average Open:', avg_open)
    print('Average High:', avg_high)
    print('Average Low:', avg_low)
    print('Average Close:', avg_close)

    print('Standard Deviation Open:', sd_open)
    print('Standard Deviation High:', sd_high)
    print('Standard Deviation Low:', sd_low)
    print('Standard Deviation Close:', sd_close)

    # print('Skewness Open:', skew_open)
    # print('Skewness High:', skew_high)
    # print('Skewness Low:', skew_low)
    # print('Skewness Close:', skew_close)

    """ Print that number to output to generate algo output"""
    with open("/Users/itschris/Desktop/Pontus-X/repo/PETS-marketplace-adv/data/outputs/result", "w") as f:
        result = {
            'non_blank_lines': non_blank_count,
            'avg_open': avg_open,
            'avg_high': avg_high,
            'avg_low': avg_low,
            'avg_close': avg_close,
            'sd_open': sd_open,
            'sd_high': sd_high,
            'sd_low': sd_low,
            'sd_close': sd_close,
            # 'skew_open': skew_open,
            # 'skew_high': skew_high,
            # 'skew_low': skew_low,
            # 'skew_close': skew_close


        }
        f.write(json.dumps(result, indent=4))

if __name__ == '__main__':
    data_average(get_job_details())
