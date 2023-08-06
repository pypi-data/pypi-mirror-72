#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : ML Studio                                                         #
# Version : 0.1.14                                                            #
# File    : test_objectives.py                                                #
# Python  : 3.8.3                                                             #
# --------------------------------------------------------------------------  #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/MLStudio                       #
# --------------------------------------------------------------------------  #
# Created       : Monday, June 15th 2020, 3:45:31 pm                          #
# Last Modified : Monday, June 15th 2020, 3:45:31 pm                          #
# Modified By   : John James (jjames@decisionscients.com)                     #
# --------------------------------------------------------------------------  #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
#%%
import math
import os
from pathlib import Path
import sys

import glob
import numpy as np
import pandas as pd
import pytest
from pytest import mark
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_regression, make_classification
from sklearn.datasets import make_multilabel_classification

homedir = str(Path(__file__).parents[3])
datadir = os.path.join(homedir, "tests\\test_data")
sys.path.append(homedir)
sys.path.append(datadir)

from mlstudio.supervised.core.objectives import MSE, CrossEntropy
from mlstudio.supervised.core.objectives import CategoricalCrossEntropy
from mlstudio.supervised.core.regularizers import L1, L2, L1_L2
# --------------------------------------------------------------------------  #
@mark.objectives
@mark.mse
class MSETests:

    @mark.mse_cost
    def test_cost(self, get_objective_mse_package):
        p = get_objective_mse_package
        obj = MSE()
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost'][0])

    @mark.mse_cost
    def test_cost_l1(self, get_objective_mse_package):
        p = get_objective_mse_package
        obj = MSE(L1(alpha=0.1))
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost_l1'][0])

    @mark.mse_cost
    def test_cost_l2(self, get_objective_mse_package):
        p = get_objective_mse_package
        obj = MSE(L2(alpha=0.1))
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost_l2'][0])

    @mark.mse_cost        
    def test_cost_l1_l2(self, get_objective_mse_package):
        p = get_objective_mse_package
        obj = MSE(L1_L2(alpha=0.1, ratio=0.5))
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost_l1_l2'][0])    

    # ----------------------------------------------------------------------  #
    @mark.mse_grad
    def test_gradient(self, get_objective_mse_package):
        p = get_objective_mse_package
        obj = MSE()
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad'])

    @mark.mse_grad
    def test_gradient_l1(self, get_objective_mse_package):
        p = get_objective_mse_package
        obj = MSE(regularizer=L1(alpha=0.1))
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad_l1'])

    @mark.mse_grad
    def test_gradient_l2(self, get_objective_mse_package):
        p = get_objective_mse_package
        obj = MSE(regularizer=L2(alpha=0.1))
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad_l2'])

    @mark.mse_grad
    def test_gradient_l1_l2(self, get_objective_mse_package):
        p = get_objective_mse_package
        obj = MSE(regularizer=L1_L2(alpha=0.1, ratio=0.5))
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad_l1_l2'])
    

# --------------------------------------------------------------------------  #
@mark.objectives
@mark.cross_entropy
class CrossEntropyTests:

    @mark.cross_entropy_cost
    def test_cost(self, get_objective_xe_package):
        p = get_objective_xe_package
        obj = CrossEntropy()
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost'][0])

    @mark.cross_entropy_cost
    def test_cost_l1(self, get_objective_xe_package):
        p = get_objective_xe_package
        obj = CrossEntropy(L1(alpha=0.1))
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost_l1'][0])

    @mark.cross_entropy_cost
    def test_cost_l2(self, get_objective_xe_package):
        p = get_objective_xe_package
        obj = CrossEntropy(L2(alpha=0.1))
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost_l2'][0])

    @mark.cross_entropy_cost        
    def test_cost_l1_l2(self, get_objective_xe_package):
        p = get_objective_xe_package
        obj = CrossEntropy(L1_L2(alpha=0.1, ratio=0.5))
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost_l1_l2'][0])    

    # ----------------------------------------------------------------------  #
    @mark.cross_entropy_grad
    def test_gradient(self, get_objective_xe_package):
        p = get_objective_xe_package
        obj = CrossEntropy()
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad'])

    @mark.cross_entropy_grad
    def test_gradient_l1(self, get_objective_xe_package):
        p = get_objective_xe_package
        obj = CrossEntropy(regularizer=L1(alpha=0.1))
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad_l1'])

    @mark.cross_entropy_grad
    def test_gradient_l2(self, get_objective_xe_package):
        p = get_objective_xe_package
        obj = CrossEntropy(regularizer=L2(alpha=0.1))
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad_l2'])

    @mark.cross_entropy_grad
    def test_gradient_l1_l2(self, get_objective_xe_package):
        p = get_objective_xe_package
        obj = CrossEntropy(regularizer=L1_L2(alpha=0.1, ratio=0.5))
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad_l1_l2'])
        
# --------------------------------------------------------------------------  #
@mark.objectives
@mark.multiclass
class CategoricalCrossEntropyTests:

    @mark.multiclass_cost
    def test_cost(self, get_objective_cxe_package):
        p = get_objective_cxe_package
        obj = CategoricalCrossEntropy()
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost'][0])

    @mark.multiclass_cost
    def test_cost_l1(self, get_objective_cxe_package):
        p = get_objective_cxe_package
        obj = CategoricalCrossEntropy(L1(alpha=0.1))
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost_l1'][0])

    @mark.multiclass_cost
    def test_cost_l2(self, get_objective_cxe_package):
        p = get_objective_cxe_package
        obj = CategoricalCrossEntropy(L2(alpha=0.1))
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost_l2'][0])

    @mark.multiclass_cost        
    def test_cost_l1_l2(self, get_objective_cxe_package):
        p = get_objective_cxe_package
        obj = CategoricalCrossEntropy(L1_L2(alpha=0.1, ratio=0.5))
        J = obj(p['theta'], p['y'], p['y_pred'])
        assert np.isclose(J, p['cost_l1_l2'][0])    

    # ----------------------------------------------------------------------  #
    @mark.multiclass_grad
    def test_gradient(self, get_objective_cxe_package):
        p = get_objective_cxe_package
        obj = CategoricalCrossEntropy()
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad'])

    @mark.multiclass_grad
    def test_gradient_l1(self, get_objective_cxe_package):
        p = get_objective_cxe_package
        obj = CategoricalCrossEntropy(regularizer=L1(alpha=0.1))
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad_l1'])

    @mark.multiclass_grad
    def test_gradient_l2(self, get_objective_cxe_package):
        p = get_objective_cxe_package
        obj = CategoricalCrossEntropy(regularizer=L2(alpha=0.1))
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad_l2'])

    @mark.multiclass_grad
    def test_gradient_l1_l2(self, get_objective_cxe_package):
        p = get_objective_cxe_package
        obj = CategoricalCrossEntropy(regularizer=L1_L2(alpha=0.1, ratio=0.5))
        g = obj.gradient(p['theta'], p['X'], p['y'], p['y_pred'])
        assert np.allclose(g, p['grad_l1_l2'])        