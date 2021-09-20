__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."

from ..helpers import utilities
import requests

class rest_scaffold:
    def __init__(self, credential):
        self.CRED=credential

    def get_obj(self, endpoint):
        url=self.CRED['rest_url'] + endpoint
        resp_obj=requests.get(url)
        return resp_obj.json()

    # TODO This needs to be experimented with it will likely not work
    def put_obj(self, endpoint, obj):
        url=self.CRED['rest_url'] + endpoint
        resp_obj=requests.put(url, json=obj)
        return resp_obj.json()



class Auth:
    def __init__(self, rest_server_url, user_name, secret, server_type="json"):
        self.REST_URL=rest_server_url
        self.SERVER_TYPE=server_type
        self.USER=user_name
        self.SECRET=secret
        self.utils=utilities()

    def login(self):
        token=self.utils.hash_it(self.USER + self.SECRET)
        return {
            "access_token": token,
            "refresh_token": token,
            "server_type": self.SERVER_TYPE,
            "user_name": self.USER,
            "rest_url": self.REST_URL
        }

    def logout(self):
        pass


class Studies:
    def __init__(self, credential):
        self.URL=rest_server_url
        self.SERVER_TYPE=server_type
    
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
        self.URL=rest_server_url
        self.SERVER_TYPE=server_type
    
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
        self.calls=rest_scaffold(credential)
    
    def get_all(self):
        my_url='/interactions'
        return self.calls.get_obj(my_url)

    def get_all_unsummarized(self):
        my_url='/interactions?state=unsummarized'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            filtered_objs.append(
                {"interactionName": my_obj['interactionName'],
                "GUID": my_obj['GUID'],
                "state": my_obj['state'],
                "abstract": my_obj['abstract'],
                "url": my_obj['url']}
            )
        return filtered_objs

    def get_guid_by_name(self, name):
        my_url='/interactions?interactionName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'interactionName': my_obj['interactionName'],
            'GUID': my_obj['GUID']            
        }

    def get_name_by_guid(self, guid):
        my_url='/interactions?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'interactionName': my_obj['interactionName']
        }

    def get_url_by_guid(self, guid):
        my_url='/interactions?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'interactionName': my_obj['interactionName'],
            'url': my_obj['url'],
        }

    def get_abs_by_guid(self, guid):
        my_url='/interactions?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'interactionName': my_obj['interactionName'],
            'abstract': my_obj['abstract'],
        }
    
    def get_by_name(self, name):
        my_url='/interactions?interactionName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_by_guid(self, guid):
        my_url='/interactions?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj