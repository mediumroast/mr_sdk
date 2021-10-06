#!/bin/env python3

import sys, pprint, argparse, json

from mediumroast.api.high_level import Auth as authenticate
from mediumroast.api.high_level import Interactions as interaction

def parse_cli_args(program_name='update_interactions', desc='A mediumroast.io example utility that updates interaction properties using mr_api.'):
    parser=argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument ('--rest_url', help="The URL of the target REST server", type=str, dest='rest_url', default='http://mr-01:3000')
    parser.add_argument ('--guid', help="Specify the GUID of the object to operate on", type=str, dest='guid', required=True)
    parser.add_argument ('--set_state', help="Set the state of the interaction", type=str, dest='state', choices=['processing', 'summarized', 'unsummarized'])
    parser.add_argument ('--set_all_state', help="Set the state of all interactions", type=str, dest='all_state', choices=['processing', 'summarized', 'unsummarized'])
    parser.add_argument ('--set_summary', help="Set the abstract/summary of the interaction", type=str, dest='summary')
    parser.add_argument ('--set_property', help="Set an arbitrary property for the interaction using well formed JSON", type=str, dest='property')
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
    if my_args.state:
        success, resp=interaction_ctl.set_state(my_args.guid, my_args.state)
    elif my_args.all_state:
        success, resp=interaction_ctl.set_all_states(my_args.all_state)
    elif my_args.summary:
        success, resp=interaction_ctl.set_summary(my_args.guid, my_args.summary)
    elif my_args.property:
        success, resp=interaction_ctl.set_property(my_args.guid, json.loads(my_args.property))
    else:
        print('CLI ERROR: Either no additional argument beyond --guid=<guid_string> was specified or something else happened.')
        sys.exit(-1)
    
    if success:
        printer.pprint(resp)
    else:
        printer.pprint(resp)
        sys.exit(-1)