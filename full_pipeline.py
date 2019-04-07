from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDRegressor
import pandas as pd
from nltk.tokenize import word_tokenize
from string import punctuation
import logging
import pickle
import csv
ROWS_TOTAL = 10000
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

REVIEWS_TOKENS_FILE_IN = '/media/diego/QData/datasets/yelp/review.csv'
REVIEWS_PIPELINE = '/media/diego/QData/datasets/yelp/review.pipeline'

df = pd.read_csv(REVIEWS_TOKENS_FILE_IN, nrows=ROWS_TOTAL, usecols=['stars'])




class TokenCountVectorizer(CountVectorizer):

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


text_clf = Pipeline([
     ('vect', TokenCountVectorizer(tokenizer=TokenCountVectorizer.to_tokens, max_df=0.5, min_df=5)),
     ('tfidf', TfidfTransformer()),
     ('clf', SGDRegressor())
])

text_clf.fit(TokenCountVectorizer.iterate_ratings(), df.stars)

with open(REVIEWS_PIPELINE, 'wb') as wmo:
    pickle.dump(text_clf, wmo)

print(text_clf.predict(["This place is great","I hate this place, it sucks","Food is bad, drinks are average, very expensive"]))

