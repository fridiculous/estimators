

class DataSet():

    """docstring for DataSet"""

    def __init__(self, **options):
        self.data = options.pop('data', None)

        if options:
            raise ValueError("Unexpected kw arguments: %r" % options.keys())
