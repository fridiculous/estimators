import os
import tempfile

import pytest

from estimators import DataSet, Estimator


@pytest.fixture(scope='session')
def temporary_root_dir():
    t = tempfile.TemporaryDirectory()
    os.chdir(t.name)
    Estimator.initialize_root_dir()
    DataSet.initialize_root_dir()
    yield
    t.cleanup()
