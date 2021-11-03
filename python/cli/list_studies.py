#!/bin/env python3

import sys, pprint, argparse

from mediumroast.api.high_level import Auth as authenticate
from mediumroast.api.high_level import Studies as study

def parse_cli_args(program_name='list_studies', desc='A mediumroast.io example utility that lists studies using mr_api.'):
    parser=argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument ('--rest_url', help="The URL of the target REST server", type=str, dest='rest_url', default='http://mr-01:3000')
    parser.add_argument ('--get_name_by_guid', help="Get study name by GUID", type=str, dest='name_by_guid')
    parser.add_argument ('--get_guid_by_name', help="Get GUID by study name", type=str, dest='guid_by_name')
    parser.add_argument ('--get_substudies', help="Get all iterations or by status", type=str, dest='get_substudies', choices=['all', 'unthemed'])
    parser.add_argument ('--get_by_guid', help="Get study object by GUID", type=str, dest='by_guid')
    parser.add_argument ('--get_by_name', help="Get study object by study name", type=str, dest='by_name')
    parser.add_argument ('--user', help="User name", type=str, dest='user', default='foo')
    parser.add_argument ('--secret', help="Secret or password", type=str, dest='secret', default='bar')
    cli_args = parser.parse_args ()
    return cli_args

if __name__ == "__main__":
    printer=pprint.PrettyPrinter()
    my_args=parse_cli_args()

    auth_ctl=authenticate(user_name=my_args.user, secret=my_args.secret, rest_server_url=my_args.rest_url)
    credential=auth_ctl.login()
    study_ctl=study(credential)
    resp=list()
    success=bool()
    if my_args.name_by_guid:
        success, resp=study_ctl.get_name_by_guid(my_args.name_by_guid)
    elif my_args.guid_by_name:
        success, resp=study_ctl.get_guid_by_name(my_args.guid_by_name)
    elif my_args.by_guid:
        success, resp=study_ctl.get_by_guid(my_args.by_guid)
    elif my_args.by_name:
        success, resp=study_ctl.get_by_name(my_args.by_name)
    elif my_args.get_substudies == 'all':
        success, resp=study_ctl.get_substudies()
    elif my_args.get_substudies == 'unthemed':
        success, resp=study_ctl.get_unthemed_substudies()
    else:
        success, resp=study_ctl.get_all()

    if success:
        printer.pprint(resp)
    else:
        print('CLI ERROR: This is a generic error message, as something went wrong.')
        sys.exit(-1)