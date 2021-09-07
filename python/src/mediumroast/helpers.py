__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."


from geopy.geocoders import ArcGIS
from summarizer import Summarizer
import hashlib, time
import configparser as conf

class utilities:

    def __init__ (self):
        self.locator = ArcGIS (timeout=2)

        # TODO Parcel out the relevant functions into the right modules like interactions to interactions, etc.
        # TODO rename functions as appropriate to be what makes sense like mkStudy could be associate_study
        # TODO figure out a deterministic way to create GUIDs but only for the JSON file, example always hash name + desc
        # TODO only leave true utility functions in this module like hashIt totalItem
        # TODO create a defaults config file for a few things

    def total_item (self, items):
        """Total items in dicts and lists and return the result.

        """
        return len (items)

    def hash_it(self, stringToHash, HASH='sha256'):
        h = hashlib.new (HASH)
        h.update (stringToHash.encode('utf-8'))
        return h.hexdigest ()

    def locate (self, place):
        """Using an input string return the lat long combo using geopy

        """
        l = self.locator.geocode (place)
        return [l.longitude, l.latitude]

    def save (self, file_name, string_data):
        """ Save string content to a file

        """
        my_file = open (file_name, 'w')
        my_file.write (string_data)
        my_file.close ()
        return True


    def correct_date (self, date_time):
        """Ensure that the date and time are correct

        """
        my_time=self.config['DEFAULT']['interviewTime']
        my_date=date_time
        if len (date_time) > 8:
            my_time=my_date[8:]
            my_date=my_date[0:8]
        return (my_date, my_time)


    def get_date_time (self):
        """Get the time presently and return in two formats

        """
        the_time_is=time.localtime()
        time_concat=the_time_is.tm_year + the_time_is.tm_mon + the_time_is.tm_mday + the_time_is.tm_hour + the_time_is.tm_min
        time_formal=time.asctime(the_time_is)
        return time_concat, time_formal


    def make_note (self, obj_type, creator='Mediumroast SDK load utility.'):
        """Create a sample note for an object or a child object

        """
        (time_stamp, time_string)=self.get_date_time()
        return {"1":{time_stamp: "This is an example note created for the '" + obj_type + "' object on " + time_string + " by a " + creator}}

class companies:

    def __init__ (self, rewrite_config_dir="../src/mediumroast/transformers/"):
        self.RULES={
            'dir': rewrite_config_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }  
        self.rules=conf.ConfigParser()
        self.rules.read(self.RULES['dir'] + self.RULES['company'])
        self.util=utilities() 

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


    def get_description (self, company_name):
        """Lookup a company description from the configuration file and return it.

        As appropriate return a long form description of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.

        Returns:
            string: A textual description from the configuration file OR if none is present the default.
        """
        if self.rules.has_option ('descriptions', company_name): 
            return self.rules.get('descriptions', company_name)
        else: 
            return self.rules.get('DEFAULT', 'description')


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


class studies:

    def __init__ (self, rewrite_config_dir="../src/mediumroast/transformers/"):
        self.RULES={
            'dir': rewrite_config_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }  
        self.rules=conf.ConfigParser()
        self.rules.read(self.RULES['dir'] + self.RULES['study']) 
        self.util=utilities()


    def get_name (self, study_name):
        """Lookup a study's name from the configuration file and return it.

        As appropriate return the proper name of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            study_name (str): The study name which aligns to the name within the configuration file.

        Returns:
            string: A reformatted name of the study OR the argument passed in if nothing exists in the configuration file

        """
        if self.rules.has_option ('names', study_name): 
            return self.rules.get('names', study_name)
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
        if self.rules.has_option ('descriptions', study_name): 
            return self.rules.get('descriptions', study_name)
        else: 
            return self.rules.get('DEFAULT', 'description')


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

class interactions:

    def __init__ (self, rewrite_config_dir="../src/mediumroast/transformers/"):
        self.RULES={
            'dir': rewrite_config_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }  
        self.rules=conf.ConfigParser()
        self.rules.read(self.RULES['dir'] + self.RULES['interaction']) 
        self.util=utilities()


    def get_name (self, date, study_name):
        """Create an interaction name and return the resulting string.

        Generate an interaction name from the date and study_name

        Args:
            study_name (str): The study name which should ideally be reformatted to the proper name.
            date (str): A raw date for the interaction, this needs to be the same date fed to the interaction transform

        Returns:
            string: The generated name of the interaction which is the synthesis of the date string and study name

        """
        return str(date) + '-' + str(study_name)


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
        description=self.rules.get('DEFAULT', 'description')
        description=description.replace ("COMPANY", str(company_name))
        description=description.replace ("STUDYNAME", str(study_name))
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

class abstracts:

    def __init__(self):
        pass

    def make(self, text, sentences=5, ratio=0.2):
        model=Summarizer()
        return model(text, ratio=ratio)
