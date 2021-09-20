__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

from .json_server import Interactions as json_interactions
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
    
    def get_all(self):
        pass

    def get_all_corpuses_unsummarized(self):
        pass

    def get_all_corpuses_unthemed(self):
        pass

    def get_guid_by_name(self, name):
        pass

    def get_name_by_guid(self, guid):
        pass
    
    def get_by_name(self, study_name):
        pass

    def get_by_guid(self, guid):
        pass

    def get_corpuses(self, guid):
        pass

    def get_corpuses_unsummarized(self, guid):
        pass

    def get_corpuses_unthemed(self, guid):
        pass

class Companies:
    def __init__(self, credential):
        self.CRED=credential
    
    def get_all(self):
        pass

    def get_all_corpuses_unsummarized(self):
        pass

    def get_all_corpuses_unthemed(self):
        pass

    def get_guid_by_name(self, name):
        pass

    def get_name_by_guid(self, guid):
        pass
    
    def get_by_name(self, study_name):
        pass

    def get_by_guid(self, guid):
        pass

    def get_corpuses(self, guid):
        pass

    def get_corpuses_unsummarized(self, guid):
        pass

    def get_corpuses_unthemed(self, guid):
        pass


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
