import os

import dill
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

from . import hashing


class DataBase:

    def __init__(self, url='sqlite:///default.db'):
        """
        devdb = 'sqlite:///:memory:'
        """

        self.engine = create_engine(
            os.environ.get('DATABASE_URL', url),
            echo=True,
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine, expire_on_commit=False))

    def initialize_database(self):
        Base.metadata.bind = self.engine
        Base.metadata.extend_existing = True
        result = Base.metadata.create_all(self.engine)
        return result


Base = declarative_base()


class PrimaryMixin:

    id = Column(Integer, primary_key=True)
    create_date = Column('create_date', DateTime, default=func.now())


class HashableFileMixin(PrimaryMixin):

    _hash = Column('hash', String(64), unique=True, nullable=False)
    _file_name = Column('file_name', String, default=None, nullable=False)

    _object_property_name = NotImplementedError()

    @classmethod
    def initialize_root_dir(cls):
        if not os.path.isdir(cls.ROOT_DIR):
            os.makedirs(cls.ROOT_DIR)

    @classmethod
    def compute_hash(cls, obj):
        return hashing.hash(obj)

    @property
    def hash(self):
        return self._hash

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = os.path.join(self.ROOT_DIR, value)

    @property
    def is_persisted(self):
        return os.path.isfile(self.file_name)

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
        object_hash = self.compute_hash(value)
        self.object_property = value
        self._hash = object_hash
        self.file_name = object_hash

    def persist(self):
        """a private method that persists an object to the filesystem"""
        if self.hash:
            with open(self.file_name, 'wb') as f:
                dill.dump(self.object_property, f)
            return True
        return False

    def load(self):
        """a private method that loads an object from the filesystem"""
        if self.is_persisted:
            with open(self.file_name, 'rb') as f:
                self.object_property = dill.load(f)
