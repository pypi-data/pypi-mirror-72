#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#
from __future__ import absolute_import, division, print_function, unicode_literals

from h2o.estimators.estimator_base import H2OEstimator
from h2o.exceptions import H2OValueError
from h2o.frame import H2OFrame
from h2o.utils.typechecks import assert_is_type, Enum, numeric


class H2OGenericEstimator(H2OEstimator):
    """
    Import MOJO Model

    """

    algo = "generic"
    param_names = {"model_id", "model_key", "path"}

    def __init__(self, **kwargs):
        super(H2OGenericEstimator, self).__init__()
        self._parms = {}
        for pname, pvalue in kwargs.items():
            if pname == 'model_id':
                self._id = pvalue
                self._parms["model_id"] = pvalue
            elif pname in self.param_names:
                # Using setattr(...) will invoke type-checking of the arguments
                setattr(self, pname, pvalue)
            else:
                raise H2OValueError("Unknown parameter %s = %r" % (pname, pvalue))

    @property
    def model_key(self):
        """
        Key to the self-contained model archive already uploaded to H2O.

        Type: ``H2OFrame``.

        :examples:

        >>> from h2o.estimators import H2OGenericEstimator, H2OXGBoostEstimator
        >>> import tempfile
        >>> airlines= h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/testng/airlines_train.csv")
        >>> y = "IsDepDelayed"
        >>> x = ["fYear","fMonth","Origin","Dest","Distance"]
        >>> xgb = H2OXGBoostEstimator(ntrees=1, nfolds=3)
        >>> xgb.train(x=x, y=y, training_frame=airlines)
        >>> original_model_filename = tempfile.mkdtemp()
        >>> original_model_filename = xgb.download_mojo(original_model_filename)
        >>> key = h2o.lazy_import(original_model_filename)
        >>> fr = h2o.get_frame(key[0])
        >>> model = H2OGenericEstimator(model_key=fr)
        >>> model.train()
        >>> model.auc()
        """
        return self._parms.get("model_key")

    @model_key.setter
    def model_key(self, model_key):
        self._parms["model_key"] = H2OFrame._validate(model_key, 'model_key')


    @property
    def path(self):
        """
        Path to file with self-contained model archive.

        Type: ``str``.

        :examples:

        >>> from h2o.estimators import H2OIsolationForestEstimator, H2OGenericEstimator
        >>> import tempfile
        >>> airlines= h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/testng/airlines_train.csv")
        >>> ifr = H2OIsolationForestEstimator(ntrees=1)
        >>> ifr.train(x=["Origin","Dest"], y="Distance", training_frame=airlines)
        >>> generic_mojo_filename = tempfile.mkdtemp("zip","genericMojo")
        >>> generic_mojo_filename = model.download_mojo(path=generic_mojo_filename)
        >>> model = H2OGenericEstimator.from_file(generic_mojo_filename)
        >>> model.model_performance()
        """
        return self._parms.get("path")

    @path.setter
    def path(self, path):
        assert_is_type(path, None, str)
        self._parms["path"] = path


    def _requires_training_frame(self):
        """
        Determines if Generic model requires a training frame.
        :return: False.
        """
        return False

    @staticmethod
    def from_file(file=str):
        """
        Creates new Generic model by loading existing embedded model into library, e.g. from H2O MOJO.
        The imported model must be supported by H2O.

        :param file: A string containing path to the file to create the model from
        :return: H2OGenericEstimator instance representing the generic model

        :examples:

        >>> from h2o.estimators import H2OIsolationForestEstimator, H2OGenericEstimator
        >>> import tempfile
        >>> airlines= h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/testng/airlines_train.csv")
        >>> ifr = H2OIsolationForestEstimator(ntrees=1)
        >>> ifr.train(x=["Origin","Dest"], y="Distance", training_frame=airlines)
        >>> original_model_filename = tempfile.mkdtemp()
        >>> original_model_filename = ifr.download_mojo(original_model_filename)
        >>> model = H2OGenericEstimator.from_file(original_model_filename)
        >>> model.model_performance()
        """
        model = H2OGenericEstimator(path = file)
        model.train()

        return model
