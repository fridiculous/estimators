

class Estimator:

    """docstring for Estimators"""

    def __init__(self, **options):
        self.estimator = options.pop('estimator', None)

        if options:
            raise ValueError("Unexpected kw arguments: %r" % options.keys())
