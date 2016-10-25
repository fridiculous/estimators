from .database import Base, HashableFileMixin
from sqlalchemy import Column, Integer


class DataSet(HashableFileMixin, Base):

    """
    Proxy object for a numpy or pandas data object
    """
    n_rows = Column('n_rows', Integer, nullable=False)
    n_cols = Column('n_cols', Integer, nullable=False)

    ROOT_DIR = 'files/datasets'
    _object_property_name = '_data'
    _data = None

    __tablename__ = 'dataset'

    def __init__(self, **options):
        self.data = options.pop('data', None)

    @property
    def data(self):
        return self.get_object()

    @data.setter
    def data(self, obj):
        self.set_object(obj)
        shape = DataSet.get_shape_from_data(obj)
        if isinstance(shape, tuple):
            self.n_rows = shape[0]
            self.n_cols = shape[1]

    def __repr__(self):
        return '<Dataset(id=%s hash=%s)>' % (self.id, self.hash)

    @classmethod
    def get_shape_from_data(cls, obj):
        if obj is not None:
            shape = getattr(obj, 'shape', None)

            # for pandas and numpy objects
            if shape and isinstance(shape, tuple):
                n_rows = shape[0]
                n_cols = 1
                if len(shape) > 1:
                    n_cols = shape[1]

            # for list objects
            elif isinstance(obj, list):
                n_rows = len(obj)
                n_cols = 1
                if isinstance(obj[0], list):
                    n_cols = len(obj[0])

            return n_rows, n_cols
