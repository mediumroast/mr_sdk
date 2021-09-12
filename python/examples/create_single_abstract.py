import sys, spacy, re, os
sys.path.append ('../src')

# TODO this needs to be rewritten to experiment with a single interaction

from mediumroast.helpers import summarization
from pdfminer.high_level import extract_text



def rm_enumerators(text, debug=False):
    tokens=text.split('\n')
    final=[]
    skip_return=re.compile('^\n+')
    skip_date=re.compile(r'\w+\.\s{1}\d{1,2}\,\s{1}\d{4}\s{1}\d{1,2}\:\d{2}\w{2}\s{1}\w{3}')
    for token in tokens:
        token=token.strip()
        token=re.sub(r'^\S\.','', token)
        if not token: continue
        elif skip_return.search(token): continue
        elif skip_date.search(token): continue
        if debug: print('token>>> "' + token + '"')
        final.append(token)
    return final

def rm_questions (interactions, questions, debug=False):
    final=[]
    for token in interactions:
        for question in questions:
            token=re.sub(question, '', token)
            if debug: print('token>>> "' + token + '"')
        final.append(token)
    return " ".join(final)


    return(" ".join(final))

# TODO Stop words and phrases

if __name__=='__main__':
    extractor=summarization()
    directory='../sample_data/'
    files=[
        '201912151800-AMER-US-CA-SAN DIEGO-ICT-Customer Insights-Aha-Online.pdf',
        '201912172000-AMER-US-CA-SAN DIEGO-ICT-Customer Insights-Aha-Online.pdf',
        '201402241004-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201402240930-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf'
    ]
    for fil in files:
        #question_text=extract_text('../sample_data/Interview - Questionnaire.pdf')
        interaction_text=extract_text(directory + fil)
        interactions=rm_enumerators(interaction_text)
        clean_text=" ".join(interactions)
        abstract=extractor.extractive_bert(clean_text)
        
        print ('='*25 + ' ///BEGIN Summarization for:  [' + fil + '] /// ' + '='*25)
        print ('-'*90 + ' <<<Example BERT>>> ' + '-'*90)
        print(abstract)
        print ('-'*90 + ' <<<Example T5>>> ' + '-'*90)
        abstract=extractor.extractive_t5(clean_text)
        print(abstract)
        print ('='*100 + ' ///END/// ' + '='*100 + "\n\n")



