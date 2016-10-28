
from estimators.database import Base, HashableFileMixin, PrimaryMixin


class Estimator(HashableFileMixin, PrimaryMixin, Base):

    """A database model and proxy object for estimators.

    The Estimator class is the data model for the table `estimator`.

    The Estimator object functions as a proxy for the estimator model,
    which can be accessed by the `estimator` property.
    """

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
