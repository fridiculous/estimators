from unittest.mock import patch

import pytest

from estimators import EvaluationResult, Evaluator

from .conftest import EstimatorFactory


@pytest.mark.usefixtures("with_session")
class TestEvaluation:

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
