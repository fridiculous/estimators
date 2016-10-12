from estimators import EvaluationResult, Evaluator

from unittest import TestCase
from unittest.mock import patch
from estimators import Estimator

import factory
import factory.alchemy
import factory.fuzzy

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

Session = orm.scoped_session(orm.sessionmaker())
engine = create_engine('sqlite://', echo=False)
Session.configure(bind=engine)
Base = declarative_base()
session = Session()

import random


def random_list(min_value=0, max_value=100, length=100):
    return [random.randint(min_value, max_value) for i in range(length)]


class EstimatorFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Estimator
        sqlalchemy_session = session

    id = factory.Sequence(lambda n: n)
    create_date = factory.LazyFunction(datetime.now)
    _hash = factory.fuzzy.FuzzyText(length=32)
    _file_name = factory.LazyAttribute(lambda o: 'files/estimators/%s' % o._hash)

    from sklearn.dummy import DummyClassifier, DummyRegressor
    _estimator = factory.Iterator([
        DummyClassifier().fit(random_list(), random_list()),
        DummyRegressor().fit(random_list(), random_list()),
    ])
    estimator = factory.SelfAttribute('_estimator')


class EvaluationTest(TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)

    def test_evaluator_init(self):
        obj = EstimatorFactory()
        job_config = {
            'estimator': obj,
            'X_test': [[1, 2], [3, 4]],
            'y_test': [1, 0]
        }
        ej = Evaluator(**job_config)

        assert ej.estimator == obj.estimator
        assert ej.X_test == [[1, 2], [3, 4]]
        assert ej.y_test == [1, 0]

    def test_evaluator_evaluate(self):
        job_config = {
            'estimator': EstimatorFactory(),
            'X_test': [[1, 3], [3, 4]],
            'y_test': [2, 0]
        }
        with patch.object(EvaluationResult, 'persist_results', return_value=None):
            ej = Evaluator(**job_config)

            er = ej.evaluate()
            assert isinstance(er, EvaluationResult)
            assert len(ej.y_test) == len(er.y_predicted)

    def tearDown(self):
        Base.metadata.drop_all(engine)
