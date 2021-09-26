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

    def set_property(self, guid, json):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.set_property(guid, json)
        else:
            raise NotImplementedError
            
    def set_interactions_state(self, guid, state='unsummarized'):
        if self.CRED['server_type'] == 'json':
            interactions_ctl=Interactions()
            all_interactions=interactions_ctl.get_all_unsummarized()
            all_iterations=self.companies.get_iterations_by_state()
            return True, self.companies.set_interaction_state(guid, state)
        else:
            raise NotImplementedError


    # TODO need to implement this function it is not yet coded
    def set_states_by_guid(self, guid, states):
        if self.CRED['server_type'] == 'json':
            return True, self.companies.set_property(guid, json)
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
            return True, self.interactions.get_all_unsummarized_list()
        else:
            raise NotImplementedError

    def get_all_unsummarized_dict(self):
        if self.CRED['server_type'] == 'json':
            return True, self.interactions.get_all_unsummarized_dict()
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

    def set_state(self, guid, state):
        # TODO Change to try except structure to bettle handle errors
        if self.CRED['server_type'] == 'json':
            my_status, my_obj=self.interactions.set_state(guid, state)
            return my_status, my_obj
        else:
            raise NotImplementedError

    def set_all_states(self, state):
        if self.CRED['server_type'] == 'json':
            final_objs=[]
            interactions=self.interactions.get_all_states()
            for interaction in interactions:
                prev_state=interaction['state']
                if state == prev_state: continue # Skip if this is already at desired state
                my_status, my_obj=self.set_state(interaction['GUID'], state)
                if not my_status: return my_status, my_obj # Oops there was an error in the request and we need to bale
                final_objs.append({
                    "interactionName": interaction['interactionName'],
                    'GUID': my_obj['id'],
                    'state': my_obj['state'],
                    'previous state': prev_state
                })
            return True, final_objs
        else:
            raise NotImplementedError

    def set_summary(self, guid, summary):
        if self.CRED['server_type'] == 'json':
            my_status, my_obj=self.interactions.set_summary(guid, summary)
            return my_status, my_obj
        else:
            raise NotImplementedError

    def set_property(self, guid, json):
        if self.CRED['server_type'] == 'json':
            my_status, my_obj=self.interactions.set_property(guid, json)
            return my_status, my_obj
        else:
            raise NotImplementedError
