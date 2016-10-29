from sqlalchemy import Column, Integer

from estimators.database import Base, HashableFileMixin, PrimaryMixin


class DataSet(HashableFileMixin, PrimaryMixin, Base):

    """A database model and proxy object for datasets.

    The DataSet class is the data model for the table `dataset`.

    The DataSet object functions as a proxy for the dataset model,
    which can be accessed by the `data` property.
    """

    n_rows = Column('n_rows', Integer, nullable=False)
    n_cols = Column('n_cols', Integer, nullable=False)

    ROOT_DIR = 'files/datasets'
    _object_property_name = '_data'
    _data = None

    __tablename__ = 'dataset'

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
