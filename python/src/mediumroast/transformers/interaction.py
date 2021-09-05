__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-31'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

import sys
sys.path.append('../')

from mediumroast.helpers import utilities
from mediumroast.helpers import companies
from mediumroast.helpers import studies
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

    def __init__ (self, rewrite_config='./interaction.ini', debug=False):
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

    def _transform_interaction (self, study_name, extended_rewrite=False):
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


    def get_name (self, date, study_name):
        """Create an interaction name and return the resulting string.

        Generate an interaction name from the date and study_name

        Args:
            study_name (str): The study name which should ideally be reformatted to the proper name.
            date (str): A raw date for the interaction, this needs to be the same date fed to the interaction transform

        Returns:
            string: The generated name of the interaction which is the synthesis of the date string and study name

        """
        return date + '-' + study_name


    def get_description (self, company_name, study_name):
        """Create a description from the interaction.

        Using a default in the configuration file merge in company and study names to generate a description for 
        the interaction.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.
            study_name (str): The study name which aligns to the name within the configuration file.

        Returns:
            string: A generated textual description generated from the company and study names.
        """
        description=self.rules.DEFAULT.description
        description=description.replace ("COMPANY", company_name)
        description=description.replace ("STUDYNAME", study_name)
        return description
        


    def make_id (self, date, company_name, study_name, file_output=True):
        """Create an identifier for the interation.

        Create a identifier for the interaction which is either 'NULL_GUID' or a GUID generated by hashing
        the interaction name with the interaction description.  The latter is only done when the output is to a JSON
        file.  In the implementation with the backend we should revisit this logic to see if it is enven necessary
        or perhaps the backend handles all of this.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.
            study_name (str): The study name which aligns to the name within the configuration file.
            file_output (bool): A switch for determining if we're storing the output in a file or not

        Returns:
            string: A textual representation of the interactions's ID
        """
        interaction_name=self.get_name(date, study_name)
        description=self.get_description(company_name, study_name)
        id='NULL_GUID' # This should never happen, but leaving here in case something is odd in the configuration file
        if file_output: id=self.util.hash_it(interaction_name + description) 
        return id
 
    # TODO Correct to follow load_interactions
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
            'totalInteractions': 0,
            'studies': []
        }  

        tmp_objects={}

        for object in raw_objects:

            # Perform basic transformation of company data based upon data in the configuration file
            company_obj=self._transform_interaction(object[self.RAW_study_name])

            # Capture the right company_name and then fetch the study's ID
            company_name = companies.get_name (object[self.RAW_COMPANY_NAME]) # TODO Create this function inside the study module 
            company_id = companies.make_id (company_name) # TODO Create this function inside the study module
            
            # Capture the right study_name and then fetch the study's ID
            study_name = studies.get_name (object[self.RAW_STUDY_NAME]) 
            study_id = studies.make_id (study_name) 

            if tmp_objects.get (object[self.RAW_study_name]) == None:
                long_lat = self.util.locate (object[self.CITY] + ',' + object[self.STATE_PROVINCE] + ',' + object[self.COUNTRY])
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
                    "linkedStudies": {study_name: study_id},
                    "linkedCompanies": {company_name: company_id},
                    "longitude": long_lat[0],
                    "latitude": long_lat[1],
                    "notes": self.util.make_note(obj_type='Company Object: [' + company_obj.name + ']')
                }
            else:
                tmp_objects[object[self.RAW_STUDY_NAME]]["linkedStudies"][study_name] = study_id
                tmp_objects[object[self.RAW_STUDY_NAME]]["linkedCompanies"][company_name] = company_id

        for study in tmp_objects.keys ():
            if file_output:
                # Generally the model to create a GUID is to hash the name and the description for all objects.
                # We will only use this option when we're outputing to a file.
                tmp_objects[study]['GUID'] = self.util.hash_it(study + tmp_objects[study].simpleDesc)
            tmp_objects[study]['totalStudies'] = self.util.total_item(tmp_objects[study].linkedStudies)
            tmp_objects[study]['totalCompanies'] = self.util.total_item(tmp_objects[study].linkedCompanies)
            final_objects.studies.append (tmp_objects[study])

        final_objects.totalStudies = self.util.total_item(final_objects.studies)

        return final_objects

    