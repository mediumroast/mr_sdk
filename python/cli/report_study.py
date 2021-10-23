#!/bin/env python3

import sys, pprint, argparse, configparser

from docx import Document
from datetime import datetime
from mediumroast.api.high_level import Auth as authenticate
from mediumroast.api.high_level import Studies as study
from mediumroast.api.high_level import Interactions as interaction

def parse_cli_args(program_name='report_study', desc='A mediumroast.io utility that generates a report for a study.'):
    parser=argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument ('--rest_url', help="The URL of the target REST server", type=str, dest='rest_url', default='http://mr-01:3000')
    parser.add_argument ('--guid', help="The GUID for the study to be reported on.", type=str, dest='guid', required=True)
    parser.add_argument ('--report_type', help="Specify the type of report to produce", type=str, dest='report_type', choices=['all', 'references', 'summary'], default='all')
    parser.add_argument ('--report_format', help="Define the report output format", type=bool, dest='report_format', choices=['docx', 'pdf'], default='docx')
    parser.add_argument ('--user', help="User name", type=str, dest='user', default='foo')
    parser.add_argument ('--secret', help="Secret or password", type=str, dest='secret', default='bar')
    parser.add_argument ('--config_file', help="The location to the configuration files", type=str, dest='config_file', default='./reports.ini')
    cli_args = parser.parse_args ()
    return cli_args

def read_config(conf_file='./reports.ini'):
    c=configparser.ConfigParser()
    c.read(conf_file)
    return c

def _create_header(doc_obj, conf):
    date_string=f'{datetime.now():%Y-%m-%d %H:%M}'
    s=doc_obj.sections[0]
    header=s.header
    header_p=header.paragraphs[0]
    header_p.text=conf['org'] + "\t | \t Created on: " + date_string 

def _create_footer():
    pass

def _create_title():
    pass

def report(study, format, conf):
    # Create doc object
    d=Document()
    _create_header(d, conf)

    # d=report_summary(study, format, all=True, doc=d)
    # d=report_references(study, format, all=True, doc=d)
    return d

def report_summary(study, format, all=False, doc=None):
    # Get the key themes
    # Construct the table for the key themes including if possible the refereneces within the document
    # Build the summary paragraph
    pass

def report_references(study, format, all=False, doc=None):
    interaction_ctl=interaction(credential)
    # create doc object
    # Loop over the interaction GUIDs
    #   Get each interaction by GUID
    #   Obtain each abstract
    #   Shorten the abstract
    #   Obtain each interaction URL
    #   Obtain each interactionName
    #   Obtain each interaction date & time
    #   Obtain each interaction city, state/province, country
    #   Format the interaction data
    #   Add to parent object, but we might need to added to the docx structure here
    # Save the document
    # If the save works return true and exit
    # Should also consider if this was called by report_all we need to do something different, see the all and doc arguments above
    pass

if __name__ == "__main__":
    printer=pprint.PrettyPrinter()
    my_args=parse_cli_args()
    configurator=read_config(conf_file=my_args.config_file)

    # Set default items from the configuration file for the report
    report_conf={
        'org': configurator['DEFAULT']['organization_name'],
        'logo': configurator['DEFAULT']['logo_image'],
        'font': configurator['DEFAULT']['font_type'],
        'font_size': configurator['DEFAULT']['font_size'],
        'font_measure': configurator['DEFAULT']['font_measure'],
        'copyright': configurator['DEFAULT']['copy_right_notice'],
        'confidentiality': configurator['DEFAULT']['confidential_notice'],
    }

    auth_ctl=authenticate(user_name=my_args.user, secret=my_args.secret, rest_server_url=my_args.rest_url)
    credential=auth_ctl.login()
    study_ctl=study(credential)
    success, study_obj=study_ctl.get_by_guid(my_args.guid)
    if success:
        document=report(study_obj, my_args.report_format, report_conf)
        
    else:
        print('CLI ERROR: This is a generic error message, as something went wrong.')
        sys.exit(-1)