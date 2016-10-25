from unittest.mock import patch

import pytest

from estimators import EvaluationResult, Evaluator

from .factories import DataSetFactory, EstimatorFactory, random_array


class TestEvaluator:

    def test_evaluator_init(self):
        obj = EstimatorFactory().estimator
        X_train = DataSetFactory(shape=(100, 3)).data
        y_train = DataSetFactory().data
        obj.fit(X_train, y_train)

        X_test = DataSetFactory(shape=(100, 3)).data
        y_test = DataSetFactory().data
        job_config = {
            'estimator': obj,
            'X_test': X_test,
            'y_test': y_test
        }
        ej = Evaluator(**job_config)

        assert ej.estimator == obj
        assert ej.X_test.all() == X_test.all()
        assert ej.y_test.all() == y_test.all()

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
            'y_test': y_test
        }
        with patch.object(EvaluationResult, 'persist_results', return_value=None):
            ej = Evaluator(**job_config)

            er = ej.evaluate()
            assert isinstance(er, EvaluationResult)
            assert len(ej.y_test) == len(er.y_predicted)
