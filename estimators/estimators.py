
from .database import Base, HashableFileMixin, PrimaryMixin


class Estimator(HashableFileMixin, PrimaryMixin, Base):

    """docstring for Estimators"""
    ROOT_DIR = 'files/estimators'
    _object_property_name = '_estimator'
    _estimator = None

    __tablename__ = 'estimator'

    @property
    def estimator(self):
        return self.get_object()

    @estimator.setter
    def estimator(self, obj):
        self.set_object(obj)

    def __repr__(self):
        return '<Estimator(id=%s hash=%s %s)>' % (self.id, self.hash, self.estimator)
