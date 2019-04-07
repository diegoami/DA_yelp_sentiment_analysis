import logging
import os
import csv
import subprocess
from nltk import word_tokenize
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
REVIEWS_CSV_FILE = '/media/diego/QData/datasets/yelp/review.csv'
REVIEWS_TOKENS_FILE = '/media/diego/QData/datasets/yelp/review_tokenized_2.csv'

len_num = 0


# def spacy_tokenize(text):
#     global len_num
#     tok_doc = spacy_nlp(text)
#     tokens = [word.lemma_ for word in tok_doc if not word.is_stop and not word.is_space]
#     len_num += 1
#     if len_num % 100 == 0:
#         logging.info(f'Converted {len_num} reviews')
#     return tokens

if not os.path.isfile(REVIEWS_TOKENS_FILE):
    with open(REVIEWS_TOKENS_FILE, 'w', encoding='UTF-8') as wif:
        csv_file = csv.writer(wif)
        csv_file.writerow(['review_id', 'text', 'stars'])

with open(REVIEWS_TOKENS_FILE, 'r', encoding='UTF-8') as wif:
    write_count = len(wif.readlines())
logging.info(f'Token file has {write_count} rows')

with open(REVIEWS_CSV_FILE, 'r', encoding='UTF-8') as rif:
    with open(REVIEWS_TOKENS_FILE, 'w', encoding='UTF-8') as wif:
        csv_file = csv.writer(wif)
        csvreader = csv.reader(rif)
        for line_num, row in enumerate(csvreader):
            row.append(word_tokenize(row[1]))
            csv_file.writerow([row[2], row[3]])
            if line_num % 1000 == 0:
                logging.info(f'Writing line {line_num}')


