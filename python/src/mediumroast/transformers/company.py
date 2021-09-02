__version__ = '1.0'
__author__  = "Michael Hay, John Goodman"
__date__    = '2021-August-31'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

import configparser as conf
from geopy.geocoders import ArcGIS

class Transform:
    """Perform transformation of input data into a proper company object.

    Returns:
        list: A list of dicts which can be pass along to additional 

    Methods:
        create_object()
            Using the attributes set when the object was constructed get the data from the file.
    """

    def __init__ (self, rewrite_config='./company.ini'):
        self.RAW_COMPANY_NAME=7
        self.RAW_STUDY_NAME=6
        self.RAW_DATE=0
        self.REGION=1
        self.COUNTRY=2
        self.STATE_PROVINCE=3
        self.CITY=4
        self.CONF=rewrite_config
        self.rules=conf.ConfigParser()
        self.rules.read(self.CONF)
        

    def _transform_company (self, company_name):
        """Internal method to rewrite or augment key aspects of a company object as per definitions in the configuration file."""
        industry=self.rules.industries[company_name] if self.rules.industries[company_name] else self.rules.DEFAULT.industry
        role=self.rules.roles[company_name] if self.rules.roles[company_name] else self.rules.DEFAULT.role
        description=self.rules.descriptions[company_name] if self.rules.descriptions[company_name] else self.rules.DEFAULT.description
        return (company_name, role, industry, description)


    def create_object (self, raw_objects):
        pass

    