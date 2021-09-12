import sys, os, pprint
sys.path.append ('../src')
# Local mediumroast.io module imports
from mediumroast.helpers import Summarization
from mediumroast.helpers import TextPreprocessing


if __name__ == '__main__':
    """Illustrate text mining and summarization using mediumroast.io modules
    
    Illustrate how interactions summaries are made using the mediumroast.io text preprocessing
    and summarization modules.  Summarizations are used as a key part of the interaction objects,
    and illustrating how they can be done with a known set of sample data prior to strong ingestion
    into the mediumroast.io backend or simulated server is essential.  This experimentation has shown
    that it is critical to do separation of interaction document processing into logically divided
    sub-corpuses.  This way, in the worst case where there is no provided questionnaire, it is possible
    to detect key noise across the corpus and remove it from the corpus prior to at least extractive
    summarization.
    
    Two kinds of processing actions are executed:
        1. With a provided questionnaire that can be subtracted from the corpus
        2. Without a provided questionnaire, and the noise of the corpus discovered and subtracted

    Implementation hints, which could change over time:
        - For the interaction extractor some approach to logically group interactions, into a sub-corpus, is needed
        - Interaction objects must have a 'summarizationStatus: True|False' attribute enabling NLP services to understand status
        - Interaction objects must have some way to link them to a named corpus
    """

    # Needed objects
    printer=pprint.PrettyPrinter()
    summarizer=Summarization()
    text_prep=TextPreprocessing()

    # Base directory for all sample data
    SAMPLE_DIRECTORY='../sample_data/'
    

    # This is the first corpus within the Customer Insights study
    HDS_QUESTIONNAIRE='Interview - Questionnaire.pdf'
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
    questionnaire=text_prep.get_documemt_pdf(SAMPLE_DIRECTORY, HDS_QUESTIONNAIRE)
    hds_corpus_clean=text_prep.get_corpus_pdf(SAMPLE_DIRECTORY, HDS_CORPUS)
    hds_corpus_without_noise=text_prep.rm_noise(hds_corpus_clean, questionnaire)

    # This is the second corpus within the Customer Insights study
    AHA_CORPUS=[
        ''
    ]