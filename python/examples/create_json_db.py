import sys, pprint
sys.path.append ('../src')

from mediumroast.extractors.file import Extract as mr_extract
from mediumroast.transformers.company import Transform as xform_companies 
from mediumroast.transformers.study import Transform as xform_studies

# Establish a print function for better visibility
printer=pprint.PrettyPrinter()

# TODO define options to specify the file_name from the command line

def extract (file_name='../sample_data/minio_share_list.txt'):
    # Capture the source data from the file specified in file_name  
    print ('Extracting data from source file [' + file_name + ']...')
    src_obj=mr_extract(filename=file_name)
    src_data=src_obj.get_data()
    no_items=len(src_data)
    print ('Extracted [' + str(no_items) + '] total items from source file [' + file_name +']...')
    return src_data


# TODO Transform the output into a string and hash it, we can then compare the hash across runs to verify correctness <-- Useful for testing

# TODO Create some README.md files to cover key thoughts around testing for the system
#   Starts with system setup of minio, running sample test scripts to ETL data, etc.



def transform_studies (src_data):
    # Create study objects
    print ('Preparing to transform extracted data into [Study] objects...')
    xformer=xform_studies(rewrite_config_dir='../src/mediumroast/transformers/', debug=True)
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

# Create interaction objects

def transform_companies(src_data):
    # Create company objects
    print ('Preparing to transform extracted data into [Company] objects...')
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



if __name__ == "__main__":
    extracted_data=extract()
    
    # Transform the extracted data into a proper JSON structure 
    transformed_data={
        "studies": [],
        "companies": [],
        "interactions": []
    }

    # Companies transformation
    #transformed_companies=transform_companies(extracted_data)

    # Studies transformation
    transformed_studies=transform_studies(extracted_data)
    
    # Serialize to the file specified on the command line or the default
    printer.pprint (transformed_studies)