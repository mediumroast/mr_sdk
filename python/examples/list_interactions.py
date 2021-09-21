#!/bin/env python3

import sys, pprint, argparse

from mediumroast.api.high_level import Auth as authenticate
from mediumroast.api.high_level import Interactions as interaction

def parse_cli_args(program_name='list_interactions', desc='A mediumroast.io example utility that lists interactions using mr_api.'):
    parser=argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument ('--rest_url', help="The URL of the target REST server", type=str, dest='rest_url', default='http://mr-01:3000')
    parser.add_argument ('--get_name_by_guid', help="Get interaction name by GUID", type=str, dest='name_by_guid')
    parser.add_argument ('--get_guid_by_name', help="Get GUID by interaction name", type=str, dest='guid_by_name')
    parser.add_argument ('--get_url_by_guid', help="Get interaction url by GUID", type=str, dest='url_by_guid')
    parser.add_argument ('--get_abs_by_guid', help="Get interaction abstract by GUID", type=str, dest='abs_by_guid')
    parser.add_argument ('--get_by_guid', help="Get interaction object by GUID", type=str, dest='by_guid')
    parser.add_argument ('--get_by_name', help="Get interaction object by interaction name", type=str, dest='by_name')
    parser.add_argument ('--get_all_unsummarized', help="Get all interactions that are unsummarized", type=bool, dest='all_unsummarized')
    parser.add_argument ('--user', help="User name", type=str, dest='user', default='foo')
    parser.add_argument ('--secret', help="Secret or password", type=str, dest='secret', default='bar')
    cli_args = parser.parse_args ()
    return cli_args

if __name__ == "__main__":
    printer=pprint.PrettyPrinter()
    my_args=parse_cli_args()

    auth_ctl=authenticate(user_name=my_args.user, secret=my_args.secret, rest_server_url=my_args.rest_url)
    credential=auth_ctl.login()
    interaction_ctl=interaction(credential)
    resp=list()
    success=bool()
    if my_args.name_by_guid:
        success, resp=interaction_ctl.get_name_by_guid(my_args.name_by_guid)
    elif my_args.guid_by_name:
        success, resp=interaction_ctl.get_guid_by_name(my_args.guid_by_name)
    elif my_args.by_guid:
        success, resp=interaction_ctl.by_guid(my_args.by_guid)
    elif my_args.by_name:
        success, resp=interaction_ctl.get_by_name(my_args.by_name)
    elif my_args.url_by_guid:
        success, resp=interaction_ctl.get_url_by_guid(my_args.url_by_guid)
    elif my_args.abs_by_guid:
        success, resp=interaction_ctl.get_abs_by_guid(my_args.abs_by_guid)
    elif my_args.all_unsummarized:
        success, resp=interaction_ctl.get_all_unsummarized()
    else:
        success, resp=interaction_ctl.get_all()
    
    if success:
        printer.pprint(resp)
    else:
        print('CLI ERROR: This is a generic error message, as something went wrong.')
        sys.exit(-1)