import sys, spacy, re
sys.path.append ('../src')

from mediumroast.helpers import abstracts
from pdfminer.high_level import extract_text
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

raw_text=extract_text('../sample_data/201402240930-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf')
nlp=spacy.load('en_core_web_sm')
text=nlp(raw_text)
stopwords=list(STOP_WORDS)
pos_tags=['PROPN', 'ADJ', 'NOUN', 'VERB']
keyword=[]
for token in text:
            if (token.text in stopwords or token.text in punctuation): continue
            if (token.pos_ in pos_tags): keyword.append (token.text)


summary=abstracts()
abst=summary.make(str(text))