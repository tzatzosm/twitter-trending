from numpy import ndenumerate
from scipy import linalg,dot
from sklearn.feature_extraction.text import TfidfVectorizer

from.lsa import LSA

# 1. I should reconstruct the svd with reduced dimensions
# 2. Stopwords should be removed
# 3. A synonym list might be used
# 4. Stemming definitely should be used
# 5. Remove Singly Occurring (terms that occur in no more than 1 document).
# 6. Remove numeric terms
# steps 2-6 will be done in elastic search

class ElasticTermVectorCollector(object):

    index = 0

    def __init__(self, docs):
        # all impl
        self.docs = docs

        self.vectorizer = TfidfVectorizer()
        self.sparse = self.vectorizer.fit_transform(self.docs)
        #sparse array containing our feature names
        #todense will give us the dense representation
        self.vectors = self.sparse.todense()
        #all the features (columns) of the dense representation
        self.features = self.vectorizer.get_feature_names()

        self.lsa = LSA(self.vectors)
        self.lsa_vectors = self.lsa.transform(10)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.vectors):
            ret_val =  {
                'document': self.index,
                'words':[ (self.features[index[1]], tfidf)
                          for index, tfidf in ndenumerate(self.lsa_vectors[self.index]) if tfidf > 0]
            }
            self.index += 1
            return ret_val
        else:
            raise StopIteration()

    def __str__(self):
        res = f"{['{:>10}'.format(feature) for feature in self.features]}\n"

        for index, doc in enumerate(self.docs):
            res += f"{['{:>.8f}'.format(weight) for _, weight in ndenumerate(self.lsa_vectors[index])]}\n"

        return res
