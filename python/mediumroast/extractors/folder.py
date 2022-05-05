__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2022 mediumroast.io. All rights reserved."

import os, datetime, re, spacy
from mediumroast.helpers import utilities

class Extract:
    """Perform raw data extract from a folder structure, which is then passed to a human for correction.

    In this form of extraction a folder and one layer deep subfolders is interrogated for key data.  These
    data are then used to generate Mediumroast objects.

    We assume that the topmost folder is the study and any subfolders are substudies. However, if any
    subfolder itself contains a subfolder we won't process it.

    Args:
        dir_name (str): The fully qualified path name (default is '../../sample_data/sample_dir')
        base_url (str): A base URL to use when addressing the files

    Returns:
        list: A list of dicts which can be further processed

    Methods:
        get_data()
            Traverse a simple folder/directory structure infering basics to create objects

    """

    def __init__ (self, dir_name='../../sample_data/sample_dir', base_url='file://', model = 'en_core_web_lg'):
        self.folder = dir_name
        self.base_url = base_url
        self.TRAVERSE_LIMIT = 1 # Define how deep we can go from a directory perspective
        self.idx = 0 # Set the base indexer for substudies

        # Create the nlp obj for NER via spacy
        self.nlp = spacy.load(model)

        # We will use this to determine substudy metadata later
        self.substudies = {}
        
        # Pull in helper utilities so we don't need to repeat simple things
        self.util=utilities()
        
        # Create a default date at the parent object level
        the_time = datetime.datetime.now()
        self.date = the_time.strftime("%Y%m%d") # Format YYYYMM
        self.time = the_time.strftime("%H%M") # Format HHMM

    ### Internal helper methods
    
    def _decode_folder(self, folder, folder_data, can_traverse = 1):
        # Assume if we're at the topmost folder then that's the study name otherwise it is a substudy name
        self.substudy_name = 'default'
        if can_traverse > 0: 
            self.study_name = folder.split('/')[-1]
        else: 
            self.substudy_name = folder.split('/')[-1]
            self.substudies[folder.split('/')[-1]] = {'index': self.idx}
            self.idx+=1
        
        # Temp storage for the folders
        raw_data = []
        for item in folder_data:
            item_type = 'Unknown' # Defaults to Unknown, and is set below
            item_type = 'directory' if os.path.isdir(folder + '/' + item) else self.util.get_item_type(folder, item)

            if item_type == 'directory' and can_traverse > 0:
                my_items = self._decode_folder(folder + '/' + item, os.listdir(folder + '/' + item), can_traverse = 0)
                raw_data+=my_items
                can_traverse = can_traverse - self.TRAVERSE_LIMIT
            elif item_type != 'directory':
                raw_data.append({
                    'raw_name': item,
                    'interaction_name': item.split('.')[0],
                    'full_path': folder + '/' + item,
                    'type': item_type,
                    'temp_id': self.util.hash_it(item + self.folder + '/' + item + item_type), # This is temporary
                    'substudy': self.substudy_name,
                    'study': self.study_name,
                    'url': self.base_url + folder + '/' + item
                })
            else:
                continue

        return raw_data


    def _get_objects(self):
        my_objs = self._decode_folder(self.folder, os.listdir(self.folder))
        # Get dates and raw text from the objects if the type is supported
        for obj_idx in my_objs:
            my_obj = my_objs[obj_idx]
             # Extract essential metadata from PDFs
            if re.match(r'^PDF', my_obj['type'], re.IGNORECASE):
                [my_meta, my_text] = self._get_pdf_meta(sub_folder + '/' + item)
                doc = nlp(my_text)
                if 'xap' in my_meta:
                    raw_date = my_meta['xap']['CreateDate']
                    [date, time] = raw_date.split('T')
                    date = date.replace('-', '')
                    time = ''.join(time.split('-')[0].split(':')[0:2])
                for my_ent in doc.ents:
                    my_text = re.sub(r'\n+', ' ', my_ent.text)
                    entities.append([my_text, my_ent.label_, spacy.explain(my_ent.label_)])


            # Extract essential metadata from PPTX
            elif re.match(r'^Microsoft PowerPoint', my_obj['type'], re.IGNORECASE): 
                my_meta = self._get_pptx_meta(sub_folder + '/' + item)
                date = my_meta['CreateDate'].strftime("%Y%m%d")
                time = my_meta['CreateDate'].strftime("%H%M")

            # Extract essential metadata from DOCX
            elif re.match(r'^Microsoft Word', my_obj['type'], re.IGNORECASE):
                my_meta = self._get_docx_meta(sub_folder + '/' + item)
                date = my_meta['CreateDate'].strftime("%Y%m%d")
                time = my_meta['CreateDate'].strftime("%H%M")

            doc = self.nlp(my_text)


        



    ### Main extraction method

    def get_data (self):
        """Read content from a folder to extract key metadata from file names
        """
        return self._get_objects()

        