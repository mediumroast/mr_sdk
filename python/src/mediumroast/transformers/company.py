__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-31'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

import sys
sys.path.append('../')

from mediumroast.helpers import utilities
from mediumroast.helpers import studies
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

        get_name()
            Lookup a company from the configuration file and return it.

        make_id()
            Create a unique company identifier if needed.

        create_objects()
            Using the attributes set when the object was constructed get the data from the file.
    """

    def __init__ (self, rewrite_config_dir="../src/mediumroast/transformers/", debug=False):
        self.RAW_COMPANY_NAME=7
        self.RAW_STUDY_NAME=6
        self.RAW_DATE=0
        self.REGION=1
        self.COUNTRY=2
        self.STATE_PROVINCE=3
        self.CITY=4
        self.RULES={
            'dir': rewrite_config_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }
        
        # TODO wrap a try catch loop around the config file read
        self.rules=conf.ConfigParser()
        self.rules.read(self.RULES['dir'] + self.RULES['company'])

        # This imports the local utilies from mr_sdk for Python
        self.util=utilities()

        # Set debug to true or false
        self.debug=debug


    def _transform_company (self, company_name, extended_rewrite=False):
        """Internal method to rewrite or augment key aspects of a company object as per definitions in the configuration file."""
        
        # Add the items which are either rewritten or not present in the file_name metadata.
        industry=self.rules.get('industries', company_name) if self.rules.has_option('industries', company_name) else self.rules.get('DEFAULT', 'industry')
        role=self.rules.get('roles', company_name) if self.rules.has_option('roles', company_name) else self.rules.get('DEFAULT', 'role')
        description=self.rules.get('descriptions', company_name) if self.rules.has_option('descriptions', company_name) else self.rules.get('DEFAULT', 'description')
        url=self.rules.get('urls', company_name) if self.rules.has_option('urls', company_name) else self.rules.get('DEFAULT', 'url')
        cik=self.rules.get('ciks', company_name) if self.rules.has_option('ciks', company_name) else self.rules.get('DEFAULT', 'cik')
        stockSymbol=self.rules.get('stockSymbols', company_name) if self.rules.has_option('stockSymbols', company_name) else self.rules.get('DEFAULT', 'stockSymbol')
        recent10kURL=self.rules.get('recent10kURLs', company_name) if self.rules.has_option('recent10kURLs', company_name) else self.rules.get('DEFAULT', 'recent10kURL')
        recent10qURL=self.rules.get('recent10qURLs', company_name) if self.rules.has_option('recent10qURLs', company_name) else self.rules.get('DEFAULT', 'recent10qURL')
        phone=self.rules.get('phones', company_name) if self.rules.has_option('phones', company_name) else self.rules.get('DEFAULT', 'phone')
        streetAddress=self.rules.get('streetAddresss', company_name) if self.rules.has_option('streetAddresss', company_name) else self.rules.get('DEFAULT', 'streetAddress')
        zipPostal=self.rules.get('zipPostals', company_name) if self.rules.has_option('zipPostals', company_name) else self.rules.get('DEFAULT', 'zipPostal')
        
        # Should we want to have inputs totally worked through the configuration file we can set up the rewrite logic to look for
        # an extended_rewrite.  This will then create all of the fields which are normally pulled in through the file_name metadata,
        # in addition to the ones not included with the file metadata.
        if extended_rewrite:
            stateProvince=self.rules.get('stateProvinces', company_name) if self.rules.has_option('stateProvinces', company_name) else self.rules.get('DEFAULT', 'stateProvince')
            city=self.rules.get('cities', company_name) if self.rules.has_option('cities', company_name) else self.rules.get('DEFAULT', 'city')
            country=self.rules.get('countries', company_name) if self.rules.has_option('countries', company_name) else self.rules.get('DEFAULT', 'country')
            region=self.rules.get('regions', company_name) if self.rules.has_option('regions', company_name) else self.rules.get('DEFAULT', 'region')
            latitude=self.rules.get('latitudes', company_name) if self.rules.has_option('latitudes', company_name) else self.rules.get('DEFAULT', 'latitude')
            longitude=self.rules.get('longitudes', company_name) if self.rules.has_option('longitudes', company_name) else self.rules.get('DEFAULT', 'longitude')
            country=self.rules.get('countries', company_name) if self.rules.has_option('countries', company_name) else self.rules.get('DEFAULT', 'country')

            return {'name': company_name, 
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
            return {'name': company_name, 
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

    # TODO Delete this method as it is deprecated
    def get_name (self, company_name):
        """Lookup a company's name from the configuration file and return it.

        As appropriate return the proper name of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.

        Returns:
            string: A reformatted name of the company

        Notes:
            This initial implementation doesn't really do anything since we assume the company name is correct.
        """
        return company_name

    # TODO Delete this method as it is deprecated
    def get_description (self, company_name):
        """Lookup a company description from the configuration file and return it.

        As appropriate return a long form description of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.

        Returns:
            string: A textual description from the configuration file OR if none is present the default.
        """
        if self.rules.descriptions.get (company_name): 
            return self.rules.descriptions[company_name]
        else: 
            return self.rules.DEFAULT.description

    # TODO Delete this method as it is deprecated
    def get_industry (self, company_name):
        """Lookup a company industry from the configuration file and return it.

        As appropriate return the full industry of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.

        Returns:
            string: A textual representation of the company's industry from the configuration file OR if none is present the default.
        """
        if self.rules.industries.get (company_name): 
            return self.rules.industries[company_name]
        else: 
            return self.rules.DEFAULT.industry

    # TODO Delete this method as it is deprecated
    def make_id (self, company_name, file_output=True):
        """Create an identifier for the company 

        Create a identifier for the company_name which is either 'NULL_GUID' or a GUID generated by hashing
        the company name with the company description.  The latter is only done when the output is to a JSON
        file.  In the implementation with the backend we should revisit this logic to see if it is enven necessary
        or perhaps the backend handles all of this.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.
            file_output (bool): A switch for determining if we're storing the output in a file or not

        Returns:
            string: A textual representation of the company's ID
        """
        description=self.get_description(company_name)
        id='NULL_GUID'
        if file_output: id=self.util.hash_it(company_name + description) 
        return id
 

    def create_objects (self, raw_objects, file_output=True):
        """Create company objects from a raw list of input data.

        As this is the main transformation function of the class enabling a properly formatted set of objects that can
        either be passed to a file or the backend.  The former is more for advancing the GUI, etc. while the latter
        is related to exercising the entire system.

        Args:
            raw_objects (list): Raw objects generated from a one of the extractor methods.

        Returns:
            dict: An object containing a list of all company objects and the total number of company objects processed
        """
        final_objects={
            'totalCompanies': 0,
            'companies': []
        }  

        # Construct objects
        interaction_xform=interactions(rewrite_config_dir=self.RULES['dir'])  
        study_xform=studies(rewrite_config_dir=self.RULES['dir'])

        # Temp storage for objects
        tmp_objects={}

        for object in raw_objects:

            # Perform basic transformation of company data based upon data in the configuration file
            company_obj=self._transform_company(object[self.RAW_COMPANY_NAME])

            # Capture the right study_name and then fetch the study's ID
            study_name = study_xform.get_name (object[self.RAW_STUDY_NAME])
            study_id = study_xform.make_id (study_name) 
            
            # Capture the right study_name and then fetch the study's ID
            interaction_name=interaction_xform.get_name(object[self.RAW_DATE], study_name)
            interaction_id=interaction_xform.make_id (object[self.RAW_DATE], company_obj['name'], study_name)

            if tmp_objects.get (object[self.RAW_COMPANY_NAME]) == None:
                long_lat = self.util.locate (object[self.CITY] + ',' + object[self.STATE_PROVINCE] + ',' + object[self.COUNTRY])
                tmp_objects[object[self.RAW_COMPANY_NAME]] = {
                    "companyName": company_obj['name'],
                    "industry": company_obj['industry'],
                    "role": company_obj['role'],
                    "url": company_obj['url'],
                    "streetAddress": company_obj['streetAddress'],
                    "city": object[self.CITY],
                    "stateProvince": object[self.STATE_PROVINCE],
                    "country": object[self.COUNTRY],
                    "region": object[self.REGION],
                    "iterations": {},
                    "phone": company_obj['phone'],
                    "simpleDesc": company_obj['description'],
                    "cik": company_obj['cik'],
                    "stockSymbol": company_obj['stockSymbol'],
                    "Recent10kURL": company_obj['recent10kURL'],
                    "Recent10qURL": company_obj['recent10qURL'],
                    "zipPostal": company_obj['zipPostal'],
                    "linkedStudies": {study_name: study_id},
                    "linkedInteractions": {interaction_name: interaction_id},
                    "longitude": long_lat[0],
                    "latitude": long_lat[1],
                    "notes": self.util.make_note(obj_type='Company Object: [' + company_obj['name'] + ']')
                }
            else:
                tmp_objects[object[self.RAW_COMPANY_NAME]]["linkedStudies"][study_name]=study_id
                tmp_objects[object[self.RAW_COMPANY_NAME]]["linkedInteractions"][interaction_name]=interaction_id

            id+=1

        for company in tmp_objects.keys ():
            if file_output:
                # Generally the model to create a GUID is to hash the name and the description for all objects.
                # We will only use this option when we're outputing to a file.
                guid=self.util.hash_it(str(company) + str(tmp_objects[company]['simpleDesc']))
                tmp_objects[company]['GUID']=guid
                tmp_objects[company]['id']=guid
            tmp_objects[company]['totalInteractions'] = self.util.total_item(tmp_objects[company]['linkedInteractions'])
            tmp_objects[company]['totalStudies'] = self.util.total_item(tmp_objects[company]['linkedStudies'])
            tmp_objects[company]["iterations"]=self.util.get_iterations(tmp_objects[company]['linkedInteractions'], interaction_xform, "company")
            if (self.debug): print (tmp_objects[company])
            final_objects['companies'].append(tmp_objects[company])

        final_objects['totalCompanies'] = self.util.total_item(final_objects['companies'])

        return final_objects

    