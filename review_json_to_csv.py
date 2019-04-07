import logging
import json
import csv
import yaml
import os


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)


REVIEWS_INPUT_FILE = os.path.join(config['SOURCE_DIR'], config['REVIEW_JSON_FILE'])
REVIEWS_CSV_FILE = os.path.join(config['TARGET_DIR'], config['REVIEW_CSV_FILE'])

line_num = 0
with open(REVIEWS_INPUT_FILE, 'r', encoding='UTF-8') as rif:
    with open(REVIEWS_CSV_FILE, 'w', encoding='UTF-8') as wif:
        csv_file = csv.writer(wif)
        csv_file.writerow(['review_id', 'text', 'stars'])
        for line in rif.readlines():
            record = json.loads(line)
            record_to_write = [record['review_id'], record['text'], record['stars']]
            csv_file.writerow(record_to_write)
            line_num += 1
            if line_num % 10000 == 0:
                logging.info(f'Written {line_num} lines')