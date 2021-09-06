__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-31'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

from os import sep
import sys, re
sys.path.append('../')

from mediumroast.helpers import utilities
from mediumroast.helpers import companies
from mediumroast.helpers import interactions
import configparser as conf

class Transform:
    """Perform transformation of input data into a proper company object.

    Returns:
        list: A list of dicts which can be pass along to additional 

    Methods:
        get_description()
            Lookup a company description from the configuration file and return it.

        get_industry()
            Lookup a company industry from the configuration file and return it.

        create_objects()
            Using the attributes set when the object was constructed get the data from the file.
    """

    def __init__ (self, rewrite_config='./study.ini', debug=False):
        self.RAW_COMPANY_NAME=7
        self.RAW_STUDY_NAME=6
        self.RAW_DATE=0
        self.REGION=1
        self.COUNTRY=2
        self.STATE_PROVINCE=3
        self.CITY=4
        
        # TODO wrap a try catch loop around the config file read
        self.rules=conf.ConfigParser()
        self.rules.read(str(rewrite_config))

        # This imports the local utilies from mr_sdk for Python
        self.util=utilities()

        # Set debug to true or false
        self.debug=debug

    def _transform_study (self, study_name, extended_rewrite=False):
        """Internal method to rewrite or augment key aspects of a study object as per definitions in the configuration file."""
        
        # Add the items which are either rewritten or not present in the file_name metadata.
        name=self.rules.get('names', study_name) if self.rules.has_option('names', study_name) else study_name
        groups=self.rules.get('groups', study_name) if self.rules.has_option('groups', study_name) else self.rules.get('DEFAULT', 'groups')
        description=self.rules.get('descriptions', study_name) if self.rules.has_option('descriptions', study_name) else self.rules.get('DEFAULT', 'description')
        security_scope=self.rules.get('security_scopes', study_name) if self.rules.has_option('security_scopes', study_name) else self.rules.get('DEFAULT', 'security_scope')
        security_scope=True if security_scope == 'True' else False
    

        return {'name': name, 
                'groups': groups,
                'public': security_scope, 
                'description': description}


    def _reformat_name(self, study_name, separator='_'):
        """Internal method to reformat the study name by replacing spaces with the separator."""
        return study_name.replace(' ', separator)

    # Transform either default or study specific keythemes into the proper data structure
    def _get_keythemes(self, study_name):
        """Internal method to rewrite or augment key aspects of a study object as per definitions in the configuration file."""
        pass

    # Transform either default or study specific keytheme quotes into the proper data structure
    def _quotes_helper(self, section, separator='<->', sub_separator='|'):
        """Helper method for _get_keytheme_quotes to obtain, parse, format and return the quotes"""
        quotes={}
        many_quotes=re.compile(separator) # For the case when there are more than 1 quote per theme
        for idx in list(self.rules[section]):
            if many_quotes.search(self.rules[section][idx]): # More than 1 quote
                for set in self.rules[section][idx].split(separator):
                    (quote, name)=set.split(sub_separator)
                    quotes[idx][name]=quote
            else: # Only 1 quote
                (quote, name)=set.split(sub_separator)
                quotes[idx][name]=quote
        return quotes

    def _get_keytheme_quotes (self, study_name, default='DEFAULT_KeyTheme_Quotes'):
        """Internal method to obtain either the default set of keytheme quotes or the study specific set of quotes."""
        section=self._reformat_name(study_name) + '_KeyTheme_Quotes'
        quotes=self._quotes_helper(section) if self.rules.has_section(section) else self._quotes_helper(default)
        return quotes

    # Transform either default or study specific keytheme frequencies into the proper data structure
    def _frequencies_helper(self, section, separator=',', sub_separator='|'):
        """Helper method for _get_keytheme_frequencies to obtain, parse, format and return the frequencies."""
        frequencies={}
        for idx in list(self.rules[section]):
            for set in self.rules[section][idx].split(separator):
                (name, frequency)=set.split(sub_separator)
                frequencies[idx][name]=frequency
        return frequencies

    def _get_keytheme_frequencies(self, study_name, default='DEFAULT_KeyTheme_Frequencies'):
        """Internal method to obtain either the default set of keytheme frequencies or the study specific set of frequencies."""
        section=self._reformat_name(study_name) + '_KeyTheme_Frequencies'
        frequencies=self._frequencies_helper(section) if self.rules.has_section(section) else self._frequencies_helper(default)
        return frequencies

    
    def _questions_helper(self, section, separator='|'):
        """Helper method for _get_keyquestions to obtain, parse, format and return the questions."""
        questions={}
        for idx in list(self.rules[section]):
            question=self.rules[section][idx].split(separator)
            state=True if question[1] == 'True' else False
            questions[idx]={
                "question": question[0],
                "notes": question[2],
                "included": state
            }
        return questions

    def _get_keyquestions(self, study_name, default='DEFAULT_Questions'):
        """Internal method to obtain either the default set of questions or the study specific set of questions."""
        section=self._reformat_name(study_name) + '_Questions'
        questions=self._questions_helper(section) if self.rules.has_section(section) else self._questions_helper(default)
        return questions


    def _get_document (self, study_name):
        """Internal method to rewrite or augment key aspects of a study object as per definitions in the configuration file."""
        pass


    def create_objects (self, raw_objects, file_output=True):
        """Create study objects from a raw list of input data.

        As this is the main transformation function of the class enabling a properly formatted set of objects that can
        either be passed to a file or the backend.  The former is more for advancing the GUI, etc. while the latter
        is related to exercising the entire system.

        Args:
            raw_objects (list): Raw objects generated from a one of the extractor methods.

        Returns:
            dict: An object containing a list of all study objects and the total number of study objects processed
        """
        final_objects={
            'totalStudies': 0,
            'studies': []
        }  

        tmp_objects={}

        for object in raw_objects:

            # Perform basic transformation of company data based upon data in the configuration file
            study_obj=self._transform_study(object[self.RAW_study_name])

            # Capture the right company_name and then fetch the study's ID
            company_name = companies.get_name (object[self.RAW_COMPANY_NAME])
            company_id = companies.make_id (company_name)
            
            # Capture the right study_name and then fetch the study's ID
            interaction_name=interactions.get_name(object[self.RAW_STUDY_NAME], object[self.RAW_DATE])
            interaction_id=interactions.make_id (object[self.RAW_DATE], company_name, self.RAW_STUDY_NAME)

            if tmp_objects.get (object[self.RAW_study_name]) == None:
                tmp_objects[self.RAW_STUDY_NAME] = {
                    "studyName": study_obj['name'],
                    "description": study_obj['description'],
                    "linkedCompanies": {company_name: company_id},
                    "totalCompanies": 0,
                    "linkedInteractions": {interaction_name: interaction_id},
                    "totalInteractions": 0,
                    "keyThemes": self._get_keythemes(study_obj['name']),
                    "keyThemeQuotes": self._get_keytheme_quotes(study_obj['name']),
                    "keyThemeFrequencies": self._get_keytheme_frequencies(study_obj['name']),
                    "totalKeyThemes": 0,
                    "keyQuestions": self._get_keyquestions(study_obj['name']),
                    "totalKeyQuestions": 0,
                    "document": self._get_document(study_obj['name']),
                    "public": study_obj['public'],
                    "groups": study_obj['groups']
                }
            else:
                tmp_objects[object[self.RAW_STUDY_NAME]]["linkedCompanies"][company_name]=company_id
                tmp_objects[object[self.RAW_STUDY_NAME]]["linkedInteractions"][interaction_name]=interaction_id

        for study in tmp_objects.keys ():
            if file_output:
                # Generally the model to create a GUID is to hash the name and the description for all objects.
                # We will only use this option when we're outputing to a file.
                tmp_objects[study]['GUID'] = self.util.hash_it(study + tmp_objects[study]['description'])
            tmp_objects[study]['totalInteractions'] = self.util.total_item(tmp_objects[study]['linkedInteractions'])
            tmp_objects[study]['totalCompanies'] = self.util.total_item(tmp_objects[study]['linkedCompanies'])
            tmp_objects[study]['totalKeyThemes'] = self.util.total_item(tmp_objects[study]['keyThemes'])
            tmp_objects[study]['totalKeyQuestions'] = self.util.total_item(tmp_objects[study]['keyQuestions'])
            if (self.debug): print (tmp_objects[study])
            final_objects['companies'].append(tmp_objects[company])

        final_objects.totalStudies = self.util.total_item(final_objects.studies)

        return final_objects

    