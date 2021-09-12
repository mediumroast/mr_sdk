import sys, spacy, re, os, pprint
sys.path.append ('../src')

from mediumroast.helpers import summarization
from pdfminer.high_level import extract_text

import nltk
from nltk.util import everygrams as nltk_ngrams








"""
# An experiment to see what summarization of the questionnaire 
fil='question_tokens'
print ('='*25 + ' ///BEGIN Summarization for:  [' + fil + '] /// ' + '='*25)
print ('-'*90 + ' <<<Example BERT>>> ' + '-'*90)
clean_text=" ".join(question_tokens)
abstract=text_processor.extractive_bert(clean_text)
print(abstract)
print ('='*100 + ' ///END/// ' + '='*100 + "\n\n")

fil='cleaned_corpus'
print ('='*25 + ' ///BEGIN Summarization for:  [' + fil + '] /// ' + '='*25)
print ('-'*90 + ' <<<Example BERT>>> ' + '-'*90)
clean_text=" ".join(cleaned_corpus)
abstract=text_processor.extractive_bert(clean_text)
print(abstract)
print ('='*100 + ' ///END/// ' + '='*100 + "\n\n")
"""

def get_corpus(directory, filenames, debug=False):
    cleaned_corpus=[]
    for doc in filenames:
        if debug: print('Extracting, cleaning and tokenizing document [' + doc + ']')
        raw_text=extract_text(directory + doc)
        cleaned_tokenized=text_processor.rm_enumerators(raw_text)
        cleaned_corpus.append(cleaned_tokenized)
    return cleaned_corpus


def get_ngram_intersections(list_of_token_sets, start=19, stop=20):
    raw_ngrams=dict()
    idx=0
    for lst in list_of_token_sets:
        raw_ngrams[idx]=set(nltk_ngrams(lst, max_len=stop))
        idx+=1
    foo=list(raw_ngrams.values()) 
    common=set.intersection(*foo)
    return list(sum(common, ()))


if __name__ == '__main__':
    SAMPLE_DIRECTORY='../sample_data/'
    QUESTIONNAIRE='Interview - Questionnaire.pdf'
    HDS_CORPUS=[
        '201402241004-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201402240930-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201402250831-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201402250915-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201402270900-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201402271515-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201402281310-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201403101041-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201403110945-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201403111306-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201403121034-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201403130801-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf',
        '201403140702-AMER-US-CA-SANTA CLARA-ICT-Customer Insights-HDS-Interview.pdf'
    ]

    # Needed objects
    text_processor=summarization()
    printer=pprint.PrettyPrinter()

    # Corpus Questionnaire <-- Includes questionnaire for comparison
    question_text=extract_text(SAMPLE_DIRECTORY + QUESTIONNAIRE)
    question_tokens=text_processor.rm_enumerators(question_text)

    # The Corpus
    cleaned_corpus=get_corpus(SAMPLE_DIRECTORY, HDS_CORPUS)

    # Extracted question <-- We've discovered these from the corpus
    extracted_questions=get_ngram_intersections(cleaned_corpus)
    #printer.pprint(extracted_questions)

    idx=1
    for tokens in cleaned_corpus:
        print ('='*25 + ' ///BEGIN Summarization experiment set:  [' + str(idx) + '] /// ' + '='*25)
        print ('-'*70 + ' <<<Included Questions>>> ' + '-'*70)
        minus_questions=text_processor.rm_questions(tokens, question_tokens)
        abstract=text_processor.extractive_bert(minus_questions)
        print(abstract + '\n')
        print ('-'*70 + ' <<<Discovered Questions>>> ' + '-'*70)
        minus_questions=text_processor.rm_questions(tokens, extracted_questions)
        abstract=text_processor.extractive_bert(minus_questions)
        print(abstract + '\n')
        print ('='*95 + ' ///END/// ' + '='*95 + "\n\n")
        idx+=1





