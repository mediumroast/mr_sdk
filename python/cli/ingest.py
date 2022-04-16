#!/usr/bin/python3
import os, argparse, cmd, re, magic, pyfiglet

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
        self.authors = ['Michael Hay']
        self.copyright = "Copyright 2022 Mediumroast, Inc. All rights reserved."
        self.src_type = src_type
        self.env={}
        super(IngestShell, self).__init__()

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

    def item_type(self, item):
        return magic.from_file(self.folder + '/' + item) #, mime=True) 
    
    def decode_folder(self):
        folder_string = "\n" + self.folder + " [folder]\n"
        idx = 1
        for item in self.folder_data:
            if os.path.isdir(self.folder + '/' + item):
                folder_string+= "\t" + str(idx) +". " + item + " [dir]\n"
            else:
                folder_string+= "\t" + str(idx) +". " + item + " [" + self.item_type(item) + "]\n" 
            idx+=1
        return folder_string

    def do_list(self, folder):
        self.folder = folder
        self.folder_data = self.filter_raw(os.listdir(self.folder))
        print(self.decode_folder())

    def help_list(self):
        my_help = {
            'Name': 'list',
            'Argument': '<folder_name>',
            'Description': "\n\tList contents of a folder to explore for an ingestion strategy." + 
                "\n"
        }
        self.print_help(help=my_help)

    def do_process(self, folder):
        pass

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

    def help_process(self):
        print("\nprocess [folder name]\nPerform steps needed to process an individual folder and the children.")

    def print_object(self, obj):
        for item in obj:
            print("\t", item + ':', obj[item])

    def add_company(self):
        my_script = [
            'name',
            'description',
            'address',
            'city',
            'state/province',
            'zip/postal code',
            'country',
            'region',
            'phone number',
            'website',
            'logo URL',
            'industry',
            'CIK',
            'stock symbol'
        ]
        my_company = {}
        for topic in my_script:
            default = 'Unknown'
            print('Do you know the company\'s ' + topic + ' [Default: Unknown]?  ', end='')
            answer = input().strip()
            if not answer: answer = default
            my_company[topic] = answer

        print('Preparing to add company with the following attributes:')
        self.print_object(my_company)


    def do_add(self, sub_command):
        sub_command = sub_command.strip().lower()
        if sub_command == 'company':
            self.add_company()
        elif sub_command == 'study':
            self.add_study()
        elif sub_command == 'interaction':
            self.add_interaction()


if __name__ == "__main__":

    my_args=parse_cli_args()
    if my_args.src_type == 'local':
        pass
    else:
        exit()

    IngestShell('foo').cmdloop()