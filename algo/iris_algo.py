# algorithm written in Python, based on Python v3.9

import pandas as pd
import numpy as np
import os
import time
import json

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
            # get the ddo from disk
            filename = root + '/data/ddos/' + did
            print(f'Reading json from {filename}')
            with open(filename) as json_file:
                ddo = json.load(json_file)
                # search for metadata service
                for service in ddo['service']:
                    if service['type'] == 'metadata':
                        job['files'][did] = list()
                        index = 0
                        for file in service['attributes']['main']['files']:
                            job['files'][did].append(
                                root + '/data/inputs/' + did + '/' + str(index))
                            index = index + 1
    if algo_did is not None:
        job['algo']['did'] = algo_did
        job['algo']['ddo_path'] = root + '/data/ddos/' + algo_did
    return job


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
            # get the ddo from disk
            filename = root + '/data/ddos/' + did
            print(f'Reading json from {filename}')
            with open(filename) as json_file:
                ddo = json.load(json_file)
                # search for metadata service
                for service in ddo['service']:
                    if service['type'] == 'metadata':
                        job['files'][did] = list()
                        index = 0
                        for file in service['attributes']['main']['files']:
                            job['files'][did].append(
                                root + '/data/inputs/' + did + '/' + str(index))
                            index = index + 1
    if algo_did is not None:
        job['algo']['did'] = algo_did
        job['algo']['ddo_path'] = root + '/data/ddos/' + algo_did
    return job



def iris_algo(job_details):
    root = os.getenv('ROOT_FOLDER', '')
    """Executes the line counter based on inputs"""
    print('Starting compute job with the following input information:')
    print(json.dumps(job_details, sort_keys=True, indent=4))

    """ Now, count the lines of the first file in first did """
    first_did = job_details['dids'][0]
    filename = job_details['files'][first_did][0]

    # print("====================================")
    # print('Reading dataset from:', filename)

    non_blank_count = 0
    with open(filename) as infp:
        for line in infp:
            if line.strip():
                non_blank_count += 1
    print ('number of non-blank lines found %d' % non_blank_count)

    # Read csv data into DataFrame
    df = pd.read_csv(filename)

    # result = {}

    # for column in df.columns:
    #     if pd.api.types.is_numeric_dtype(df[column]):
    #         # If the column is numeric, calculate the average
    #         result[f'avg_{column}'] = df[column].mean()
    #         print(f'Average {column}: {result[f"avg_{column}"]}')

    #     else:
    #         # If the column is categorical, count the number of unique categories
    #         result[f'num_categories_{column}'] = df[column].nunique()
    #         print(f'Number of categories in {column}: {result[f"num_categories_{column}"]}')


    # f = open(root + "/data/outputs/result", "w")
    # for key, value in result.items():
    #     f.write(f'{key}: {value}\n')
    # f.close()


    """ Calculate average of numeric column """
    avg_SepalLength = df['SepalLengthCm'].mean() if 'SepalLengthCm' in df.columns else None
    avg_SepalWidth = df['SepalWidthCm'].mean() if 'SepalWidthCm' in df.columns else None
    avg_PetalLength = df['PetalLengthCm'].mean() if 'SepalWidthCm' in df.columns else None
    avg_PetalWidth = df['PetalWidthCm'].mean() if 'PetalWidthCm' in df.columns else None

    print('Average SepalLengthCm:', avg_SepalLength)
    print('Average SepalWidthCm:', avg_SepalWidth)
    print('Average PetalLengthCm:', avg_PetalLength)
    print('Average PetalWidthCm:', avg_PetalWidth)

    """ Print that number to output to generate algo output"""
    # with open("/Users/itschris/Desktop/Pontus-X/repo/PETS-marketplace-adv/data/outputs/result", "w") as f:
    with open("data/outputs/result", "w") as f:
        result = {
            'non_blank_lines': non_blank_count,
            'avg_SepalLength': avg_SepalLength,
            'avg_SepalWidth': avg_SepalWidth,
            'avg_PetalLength': avg_PetalLength,
        }
        f.write(json.dumps(result, indent=4))

if __name__ == '__main__':
    iris_algo(get_job_details())
