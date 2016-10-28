from datetime import datetime

import factory
import factory.fuzzy
import numpy as np
import pandas as pd
from factory.alchemy import SQLAlchemyModelFactory
from pympler import asizeof
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from estimators import DataSet, Estimator, EvaluationResult, hashing
from tests.shared import db


def compute_hash(obj):
    return hashing.hash(obj)


def compute_size(obj):
    return asizeof.asizeof(obj)


def random_array(min_value=0, max_value=100, shape=(100, ), datatype="array"):
    l = np.random.randint(min_value, max_value, shape)
    if datatype == "list":
        return l.tolist()
    elif datatype == "series":
        return pd.Series(l)
    # or a tuple
    elif datatype == "dataframe":
        return pd.DataFrame(l)
    return l


class EstimatorFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Estimator
        sqlalchemy_session = db.Session

    id = factory.Sequence(lambda n: n)
    create_date = factory.LazyFunction(datetime.now)

    _estimator = factory.Iterator([
        RandomForestRegressor(),
        RandomForestClassifier(),
    ])
    estimator = factory.SelfAttribute('_estimator')

    _hash = factory.LazyAttribute(lambda o: compute_hash(o.estimator))
    _file_name = factory.LazyAttribute(lambda o: 'files/estimators/%s' % o._hash)
    byte_size = factory.LazyAttribute(lambda o: compute_size(o.estimator))

    @factory.post_generation
    def persist_file(self, create, extracted, **kwargs):
        self.persist()
        return self.is_persisted


class DataSetFactory(SQLAlchemyModelFactory):

    class Meta:
        model = DataSet
        sqlalchemy_session = db.Session

    class Params:
        min_random_value = 0
        max_random_value = 100
        shape = (100, )
        datatype = "array"

    id = factory.Sequence(lambda n: n)
    create_date = factory.LazyFunction(datetime.now)

    _data = factory.LazyAttribute(lambda o: random_array(
        min_value=o.min_random_value,
        max_value=o.max_random_value,
        shape=o.shape,
        datatype=o.datatype))
    data = factory.SelfAttribute('_data')
    n_rows = factory.LazyAttribute(lambda o: o.shape[0])
    n_cols = factory.LazyAttribute(lambda o: o.shape[1] if len(o.shape) > 1 else 1)

    _hash = factory.LazyAttribute(lambda o: compute_hash(o.data))
    _file_name = factory.LazyAttribute(lambda o: 'files/datasets/%s' % o._hash)
    byte_size = factory.LazyAttribute(lambda o: compute_size(o.data))

    @factory.post_generation
    def persist_file(self, create, extracted, **kwargs):
        self.persist()
        return self.is_persisted


class EvaluationResultFactory(SQLAlchemyModelFactory):

    class Meta:
        model = EvaluationResult
        sqlalchemy_session = db.Session

    id = factory.Sequence(lambda n: n)
    create_date = factory.LazyFunction(datetime.now)

    _estimator_proxy = factory.SubFactory(EstimatorFactory)
    _X_test_proxy = factory.SubFactory(DataSetFactory, shape=(100, 3))
    _y_test_proxy = factory.SubFactory(DataSetFactory)
    _y_predicted_proxy = factory.SubFactory(DataSetFactory)

    estimator_id = factory.SelfAttribute('_estimator_proxy.id')
    X_test_id = factory.SelfAttribute('_X_test_proxy.id')
    y_test_id = factory.SelfAttribute('_y_test_proxy.id')
    y_predicted_id = factory.SelfAttribute('_y_predicted_proxy.id')
