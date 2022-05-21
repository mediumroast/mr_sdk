#!/usr/bin/python3
import os
import argparse
import cmd
import re
from matplotlib.font_manager import json_dump
import pyfiglet
import pprint
import json
import pathlib

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
    parser.add_argument('--env_file', help="Fully qualified filename for storing the environment variables.",
                        type=str, dest='env_file', default=str(pathlib.Path.home()) + '/.mediumroast/ingest.json')
    cli_args = parser.parse_args()
    return cli_args


class IngestShell(cmd.Cmd):
    prompt = 'mr_ingest> '
    intro = pyfiglet.figlet_format('Welcome to Mediumroast ingest tools.')
    ruler = '_'

    def __init__(self, src_type, env_file, env = None):
        self.src_type = src_type
        self.companies = []
        self.studies = []
        self.interactions = []

        self.env_file = env_file
        self.env = env if env else {
            'copyright': "Copyright 2022 Mediumroast, Inc. All rights reserved.",
            'support email': 'help@mediumroast.io',
            'version': '1.0.0',
            'folder': "",
            'max interactions': 5
        }

        self.printer = pprint.PrettyPrinter(indent=4)
        self.util = utilities()
        super(IngestShell, self).__init__()


    ## TODO Create utilities for saving/caching and recovering work


    #############################################################################
    # Description: Basic reusable utility functions for the command shell
    #
    # TODO consider moving out into helpers or consider a shell class to include
    #
    #############################################################################

    def _print_raw_objs(self, objs):
        """Print basic data suitable for driving discovery from a file/object store of some kind.
        """
        for obj in sorted(objs):
            # printing format is two tabs <key>. <value>
            print('\t\t', str(obj) + '.', objs[obj])

    def _print_help(self, help):
        """Consistently print help outputs for the shell. This internal method expects a dict of structure:
            {
                'Name': <command name>,
                'Description': <description>,
                'Argument': <arguments could be None>
            }
        Note: Each value in the dict is a string which can include formatting like newlines, tabs, etc.
        """
        print("\n" + help['Name'] + ' ' +
              help['Argument'] + help['Description'])

    def _filter_raw(self, dir_list):
        """Safely filter out file system objects that should not be interrogated
        """
        final_list = []
        for item in dir_list:
            if re.match(r'^\.', item):
                continue
            elif re.match(r'^Icon', item):
                continue
            else:
                final_list.append(item)
        return final_list

    def _decode_folder(self):
        """When passed a folder structure, print out contents of the folder including the object type.
        """
        folder_string = "\n" + self.env['folder'] + " [folder]\n"
        idx = 1
        for item in self.folder_data:
            if os.path.isdir(self.env['folder'] + '/' + item):
                folder_string+= "\t" + str(idx) +". " + item + " [dir]\n"
            else:
                folder_string+= "\t" + str(idx) +". " + item + " [" + self.util.get_item_type(item) + "]\n" 
            idx+=1
        return folder_string

    def _print_discovered_objects(self, obj):
        """To the console print out the top level objects discovered from a file or object store.
        """
        index = 0
        for item in obj:
            print('Item index: ' + str(index))
            for attribute in item:
                print("\t", attribute + ':', item[attribute])
            print('-' * 30)
            index += 1


    #############################################################################
    # Description: Core functions for the command shell
    #
    # TODO consider adding envsave to set and del functions
    #
    #############################################################################

    def emptyline(self):
        """Needed for the empytline processing in the shell. Do not remove or change the name.
        """
        pass

    def do_exit(self, unused):
        """Required for exiting the shell argument is unused. Do not remove or change the name.
        """
        return True

    def help_exit(self):
        """Help for exit.
        """
        my_help = {
            'Name': 'exit',
            'Argument': 'None',
            'Description': "\n\tExit the mediumroast ingestion utility shell." +
            "\n"
        }
        self._print_help(help=my_help)


    def do_print(self, obj_type):
        """Print out objects which are discovered from the file system or object store. Only accepts objects including companies, interactions and studies.  If the object is unsupported it will provide an error.
        """
        obj_type = obj_type.strip().lower()
        print('The following ' + obj_type + ' are prepared for ingestion.')
        if obj_type == 'companies':
            self._print_discovered_objects(self.companies)
        elif obj_type == 'studies':
            self._print_discovered_objects(self.studies)
        elif obj_type == 'interactions':
            self._print_discovered_objects(self.interactions)
        else:
            print("\n\tError: Unsupported object type [" + obj_type +
                  ']. Supported types are: studies, companies or interactions.')

    def help_print(self):
        """Help for do_print
        """
        my_help = {
            'Name': 'print',
            'Argument': '<object type>',
            'Description': "\n\tPrint out the current set of objects ready for ingestion, where object types are companies, studies or interactions." +
            "\n"
        }
        self._print_help(help=my_help)

    def do_list(self, folder):
        """List a supplied folder and store the it as the current folder for later usage in discovery.
        """
        self.env['folder'] = folder if folder else self.env['folder']
        self.folder_data = self._filter_raw(os.listdir(self.env['folder']))
        print(self._decode_folder())

    def help_list(self):
        """Help for do_list
        """
        my_help = {
            'Name': 'list',
            'Argument': '<folder_name>',
            'Description': "\n\tList contents of a folder to explore for an ingestion strategy." +
            "\n"
        }
        self._print_help(help=my_help)

    def do_set(self, env_var):
        """Set environment variables to use in the ingestion shell. Note that unless envsave is performed the variables aren't saved over multiple runs of the tools.
        """
        variable, value = env_var.split('=')
        self.env[variable.strip()] = value.strip()

    def help_set(self):
        """Help for do_set
        """
        my_help = {
            'Name': 'set',
            'Argument': '<variable>=<value>',
            'Description': "\n\tSet an environment variable for the ingest shell to use while processing." +
            "\n"
        }
        self._print_help(help=my_help)

    def do_del(self, env_var):
        """Remove an environment variable. Note that unless envsave is performed the variables aren't removed over multiple runs of the tools.
        """
        del self.env[env_var]

    def help_del(self):
        """Help for do_del
        """
        my_help = {
            'Name': 'del',
            'Argument': '<variable>',
            'Description': "\n\Delete an environment variable." +
            "\n"
        }
        self._print_help(help=my_help)

    def do_envsave(self, unused):
        """Save the environment variables to local storage as defined in the self.env_file attribute.
        """
        self.util.save(self.env_file, json.dumps(self.env))

    def help_envsave(self):
        """Help for do_envsave
        """
        my_help = {
            'Name': 'envsave',
            'Argument': 'None',
            'Description': "\n\tSave the environmental settings to the ~/.mediumroast/ingest.json file." +
            "\n"
        }
        self._print_help(help=my_help)

    def do_envprint(self, unused):
        """Print out the environment variables to the console.
        """
        for key in self.env:
            print ('\t' + key + ':', self.env[key])

    def help_envprint(self):
        """Help for do_envprint
        """
        my_help = {
            'Name': 'envprint',
            'Argument': 'None',
            'Description': "\n\tPrint the environmental settings." +
            "\n"
        }
        self._print_help(help=my_help)


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
    # TODO Create document strings for each method
    # TODO Add a second phase post initial ingestion that fixes the linked_companies, et al, guids
    # TODO Consider how to create a discover option that will traverse into a top level folder, or 
    #       enable a folder to be added to an existing study as a substudy.  The second one is likely
    #       better as it will keep the tool simpler.
    #
    #############################################################################

    def _merge_dicts(self, primary, to_merge):
        my_keys = primary.keys()
        # last_key = my_keys[-1] # TODO fix this error is TypeError: 'dict_keys' object is not subscriptable
        last_key = self.util.total_item(primary)
        for key in to_merge:
            primary[last_key] = to_merge[key]
            last_key += 1
        return primary

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

    def _retain_companies(self, index, companies, study_name):
        for idx in index:
            key = int(idx)
            self.companies.append({
                'companyName': companies[key],
                'temp_id': self.util.hash_it(companies[key]),
                'linkedStudies': {study_name: self.util.hash_it(study_name)},
                'linkedInteractions': {}
            })

    def _choose_company(self, interaction_name, companies):
        print('\tPlease choose which company is associated to the interaction [' + interaction_name + '].\n')
        for company in sorted(companies):
            print('\t' + str(company) + '. ', companies[company])
        selected_company = int(input(
            '\n\tSelect the company using the index [Ex. - \'1,3,7\']: ').strip())
        return {companies[selected_company]: self.util.hash_it(companies[selected_company])}

    def _retain_interactions(self, index, interactions, study_name):
        my_substudies = {}
        idx = 0
        for i in index:
            key = int(i) - 1

            # Choose the associated company
            linked_company = self._choose_company(
                interactions[key]['interaction_name'],
                interactions[key]['candidate_companies'])

            # Add the interaction
            self.interactions.append(
                {
                    'interactionName': interactions[key]['interaction_name'], # CONFIRM on the attribute name 'interactionName or 'name'?
                    'linkedStudies': {
                        interactions[key]['study']: self.util.hash_it(
                            study_name)  # TODO replace with the real GUID
                    },
                    'linkedCompanies': linked_company,  # TODO replace with the real GUID
                    'date': interactions[key]['date'],
                    'time': interactions[key]['time'],
                    'state': 'unsummarized',  # CONFIRM this is not boolean
                    'description': 'Unknown',  # CONFIRM that this is the right attribute
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
                    'notes': {},  # TODO create a note stating this was ingested by mr-ingest
                    'url': interactions[key]['url'],
                    # TODO reset to the actual GUID and delete
                    'temp_id': interactions[key]['temp_id']
                }
            )

            # Check if dict key exists first, and if not create the object
            if my_substudies.get(interactions[key]['substudy']) == None:
                my_substudies[interactions[key]['substudy']] = {
                    'description': 'This is the default substudy' if interactions[key]['substudy'] == 'default' else 'Unknown',
                    'name': 'default' if interactions[key]['substudy'] == 'default' else 'Unknown',
                    'interactions': {
                        interactions[key]['interaction_name']: {
                            'temp_id': interactions[key]['temp_id']  # TODO
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

                my_substudies[interactions[key]['substudy']]['noises'] = self._merge_dicts(
                    my_substudies[interactions[key]['substudy']]['noises'], interactions[key]['noises'])

            # print companies
            # select company
            #

        return my_substudies

    def do_discover(self, sub_folder):
        # Set up the extractor to do object level discovery
        extractor = Extract(folder_name=self.env['folder'] + '/' + sub_folder) if self.env['folder'] else Extract(folder_name=sub_folder)

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
        self._print_raw_objs(my_companies)
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
        my_study['substudies'] = self._retain_interactions(
            selected_interactions, my_interactions, my_study['studyName'])
        self.studies.append(my_study)

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
        self._print_help(help=my_help)


if __name__ == "__main__":

    # Determine if we're running on the local file system or remote
    my_args = parse_cli_args()
    if my_args.src_type == 'local': # TODO when other drives are supported add choices in parse_args for the switch
        pass
    else:
        exit()
    # TODO investigate adding: GDrive and OneDrive

    # Check to see if the env_file exists and if it does read it in and pass to the shell
    u = utilities()
    [exists, msg] = u.check_file_system_object(my_args.env_file)
    if exists:
        [status, my_env] = u.json_read(my_args.env_file)
        IngestShell(my_args.src_type, my_args.env_file, env=my_env).cmdloop()
    else:   
        IngestShell(my_args.src_type, my_args.env_file).cmdloop()
