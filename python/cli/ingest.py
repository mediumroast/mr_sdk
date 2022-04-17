#!/usr/bin/python3
import os, argparse, cmd, re, magic, pyfiglet, pdfx

def parse_cli_args(program_name='ingest', desc='A mediumroast.io example utility to ingest data into the backend.'):
    parser=argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument ('--rest_url', help="The URL of the target REST server", type=str, dest='rest_url', default='http://mr-01:3000')
    parser.add_argument ('--folder', help="The full path to the folder to inspect for ingestion", type=str, dest='folder')
    parser.add_argument ('--src_type', help="The source type for ingestion", type=str, dest='src_type', default='local', choices=['local', 'sharepoint'])
    parser.add_argument ('--user', help="User name", type=str, dest='user', default='foo')
    parser.add_argument ('--secret', help="Secret or password", type=str, dest='secret', default='bar')
    cli_args = parser.parse_args ()
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
        self.env={
            'copyright': "Copyright 2022 Mediumroast, Inc. All rights reserved.",
            'support email': 'help@mediumroast.io',
            'version': '1.0.0',
            'folder': ""
        }
        super(IngestShell, self).__init__()

    #############################################################################
    # Description: Basic reusable utility functions for the command shell
    #
    #
    #
    #############################################################################

    def print_help(self, help):
        print("\n" + help['Name'] + ' ' + help['Argument'] + help['Description'])

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
    
    def do_print (self, obj_type):
        obj_type = obj_type.strip().lower()
        print('The following ' + obj_type + ' are prepared for ingestion.')
        if obj_type == 'companies':
            self.print_objects(self.companies)
        elif obj_type == 'studies':
            self.print_objects(self.studies)
        elif obj_type == 'interactions':
            self.print_objects(self.interactions)
        else:
            print("\n\tError: Unsupported object type [" + obj_type + ']. Supported types are: studies, companies or interactions.')

    def help_print(self):
        my_help = {
            'Name': 'print',
            'Argument': '<object type>',
            'Description': "\n\tPrint out the current set of objects ready for ingestion, where object types are companies, studies or interactions." +
                "\n"
        }
        self.print_help(help=my_help)

    def item_type(self, item):
        return magic.from_file(self.env['folder'] + '/' + item)
    
    def decode_folder(self):
        folder_string = "\n" + self.env['folder'] + " [folder]\n"
        idx = 1
        for item in self.folder_data:
            if os.path.isdir(self.env['folder'] + '/' + item):
                folder_string+= "\t" + str(idx) +". " + item + " [dir]\n"
            else:
                folder_string+= "\t" + str(idx) +". " + item + " [" + self.item_type(item) + "]\n" 
            idx+=1
        return folder_string

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
            index+=1

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
            print('Enter the '+ obj_type + '\'s ' + obj_topic + ' [Default: Unknown]?  ', end='')
            answer = input().strip()
            if not answer: answer = default
            my_obj[obj_script[obj_topic]] = answer # Set to the final structure for the API
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
        return self._add_object('interaction',my_script)

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
            print("\n\tError: Unsupported subcommand [" + sub_command + ']. Supported subcommands are: study, company or interaction.')

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
    #   discover Competition - creates a study called 'Competition', and tries to discover companies and interactions in 'Competition'
    #
    #############################################################################

    def _get_pdf_meta(self, item):
        pdf = pdfx.PDFx(self.env['folder'] + '/' + item)
        meta = pdf.get_metadata()
        return meta

    def do_discover(self, sub_folder):
        my_study = {'studyName': sub_folder}
        my_interactions = []
        my_companies = []
        self.folder_data = self.filter_raw(os.listdir(self.env['folder'] + '/' + sub_folder))
        for item in self.folder_data:
            doc_type = self.item_type(sub_folder + '/' + item)
            if re.match(r'^PDF', doc_type):
                my_meta = self._get_pdf_meta(sub_folder + '/' + item)
                date = None
                time = None
                if 'xap' in my_meta:
                    raw_date = my_meta['xap']['CreateDate']
                    [date, time] = raw_date.split('T')
                    date = date.replace('-', '')
                    time = ''.join(time.split('-')[0].split(':')[0:2])
            my_interaction = {
                'interactionName': item.split('.')[0],
                'time': time,
                'date': date,
            }
            my_interactions.append(my_interaction)

        self.interactions+=my_interactions

        

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

    my_args=parse_cli_args()
    if my_args.src_type == 'local':
        pass
    else:
        exit()

    IngestShell('foo').cmdloop()