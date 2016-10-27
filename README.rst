
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
First let's imagine you're building a classifer on dataset like so...
::
        from sklearn.ensemble import RandomForestClassifier
        import numpy as np

        rfc = RandomForestClassifier()
        # fake dataset
        X =  np.random.randint(0, 20, (100, 5))
        y =  np.random.randint(0, 3, (100,))

        # pseudo-crossvalidation
        X_train, X_test = X[:70], X[70:]
        y_train, y_test = y[:70], y[70:] 
        rfc.fit(X_train, y_train)


1. Now import an `Evaluator` object that builds a plan 
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


2.  At a later date, you can retrieve your model using sqlalchemy orm. 
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
        ds[0].shape
        ds[0].data


Furthermore, we can run more evaluations using our new proxy objects.  The Evaluator
object handles the setting appropriately for proxy objects such as Estimator and DataSet.
::

        plan = Evaluator() 
        plan.estimator = es 
        plan.X_test = result.X_test 
        plan.y_test = result.y_test 

        result_two = plan.evaluate()


Additionally, we can pass the sqlalchemy session object to the evaluator.
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

