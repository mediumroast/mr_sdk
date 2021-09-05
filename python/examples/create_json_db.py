import sys, pprint
sys.path.append ('../src')

from mediumroast.extractors.file import Extract as mr_extract
from mediumroast.transformers.company import Transform as xform_companies

# Establish a print function for better visibility
printer=pprint.PrettyPrinter()

# TODO define options to specify the file_name from the command line

# Capture the source data from the file specified in file_name
file_name='../sample_data/minio_share_list.txt'
src_obj=mr_extract(filename=file_name)
src_data=src_obj.get_data()

# TODO Transform the output into a string and hash it, we can then compare the hash across runs to verify correctness <-- Useful for testing

# TODO Create some README.md files to cover key thoughts around testing for the system
#   Starts with system setup of minio, running sample test scripts to ETL data, etc.

# Transform the extracted data into a proper JSON structure 
tgt_data={
    "studies": [],
    "companies": [],
    "interactions": []
}

# Create study objects

# Create interaction objects

# Create company objects
xformer=xform_companies(rewrite_config_dir='../src/mediumroast/transformers/')
tgt=xformer.create_objects(src_data)

#tgt_data.companies=tgt.companies


# Serialize to the file specified on the command line or the default

printer.pprint (tgt)