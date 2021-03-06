import logging
import pickle
import os
import pandas as pd
import yaml


from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from token_count_vectorizer import TokenCountVectorizer

with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

ROWS_TOTAL = config['REVIEWS_USED']
REVIEWS_TOKENS_FILE_IN = os.path.join(config['TARGET_DIR'], config['REVIEW_CSV_FILE'])
REVIEWS_PIPELINE = os.path.join(config['TARGET_DIR'], f'review.pipeline-{ROWS_TOTAL}')

# Read Reviews from CSV File
logging.info(f'Reading {ROWS_TOTAL} reviews...')
df = pd.read_csv(REVIEWS_TOKENS_FILE_IN, nrows=ROWS_TOTAL, usecols=['text', 'stars'])
df = df.sample(frac=1)
df_train, df_test = train_test_split(df, test_size=0.2)
logging.info('Done.')



if os.path.isfile(REVIEWS_PIPELINE):
    # Model trained, loading
    logging.info(f'Model already exists: {REVIEWS_PIPELINE}')

    with open(REVIEWS_PIPELINE, 'rb') as wmr:
        text_clf = pickle.load(wmr)
else:
    # Create and train model

    logging.info(f'Model does not exist - creating it...')
    text_clf = Pipeline([
         ('vect', TokenCountVectorizer(tokenizer=TokenCountVectorizer.to_tokens, ngram_range=(1, 2), max_df=0.3, min_df=10)),
         ('tfidf', TfidfTransformer()),
         ('sgd_regressor', SGDRegressor(verbose=config['VERBOSE']))
    ])

    logging.info("Fitting Model .....")
    text_clf.fit(TokenCountVectorizer.iterate_pandas_text(df_train), df_train.stars)
    logging.info(f'Saving model to {REVIEWS_PIPELINE}.....')

    with open(REVIEWS_PIPELINE, 'wb') as wmo:
        pickle.dump(text_clf, wmo)

    logging.info("Done")

# Evaluate model
logging.info('Calculating error for training set...')
train_predicted = text_clf.predict(df_train.text)
logging.info(f'Train MSE : {mean_squared_error(df_train.stars, train_predicted):{6}.{3}}')

logging.info('Calculating error for test set...')
test_predicted = text_clf.predict(df_test.text)
logging.info(f'Test MSE : {mean_squared_error(df_test.stars, test_predicted):{6}.{3}}')
