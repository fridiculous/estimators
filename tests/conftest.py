
import factory.alchemy
import pytest

from estimators import DataBase


@pytest.fixture(scope='session')
def create_session():
    db = DataBase(url='sqlite://')
    return db.Session


class SessionFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = create_session()


@pytest.fixture(scope='module')
def with_session(create_session):
    session = create_session()
    yield
    # Rollback the session => no changes to the database
    session.rollback()
    # Remove it, so that the next test gets a new Session()
    create_session.remove()
