import sys, spacy, re
sys.path.append ('../src')

from mediumroast.helpers import summarization
from pdfminer.high_level import extract_text

interaction_text=extract_text('../sample_data/201402241004-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf')
question_text=extract_text('../sample_data/Interview - Questionnaire.pdf')

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

extractor=summarization()

questions=rm_enumerators(question_text)
interactions=rm_enumerators(interaction_text)
clean_text=rm_questions(interactions,questions)
abstract=extractor.make(clean_text)
print(abstract)

