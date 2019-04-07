import logging
import csv
import ast


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
REVIEWS_TOKENS_FILE_IN = '/media/diego/QData/datasets/yelp/review_tokenized.csv'
REVIEWS_TOKENS_FILE_OUT = '/media/diego/QData/datasets/yelp/review_tokenized_2.csv'

from string import punctuation

with open(REVIEWS_TOKENS_FILE_IN, 'r', encoding='UTF-8') as rif:
    with open(REVIEWS_TOKENS_FILE_OUT, 'w', encoding='UTF-8') as wif:
        csv_file = csv.writer(wif)
        csvreader = csv.reader(rif)
        for line_num, row in enumerate(csvreader):
            if line_num == 0:
                csv_file.writerow(['stars', 'text'])
            else:
                tokenized_as_str = row[1]
                tokenized = ast.literal_eval(tokenized_as_str)
                token_without_punctuations = [token.lower() for token in tokenized if token not in punctuation]
                csv_file.writerow([row[0], token_without_punctuations])

