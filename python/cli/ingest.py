#!/usr/bin/python3
from ctypes import util
import os
import argparse
import cmd
import re
import pyfiglet
import pprint

from soupsieve import select
from mediumroast.extractors.folder import Extract
from mediumroast.helpers import utilities


def parse_cli_args(program_name='ingest', desc='A mediumroast.io example utility to ingest data into the backend.'):
    parser = argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument('--rest_url', help="The URL of the target REST server",
                        type=str, dest='rest_url', default='http://mr-01:3000')
    parser.add_argument(
        '--folder', help="The full path to the folder to inspect for ingestion", type=str, dest='folder')
    parser.add_argument('--src_type', help="The source type for ingestion",
                        type=str, dest='src_type', default='local', choices=['local', 'sharepoint'])
    parser.add_argument('--user', help="User name",
                        type=str, dest='user', default='foo')
    parser.add_argument('--secret', help="Secret or password",
                        type=str, dest='secret', default='bar')
    cli_args = parser.parse_args()
    return cli_args


class IngestShell(cmd.Cmd):
    prompt = 'mr_ingest> '
    intro = pyfiglet.figlet_format('Welcome to Mediumroast ingest tools.')
    ruler = '_'

    def __init__(self, src_type):
        self.src_type = src_type
        self.companies = []
        self.studies = []
        self.interactions = []
        self.env = {
            'copyright': "Copyright 2022 Mediumroast, Inc. All rights reserved.",
            'support email': 'help@mediumroast.io',
            'version': '1.0.0',
            'folder': "",
            'max interactions': 5
        }

        self.printer = pprint.PrettyPrinter(indent=4)
        self.util = utilities()
        super(IngestShell, self).__init__()

    #############################################################################
    # Description: Basic reusable utility functions for the command shell
    #
    #
    #
    #############################################################################

    def print_help(self, help):
        print("\n" + help['Name'] + ' ' +
              help['Argument'] + help['Description'])

    def emptyline(self):
        pass

    def do_exit(self, line):
        return True

    def help_exit(self):
        print("\nExit the shell")

    def filter_raw(self, dir_list):
        final_list = []
        for item in dir_list:
            if re.match(r'^\.', item):
                continue
            elif re.match(r'^Icon', item):
                continue
            else:
                final_list.append(item)
        return final_list

    def do_print(self, obj_type):
        obj_type = obj_type.strip().lower()
        print('The following ' + obj_type + ' are prepared for ingestion.')
        if obj_type == 'companies':
            self.print_objects(self.companies)
        elif obj_type == 'studies':
            self.print_objects(self.studies)
        elif obj_type == 'interactions':
            self.print_objects(self.interactions)
        else:
            print("\n\tError: Unsupported object type [" + obj_type +
                  ']. Supported types are: studies, companies or interactions.')

    def help_print(self):
        my_help = {
            'Name': 'print',
            'Argument': '<object type>',
            'Description': "\n\tPrint out the current set of objects ready for ingestion, where object types are companies, studies or interactions." +
            "\n"
        }
        self.print_help(help=my_help)

    def do_list(self, folder):
        self.env['folder'] = folder if folder else self.env['folder']
        self.folder_data = self.filter_raw(os.listdir(self.env['folder']))
        print(self.decode_folder())

    def help_list(self):
        my_help = {
            'Name': 'list',
            'Argument': '<folder_name>',
            'Description': "\n\tList contents of a folder to explore for an ingestion strategy." +
            "\n"
        }
        self.print_help(help=my_help)

    def do_set(self, env_var):
        variable, value = env_var.split('=')
        self.env[variable] = value
        print(self.env)

    def help_set(self):
        my_help = {
            'Name': 'set',
            'Argument': '<variable>=<value>',
            'Description': "\n\tSet an environment variable for the ingest shell to use while processing." +
            "\n"
        }
        self.print_help(help=my_help)

    def print_objects(self, obj):
        index = 1
        for item in obj:
            print('Item index: ' + str(index))
            for attribute in item:
                print("\t", attribute + ':', item[attribute])
            print('-' * 30)
            index += 1

    #############################################################################
    #
    # NAME: Add Objects
    # Description: Core logic and helpers to add objects one at a time using a prompt
    # Syntax: add <object type>
    # Argument: <object type> can be one of study, company or interaction
    # Core methods:
    #   add study - starts a prompt based interface to add a study
    #   print studies - prints out all added studies
    #
    #############################################################################
    def _add_object(self, obj_type, obj_script):
        my_obj = {}
        for obj_topic in obj_script:
            default = 'Unknown'
            answer = input('Enter the ' + obj_type + '\'s ' +
                           obj_topic + ' [Default: Unknown]?  ').strip()
            if not answer:
                answer = default
            # Set to the final structure for the API
            my_obj[obj_script[obj_topic]] = answer
        return my_obj

    def add_study(self):
        # TODO in the far future consider type checking for select attributes
        my_script = {
            'name': 'studyName',
            'description': 'description',
            'access privileges': 'public',
            'accessible groups': 'groups',
        }
        return self._add_object('study', my_script)

    def add_interaction(self):
        # TODO in the far future consider type checking for select attributes
        my_script = {
            'name': 'interactionName',
            'time': 'time',
            'date': 'date',
            'state': 'state',
            'description': 'description',
            'contact name': 'contactName',
            'contact address': 'contactAddress',
            'contact city': 'contactCity',
            'contact state/province': 'contactStateProvince',
            'contact zip/postal code': 'contactZipPostal',
            'contact country': 'contactCountry',
            'contact region': 'contactRegion',
            'contact phone number': 'contactPhone',
            'contact LinkedIn profile': 'contactLinkedIn',
            'contact Twitter profile': 'contactTwitter',
            'contact email address': 'contactEmail',
            'access privileges': 'public',
            'interaction type': 'interactionType',
            'status': 'status',
            'url': 'url'
        }
        return self._add_object('interaction', my_script)

    def add_company(self):
        # TODO in the far future consider type checking for select attributes
        my_script = {
            'name': 'companyName',
            'description': 'description',
            'address': 'address',
            'city': 'city',
            'state/province': 'stateProvince',
            'zip/postal code': 'zipPostal',
            'country': 'country',
            'region': 'region',
            'phone number': 'phone',
            'website': 'url',
            'logo URL': 'logoURL',
            'industry': 'industry',
            'CIK': 'cik',
            'stock symbol': 'stockSymbol'
        }
        return self._add_object('company', my_script)

    def do_add(self, sub_command):
        sub_command = sub_command.strip().lower()
        if sub_command == 'company':
            self.companies.append(self.add_company())
        elif sub_command == 'study':
            self.studies.append(self.add_study())
        elif sub_command == 'interaction':
            self.interactions.append(self.add_interaction())
        else:
            print("\n\tError: Unsupported subcommand [" + sub_command +
                  ']. Supported subcommands are: study, company or interaction.')

    def help_add(self):
        my_help = {
            'Name': 'add',
            'Argument': '<subcommand>',
            'Description': "\n\tAdd one or more company, interaction or study objects by hand through a series of prompts." +
            "\n\tSubcommand can be one of study, company or interaction." +
            "\n"
        }
        self.print_help(help=my_help)

    #############################################################################
    #
    # NAME: Discover Objects
    # Description: Core logic and helpers to discover objects based upon a folder
    # Syntax: discover <sub_folder>
    # Argument: <sub_folder> is a child to the internally set folder in the 'env'
    # Core methods:
    #   discover Competition - creates a study called 'Competition', and
    #       tries to discover companies and interactions in 'Competition'
    #
    #############################################################################

    def _setup_study(self, study_name):
        """Script to define several default attributes for the discovered study
        """
        study_name = study_name.split('/')[-1]
        default = 'Unknown'
        my_study = {}
        my_script = {
            'description': 'description',
            'access privileges': 'public',
            'accessible groups': 'groups',
        }
        print('\nStep 1: Define key attributes for the study.')
        answer = input('\tname [default: ' + study_name + ']: ').strip()
        if not answer:
            answer = study_name
        my_study['studyName'] = answer
        for attribute in my_script:
            answer = input('\t' + attribute + ': ').strip()
            if not answer:
                answer = default
            my_study[attribute] = answer
        my_study['substudies'] = {}
        my_study['temp_id'] = self.util.hash_it(my_study['studyName'])
        return my_study

    def _print_objs(self, objs):
        for obj in sorted(objs):
            print('\t\t', str(obj) + '. ', objs[obj])

    def _retain_companies(self, index, companies, study_name):
        for idx in index:
            key = int(idx)
            self.companies.append({
                'companyName': companies[key],
                'temp_id': self.util.hash_it(companies[key]),
                'linkedStudies': {study_name: self.util.hash_it(study_name)},
                'linkedInteractions': {}
            })

    def _choose_company(self, companies):
        print('\tPlease choose which company is associated to the interaction.\n')
        for company in sorted(companies):
            print('\t' + str(company),'. ', companies)
        selected_company = input(
            '\n\tSelect the company using the index [Ex. - \'1,3,7\']: ').strip().split(',')
        return {companies[selected_company]: self.util.hash_it(companies[selected_company])}

    def _retain_interactions(self, index, interactions, study_name):
        my_substudies = {}
        idx = 0
        for i in index:
            key = int(i) - 1

            # Choose the associated company
            linked_company = self._choose_company(interactions[key]['candidate_companies'])

            # Add the interaction
            self.interactions.append(
                {
                    'interactionName': interactions[key]['interaction_name'], #TODO should we replace with name?
                    'linkedStudies': {
                        interactions[key]['study']: self.util.hash_it(study_name) # TODO replace with the real GUID
                    },
                    'linkedCompanies': linked_company, # TOTO replace with the real GUID
                    'date': interactions[key]['date'],
                    'time': interactions[key]['time'],
                    'state': 'unsummarized', # CONFIRM this is not boolean
                    'description': 'Unknown', # CONFIRM that this is the right attribute
                    'contactAddress': 'Unknown',
                    'contactZipPostal': 'Unknown',
                    'contactPhone': 'Unknown',
                    'contactLinkedIn': 'Unknown',
                    'contactEmail': 'Unknown',
                    'contactTwitter': 'Unknown',
                    'contactName': 'Unknown',
                    'public': False,
                    'abstract': 'Unknown',
                    'interactionType': 'Unknown',
                    'status': 'completed',
                    'longitude': 'Unknown',
                    'latitude': 'Unknown',
                    'notes': {}, # TODO create a note stating this was intgested by mr-ingest
                    'url': interactions[key]['url'],
                    'temp_id': interactions[key]['temp_id'] # TODO reset to the actual GUID and delete
                }
            )

            # Check if dict key exists first, and if not create the object
            if my_substudies.get(interactions[key]['substudy']) == None:
                my_substudies[interactions[key]['substudy']] = {
                    'description': 'This is the default substudy' if interactions[key]['substudy'] == 'default' else 'Unknown',
                    'name': 'default' if interactions[key]['substudy'] == 'default' else 'Unknown',
                    'interactions': {
                        interactions[key]['interaction_name']: {
                            'temp_id': interactions[key]['temp_id'] # TODO 
                        }
                    },
                    'themesState': False,
                    'noises': interactions[key]['noises'],
                    'keyThemes': {},
                    'keyThemeQuotes': {}
                }
            # If the key exists add to the object
            else:
                my_substudies[interactions[key]['substudy']]['interactions'][interactions[key]
                                                                              ['interaction_name']] = {'temp_id': interactions[key]['temp_id']}
                # This is broken as it will merge the dicts and replace duplicate keys
                # TODO create a new function that unrolls and rebuilds a dict that is reindexed
                my_substudies[interactions[key]['substudy']]['noises'] |= interactions[key]['noises']

            # print companies
            # select company
            #

        return my_substudies

    def do_discover(self, sub_folder):
        # Set up the extractor to do object level discovery
        extractor = Extract(folder_name=sub_folder)

        # Setup the study
        my_study = self._setup_study(sub_folder)

        # Inspect the files to generate candidate interactions and companies
        print('\nStep 2: Discover interactions and companies associated to the study.')

        # Perform discovery
        [my_interactions, my_companies] = extractor.get_data()
        total_interactions = self.util.total_item(my_interactions)
        total_companies = self.util.total_item(my_companies)
        print('\tDiscovered [' + str(total_interactions) + '] candidate interactions and [' +
              str(total_companies) + '] candidate companies.')

        # Process companies
        print('\nStep 3: Process candidate companies.')
        print('\tListing candidate companies for review:')
        self._print_objs(my_companies)
        selected_companies = input(
            '\n\tSelect companies to retain using their index [Ex. - \'1,3,7\']: ').strip().split(',')
        print(
            '\tRetaining [' + str(self.util.total_item(selected_companies)) + '] companies.')
        self._retain_companies(
            selected_companies, my_companies, my_study['studyName'])

        # Process interactions
        print('\nStep 4: Process candidate interactions.')
        print('\tListing candidate interactions for review:')
        idx = 1
        for interaction in my_interactions:
            print('\t\t', str(idx) + '. ', interaction['interaction_name'])
            idx += 1
        selected_interactions = input(
            '\n\tSelect interactions to retain using their index [Ex. - \'1,3,7\']: ').strip().split(',')
        print(
            '\tRetaining [' + str(self.util.total_item(selected_interactions)) + '] interactions.')
        self._retain_interactions(
            selected_interactions, my_interactions, my_study['studyName'])

        # if len(self.folder_data) <= self.env['max interactions']:
        #     print ('\tIt appears there\'s ' + str(self.env['max interactions']) + ' or less target interactions, so the ingest tools will explore them with you one-by-one.')

    def help_discover(self):
        my_help = {
            'Name': 'discover',
            'Argument': '<subfolder>',
            'Description': "\n\tDiscover a study, companies and interactions " +
            "\n\tSubcommand can be one of study, company or interaction." +
            "\n"
        }
        self.print_help(help=my_help)


if __name__ == "__main__":

    my_args = parse_cli_args()
    if my_args.src_type == 'local':
        pass
    else:
        exit()

    IngestShell('foo').cmdloop()
