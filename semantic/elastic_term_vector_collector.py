from numpy import ndenumerate
from numpy.linalg import svd
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. I should reconstruct the svd with reduced dimensions
# 2. Stopwords should be removed
# 3. A synonym list might be used
# 4. Stemming definitely should be used
# 5. Remove Singly Occurring (terms that occur in no more than 1 document).
# 6. Remove numeric terms
# steps 2-6 will be done in elastic search

class ElasticTermVectorCollector(object):

    index = 0
    dummy_docs = [
        'Yellow banana peels.',
        'A banana is a long yellow fruit.',
        'This mystery fruit is long and yellow and has a peel.'
    ]

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.sparse = self.vectorizer.fit_transform(self.dummy_docs)
        #sparse array containing our feature names
        #todense will give us the dense representation
        self.vectors = self.sparse.todense()
        #all the features (columns) of the dense representation
        self.features = self.vectorizer.get_feature_names()
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.vectors):
            ret_val =  {
                'document': self.index,
                'words':[ (self.features[index[1]], tfidf)
                          for index, tfidf in ndenumerate(self.vectors[self.index]) if tfidf > 0]
            }
            self.index += 1
            return ret_val
        else:
            raise StopIteration()

