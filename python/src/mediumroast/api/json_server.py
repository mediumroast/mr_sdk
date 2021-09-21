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

    # TODO implement put and patch objects
    # TODO implement interaction.set_abstract
    # TODO implement interaction.set_state
    # TODO implement study.corpus.set_state <-- should be done for parent/children
    # TODO implement company.corpus.set_state <-- should be done for parent/children
    # TODO change all corpuses to iterations



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
        self.CRED=credential
        self.calls=rest_scaffold(credential)
    
    def get_all(self):
        my_url='/studies'
        return self.calls.get_obj(my_url)


    def get_guid_by_name(self, name):
        my_url='/studies?studyName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'studyName': my_obj['studyName'],
            'GUID': my_obj['GUID']            
        }

    def get_name_by_guid(self, guid):
        my_url='/studies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'studyName': my_obj['studyName']
        }
    
    def get_by_name(self, name):
        my_url='/studies?studyName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_by_guid(self, guid):
        my_url='/studies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_iterations(self):
        my_url='/studies'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            filtered_objs.append(
                {"studyName": my_obj['studyName'],
                "GUID": my_obj['GUID'],
                "iterations": my_obj['iterations']}
            )
        return filtered_objs

    def get_questions(self):
        my_url='/studies'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            filtered_objs.append(
                {"studyName": my_obj['studyName'],
                "GUID": my_obj['GUID'],
                "questions": my_obj['questions']}
            )
        return filtered_objs

    def get_iterations_by_state(self, state="unthemed"):
        my_url='/studies?iterations.state=unprocessed_unprocessed'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            entry={"studyName": my_obj['studyName'],
                    "GUID": my_obj['GUID'],
                    "iterations": my_obj['iterations']}
            theme_state, summary_state=my_obj['iterations']['state'].split('_')
            if state == "unthemed" and theme_state != "themed":
                filtered_objs.append(entry)
            elif state == "unsummarized" and theme_state != "summarized":
                filtered_objs.append(entry)
            else:
                continue
        return filtered_objs


class Companies:
    def __init__(self, credential):
        self.CRED=credential
        self.calls=rest_scaffold(credential)
    
    def get_all(self):
        my_url='/companies'
        return self.calls.get_obj(my_url)

    def get_iterations(self):
        my_url='/companies'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            filtered_objs.append(
                {"companyName": my_obj['companyName'],
                "GUID": my_obj['GUID'],
                "iterations": my_obj['iterations']}
            )
        return filtered_objs

    def get_guid_by_name(self, name):
        my_url='/companies?companyName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'companyName': my_obj['companyName'],
            'GUID': my_obj['GUID']            
        }

    def get_name_by_guid(self, guid):
        my_url='/companies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return {
            'GUID': my_obj['GUID'],
            'companyName': my_obj['companyName']
        }
    
    def get_by_name(self, name):
        my_url='/companies?companyName=' + name
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_by_guid(self, guid):
        my_url='/companies?GUID=' + guid
        my_obj=self.calls.get_obj(my_url)[0]
        return my_obj

    def get_iterations_by_state(self, state="unthemed"):
        my_url='/companies?iterations.state=unprocessed_unprocessed'
        my_objs=self.calls.get_obj(my_url)
        filtered_objs=[]
        for my_obj in my_objs:
            entry={"companyName": my_obj['companyName'],
                    "GUID": my_obj['GUID'],
                    "iterations": my_obj['iterations']}
            theme_state, summary_state=my_obj['iterations']['state'].split('_')
            if state == "unthemed" and theme_state != "themed":
                filtered_objs.append(entry)
            elif state == "unsummarized" and theme_state != "summarized":
                filtered_objs.append(entry)
            else:
                continue
        return filtered_objs



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