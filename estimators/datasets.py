from .database import Base, HashableFileMixin


class DataSet(HashableFileMixin, Base):

    """
    Proxy object for a numpy or pandas data object
    """

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

    def __repr__(self):
        return '<Dataset(id=%s hash=%s)>' % (self.id, self.hash)
