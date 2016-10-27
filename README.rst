
.. image:: https://travis-ci.org/fridiculous/estimators.svg?branch=master
    :target: https://travis-ci.org/fridiculous/estimators

.. image:: https://landscape.io/github/fridiculous/estimators/master/landscape.svg?style=flat
   :target: https://landscape.io/github/fridiculous/estimators/master
   :alt: Code Health

Estimators
==========

Machine Learning Versioning made Simple


Intro
-----

Estimators helps version and track machine learning models and datasets.

It can be used to version and deploy models.  It's highly extensible and can be used with almost any python object (scikit-learn, numpy arrays, and custom modules).

This repo utilizes sqlalchemy as an ORM.  If you're using django, try `django-estimators <https://github.com/fridiculous/django-estimators.git>`_ instead.


Installation
------------


Estimators is not yet on PyPI, so just run: ::

    pip install git+https://github.com/fridiculous/estimators.git


Basic Usage
-----------

We can see the power of Estimators in 2 steps.
For a use case, let's say we are developing a classifier.  We'll 
::
        from sklearn.datasets import load_digits
        from sklearn.ensemble import RandomForestClassifier

        digits = load_digits() # 1797 by 64
        X = digits.data
        y = digits.target 

        # simple splitting for validation testing
        X_train, X_test = X[:1200], X[1200:]
        y_train, y_test = y[:1200], y[1200:] 

        rfc = RandomForestClassifier()
        rfc.fit(X_train, y_train)


1. First import an `Evaluator` object that instantiates an evaluation plan.  Set the `estimator`, `X_test` and `y_test` to that evaluator object.
:: 
        from estimators import Evaluator

        plan = Evaluator()
        plan.estimator = rfc
        plan.X_test = X_test
        plan.y_test = y_test

        # persist all objects upon prediction
        result = plan.evaluate()

        # including our predictions
        result.y_predicted


2.  At a later date, we can retrieve the results, along with the original estimator, X_test dataset and y_test dataset using sqlalchemy orm. 
::

        from estimators import DataBase, EvaluationResult
        db = DataBase()

        result = db.Session.query(EvaluationResult).first()

        # which has all our attributes
        result.id
        result.create_date
        result.estimator
        result.X_test
        result.y_test
        result.y_predicted


Advanced Usage
--------------

Continuing with the above example, we can pull specific estimators or datasets 
::

        from estimators import Estimator, DataSet

        # to return an estimator proxy object
        es = db.Session.query(Estimator).first()
        
        # return our fitted RandomForestClassifier
        es.estimator 

        # to returns all datasets as proxy objects
 
        ds = db.Session.query(DataSet).all()
        ds[0].data

But we can continue on to use all of sqlalchemy's expressions
::
        X_test_one = db.Session.query(DataSet).filter(DataSet.hash=='a381b220d0cd271d608a27eb52dfb654').first()
        y_test_one = db.Session.query(DataSet).filter(DataSet.hash=='fe773b5c53aec02fd98ffc65feb4714d').first()


Furthermore, we can run more evaluations using our new proxy objects.  The Evaluator
object handles the proxy Estimator and DataSet objects just like regular data.
::

        plan = Evaluator() 
        plan.estimator = es 
        plan.X_test = X_test_one
        plan.y_test = y_test_one

        result_two = plan.evaluate()


Additionally if we want to use a different database connection, we can pass the sqlalchemy session object to the evaluator.
::
        from estimators import DataBase
        db = DataBase(url='sqlite://')

        plan = Evaluator()
        plan.session = db.Session
        # and continue as expected otherwise


Development Installation 
------------------------

To install the latest version of estimators, clone the repo, change directory to the repo, and pip install it into your current virtual environment.::

    $ git clone git@github.com:fridiculous/estimators.git
    $ cd estimators
    $ <activate your project’s virtual environment>
    (virtualenv) $ pip install -e .  # the dot specifies for this current repo

