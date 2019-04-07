REVIEWS_TOKENS_CV_MODEL = '/media/diego/QData/datasets/yelp/count_vectorizer.model'
REVIEWS_TOKENS_X = '/media/diego/QData/datasets/yelp/count_vectorizer.X'
REVIEWS_TOKENS_FILE_IN = '/media/diego/QData/datasets/yelp/review_tokenized_3.csv'
from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize
import pickle
import pandas as pd
from string import punctuation



class DummyCountVectorizer(CountVectorizer):
    def dummy(doc):
        return doc

with open(REVIEWS_TOKENS_CV_MODEL, 'rb') as wmo:
    cvl = pickle.load(wmo)

with open(REVIEWS_TOKENS_X, 'rb') as xmo:
    X_train_counts = pickle.load(xmo)

print(X_train_counts.shape)


def dummy(doc):
    return doc

def to_tokens(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens if token not in punctuation]
    tokens = [token for token in tokens if any([i.isalpha() for i in token])]
    return tokens

class TransformerCountVectorizer(CountVectorizer):

    @staticmethod
    def dummy(text):
        return text

    @staticmethod
    def to_tokens(text):
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens if token not in punctuation]
        tokens = [token for token in tokens if any([i.isalpha() for i in token])]
        return tokens

tcv = TransformerCountVectorizer(
    tokenizer=to_tokens,
    preprocessor=dummy,
    max_df=0.5, min_df=10,
    vocabulary=cvl.vocabulary,
    stop_words=cvl.stop_words
)


from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)


df1 = pd.read_csv(REVIEWS_TOKENS_FILE_IN,
        usecols=["stars"], nrows=X_train_tf.shape[0])

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tf, df1.stars)


def do_predict(text):
    tokens = to_tokens(text)
    bw1 = cvl.transform([tokens])
    bw2 = tf_transformer.transform(bw1)
    print(clf.predict(bw2))


do_predict("This place is great")
do_predict("I hate this place, it sucks")
do_predict("Food is bad, drinks are average, very expensive")


