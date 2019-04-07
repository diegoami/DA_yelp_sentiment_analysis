import logging
import csv

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
REVIEWS_TOKENS_FILE_IN = '/media/diego/QData/datasets/yelp/review_tokenized.csv'
REVIEWS_TOKENS_FILE_OUT = '/media/diego/QData/datasets/yelp/review_tokenized_3.csv'



with open(REVIEWS_TOKENS_FILE_IN, 'r', encoding='UTF-8') as rif:
    with open(REVIEWS_TOKENS_FILE_OUT, 'w', encoding='UTF-8') as wif:
        csv_file = csv.writer(wif)
        csvreader = csv.reader(rif)
        for line_num, row in enumerate(csvreader):
            csv_file.writerow([row[2], row[3]])
            if line_num % 1000 == 0:
                logging.info(f'Writing line {line_num}')


