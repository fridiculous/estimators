from datetime import datetime

import factory
import factory.alchemy
import factory.fuzzy
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from estimators import DataSet, Estimator, hashing

from .conftest import SessionFactory


def compute_hash(obj):
    return hashing.hash(obj)


def random_array(min_value=0, max_value=100, shape=100, datatype="array"):
    l = np.random.randint(min_value, max_value, shape)
    if datatype == "list" and type(shape) == int:
        return l.tolist()
    elif datatype == "series" and type(shape) == int:
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

    id = factory.Sequence(lambda n: n)
    create_date = factory.LazyFunction(datetime.now)

    _data = factory.LazyFunction(random_array)
    data = factory.SelfAttribute('_data')

    _hash = factory.LazyAttribute(lambda o: compute_hash(o.data))
    _file_name = factory.LazyAttribute(lambda o: 'files/datasets/%s' % o._hash)
