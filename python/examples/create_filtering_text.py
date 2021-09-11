import sys, spacy, re, os
sys.path.append ('../src')

from mediumroast.helpers import summarization
from pdfminer.high_level import extract_text


def summarize(text, debug=False):
    pass

SAMPLE_DIRECTORY='../sample_data'
text_processor=summarization()

# Corpus set 1 <-- Includes questionnaire for comparison
QUESTIONNAIRE='Interview - Questionnaire.pdf'
question_text=extract_text(SAMPLE_DIRECTORY + QUESTIONNAIRE)
question_tokens=text_processor.rm_enumerators(question_text)

CORPUS_1=[
    '201402241004-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
    '201402240930-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf'
]
