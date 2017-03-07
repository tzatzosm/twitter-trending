from scipy import linalg, dot

class LSA():
    """ Latent Semantic Analysis(LSA).
	    Apply transform to a document-term matrix to bring out latent relationships.
	    These are found by analysing relationships between the documents and the terms they
	    contain.
    """
    def __init__(self, matrix):
        self.matrix = matrix

    def transform(self, dimensions=1):
        """ Calculate SVD of objects matrix: U . SIGMA . VT = MATRIX
		    Reduce the dimension of sigma by specified factor producing sigma'.
		    Then dot product the matrices:  U . SIGMA' . VT = MATRIX'
		"""
        rows,cols = self.matrix.shape

        if dimensions <= rows:
            u, sigma, vt = linalg.svd(self.matrix)

            for index in range(rows - dimensions, rows):
                sigma[index] = 0

            transformed_matrix = dot(dot(u, linalg.diagsvd(sigma, len(self.matrix), len(vt))) ,vt)
            return transformed_matrix
        else:
            print("dimension reduction cannot be greater than {0}".format(rows))
