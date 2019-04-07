import csv
import pandas as pd
import ast
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
REVIEWS_TOKENS_FILE_IN = '/media/diego/QData/datasets/yelp/review_tokenized_3.csv'
REVIEWS_TOKENS_CV_MODEL = '/media/diego/QData/datasets/yelp/count_vectorizer.model'
REVIEWS_TOKENS_X = '/media/diego/QData/datasets/yelp/count_vectorizer.X'


from sklearn.feature_extraction.text import CountVectorizer
import pickle

def iterate_ratings():
    with open(REVIEWS_TOKENS_FILE_IN, 'r', encoding='UTF-8') as rif:
        csvreader = csv.reader(rif)
        for line_num, row in zip(range(10000), csvreader):

        #for line_num, row in enumerate(csvreader):

            if line_num > 0:
                token_list = ast.literal_eval(row[1])
                if line_num % 1000 == 0:
                    logging.info(f'Read {line_num} ratings')
                yield token_list



class DummyCountVectorizer(CountVectorizer):

    @staticmethod
    def dummy(doc):
        return doc

tfidf = DummyCountVectorizer(
    tokenizer=DummyCountVectorizer.dummy,
    preprocessor=DummyCountVectorizer.dummy,
    max_df=0.5, min_df=10
)


X = tfidf.fit_transform(iterate_ratings())
with open(REVIEWS_TOKENS_CV_MODEL, 'wb') as wmo:
    pickle.dump(tfidf, wmo)

with open(REVIEWS_TOKENS_X, 'wb') as xmo:
    pickle.dump(X, xmo)

