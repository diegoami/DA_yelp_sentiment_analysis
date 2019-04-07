
from gensim.models.phrases import Phraser, Phrases

import logging
import ast
import csv

REVIEWS_TOKENS_FILE_IN = '/media/diego/QData/datasets/yelp/review_tokenized_2.csv'
REVIEWS_GRAMS_FILE_OUT = '/media/diego/QData/datasets/yelp/review_gram.csv'
BIGRAMS_PHRASER_FILENAME   = '/media/diego/QData/datasets/yelp/bigrams_phraser'
BIGRAMS_PHRASES_FILENAME   = '/media/diego/QData/datasets/yelp/bigrams_phrases'

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
                yield (row[0], token_list)

bigrams_phraser = Phraser.load(BIGRAMS_PHRASER_FILENAME)


pgrams = bigrams_phraser.phrasegrams
gram_list = []
for word, score in pgrams.items():
    gram = b'_'.join(word)
    gram_list.append({"gram": gram, "score": score})
gram_sorted = sorted(gram_list, key=lambda x: x["score"], reverse=True)
print(gram_sorted)

def save_stuff():
    with open(REVIEWS_GRAMS_FILE_OUT, 'w', encoding='UTF-8') as wif:
        csv_file = csv.writer(wif)

        for line_num, row in enumerate(iterate_ratings()):
            bigrammed_phrase = bigrams_phraser[row[1]]
            if line_num % 1000 == 0:
                logging.info(f'Writing line {line_num}')
            csv_file.writerow([row[0], bigrammed_phrase])


