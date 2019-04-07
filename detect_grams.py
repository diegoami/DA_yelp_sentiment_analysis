
from gensim.models.phrases import Phraser, Phrases
import csv
import ast
import logging

REVIEWS_TOKENS_FILE_IN = '/media/diego/QData/datasets/yelp/review_tokenized_2.csv'
BIGRAMS_PHRASER_FILENAME   = '/media/diego/QData/datasets/yelp/bigrams_phraser'
BIGRAMS_PHRASES_FILENAME   = '/media/diego/QData/datasets/yelp/bigrams_phrases'

from string import punctuation
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def iterate_ratings():
    with open(REVIEWS_TOKENS_FILE_IN, 'r', encoding='UTF-8') as rif:
        csvreader = csv.reader(rif)
        for line_num, row in enumerate(csvreader):

        #for line_num, row in zip(range(10000), csvreader):
            if line_num > 0:
                token_list = ast.literal_eval(row[1])
                if line_num % 1000 == 0:
                    logging.info(f'Read {line_num} ratings')
                yield token_list




logging.info(f'Reading from {REVIEWS_TOKENS_FILE_IN }')


bigrams_phrases = Phrases(iterate_ratings(), scoring='npmi', threshold=0.88)
bigrams_phrases.save(BIGRAMS_PHRASER_FILENAME)

bigrams_phraser = Phraser(bigrams_phrases)
bigrams_phraser.save(BIGRAMS_PHRASER_FILENAME)