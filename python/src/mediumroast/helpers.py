__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."


from geopy.geocoders import ArcGIS
import hashlib, time

class utilities:

    def __init__ (self):
        self.foo='bar'
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

    
"""


    def lookupInteraction (self, study_name, date):
        my_study = self.lookupStudy (study_name)
        return date + '-' + my_study

    def getStudyDesc (self, study_name):
        my_desc = "Blank description"
        if self.config['studyDescriptions'].get (study_name): my_desc = self.config['studyDescriptions'][study_name]
        return my_desc




    

    def mkStudy (self, study_name):
        my_study = self.lookupStudy (study_name)

        if self.config['DEFAULT']['isFile'] == 'True':
            my_desc = self.getStudyDesc (study_name)
            #       NAME        GUID
            return my_study, self.hashIt (my_study + my_desc)
        else:
            my_desc = "BLANK"
            return my_study, my_desc

    # TODO Pull out the automated interaction description creation into a separate function
    def mkInteration (self, interaction_date, company_name, study_name):
        my_study = self.lookupStudy (study_name)
        my_interaction = self.lookupInteraction (study_name, interaction_date)
        my_desc = str (self.config['DEFAULT']['interactionDescription'])
        my_desc = my_desc.replace ("COMPANY", company_name)
        my_desc = my_desc.replace ("STUDYNAME", my_study)
        if self.config['DEFAULT']['isFile'] == 'True':
            my_desc = self.getCompanyDesc (company_name)
            #       NAME        GUID
            return my_interaction, self.hashIt (my_interaction + my_desc)
        else:
            my_desc = "BLANK"
            return my_interaction, my_desc

"""