__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-31'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

import sys
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

    # TODO rewrite this to follow the load_studies utility

    def _transform_study (self, study_name, extended_rewrite=False):
        """Internal method to rewrite or augment key aspects of a study object as per definitions in the configuration file."""
        
        # Add the items which are either rewritten or not present in the file_name metadata.
        industry=self.rules.industries[study_name] if self.rules.industries[study_name] else self.rules.DEFAULT.industry
        role=self.rules.roles[study_name] if self.rules.roles[study_name] else self.rules.DEFAULT.role
        description=self.rules.descriptions[study_name] if self.rules.descriptions[study_name] else self.rules.DEFAULT.description
        url=self.rules.urls[study_name] if self.rules.urls[study_name] else self.rules.DEFAULT.url
        cik=self.rules.ciks[study_name] if self.rules.ciks[study_name] else self.rules.DEFAULT.cik
        stockSymbol=self.rules.stockSymbols[study_name] if self.rules.stockSymbols[study_name] else self.rules.DEFAULT.stockSymbol
        recent10kURL=self.rules.recent10kURLs[study_name] if self.rules.recent10kURLs[study_name] else self.rules.DEFAULT.recent10kURL
        recent10qURL=self.rules.recent10qURLs[study_name] if self.rules.recent10qURLs[study_name] else self.rules.DEFAULT.recent10qURL
        phone=self.rules.phones[study_name] if self.rules.phones[study_name] else self.rules.DEFAULT.phone
        streetAddress=self.rules.streetAddresses[study_name] if self.rules.streetAddresses[study_name] else self.rules.DEFAULT.streetAddress
        zipPostal=self.rules.zips[study_name] if self.rules.zips[study_name] else self.rules.DEFAULT.zipPostal
        
        # Should we want to have inputs totally worked through the configuration file we can set up the rewrite logic to look for
        # an extended_rewrite.  This will then create all of the fields which are normally pulled in through the file_name metadata,
        # in addition to the ones not included with the file metadata.
        if extended_rewrite:
            stateProvince=self.rules.stateProvinces[study_name] if self.rules.stateProvinces[study_name] else self.rules.DEFAULT.stateProvince
            city=self.rules.cities[study_name] if self.rules.cities[study_name] else self.rules.DEFAULT.city
            country=self.rules.countries[study_name] if self.rules.countries[study_name] else self.rules.DEFAULT.country
            region=self.rules.regions[study_name] if self.rules.regions[study_name] else self.rules.DEFAULT.region
            latitude=self.rules.lattitudes[study_name] if self.rules.lattitudes[study_name] else self.rules.DEFAULT.lattitude
            longitude=self.rules.longitudes[study_name] if self.rules.longitudes[study_name] else self.rules.DEFAULT.longitude
            country=self.rules.countries[study_name] if self.rules.countries[study_name] else self.rules.DEFAULT.country

            return {'name': study_name, 
                    'role': role,
                    'industry': industry, 
                    'description': description, 
                    'url': url, 
                    'country': country, 
                    'cik': cik, 
                    'stockSymbol': stockSymbol, 
                    'recent10kURL': recent10kURL, 
                    'recent10qURL': recent10qURL,
                    'latitude': latitude, 
                    'longitude': longitude, 
                    'stateProvince': stateProvince, 
                    'city': city, 
                    'region': region, 
                    'phone': phone, 
                    'streetAddress': streetAddress,
                    'zipPostal': zipPostal}
        else:      
            return {'name': study_name, 
                    'role': role,
                    'industry': industry, 
                    'description': description, 
                    'url': url, 
                    'cik': cik, 
                    'stockSymbol': stockSymbol, 
                    'recent10kURL': recent10kURL, 
                    'recent10qURL': recent10qURL,
                    'phone': phone, 
                    'streetAddress': streetAddress,
                    'zipPostal': zipPostal}


    def get_name (self, study_name):
        """Lookup a study's name from the configuration file and return it.

        As appropriate return the proper name of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            study_name (str): The study name which aligns to the name within the configuration file.

        Returns:
            string: A reformatted name of the study OR the argument passed in if nothing exists in the configuration file

        """
        if self.rules.descriptions.get (study_name): 
            return self.rules.descriptions[study_name]
        else: 
            return study_name


    def get_description (self, study_name):
        """Lookup a study description from the configuration file and return it.

        As appropriate return a long form description of the study in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            study_name (str): The study name which aligns to the name within the configuration file.

        Returns:
            string: A textual description from the configuration file OR if none is present the default.
        """
        if self.rules.descriptions.get (study_name): 
            return self.rules.descriptions[study_name]
        else: 
            return self.rules.DEFAULT.description


    def make_id (self, study_name, file_output=True):
        """Create an identifier for the study 

        Create a identifier for the study_name which is either 'NULL_GUID' or a GUID generated by hashing
        the study name with the study description.  The latter is only done when the output is to a JSON
        file.  In the implementation with the backend we should revisit this logic to see if it is enven necessary
        or perhaps the backend handles all of this.

        Args:
            study_name (str): The study name which aligns to the name within the configuration file.
            file_output (bool): A switch for determining if we're storing the output in a file or not

        Returns:
            string: A textual representation of the study's ID
        """
        description=self.get_description(study_name)
        id='NULL_GUID' # This should never happen, but leaving here in case something is odd in the configuration file
        if file_output: id=self.util.hash_it(study_name + description) 
        return id
 
    # TODO Correct to follow load_studies
    def create_objects (self, raw_objects, file_output=True):
        """Create study objects from a raw list of input data.

        As this is the main transformation function of the class enabling a properly formatted set of objects that can
        either be passed to a file or the backend.  The former is more for advancing the GUI, etc. while the latter
        is related to exercising the entire system.

        Args:
            raw_objects (list): Raw objects generated from a one of the extractor methods.

        Returns:
            dict: An object containing a list of all company objects and the total number of company objects processed
        """
        final_objects={
            'totalStudies': 0,
            'studies': []
        }  

        tmp_objects={}

        for object in raw_objects:

            # Perform basic transformation of company data based upon data in the configuration file
            company_obj=self._transform_company(object[self.RAW_study_name])

            # Capture the right company_name and then fetch the study's ID
            company_name = companies.get_name (object[self.RAW_COMPANY_NAME]) # TODO Create this function inside the study module 
            study_id = companies.make_id (company_name) # TODO Create this function inside the study module
            
            # Capture the right study_name and then fetch the study's ID
            interaction_name=interactions.get_name(object[self.RAW_STUDY_NAME], object[self.RAW_DATE])
            interaction_id=interactions.make_id (object[self.RAW_DATE], company_obj.name, self.RAW_STUDY_NAME)

            if tmp_objects.get (object[self.RAW_study_name]) == None:
                tmp_objects[self.RAW_STUDY_NAME] = {
                    "companyName": company_obj.name,
                    "industry": company_obj.industry,
                    "role": company_obj.role,
                    "url": company_obj.url,
                    "streetAddress": company_obj.streetAddress,
                    "city": object[self.CITY],
                    "stateProvince": object[self.STATE_PROVINCE],
                    "country": object[self.COUNTRY],
                    "region": object[self.REGION],
                    "phone": company_obj.phone,
                    "simpleDesc": company_obj.description,
                    "cik": company_obj.cik,
                    "stockSymbol": company_obj.stockSymbol,
                    "Recent10kURL": company_obj.recent10kURL,
                    "Recent10qURL": company_obj.recent10qURL,
                    "zipPostal": company_obj.zipPostal,
                    "linkedCompanies": {company_name: study_id},
                    "linkedInteractions": {interaction_name: interaction_id},
                    "notes": self.util.make_note(obj_type='Company Object: [' + company_obj.name + ']')
                }
            else:
                tmp_objects[object[self.RAW_STUDY_NAME]]["linkedCompanies"][company_name] = study_id
                tmp_objects[object[self.RAW_STUDY_NAME]]["linkedInteractions"][interaction_name] = interaction_id

        for study in tmp_objects.keys ():
            if file_output:
                # Generally the model to create a GUID is to hash the name and the description for all objects.
                # We will only use this option when we're outputing to a file.
                tmp_objects[study]['GUID'] = self.util.hash_it(study + tmp_objects[study].simpleDesc)
            tmp_objects[study]['totalInteractions'] = self.util.total_item(tmp_objects[study].linkedInteractions)
            tmp_objects[study]['totalCompanies'] = self.util.total_item(tmp_objects[study].linkedCompanies)
            final_objects.studies.append (tmp_objects[study])

        final_objects.totalStudies = self.util.total_item(final_objects.studies)

        return final_objects

    