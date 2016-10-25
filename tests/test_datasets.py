from .factories import DataSetFactory, random_array

from estimators import DataSet

import numpy as np
import pytest

from tests.shared import db_session


class TestDataSet:

    def test_dataset_init(self):
        ds = DataSet()

        data = np.array([1, 2, 3, 4, 5])
        ds.data = data

        assert ds.data.all() == data.all()
        assert ds.hash == '6a5e8988f98e695fb4f35523de77f2fd'
        assert ds.file_name == 'files/datasets/6a5e8988f98e695fb4f35523de77f2fd'
        assert ds.n_rows == 5
        assert ds.n_cols == 1

    def test_dataset_init_with_factory(self):
        ds = DataSetFactory(shape=(10, 3))

        assert isinstance(ds, DataSet)
        assert isinstance(ds.data, np.ndarray)
        assert ds.n_rows == 10
        assert ds.n_cols == 3

        # assert persistance
        assert db_session.query(DataSet).all() == [ds]
