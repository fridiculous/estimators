from datetime import datetime

import factory
import factory.alchemy
import factory.fuzzy
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from estimators import DataSet, Estimator, hashing

from tests.shared import SessionFactory


def compute_hash(obj):
    return hashing.hash(obj)


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


class EstimatorFactory(SessionFactory):

    class Meta:
        model = Estimator

    id = factory.Sequence(lambda n: n)
    create_date = factory.LazyFunction(datetime.now)

    _estimator = factory.Iterator([
        RandomForestRegressor(),
        RandomForestClassifier(),
    ])
    estimator = factory.SelfAttribute('_estimator')

    _hash = factory.LazyAttribute(lambda o: compute_hash(o.estimator))
    _file_name = factory.LazyAttribute(lambda o: 'files/estimators/%s' % o._hash)


class DataSetFactory(SessionFactory):

    class Meta:
        model = DataSet

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
