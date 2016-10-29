import os
import pickle

from pympler import asizeof
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

from estimators import hashing


class DataBase:

    """ Returns a DataBase client object.

    A DataBase object has a sqlalchemy engine and a sqlalchemy Session object.
    The engine can be configured to work on a variety of connections.

    By default, the DataBase object takes a url corsponding to the engine URI.

    For more info, see:
        http://docs.sqlalchemy.org/en/latest/core/engines_connections.html
        http://docs.sqlalchemy.org/en/latest/orm/session.html

    The DataBase object also has the ability to initialize and drop a database.
    """

    def __init__(self, url='sqlite:///default.db'):

        self.engine = create_engine(
            os.environ.get('DATABASE_URL', url),
            echo=False
        )
        self.Session = scoped_session(sessionmaker(
            bind=self.engine,
            expire_on_commit=False))

    def initialize_database(self):
        Base.metadata.bind = self.engine
        Base.metadata.autoload = True
        Base.metadata.extend_existing = True
        result = Base.metadata.create_all(self.engine)
        return result

    def drop_database(self):
        result = Base.metadata.drop_all(self.engine)
        return result


Base = declarative_base()


class PrimaryMixin:

    """A sqlachemy schema mixin containing an id and a create_date."""

    id = Column('id', Integer, primary_key=True)
    create_date = Column('create_date', DateTime, default=func.now())


class HashableFileMixin:

    """A sqlachemy schema mixin containing a hash, a file_name and a byte_size"""

    _hash = Column('hash', String(64), nullable=False)  # unique=True,
    _file_name = Column('file_name', String, default=None, nullable=False)
    byte_size = Column('byte_size', Integer, default=None, nullable=False)

    _object_property_name = NotImplementedError()

    @classmethod
    def initialize_root_dir(cls):
        if not os.path.isdir(cls.ROOT_DIR):
            os.makedirs(cls.ROOT_DIR)

    @classmethod
    def compute_hash(cls, obj):
        return hashing.hash(obj)

    @hybrid_property
    def hash(self):
        return self._hash

    @hybrid_property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = os.path.join(self.ROOT_DIR, value)

    @property
    def is_persisted(self):
        if self.file_name:
            return os.path.isfile(self.file_name)
        return False

    @property
    def object_property(self):
        return getattr(self, self._object_property_name)

    @object_property.setter
    def object_property(self, obj):
        return setattr(self, self._object_property_name, obj)

    def get_object(self):
        if self.object_property is None:
            self.load()
        return self.object_property

    def set_object(self, value):
        if value is not None:
            object_hash = self.compute_hash(value)
            self.object_property = value
            self._hash = object_hash
            self.file_name = object_hash
            self.byte_size = asizeof.asizeof(value)

    def persist(self):
        """a private method that persists an object to the filesystem"""
        if self.hash:
            with open(self.file_name, 'wb') as f:
                pickle.dump(self.object_property, f)
            return True
        return False

    def load(self):
        """a private method that loads an object from the filesystem"""
        if self.is_persisted:
            with open(self.file_name, 'rb') as f:
                self.object_property = pickle.load(f)
