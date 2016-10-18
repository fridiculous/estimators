import random
from datetime import datetime

import factory
import factory.alchemy
import factory.fuzzy
import numpy as np
import pytest

from estimators import DataBase, Estimator


@pytest.fixture(scope='session')
def create_session():
    db = DataBase(url='sqlite://')
    return db.Session


@pytest.fixture(scope='module')
def with_session(create_session):
    session = create_session()
    yield
    # Rollback the session => no changes to the database
    session.rollback()
    # Remove it, so that the next test gets a new Session()
    create_session.remove()


def random_array(min_value=0, max_value=100, length=100):
    l = [random.randint(min_value, max_value) for i in range(length)]
    return np.array(l)


def random_matrix(min_value=0, max_value=100, length=100):
    c1 = random_array(min_value, max_value, length)
    c2 = random_array(min_value, max_value, length)
    return np.c_[c1, c2]


@pytest.mark.usefixtures("create_session")
class EstimatorFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Estimator
        sqlalchemy_session = create_session()

    id = factory.Sequence(lambda n: n)
    create_date = factory.LazyFunction(datetime.now)
    _hash = factory.fuzzy.FuzzyText(length=32)
    _file_name = factory.LazyAttribute(lambda o: 'files/estimators/%s' % o._hash)

    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    X = random_matrix()
    y = random_array()
    _estimator = factory.Iterator([
        RandomForestRegressor().fit(X, y),
        RandomForestClassifier().fit(X, y),
    ])
    estimator = factory.SelfAttribute('_estimator')
