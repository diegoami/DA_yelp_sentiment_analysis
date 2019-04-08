import logging
import pickle
import os
import yaml


SAMPLE_PREDICTIONS = ["This place is great", "It is a boring and ugly place", "Food is bad and it is very expensive"]

with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

ROWS_TOTAL = config['REVIEWS_USED']
REVIEWS_PIPELINE = os.path.join(config['TARGET_DIR'], f'review.pipeline-{ROWS_TOTAL}')

if os.path.isfile(REVIEWS_PIPELINE):
    with open(REVIEWS_PIPELINE, 'rb') as wmr:
        text_clf = pickle.load(wmr)

    logging.info("Done")

    pred_results = text_clf.predict(SAMPLE_PREDICTIONS)
    for text, prediction in zip(SAMPLE_PREDICTIONS, pred_results):
        print(f'{text} : {prediction}')

    while True:
        text = input('Review --> ')
        if (len(text.strip()) > 0):
            prediction = text_clf.predict([text])
            print(f'{text} : {prediction}')
else:
    print(f"Cannot find model file: {REVIEWS_PIPELINE}")