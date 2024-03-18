metric = """
The metric to use when calculating distance between instances in a
feature array. If metric is a string, it must be one of the options
allowed by scipy.spatial.distance.pdist for its metric parameter, or
a metric listed in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.
If metric is "precomputed", X is assumed to be a distance matrix.
Alternatively, if metric is a callable function, it is called on each
pair of instances (rows) and the resulting value recorded. The callable
should take two arrays from X as input and return a value indicating
the distance between them. The default is "euclidean" which is
interpreted as squared euclidean distance.
"""

n_iter = """
Maximum number of iterations for the optimization. Should be at least 250.
"""

perplexity = """
The perplexity is related to the number of nearest neighbors that
is used in other manifold learning algorithms. Larger datasets
usually require a larger perplexity. Consider selecting a value
between 5 and 50. Different values can result in significantly
different results. The perplexity must be less than the number
of samples.
"""

method="""
By default the gradient calculation algorithm uses Barnes-Hut
approximation running in O(NlogN) time. method='exact'
will run on the slower, but exact, algorithm in O(N^2) time. The
exact algorithm should be used when nearest-neighbor errors need
to be better than 3%. However, the exact method cannot scale to
millions of examples.
"""