from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.forest import BaseForest

from estimators import Estimator
from tests.shared import db_session

from .factories import EstimatorFactory


class TestEstimator:

    def test_estimator_init(self):
        es = Estimator()

        rfc = RandomForestClassifier()
        es.estimator = rfc

        assert es.estimator is rfc
        assert es.hash == '83d11c9bf77830ad42c4e93abe9cf397'
        assert es.file_name == 'files/estimators/83d11c9bf77830ad42c4e93abe9cf397'

    def test_estimator_init_with_factory(self):
        es = EstimatorFactory()

        assert isinstance(es.estimator, BaseForest)

        # assert persistance
        assert db_session.query(Estimator).all() == [es]
