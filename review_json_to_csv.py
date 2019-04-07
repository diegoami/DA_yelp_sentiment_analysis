
import logging
import json
import csv

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

REVIEWS_INPUT_FILE = '/media/diego/QData/datasets/yelp/review.json'
REVIEWS_CSV_FILE = '/media/diego/QData/datasets/yelp/review.csv'
line_num = 0
with open(REVIEWS_INPUT_FILE, 'r', encoding='UTF-8') as rif:
    with open(REVIEWS_CSV_FILE, 'w', encoding='UTF-8') as wif:
        csv_file = csv.writer(wif)
        csv_file.writerow(['review_id', 'text', 'stars'])
        for line in rif.readlines():
            record = json.loads(line)
            record_to_write = [record['review_id'], record['text'], record['stars'] ]
            csv_file.writerow(record_to_write)
            line_num += 1
            if line_num % 100 == 0:
                logging.info(f'Written {line_num} lines')