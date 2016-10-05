from estimators import EvaluationResult, Evaluator


class FakeEstimator:

    def predict(self, fake_data):
        return [1, 0]


def test_evaluator_init():
    obj = FakeEstimator()
    job_config = {
        'estimator': obj,
        'X_test': [[1, 2], [3, 4]],
        'y_test': [1, 0]
    }
    ej = Evaluator(**job_config)

    assert ej.estimator == obj
    assert ej.X_test == [[1, 2], [3, 4]]
    assert ej.y_test == [1, 0]


def test_evaluator_evaluate_without_persistance():
    job_config = {
        'estimator': FakeEstimator(),
        'X_test': [[1, 2], [3, 4]],
        'y_test': [1, 0]
    }
    ej = Evaluator(**job_config)

    er = ej.evaluate(persist=False)
    assert isinstance(er, EvaluationResult)
    assert len(ej.y_test) == len(er.y_predicted)
    assert er.evaluator is ej
    assert ej.is_persisted is False


def test_evaluator_evaluate():
    job_config = {
        'estimator': FakeEstimator(),
        'X_test': [[1, 2], [3, 4]],
        'y_test': [1, 0]
    }
    ej = Evaluator(**job_config)

    er = ej.evaluate()
    assert isinstance(er, EvaluationResult)
    assert len(ej.y_test) == len(er.y_predicted)
    assert er.evaluator is ej
    assert ej.is_persisted is True
