#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : ML Studio                                                         #
# Version : 0.1.0                                                             #
# File    : regularization.py                                                 #
# Python  : 3.8.2                                                             #
# --------------------------------------------------------------------------  #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/MLStudio                       #
# --------------------------------------------------------------------------  #
# Created       : Saturday, May 16th 2020, 11:17:15 pm                        #
# Last Modified : Saturday, May 16th 2020, 11:17:15 pm                        #
# Modified By   : John James (jjames@decisionscients.com)                     #
# --------------------------------------------------------------------------  #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Classes used to regularize cost and gradient computations."""
from abc import ABC, abstractmethod
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

from mlstudio.utils.data_manager import ZeroBiasTerm
# --------------------------------------------------------------------------  #
class Regularizer(ABC, BaseEstimator, TransformerMixin):
    """Base class for regularization classes."""
    @abstractmethod
    def __init__(self):
        self._zero_bias_term = ZeroBiasTerm()

    @abstractmethod
    def __call__(self, theta, m):
        """Computes regularization to be added to cost function.

        Parameters
        ----------
        theta : np.array shape = (n_features) or (n_features, n_classes)
            The model parameters

        m : int
            The sample size
        """
        pass

    @abstractmethod
    def gradient(self, theta, m):
        """Computes the regularization gradient.

        Parameters
        ----------
        theta : np.array shape = (n_features) or (n_features, n_classes)
            The model parameters

        m : int
            The sample size
        """
        pass

# --------------------------------------------------------------------------  #
class L1(Regularizer):
    """ Regularizer for Lasso Regression """
    def __init__(self, alpha=0.01):
        super(L1, self).__init__()
        self.alpha = alpha
        self.name = "Lasso (L1) Regularizer"
    
    def __call__(self, theta, m):
        theta = self._zero_bias_term.fit_transform(theta)
        return self.alpha * np.sum(np.abs(theta))

    def gradient(self, theta, m):        
        theta = self._zero_bias_term.fit_transform(theta)        
        return self.alpha * np.sign(theta)        
    
# --------------------------------------------------------------------------  #
class L2(Regularizer):
    """ Regularizer for Ridge Regression """
    def __init__(self, alpha=0.01):
        super(L2, self).__init__()
        self.alpha = alpha
        self.name = "Ridge (L2) Regularizer"
    
    def __call__(self, theta, m):
        theta = self._zero_bias_term.fit_transform(theta)
        return self.alpha * np.sum(np.square(theta))

    def gradient(self, theta, m):
        theta = self._zero_bias_term.fit_transform(theta)
        return self.alpha * theta
# --------------------------------------------------------------------------  #
class L1_L2(Regularizer):
    """ Regularizer for Elastic Net Regression """

    def __init__(self, alpha=0.01, ratio=0.5):
        super(L1_L2, self).__init__()
        self.alpha = alpha
        self.ratio = ratio
        self.name = "Elasticnet (L1_L2) Regularizer"

    def __call__(self, theta, m):
        theta = self._zero_bias_term.fit_transform(theta)
        l1_contr = self.ratio * np.sum(np.abs(theta))
        l2_contr = (1 - self.ratio) * np.sum(np.square(theta))
        return self.alpha * (l1_contr + l2_contr)

    def gradient(self, theta, m):
        theta = self._zero_bias_term.fit_transform(theta)
        l1_contr = self.ratio * np.sign(theta)
        l2_contr = (1 - self.ratio)  * theta
        return self.alpha * (l1_contr + l2_contr) 