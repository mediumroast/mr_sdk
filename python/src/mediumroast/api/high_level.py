__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

from .json_server import Interactions as json_interactions 
from .json_server import Studies as json_studies
from .json_server import Companies as json_companies
# TODO import other objects
from .json_server import Auth as json_authenticator

class Auth:
    def __init__(self, rest_server_url, user_name, secret, server_type="json"):
        self.REST_URL=rest_server_url
        self.SERVER_TYPE=server_type
        self.USER=user_name
        self.SECRET=secret

    def login(self):
        if self.SERVER_TYPE == "json":
            auth=json_authenticator(rest_server_url=self.REST_URL, user_name=self.USER, secret=self.SECRET)
            return auth.login()
        else:
            return NotImplementedError

    def logout(self):
        pass

class Studies:
    def __init__(self, credential):
        self.CRED=credential
        self.studies=json_studies(credential)
    
    def get_all(self):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_all()
        else:
            raise NotImplementedError

    def get_guid_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_guid_by_name(name)
        else:
            raise NotImplementedError

    def get_name_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_name_by_guid(guid)
        else:
            raise NotImplementedError
    
    def get_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_by_name(name)
        else:
            raise NotImplementedError

    def get_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_by_guid(guid)
        else:
            raise NotImplementedError

    def get_iterations(self):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_iterations()
        else:
            raise NotImplementedError

    def get_questions(self):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_questions()
        else:
            raise NotImplementedError

    def get_iterations_by_state(self, state="unthemed"):
        if self.CRED['server_type'] == 'json':
            return True, self.studies.get_iterations_by_state(state)
        else:
            raise NotImplementedError


class Companies:
    def __init__(self, credential):
        self.CRED=credential
        self.companies=json_companies(credential)
    
    def get_all(self):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_all()
        else:
            raise NotImplementedError

    def get_guid_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_guid_by_name(name)
        else:
            raise NotImplementedError

    def get_name_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_name_by_guid(guid)
        else:
            raise NotImplementedError
    
    def get_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_by_name(name)
        else:
            raise NotImplementedError

    def get_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_by_guid(guid)
        else:
            raise NotImplementedError

    def get_iterations(self):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_iterations()
        else:
            raise NotImplementedError

    def get_iterations_by_state(self, state="unthemed"):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.get_iterations_by_state(state)
        else:
            raise NotImplementedError


class Interactions:
    def __init__(self, credential):
        self.CRED=credential
        self.interactions=json_interactions(credential)
    
    def get_all(self):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_all()
        else:
            raise NotImplementedError

    def get_all_unsummarized(self):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_all_unsummarized()
        else:
            raise NotImplementedError

    def get_guid_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_guid_by_name(name)
        else:
            raise NotImplementedError

    def get_name_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_name_by_guid(guid)
        else:
            raise NotImplementedError

    def get_url_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_url_by_guid(guid)
        else:
            raise NotImplementedError

    def get_abs_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_abs_by_guid(guid)
        else:
            raise NotImplementedError
    
    def get_by_name(self, name):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_by_name(name)
        else:
            raise NotImplementedError

    def get_by_guid(self, guid):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_by_guid(guid)
        else:
            raise NotImplementedError
