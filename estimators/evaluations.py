from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .database import Base, DataBase, PrimaryMixin
from .datasets import DataSet
from .estimators import Estimator


class EvaluationMixin:

    @property
    def estimator(self):
        return self._estimator_proxy.estimator

    @estimator.setter
    def estimator(self, obj):
        if isinstance(obj, Estimator):
            self._estimator_proxy = obj
        else:
            self._estimator_proxy = Estimator(estimator=obj)

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

    @property
    def y_predicted(self):
        return self._y_predicted_proxy.data

    @y_predicted.setter
    def y_predicted(self, value):
        self._y_predicted_proxy = DataSet(data=value)


class Evaluator(EvaluationMixin):

    """docstring for Evaluator"""

    def __init__(self, **options):
        self.estimator = options.pop('estimator', None)
        self.X_test = options.pop('X_test', None)
        self.y_test = options.pop('y_test', None)
        self.y_predicted = options.pop('y_predicted', None)

        self.session = options.pop('session', None)
        if not self.session:
            db = DataBase()
            self.session = db.Session()

    def evaluate(self, persist=True):
        result = self.estimator.predict(self.X_test)

        options = {
            'y_predicted': result,
            'estimator': self.estimator,
            'X_test': self.X_test,
            'y_test': self.y_test,
        }
        er = EvaluationResult(**options)
        self.persist_results(er)
        return er

    def persist_results(self, er):

        try:
            self.session.add(er._estimator_proxy)
            self._estimator_proxy.persist()

            self.session.add(er._X_test_proxy)
            self._X_test_proxy.persist()

            self.session.add(er._y_test_proxy)
            self._y_test_proxy.persist()

            self.session.add(er._y_predicted_proxy)
            self._y_predicted_proxy.persist()
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()

    def __repr__(self):
        return '<Evaluator(X_test=%s estimator=%s)>' % (
            self.X_test, self.estimator)


class EvaluationResult(EvaluationMixin, PrimaryMixin, Base):

    """docstring for EvaluationResult"""
    __tablename__ = 'result'

    estimator_id = Column(Integer, ForeignKey('estimator.id'))
    X_test_id = Column(Integer, ForeignKey('dataset.id'), nullable=False)
    y_test_id = Column(Integer, ForeignKey('dataset.id'))
    y_predicted_id = Column(Integer, ForeignKey('dataset.id'))
    _estimator_proxy = relationship("Estimator", backref="EvaluationResult")
    _X_test_proxy = relationship("DataSet", foreign_keys=X_test_id)
    _y_test_proxy = relationship("DataSet", foreign_keys=y_test_id)
    _y_predicted_proxy = relationship("DataSet", foreign_keys=y_predicted_id)

    def __repr__(self):
        return '<EvaluationResult(id=%s X_test=%s estimator=%s)>' % (
            self.id, self.X_test, self.estimator)
