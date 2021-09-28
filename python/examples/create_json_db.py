#!/bin/env python3

# TODO This utility should be moved to mr_json_server and removed from this repo

import sys, pprint, argparse
sys.path.append ('../src')

from mediumroast.extractors.file import Extract as mr_extract_file
from mediumroast.extractors.s3bucket import Extract as mr_extract_s3
from mediumroast.transformers.company import Transform as xform_companies 
from mediumroast.transformers.study import Transform as xform_studies
from mediumroast.transformers.interaction import Transform as xform_interactions
from mediumroast.loaders.json import Store as load_it



# TODO define options to specify the file_name from the command line

def extract_from_file (file_name='../sample_data/minio_share_list.txt'):
    # Capture the source data from the file specified in file_name  
    print ('Extracting data from source file [' + file_name + ']...')
    src_obj=mr_extract(filename=file_name)
    src_data=src_obj.get_data()
    no_items=len(src_data)
    print ('Extracted [' + str(no_items) + '] total items from source file [' + file_name +']...')
    return src_data

def extract_from_s3 (bucket_name='interactions'):
    # Capture the source data from the file specified in file_name  
    print ('Extracting data from source bucket [' + bucket_name + ']...')
    src_obj=mr_extract_s3(bucket=bucket_name)
    src_data=src_obj.get_data()
    no_items=len(src_data)
    print ('Extracted [' + str(no_items) + '] total items from source bucket [' + bucket_name +']...')
    return src_data


# TODO Transform the output into a string and hash it, we can then compare the hash across runs to verify correctness <-- Useful for testing

# TODO Create some README.md files to cover key thoughts around testing for the system
#   Starts with system setup of minio, running sample test scripts to ETL data, etc.



def transform_studies (src_data, obj_type='Study'):
    # Create study objects
    print ('Preparing to transform extracted data into [' + obj_type + '] objects...')
    xformer=xform_studies(rewrite_config_dir='../src/mediumroast/transformers/', debug=False)
    tgt=xformer.create_objects(src_data)
    sent=tgt['totalStudies']
    recieved=len(tgt['studies'])
    print ('Transformed extracted data into study objects...')
    if sent == recieved: 
        print ('Successful transformation, sent [' + str(sent) + '] and recived [' + str(recieved) + '] transformations matched...')
        return tgt
    else: 
        print ('Failed transformation, sent [' + str(sent) + '] and recived [' + str(recieved) + '] transformations don\'t match, exiting...')
        sys.exit(-1)


def transform_companies(src_data, obj_type='Company'):
    # Create company objects
    print ('Preparing to transform extracted data into [' + obj_type + '] objects...')
    xformer=xform_companies(rewrite_config_dir='../src/mediumroast/transformers/', debug=False)
    tgt=xformer.create_objects(src_data)
    sent=tgt['totalCompanies']
    recieved=len(tgt['companies'])
    print ('Transformed extracted data into company objects...')
    if sent == recieved: 
        print ('Successful transformation, sent [' + str(sent) + '] and recived [' + str(recieved) + '] transformations matched...')
        return tgt
    else: 
        print ('Failed transformation, sent [' + str(sent) + '] and recived [' + str(recieved) + '] transformations don\'t match, exiting...')
        sys.exit(-1)


def transform_interactions(src_data, obj_type='Interaction'):
    # Create interaction objects
    print ('Preparing to transform extracted data into [' + obj_type + '] objects...')
    xformer=xform_interactions(rewrite_config_dir='../src/mediumroast/transformers/', debug=True)
    tgt=xformer.create_objects(src_data)
    sent=tgt['totalInteractions']
    recieved=len(tgt['interactions'])
    print ('Transformed extracted data into interaction objects...')
    if sent == recieved: 
        print ('Successful transformation, sent [' + str(sent) + '] and recived [' + str(recieved) + '] transformations matched...')
        return tgt
    else: 
        print ('Failed transformation, sent [' + str(sent) + '] and recived [' + str(recieved) + '] transformations don\'t match, exiting...')
        sys.exit(-1)

def parse_cli_args(program_name='create_json_db', desc='A mediumroast.io example utility that exercises ETLs to create a JSON file for usage in the Node.js json-server.'):
    parser=argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument ('--src_location', help="Can be one of s3, filesystem or file, but defaults to s3", type=str, dest='src_location', default='s3')
    parser.add_argument ('--src_container', help="The path to the source data to be used for ETL", type=str, dest='src_container')
    parser.add_argument ('--src_file', help="The name of the file to use for input of the source data", type=str, dest='src_file')
    parser.add_argument ('--s3_url', help="Using either IP or hostname the network address and port for the S3 compatible object store", type=str, dest='s3_url')
    parser.add_argument ('--s3_access_key', help="S3 access key or user name", type=str, dest='s3_access_key')
    parser.add_argument ('--s3_secret_key', help="S3 secret key", type=str, dest='s3_secret_key')
    parser.add_argument ('--output_json', help="The full path to the JSON output file", type=str, dest='output_json', default='/tmp/mr_db.json')
    cli_args = parser.parse_args ()
    return cli_args


if __name__ == "__main__":
    # Establish a print function for better visibility, parse cli args, and setup
    printer=pprint.PrettyPrinter()
    my_args=parse_cli_args()
    loader=load_it(filename=my_args.output_json)
    
    # Extract the data from the source
    if my_args.src_location == 'file':
        extracted_data=extract_from_file()
    elif my_args.src_location == 's3':
        extracted_data=extract_from_s3()
    else:
        print('Invalid or unsupported location type specified, please try either file or s3')
        sys.exit(-1)

    
    # Transform the extracted data into a proper JSON structure suitable for Node.js json-server
    transformed_data={
        "studies": [],
        "companies": [],
        "interactions": []
    }

    # Companies transformation
    transformed_data['companies']=transform_companies(extracted_data)['companies']

    # Studies transformation
    transformed_data['studies']=transform_studies(extracted_data)['studies']
    
    # Interactions transformation
    transformed_data['interactions']=transform_interactions(extracted_data)['interactions']
    
    # TODO Add the corpus information to the study object
    # NOTE we can consider the corpus object to look like the key themes that is linked by a number.
    #   This would suggest we have corpusNames or iterationNames={1: foo, 2: bar}, 
    #   keyQuestions={1: {1: q1, 2: q2}}, linkedInteractions={1:{name: guid, name: guid}}
    # NOTE the new keyQuestions could have a None entry...

    # Interactions transformation
    # Ph1 done without the abstracts <-- This is in testing
    # Ph2 
    # 1. read the corpus intelligence from each study
    # 2. generate the relevant abstracts
    # 3. add the abstracts into the relevant interaction
    # 4. proceed to the next study
    
    # Serialize to the file specified on the command line or the default
    status, result=loader.persist(transformed_data)
    if status:
        print(result)
    else:
        print('Creation of the JSON DB failed with: ' + result)
        sys.exit(-1)