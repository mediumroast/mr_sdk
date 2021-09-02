import sys, pprint
sys.path.append ('../src')

from mediumroast.extractors.file import Extract as mr_file

# Establish a print function for better visibility
printer=pprint.PrettyPrinter()

# TODO define options to specify the file_name from the command line

# Capture the source data from the file specified in file_name
file_name='../sample_data/minio_share_list.txt'
src_obj=mr_file(filename=file_name)
src_data=src_obj.get_data()

# TODO Transform the output into a string and hash it, we can then compare the hash across runs to verify correctness

# Transform the extracted data into a proper JSON structure 

# Create study objects

# Create interaction objects

# Create company objects

# Serialize to the file specified on the command line or the default

printer.pprint (src_data)