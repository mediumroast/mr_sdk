#!/bin/env python3

import sys, pprint, argparse, json

from mediumroast.api.high_level import Auth as authenticate
from mediumroast.api.high_level import Companies as company

def parse_cli_args(program_name='update_companies', desc='A mediumroast.io example utility that updates company properties using mr_api.'):
    parser=argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument ('--rest_url', help="The URL of the target REST server", type=str, dest='rest_url', default='http://mr-01:3000')
    parser.add_argument ('--guid', help="Specify the GUID of the object to operate on", type=str, dest='guid', required=True)
    parser.add_argument ('--set_interactions_state', help="Set the state of a company's interactions", type=str, dest='interactions_state', choices=['processing', 'summarized', 'unsummarized'])
    parser.add_argument ('--set_iteration_state', help="Set the state of the iteration", type=str, dest='iteration_state', choices=['processing', 'summarized', 'unsummarized', 'themed', 'unthemed'])
    parser.add_argument ('--set_container_state', help="Set the state of the iteration's container", type=str, dest='container_state')
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
    company_ctl=company(credential)
    resp=list()
    success=bool()
    if my_args.interactions_state:
        success, resp=company_ctl.set_interactions_state(my_args.guid, my_args.interactions_state)
    elif my_args.iteration_state:
        success, resp=company_ctl.set_interactions_state(my_args.guid, my_args.iteration_state)
    elif my_args.container_state:
        success, resp=company_ctl.set_interactions_state(my_args.guid, my_args.container_state)
    elif my_args.property:
        success, resp=company_ctl.set_property(my_args.guid, json.loads(my_args.property))
    else:
        print('CLI ERROR: Either no additional argument beyond --guid=<guid_string> was specified or something else happened.')
        sys.exit(-1)
    
    if success:
        printer.pprint(resp)
    else:
        printer.pprint(resp)
        sys.exit(-1)