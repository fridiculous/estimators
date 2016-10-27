import pytest

from estimators import DataSet, Estimator, EvaluationResult, Evaluator
from tests.factories import (DataSetFactory, EstimatorFactory,
                             EvaluationResultFactory)
from tests.shared import db


@pytest.mark.usefixtures("temporary_root_dir")
class TestEvalulationResult:

    def test_estimator_init(self):
        estimator = EstimatorFactory().estimator
        X_test = DataSetFactory(shape=(100, 4)).data
        y_test = DataSetFactory().data
        y_predicted = DataSetFactory().data

        er = EvaluationResult()
        er.estimator = estimator
        er.X_test = X_test
        er.y_test = y_test
        er.y_predicted = y_predicted

    def test_estimator_init_with_factory(self):
        es = EvaluationResultFactory()

        assert isinstance(es._estimator_proxy, Estimator)
        assert isinstance(es._X_test_proxy, DataSet)
        assert isinstance(es._y_test_proxy, DataSet)
        assert isinstance(es._y_predicted_proxy, DataSet)

        # assert persistance
        assert db.Session.query(EvaluationResult).all() == [es]


@pytest.mark.usefixtures("temporary_root_dir")
class TestEvaluator:

    def test_evaluator_init_with_objects(self):
        obj = EstimatorFactory()

        X_test = DataSetFactory(shape=(100, 3))
        y_test = DataSetFactory()
        job_config = {
            'estimator': obj,
            'X_test': X_test,
            'y_test': y_test
        }
        ej = Evaluator(**job_config)

        assert ej.estimator == obj.estimator
        assert ej.X_test.all() == X_test.data.all()
        assert ej.y_test.all() == y_test.data.all()

    def test_evaluator_init_with_values(self):
        obj = EstimatorFactory()

        X_test = DataSetFactory(shape=(100, 3))
        y_test = DataSetFactory()
        job_config = {
            'estimator': obj.estimator,
            'X_test': X_test.data,
            'y_test': y_test.data
        }
        ej = Evaluator(**job_config)

        assert ej.estimator == obj.estimator
        assert ej.X_test.all() == X_test.data.all()
        assert ej.y_test.all() == y_test.data.all()

    def test_evaluator_evaluate(self):
        obj = EstimatorFactory().estimator
        X_train = DataSetFactory(shape=(100, 3)).data
        y_train = DataSetFactory().data
        obj.fit(X_train, y_train)

        X_test = DataSetFactory(shape=(100, 3)).data
        y_test = DataSetFactory().data

        job_config = {
            'estimator': obj,
            'X_test': X_test,
            'y_test': y_test,
            'session': db.Session
        }
        ej = Evaluator(**job_config)

        er = ej.evaluate()
        assert isinstance(er, EvaluationResult)
        assert er.y_test is not er.y_predicted
        assert len(ej.y_test) == len(er.y_predicted)

        assert db.Session.query(EvaluationResult).all()[-1].id == er.id
