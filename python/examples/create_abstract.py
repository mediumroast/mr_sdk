import sys, spacy, re
sys.path.append ('../src')

from mediumroast.helpers import abstracts
from pdfminer.high_level import extract_text
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

raw_text=extract_text('../sample_data/201402240930-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf')

def _rm_enumerators (text):
    tokens=text.split(' ')
    start_pattern=re.compile(r'\n+\S+\.', re.IGNORECASE)
    final=[]
    for token in tokens:
        token=re.sub(' +', ' ', token).strip()
        if start_pattern.findall(token):
            continue
        else: 
            final.append(token)

    return(" ".join(final))



extractor=abstracts()
abst=extractor.make(_rm_enumerators(raw_text))
print(abst)

