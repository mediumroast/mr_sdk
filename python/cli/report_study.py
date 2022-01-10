#!/bin/env python3

import sys, argparse, configparser, docx

from docx import Document
from docx.shared import Pt
from docx.enum.dml import MSO_THEME_COLOR_INDEX
from datetime import datetime
from mediumroast.api.high_level import Auth as authenticate
from mediumroast.api.high_level import Studies as study
from mediumroast.api.high_level import Interactions as interaction

def parse_cli_args(program_name='report_study', desc='A mediumroast.io utility that generates a report for a study.'):
    parser=argparse.ArgumentParser(prog=program_name, description=desc)
    parser.add_argument ('--rest_url', help="The URL of the target REST server", type=str, dest='rest_url', default='http://mr-01:3000')
    parser.add_argument ('--guid', help="The GUID for the study to be reported on.", type=str, dest='guid', required=True)
    parser.add_argument ('--user', help="User name", type=str, dest='user', default='foo')
    parser.add_argument ('--secret', help="Secret or password", type=str, dest='secret', default='bar')
    parser.add_argument ('--config_file', help="The location to the configuration files", type=str, dest='config_file', default='./reports.ini')
    cli_args = parser.parse_args ()
    return cli_args

def read_config(conf_file='./reports.ini'):
    c=configparser.ConfigParser()
    c.read(conf_file)
    return c

def _create_header(doc_obj, conf, font_size=7):
    date_string=f'{datetime.now():%Y-%m-%d %H:%M}'
    s=doc_obj.sections[0]
    header=s.header
    header_p=header.paragraphs[0]
    header_p.text=conf['org'] + "\t | \t Created on: " + date_string
    style=doc_obj.styles['Header']
    font=style.font
    font.name=conf['font']
    font.size=Pt(font_size)
    header_p.style=doc_obj.styles['Header']

def _create_footer(doc_obj, conf, font_size=7):
    date_string=f'{datetime.now():%Y-%m-%d %H:%M}'
    s=doc_obj.sections[0]
    footer=s.footer
    footer_p=footer.paragraphs[0]
    footer_p.text=conf['confidentiality'] + "\t | \t" + conf['copyright']
    style=doc_obj.styles['Footer']
    font=style.font
    font.name=conf['font']
    font.size=Pt(font_size)
    footer_p.style=doc_obj.styles['Footer']

def _create_cover_page(doc_obj, study, conf, logo_size=60, font_size=30):
    
    # Generics
    title_font_size=Pt(font_size) # Title Font Size
    logo_size=Pt(font_size*2.5)
    
    
    # Organization name and logo
    logo=conf['logo']
    logo_title=doc_obj.add_paragraph().add_run()
    logo_title.add_picture(logo, height=logo_size)

    # Define the Cover Title Style
    org=conf['org'] # Organization
    title="\n\nTitle: " + study['studyName']
    cover_title=doc_obj.add_paragraph(title)
    style=doc_obj.styles['Title']
    font=style.font
    font.name=conf['font']
    font.size=title_font_size
    cover_title.style=doc_obj.styles['Title']

    # Define the Subtitle content
    subtitle="A " + org + " study report enabling attributable market insights."
    cover_subtitle=doc_obj.add_paragraph("")
    s=cover_subtitle.add_run(subtitle)
    subtitle_font=s.font
    subtitle_font.bold=True

    # Define the Author content
    author="Mediumroast Barrista Robot"
    cover_author=doc_obj.add_paragraph("\nAuthor: ")
    a=cover_author.add_run(author)
    author_font=a.font
    author_font.bold=True

    # Define the Creation date content
    creation_date=f'{datetime.now():%Y-%m-%d %H:%M}'
    cover_date=doc_obj.add_paragraph("Creation Date: ")
    d=cover_date.add_run(creation_date)
    date_font=d.font
    date_font.bold=True

    # Add a page break
    doc_obj.add_page_break()
    

def _create_summary(doc_obj, study_doc, conf):
    # Create the Introduction section
    section_title=doc_obj.add_paragraph('Findings') # Create the Findings section
    section_title.style=doc_obj.styles['Title']
    doc_obj.add_heading('Introduction')
    clean_intro=" ".join(study_doc['Introduction'].split("\n"))
    doc_obj.add_paragraph(clean_intro)

    # Create the Opportunity section
    doc_obj.add_heading('Opportunity')
    clean_opportunity=" ".join(study_doc['Opportunity']['text'].split("\n"))
    doc_obj.add_paragraph(clean_opportunity)
    del(study_doc['Opportunity']['text']) # Remove the text section before we process the numbered bullets
    for opp in study_doc['Opportunity']:
        clean_opp=" ".join(study_doc['Opportunity'][opp].split("\n"))
        doc_obj.add_paragraph(clean_opp, style='List Bullet')

    # Create the Action section
    doc_obj.add_heading('Actions')
    clean_action=" ".join(study_doc['Action']['text'].split("\n"))
    doc_obj.add_paragraph(clean_action)
    del(study_doc['Action']['text']) # Remove the text section before we process the numbered bullets
    for action in study_doc['Action']:
        clean_act=" ".join(study_doc['Action'][action].split("\n"))
        doc_obj.add_paragraph(clean_act, style='List Number')

    # Add a page break
    doc_obj.add_page_break()

def _add_hyperlink(paragraph, text, url):
    """Taken from https://stackoverflow.com/questions/47666642/adding-an-hyperlink-in-msword-by-using-python-docx
    """
    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
    hyperlink.set(docx.oxml.shared.qn('r:id'), r_id, )

    # Create a w:r element and a new w:rPr element
    new_run = docx.oxml.shared.OxmlElement('w:r')
    rPr = docx.oxml.shared.OxmlElement('w:rPr')

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    # Create a new Run object and add the hyperlink into it
    r = paragraph.add_run ()
    r._r.append (hyperlink)

    # A workaround for the lack of a hyperlink style (doesn't go purple after using the link)
    # Delete this if using a template that has the hyperlink style in it
    r.font.color.theme_color = MSO_THEME_COLOR_INDEX.HYPERLINK
    r.font.underline = True

    return hyperlink

def _create_reference(interaction_guid, iteration, doc_obj, conf, char_limit=500):
    interaction_ctl=interaction(credential)
    success, interaction_data=interaction_ctl.get_by_guid(interaction_guid)
    if success:
        doc_obj.add_heading(interaction_data['interactionName'], 2)
        my_time=str(interaction_data['time'][0:2]) + ':' + str(interaction_data['time'][2:4])
        my_date=str(interaction_data['date'][0:4]) + '-' + str(interaction_data['date'][4:6]) + '-' \
            + str(interaction_data['date'][6:8])
        interaction_meta="\t\t|\t".join(['Date: ' + my_date + "\t" + my_time,
            'Study Iteration: ' + iteration])
        doc_obj.add_paragraph(interaction_meta)
        doc_obj.add_paragraph(interaction_data['abstract'][0:char_limit] + '...')
        resource=doc_obj.add_paragraph('Interaction Resource: ')
        _add_hyperlink(resource, interaction_data['interactionName'], interaction_data['url'].replace('s3', 'http'))
    else:
        print('Something went wrong obtaining the interaction data for [' + interaction_guid + ']')

def _create_references(iteration_list, doc_obj, conf):
    section_title=doc_obj.add_paragraph('References') # Create the References section
    section_title.style=doc_obj.styles['Title']
    for iteration in iteration_list:
        if iteration == 'state' or iteration == 'totalInteractions' or iteration == 'totalIterations':
            continue
        for interaction in iteration_list[iteration]['interactions']:
            interaction_guid=iteration_list[iteration]['interactions'][interaction]['guid']
            _create_reference(interaction_guid, iteration, doc_obj, conf)

def _create_key_theme(doc_obj, themes):
    for theme in ['summary_theme']: #, 'discrete_themes']:
        doc_obj.add_paragraph(themes[theme]['name'])
        doc_obj.add_paragraph(themes[theme]['description'])
        doc_obj.add_paragraph(themes[theme]['tags'])





def _create_key_themes(doc_obj, substudies):
    section_title=doc_obj.add_paragraph('Key Themes') # Create the References section
    section_title.style=doc_obj.styles['Title']
    for substudy in substudies:
        doc_obj.add_heading(substudies[substudy]['description'], 2)
        _create_key_theme(doc_obj, substudies[substudy]['keyThemes'])
        
    

def report(study, conf):
    # Document generics
    d=Document() # Create doc object
    style=d.styles['Normal']
    font=style.font
    font.name=conf['font']
    font.size=Pt(int(conf['font_size']))
    _create_cover_page(d, study, conf) # Create the cover page
    _create_header(d, conf) # Create the doc header
    _create_footer(d, conf) # Create the doc footer
    _create_summary(d, study['document'], conf) # Create the intro, opportunity and actions sections
    #_create_references( study['iterations'], d, conf) # Create references sections
    _create_key_themes(d, study['substudies'])
    

    # d=report_summary(study, format, doc=d)
    # d=report_references(study, format, doc=d)
    return d



if __name__ == "__main__":
    my_args=parse_cli_args()
    configurator=read_config(conf_file=my_args.config_file)

    # Set default items from the configuration file for the report
    report_conf={
        'org': configurator['DEFAULT']['organization_name'],
        'logo': configurator['DEFAULT']['logo_image'],
        'font': configurator['DEFAULT']['font_type'],
        'font_size': configurator['DEFAULT']['font_size'],
        'font_measure': configurator['DEFAULT']['font_measure'],
        'copyright': configurator['DEFAULT']['copyright_notice'],
        'confidentiality': configurator['DEFAULT']['confidential_notice'],
    }

    auth_ctl=authenticate(user_name=my_args.user, secret=my_args.secret, rest_server_url=my_args.rest_url)
    credential=auth_ctl.login()
    study_ctl=study(credential)
    success, study_obj=study_ctl.get_by_guid(my_args.guid)
    if success:
        doc_name=study_obj['studyName'].replace(' ', '_') + "_study_report.docx"
        document=report(study_obj, report_conf)
        document.save(doc_name)

    else:
        print('CLI ERROR: This is a generic error message, as something went wrong.')
        sys.exit(-1)