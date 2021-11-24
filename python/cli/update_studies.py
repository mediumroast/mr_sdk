#!/bin/env python3

import sys, pprint, argparse, json

from mediumroast.api.high_level import Auth as authenticate
from mediumroast.api.high_level import Studies as study

def parse_cli_args(program_name='update_studies', desc='A mediumroast.io example utility that updates study properties using mr_api.'):
    parser=argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument ('--rest_url', help="The URL of the target REST server", type=str, dest='rest_url', default='http://mr-01:3000')
    parser.add_argument ('--guid', help="Specify the GUID of the object to operate on", type=str, dest='guid', required=True)
    parser.add_argument ('--set_theme_state', help="Set the theme state of a substudy", type=str, dest='theme_state', choices=['processing', 'summarized', 'unsummarized'])
    parser.add_argument ('--substudy_name', help="Set the state of the iteration", type=str, dest='substudy')
    parser.add_argument ('--set_property', help="Set an arbitrary property for the company using well formed JSON", type=str, dest='property')
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

    if my_args.theme_state:
        # Get the study obj
        # Update the theme state of the substudy
        # Set the substudies property
        pass
    elif my_args.property:
        # This is for a simple set
        success, resp=study_ctl.set_property(my_args.guid, json.loads(my_args.property))
    else:
        print('CLI ERROR: Either no additional argument beyond --guid=<guid_string> was specified or something else happened.')
        sys.exit(-1)
    
    if success:
        printer.pprint(resp)
    else:
        printer.pprint(resp)
        sys.exit(-1)