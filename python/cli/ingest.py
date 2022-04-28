#!/usr/bin/python3
import os, argparse, cmd, re, magic, pyfiglet, pdfx, pydocx, datetime, spacy, pprint
from pptx import Presentation
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

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
            'folder': "",
            'max interactions': 5
        }
        self.printer = pprint.PrettyPrinter(indent=4)
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
            answer = input('Enter the '+ obj_type + '\'s ' + obj_topic + ' [Default: Unknown]?  ').strip()
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
        doc_meta = pdf.get_metadata()
        return doc_meta, pdf.get_text()

    def _get_docx_meta(self, item):
        doc_metadata = {}
        doc = pydocx.Document(self.env['folder'] + '/' + item)
        properties = doc.core_properties
        doc_metadata['CreateDate'] = properties.created
        doc_metadata['type'] = properties.category
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return doc_metadata, '\n'.join(fullText)

    def _get_pptx_meta(self, item):
        doc_metadata = {}
        preso = Presentation(self.env['folder'] + '/' + item)
        properties = preso.core_properties
        doc_metadata['CreateDate'] = properties.created
        doc_metadata['type'] = properties.category
        return doc_metadata

    def _setup_study(self, study_name):
        """Script to define several default attributes for the discovered study
        """
        default = 'Unknown'
        my_study = {}
        my_script = {
            'description': 'description',
            'access privileges': 'public',
            'accessible groups': 'groups',
        }
        print('\nStep 1: Define key attributes for the study.')
        answer = input('\tname [default: ' + study_name + ']: ').strip()
        if not answer: answer = study_name
        my_study['studyName'] = answer
        for attribute in my_script:
            answer = input('\t' + attribute +': ').strip()
            if not answer: answer = default
            my_study[attribute] = answer
        my_study['substudies'] = {}
        return my_study

    def _print_entities(self, entities):
        idx = 0
        ENTITY_NAME = 0
        ENTITY_TYPE = 1
        ENTITY_DESC = 2
        for entity in entities:
            print('\t\t', str(idx) + '. ', 'Name: ' + entity[ENTITY_NAME], '[Type: ' + entity[ENTITY_TYPE], ' | Desc: ' + entity[ENTITY_DESC] + ']')
            idx+=1



    def do_discover(self, sub_folder):
        # Setup the study
        my_study = self._setup_study(sub_folder)

        # Create empty interactions and companies
        my_interactions = []
        my_companies = []

        # Create the nlp obj
        nlp = spacy.load("en_core_web_lg")

        # Capture the files which will be transformed into at least interactions
        print ('\nStep 2: Discover interactions and companies associated to the study.')
        self.folder_data = self.filter_raw(os.listdir(self.env['folder'] + '/' + sub_folder))
        if len(self.folder_data) <= self.env['max interactions']:
            print ('\tIt appears there\'s ' + str(self.env['max interactions']) + ' or less target interactions, so the ingest tools will explore them with you one-by-one.')


        for item in self.folder_data:
            # Set the time to now as a default in case we cannot get inputs from the content
            the_time = datetime.datetime.now()
            date = the_time.strftime("%Y%m%d") # Format YYYYMM
            time = the_time.strftime("%H%M") # Format HHMM

            # Get the type of file system object to determine how to proceed

            # We don't know the type until we check
            doc_type = 'unknown' 

            # Is this a directory?
            if os.path.isdir(self.env['folder'] + '/' + sub_folder + '/' + item): doc_type = 'dir'

            # Assumes the file type from the extension is unreliable uses libmagic instead
            else: doc_type = self.item_type(sub_folder + '/' + item)

            # Print the overall status and next steps
            print('\n\t\tInspecting', '>' * 2, item)
            print('\t\tDetecting common metadata and named entities.')

            entities = []
            # Extract essential metadata from PDFs
            if re.match(r'^PDF', doc_type, re.IGNORECASE):
                [my_meta, my_text] = self._get_pdf_meta(sub_folder + '/' + item)
                doc = nlp(my_text)
                if 'xap' in my_meta:
                    raw_date = my_meta['xap']['CreateDate']
                    [date, time] = raw_date.split('T')
                    date = date.replace('-', '')
                    time = ''.join(time.split('-')[0].split(':')[0:2])
                for my_ent in doc.ents:
                    my_text = re.sub(r'\n+', ' ', my_ent.text)
                    entities.append([my_text, my_ent.label_, spacy.explain(my_ent.label_)])


            # Extract essential metadata from PPTX
            elif re.match(r'^Microsoft PowerPoint', doc_type, re.IGNORECASE): 
                my_meta = self._get_pptx_meta(sub_folder + '/' + item)
                date = my_meta['CreateDate'].strftime("%Y%m%d")
                time = my_meta['CreateDate'].strftime("%H%M")

            # Extract essential metadata from DOCX
            elif re.match(r'^Microsoft Word', doc_type, re.IGNORECASE):
                my_meta = self._get_docx_meta(sub_folder + '/' + item)
                date = my_meta['CreateDate'].strftime("%Y%m%d")
                time = my_meta['CreateDate'].strftime("%H%M")

            elif doc_type == 'dir':
                pass
                # TODO think about how to create a function from the above and recurse into subdirs
                # TODO Set a flag to recurse only one level

            # Fallback to not doing anything
            else:
                pass

            self._print_entities(entities)
            my_company = input('\n\t\tDo any entities represent the company associated to this item? If so specify the number of the entity. ').strip()
            my_noise = input('\t\tShould we add these entities to the substudy associated to this interaction? [Y/n] ').strip()

            my_interaction = {
                'interactionName': item.split('.')[0],
                'time': time,
                'date': date,
            }
            my_interactions.append(my_interaction)

        self.interactions+=my_interactions
        self.studies = [my_study]

        

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