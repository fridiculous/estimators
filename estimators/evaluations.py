from .datasets import DataSet
from .estimators import Estimator


class Evaluator:

    """docstring for Evaluator"""

    def __init__(self, **options):
        self.estimator = options.pop('estimator', None)
        self.X_test = options.pop('X_test', None)
        self.y_test = options.pop('y_test', None)
        self.is_persisted = False
        if options:
            raise ValueError("Unexpected kw arguments: %r" % options.keys())

    @property
    def estimator(self):
        return self._estimator_proxy.estimator

    @estimator.setter
    def estimator(self, value):
        self._estimator_proxy = Estimator(estimator=value)

    @property
    def X_test(self):
        return self._X_test_proxy.data

    @X_test.setter
    def X_test(self, value):
        self._X_test_proxy = DataSet(data=value)

    @property
    def y_test(self):
        return self._y_test_proxy.data

    @y_test.setter
    def y_test(self, value):
        self._y_test_proxy = DataSet(data=value)

    def evaluate(self, persist=True):
        result = self.estimator.predict(self.X_test)
        if persist:
            self.is_persisted = True
        er = EvaluationResult(result=result, evaluator=self)
        return er


class EvaluationResult:

    """docstring for EvaluationResult"""

    def __init__(self, **options):
        self.result = options.pop('result')
        self.evaluator = options.pop('evaluator')
        self.y_predicted = self.result
