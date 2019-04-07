from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDRegressor
import pandas as pd
from nltk.tokenize import word_tokenize
from string import punctuation
import logging
import pickle
import csv
from sklearn.metrics import mean_squared_error


import numpy as np
from sklearn.model_selection import train_test_split

ROWS_TOTAL = 100000
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

REVIEWS_TOKENS_FILE_IN = '/media/diego/QData/datasets/yelp/review.csv'
REVIEWS_PIPELINE = '/media/diego/QData/datasets/yelp/review.pipeline'

df = pd.read_csv(REVIEWS_TOKENS_FILE_IN, nrows=ROWS_TOTAL, usecols=['text', 'stars'])
df = df.sample(frac=1)
df_train, df_test = train_test_split(df, test_size=0.2)


class TokenCountVectorizer(CountVectorizer):


    @staticmethod
    def iterate_pandas_text(df_arg):
        for index, row in df_arg.text.iteritems():
            yield row

    @staticmethod
    def iterate_ratings():
        with open(REVIEWS_TOKENS_FILE_IN, 'r', encoding='UTF-8') as rif:
            csvreader = csv.reader(rif)
            # for line_num, row in enumerate(csvreader):

            for line_num, row in zip(range(ROWS_TOTAL+1), csvreader):
                if line_num > 0:
                    yield row[1]

    @staticmethod
    def to_tokens(text):
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens if token not in punctuation]
        tokens = [token for token in tokens if any([i.isalpha() for i in token])]
        return tokens


logging.info("Start .....")
text_clf = Pipeline([
     ('vect', TokenCountVectorizer(tokenizer=TokenCountVectorizer.to_tokens, max_df=0.5, min_df=5)),
     ('tfidf', TfidfTransformer()),
     ('sgd_regressor', SGDRegressor())
])

logging.info("Fitting Model .....")
text_clf.fit(TokenCountVectorizer.iterate_pandas_text(df_train), df_train.stars)
logging.info("Done .....")

with open(REVIEWS_PIPELINE, 'wb') as wmo:
    pickle.dump(text_clf, wmo)

logging.info(f'Predictions: {text_clf.predict(["This place is great","I hate this place, it sucks","Food is bad, drinks are average, very expensive"])}')

test_predicted = text_clf.predict(df_test.text)
train_predicted = text_clf.predict(df_train.text)

logging.info(f'Train MSE : {mean_squared_error(df_train.stars, train_predicted)}')

logging.info(f'Test MSE : {mean_squared_error(df_test.stars, test_predicted)}')
