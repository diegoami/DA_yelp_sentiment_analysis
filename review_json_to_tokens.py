
import logging
import json
from nltk import word_tokenize
from string import punctuation
import pickle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

REVIEWS_INPUT_FILE = '/media/diego/QData/datasets/yelp/review.json'
REVIEWS_PKL_FILE = '/media/diego/QData/datasets/yelp/reviews.pkl'
line_num = 0
rating_list = []
with open(REVIEWS_INPUT_FILE, 'r', encoding='UTF-8') as rif:
    for line in rif.readlines():
        record = json.loads(line)

        record_to_write = [token.lower() for token in word_tokenize(record['text']) if token not in punctuation]
        rating_list.append((record['stars'], record_to_write))
        line_num += 1
        if line_num % 1000 == 0:
            logging.info(f'Written {line_num} lines')
            with open(REVIEWS_PKL_FILE, 'wb') as wif:
                pickle.dump(rating_list, wif)
    with open(REVIEWS_PKL_FILE, 'wb') as wif:
        pickle.dump(rating_list, wif)