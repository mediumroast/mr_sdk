import sys, pprint
sys.path.append ('../src')

from mediumroast.extractors.s3bucket import Extract as mr_extract

def extract (bucket_name='interactions'):
    # Capture the source data from the file specified in file_name  
    print ('Extracting data from source bucket [' + bucket_name + ']...')
    src_obj=mr_extract(bucket=bucket_name)
    src_data=src_obj.get_data()
    no_items=len(src_data)
    print ('Extracted [' + str(no_items) + '] total items from source bucket [' + bucket_name +']...')
    return src_data

if __name__ == '__main__':
    # Establish a print function for better visibility
    printer=pprint.PrettyPrinter()
    printer.pprint(extract())