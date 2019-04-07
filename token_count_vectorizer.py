from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize
from string import punctuation

class TokenCountVectorizer(CountVectorizer):

    @staticmethod
    def iterate_pandas_text(df_arg):
        for index, row in df_arg.text.iteritems():
            yield row

    @staticmethod
    def to_tokens(text):
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens if token not in punctuation]
        tokens = [token for token in tokens if any([i.isalpha() for i in token])]
        return tokens
