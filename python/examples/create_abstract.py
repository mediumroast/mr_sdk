import sys, spacy, re
sys.path.append ('../src')

from mediumroast.helpers import abstracts
from pdfminer.high_level import extract_text
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

raw_text=extract_text('../sample_data/201402240930-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf')

def _rm_enumerators (text):
    tokens=text.split('\n')
    start_pattern=re.compile(r'^\S+\.', re.IGNORECASE)
    final=[]
    for token in tokens:
        token=token.strip()
        if start_pattern.match(token):
            continue
        else: 
            if not token: continue
            print('token>>> "' + token + '"')
            final.append(token)

    return(" ".join(final))

# TODO Stop words and phrases

extractor=abstracts()
abst=extractor.make(_rm_enumerators(raw_text))
print(abst)

