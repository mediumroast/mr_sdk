__version__ = '1.0'
__author__  = "Michael Hay"
__date__    = '2021-August-30'
__copyright__ = "Copyright 2021 mediumroast.io. All rights reserved."


from geopy.geocoders import ArcGIS
from summarizer import Summarizer
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer
from nltk.util import everygrams as nltk_ngrams
from pdfminer.high_level import extract_text
import hashlib, time, re, nltk
import configparser as conf


class utilities:

    def __init__ (self):
        self.locator = ArcGIS (timeout=2)

        # TODO create a defaults config file for a few things

    def total_item (self, items):
        """Total items in dicts and lists and return the result.

        """
        return len (items)

    def hash_it(self, stringToHash, HASH='sha256'):
        h = hashlib.new (HASH)
        h.update (stringToHash.encode('utf-8'))
        return h.hexdigest ()

    def locate (self, place):
        """Using an input string return the lat long combo using geopy

        """
        l = self.locator.geocode (place)
        return [l.longitude, l.latitude]

    def save (self, file_name, string_data):
        """ Save string content to a file

        """
        my_file = open (file_name, 'w')
        my_file.write (string_data)
        my_file.close ()
        return True


    def correct_date (self, date_time):
        """Ensure that the date and time are correct

        """
        my_time=self.config['DEFAULT']['interviewTime']
        my_date=date_time
        if len (date_time) > 8:
            my_time=my_date[8:]
            my_date=my_date[0:8]
        return (my_date, my_time)


    def get_date_time (self):
        """Get the time presently and return in two formats

        """
        the_time_is=time.localtime()
        time_concat=the_time_is.tm_year + the_time_is.tm_mon + the_time_is.tm_mday + the_time_is.tm_hour + the_time_is.tm_min
        time_formal=time.asctime(the_time_is)
        return time_concat, time_formal


    def make_note (self, obj_type, creator='Mediumroast SDK load utility.'):
        """Create a sample note for an object or a child object

        """
        (time_stamp, time_string)=self.get_date_time()
        return {"1":{time_stamp: "This is an example note created for the '" + obj_type + "' object on " + time_string + " by a " + creator}}

class companies:

    def __init__ (self, rewrite_config_dir="../src/mediumroast/transformers/"):
        self.RULES={
            'dir': rewrite_config_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }  
        self.rules=conf.ConfigParser()
        self.rules.read(self.RULES['dir'] + self.RULES['company'])
        self.util=utilities() 

    def get_name (self, company_name):
        """Lookup a company's name from the configuration file and return it.

        As appropriate return the proper name of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.

        Returns:
            string: A reformatted name of the company

        Notes:
            This initial implementation doesn't really do anything since we assume the company name is correct.
        """
        return company_name


    def get_description (self, company_name):
        """Lookup a company description from the configuration file and return it.

        As appropriate return a long form description of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.

        Returns:
            string: A textual description from the configuration file OR if none is present the default.
        """
        if self.rules.has_option ('descriptions', company_name): 
            return self.rules.get('descriptions', company_name)
        else: 
            return self.rules.get('DEFAULT', 'description')


    def get_industry (self, company_name):
        """Lookup a company industry from the configuration file and return it.

        As appropriate return the full industry of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.

        Returns:
            string: A textual representation of the company's industry from the configuration file OR if none is present the default.
        """
        if self.rules.industries.get (company_name): 
            return self.rules.industries[company_name]
        else: 
            return self.rules.DEFAULT.industry


    def make_id (self, company_name, file_output=True):
        """Create an identifier for the company 

        Create a identifier for the company_name which is either 'NULL_GUID' or a GUID generated by hashing
        the company name with the company description.  The latter is only done when the output is to a JSON
        file.  In the implementation with the backend we should revisit this logic to see if it is enven necessary
        or perhaps the backend handles all of this.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.
            file_output (bool): A switch for determining if we're storing the output in a file or not

        Returns:
            string: A textual representation of the company's ID
        """
        description=self.get_description(company_name)
        id='NULL_GUID'
        if file_output: id=self.util.hash_it(company_name + description) 
        return id


class studies:

    def __init__ (self, rewrite_config_dir="../src/mediumroast/transformers/"):
        self.RULES={
            'dir': rewrite_config_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }  
        self.rules=conf.ConfigParser()
        self.rules.read(self.RULES['dir'] + self.RULES['study']) 
        self.util=utilities()


    def get_name (self, study_name):
        """Lookup a study's name from the configuration file and return it.

        As appropriate return the proper name of the company in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            study_name (str): The study name which aligns to the name within the configuration file.

        Returns:
            string: A reformatted name of the study OR the argument passed in if nothing exists in the configuration file

        """
        if self.rules.has_option ('names', study_name): 
            return self.rules.get('names', study_name)
        else: 
            return study_name


    def get_description (self, study_name):
        """Lookup a study description from the configuration file and return it.

        As appropriate return a long form description of the study in question.  This is a helper function
        to be used as needed during the transformation process.

        Args:
            study_name (str): The study name which aligns to the name within the configuration file.

        Returns:
            string: A textual description from the configuration file OR if none is present the default.
        """
        if self.rules.has_option ('descriptions', study_name): 
            return self.rules.get('descriptions', study_name)
        else: 
            return self.rules.get('DEFAULT', 'description')


    def make_id (self, study_name, file_output=True):
        """Create an identifier for the study 

        Create a identifier for the study_name which is either 'NULL_GUID' or a GUID generated by hashing
        the study name with the study description.  The latter is only done when the output is to a JSON
        file.  In the implementation with the backend we should revisit this logic to see if it is enven necessary
        or perhaps the backend handles all of this.

        Args:
            study_name (str): The study name which aligns to the name within the configuration file.
            file_output (bool): A switch for determining if we're storing the output in a file or not

        Returns:
            string: A textual representation of the study's ID
        """
        description=self.get_description(study_name)
        id='NULL_GUID' # This should never happen, but leaving here in case something is odd in the configuration file
        if file_output: id=self.util.hash_it(study_name + description) 
        return id

class interactions:

    def __init__ (self, rewrite_config_dir="../src/mediumroast/transformers/"):
        self.RULES={
            'dir': rewrite_config_dir,
            'company': 'company.ini',
            'study': 'study.ini',
            'interaction': 'interaction.ini'
        }  
        self.rules=conf.ConfigParser()
        self.rules.read(self.RULES['dir'] + self.RULES['interaction']) 
        self.util=utilities()


    def get_name (self, date, study_name):
        """Create an interaction name and return the resulting string.

        Generate an interaction name from the date and study_name

        Args:
            study_name (str): The study name which should ideally be reformatted to the proper name.
            date (str): A raw date for the interaction, this needs to be the same date fed to the interaction transform

        Returns:
            string: The generated name of the interaction which is the synthesis of the date string and study name

        """
        return str(date) + '-' + str(study_name)


    def get_description (self, company_name, study_name):
        """Create a description from the interaction.

        Using a default in the configuration file merge in company and study names to generate a description for 
        the interaction.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.
            study_name (str): The study name which aligns to the name within the configuration file.

        Returns:
            string: A generated textual description generated from the company and study names.
        """
        description=self.rules.get('DEFAULT', 'description')
        description=description.replace ("COMPANY", str(company_name))
        description=description.replace ("STUDYNAME", str(study_name))
        return description
        


    def make_id (self, date, company_name, study_name, file_output=True):
        """Create an identifier for the interation.

        Create a identifier for the interaction which is either 'NULL_GUID' or a GUID generated by hashing
        the interaction name with the interaction description.  The latter is only done when the output is to a JSON
        file.  In the implementation with the backend we should revisit this logic to see if it is enven necessary
        or perhaps the backend handles all of this.

        Args:
            company_name (str): The company name which aligns to the name within the configuration file.
            study_name (str): The study name which aligns to the name within the configuration file.
            file_output (bool): A switch for determining if we're storing the output in a file or not

        Returns:
            string: A textual representation of the interactions's ID
        """
        interaction_name=self.get_name(date, study_name)
        description=self.get_description(company_name, study_name)
        id='NULL_GUID' # This should never happen, but leaving here in case something is odd in the configuration file
        if file_output: id=self.util.hash_it(interaction_name + description) 
        return id


class TextPreprocessing:
    """Various methods to extract, clean and compare text sufficiently for at least extractive summarization.

    A series of methods/functions designed to extract, clean and analyze text for the purposes of extractive
    summarization using one of many summarization techniques.  Extraction can be done either  for a single document
    or for an entire corpus.  With some emphasis on the latter, there are additional functions that enable
    the removal of noise from the source documents.  Note that the corpus is presently expected to all be based
    upon the PDF format, and other formats (RTF, DOCX, OpenOffice, TXT, etc.) will, over time, be added on an
    as needed basis.

    Args:
        debug (boolean): Defaults to False and if specified the methods will report out additional information

    Methods:
        clean()
            Splits into tokens based upon carriage returns plus cleans lines by removing enumerators, dates and white space.
        rm_noise()
            Strips out the noise from a supplied list of sentence based tokens.
        get_noise_intersections()
            Discovers common noise between a supplied corpus of documents.
        get_corpus_pdf()
            Given a source directory and a list of file names extract text and return a list of lists containing extracted text.
    """
    def __init__(self, debug=False):
        self.DEBUG=debug
        self.SIZE=20

    def clean(self, text):
        """Splits into tokens based upon carriage returns plus cleans lines by removing enumerators, dates and white space.

        Can be used multiple times and for text from various interaction types, questionnaires, and so on.  Potentially can be used
        multiple times on the same text, but this is not yet tested.

        Removed Enumerators:
            Anything with not space and a period, examples: '1.', 'a.', ..., <-- code snippet token=re.sub(r'^\S\.','', token)

        Removed Dates:
            Dates of formats: 'Feb. 24, 2014 9:30AM PST', 'Mar 13, 2014 8:01 AM PDT' and 'Mar 10th, 10:41AM PDT'
            Day and time of formats: 'Mar 11 1:06PM PDT' and 'Mar 11, 9:15AM PDT'
        
        Args:
            text (str): the string of text meant for processing
        
        Returns:
            list: the list of cleaned text split apart by carriage return 
        """
        final=[] # Target for results
        tokens=text.split('\n') # Split base on carriage return
        skip_return=re.compile('^\n+') # Detect if there is a return on a line by itself
        # Detect date of formats: 'Feb. 24, 2014 9:30AM PST', 'Mar 13, 2014 8:01 AM PDT' and 'Mar 10th, 10:41AM PDT'
        skip_date=re.compile(r'\w+\.?\s{1}\S{1,4}\,?\s{1}\d{4}\s{1}\d{1,2}\:\d{2}\s?\w{2}\s{1}\w{3}')
        # Detect date of formats: 'Mar 11 1:06PM PDT' and 'Mar 11, 9:15AM PDT'
        skip_day_and_time=re.compile(r'\w+\.?\s{1}\S{1,4}\,?\s{1}\d{1,2}\:\d{2}\s?\w{2}\s{1}\w{3}')
        for token in tokens: # Process each token one at a time
            token=token.strip() # Remove white space
            token=re.sub(r'^\S\.','', token) # Remove the enumerators
            if not token: continue # If there is nothing on the line skip it
            elif skip_return.search(token): continue # If the line merely has a carriage return skip it
            elif skip_date.search(token): continue # Should 'skip_date' be detected on the line skip it
            elif skip_day_and_time.search(token): continue # Should 'skip_day_and_time' be found skip it
            if self.DEBUG: print('token>>> "' + token + '"') # Print out the token if the class debug settig is on
            final.append(token) # Add the cleaned text to the final array
        return list(final) # Ensure there is a list upon return

    def rm_noise(self, tokens, noises):
        """Strips out the noise from a supplied list of sentence based tokens.

        Whether the noise is supplied by the user or discovered by the system from a corpus, the intentions 
        of this method are the same: remove it from a supplied set of tokenized sentences.  The thinking is
        that if the noise for a corpus can be removed then the result will be better used for additional
        analysis.  Note, that a precondition is a corpus of documents that are alike in some form.  Example
        the documents could be a part of a single mediumroast.io study that includes a questionnaire.  Another
        example, the corpus could be one iteration of a study with the noise discovered by the sister method
        'get_noise_intersections'.  In both of these examples there are sets of examples -- yes this is a 
        redundant point -- this means that if the corpus contains a single of perhaps very few documents the
        power of this method might be low.  Additionally, the primary purpose of the noise removal is as a step
        before extractive text summarization.  This means that using it for things like nGram, 4Gram, 3Gram, ...
        keyword extraction hasn't yet been tested.  As this is updated we will change out this explanation.
        
        Args:
            tokens (list): a list of lines of text that have been cleaned
            noises (list): a list of lines of text representing the noises to be stripped away
        
        Returns:
            string: the list of cleaned text split apart by carriage return 
        """
        final=[] # Target for results
        for token in tokens: # Process each token one at a time
            for noise in noises: # For each token check to see if any one of the noises exist and remove it 
                token=re.sub(noise, '', token) # Remove the noise if detected
                if self.DEBUG: print('token>>> "' + token + '"') # Print out the resulting token if DEBUG is True
            final.append(token) # Add the token to the array
        return " ".join(final) # Return the resulting data as a string joined with a single space

    def get_noise_intersections(self, list_of_token_sets):
        """Discovers common noise between a supplied corpus of documents.

        When there isn't an available set of supplied noise for a corpus discover it by looking at all documents in the corpus and,
        finding the noise for each document in the corpus and then looking for the intersection of all documents in the corpus to
        'discover' the noise.  Later steps like 'rm_noise' can then use this discovery to strip out the noise from each document
        in the corpus such that each document is devoid of noise, clean and ready for summarization.  This method makes use of 
        'nltk.utils.everygrams' and was derived from the ideas from Tony Hurst (https://blog.ouseful.info/author/psychemedia/) via this blog post:
        https://blog.ouseful.info/2015/12/13/finding-common-phrases-or-sentences-across-different-documents/.  A thank you for
        the inspiration.
        
        Args:
            list_of_token_sets (list): a list of lists, where each sublist represents an individual document in the corpus. It is
                required that the sublist is cleaned and tokenized coarsely by sentences/phrases (a.k.a. split by carriage return)
        
        Returns:
            list: a flat list of everygrams that are common among the corpuse this is also know as the corpus' noise
        """
        raw_ngrams=dict() # intermediate storage for the noise per doc
        idx=0 # an index for the raw_ngrams dict
        for lst in list_of_token_sets: # process each doc
            raw_ngrams[idx]=set(nltk_ngrams(lst, max_len=self.SIZE)) # detect the set of everygrams in each doc
            idx+=1 # increment the index
        ngram_list=list(raw_ngrams.values()) # coerce the dict of raw_ngrams into a list 
        common=set.intersection(*ngram_list) # compute the intersection of the set 
        return list(sum(common, ())) # coerce the tuple of tuples into a flatted list and return the flattened list

    def get_corpus_pdf(self, directory, filenames):
        """Given a source directory and a list of file names extract text and return a list of lists containing extracted text.

        Assuming the context is PDF the listing of content has the text extracted, cleaned and added to a list.  The list of lists
        is then returned to the caller.  
        
        Args:
            directory (string): the directory containing the files
            filenames (list): a listing of PDF file names
        
        Returns:
            list: a list of lists containing all extracted content from the corpus
        """
        final=[] # Target for results
        for doc in filenames: # process each file
            if self.DEBUG: print('Extracting, cleaning and tokenizing document [' + doc + ']') # print if DEBUG is set to True
            raw_text=extract_text(directory + doc) # extract the PDF text
            cleaned_tokenized=self.clean(raw_text) # clean the text
            final.append(cleaned_tokenized) # add the document to the corpus
        return final # return the corpus

    def get_document_pdf(self, directory, filename):
        """Given a source directory and a file name extract text and return a list containing extracted text.

        Assuming the context is PDF the content has the text extracted, cleaned and added to a list.  
        The list of tokenized sentences is then returned to the caller.  
        
        Args:
            directory (string): the directory containing the files
            filename (string): a PDF file name
        
        Returns:
            list: a list containing all extracted content from the corpus
        """
        final=[] # Target for results
        if self.DEBUG: print('Extracting, cleaning and tokenizing document [' + filename + ']') # print if DEBUG is set to True
        raw_text=extract_text(directory + filename) # extract the PDF text
        final=self.clean(raw_text) # clean the text
        return final # return the document


class Summarization:

    def __init__(self, ratio=0.2, sentence_count=0):
        self.RATIO=ratio
        self.SENTENCE_COUNT=sentence_count

    # TODO this is deprecated and should be removed
    def rm_enumerators(self, text, debug=False):
        final=[]
        tokens=text.split('\n') 
        skip_return=re.compile('^\n+') 
        skip_date=re.compile(r'\w+\.?\s{1}\S{1,4}\,?\s{1}\d{4}\s{1}\d{1,2}\:\d{2}\s?\w{2}\s{1}\w{3}')
        # Detects this date format 
        skip_day_and_time=re.compile(r'\w+\.?\s{1}\S{1,4}\,?\s{1}\d{1,2}\:\d{2}\s?\w{2}\s{1}\w{3}')
        for token in tokens:
            token=token.strip() # Remove white space
            token=re.sub(r'^\S\.','', token)
            if not token: continue
            elif skip_return.search(token): continue
            elif skip_date.search(token): continue
            elif skip_day_and_time.search(token): continue
            if self.DEBUG: print('token>>> "' + token + '"')
            final.append(token)
        return list(final)

    # TODO this is deprecated and should be removed
    def rm_questions (self, tokens, questions, debug=False):
        final=[]
        for token in tokens:
            for question in questions:
                token=re.sub(question, '', token)
                if debug: print('token>>> "' + token + '"')
            final.append(token)
        return " ".join(final)

    def extractive_bert(self, text):
        model=Summarizer()
        if self.SENTENCE_COUNT > 0:
            result=model(text, sentences=self.SENTENCE_COUNT)
        else:
            result=model(text, ratio=self.RATIO)
        return result


    # TODO continue doing some testing to determine if this extractive model is useful
    def extractive_t5(self, text):
        # NOTE While this works at the present stage it won't actually produce a good quality output.
        # TODO After there is some light corpus level summarization done then retry T5 to see if it is better
        # TODO Play with the model parameters to see if we get a longer and cleaner output
        model = T5ForConditionalGeneration.from_pretrained("t5-base")
        # initialize the model tokenizer
        tokenizer = T5Tokenizer.from_pretrained("t5-base")
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
        # generate the summarization output
        outputs = model.generate(
            inputs, 
            max_length=200, 
            min_length=40, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True)
        # just for debugging
        return tokenizer.decode(outputs[0])

