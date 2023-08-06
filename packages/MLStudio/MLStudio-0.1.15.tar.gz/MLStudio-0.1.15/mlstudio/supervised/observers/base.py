#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : MLStudio                                                           #
# Version : 0.1.0                                                              #
# File    : observers.py                                                       #
# Python  : 3.8.2                                                              #
# ---------------------------------------------------------------------------- #
# Author  : John James                                                         #
# Company : DecisionScients                                                    #
# Email   : jjames@decisionscients.com                                         #
# URL     : https://github.com/decisionscients/MLStudio                        #
# ---------------------------------------------------------------------------- #
# Created       : Sunday, March 15th 2020, 7:27:16 pm                          #
# Last Modified : Sunday, March 15th 2020, 7:37:00 pm                          #
# Modified By   : John James (jjames@decisionscients.com)                      #
# ---------------------------------------------------------------------------- #
# License : BSD                                                                #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
"""Module containing functionality called during the training process.

Note: The ObserverList and Observer abstract base classes were inspired by
the Keras implementation.  
"""
from abc import ABC, abstractmethod, ABCMeta
import warnings
warnings.filterwarnings("once", category=RuntimeWarning, module='base')

import datetime
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator

from mlstudio.utils.validation import validate_int, validate_zero_to_one
from mlstudio.utils.validation import validate_metric
# --------------------------------------------------------------------------- #
#                             CALLBACK LIST                                   #
# --------------------------------------------------------------------------- #
class ObserverList:
    """Container of observers."""

    def __init__(self, observers=None):
        """ObserverList constructor
        
        Parameters
        ----------
        observers : list
            List of 'Observer' instances.        
        """
        observers = observers or []
        self.observers = [c for c in observers]        
        self.params = {}
        self.model = None

    def append(self, observer):
        """Appends observer to list of observers.
        
        Parameters
        ----------
        observer : Observer instance            
        """
        self.observers.append(observer)

    def set_params(self, params):
        """Sets the parameters variable, and in list of observers.
        
        Parameters
        ----------
        params : dict
            Dictionary containing model parameters
        """
        self.params = params
        for observer in self.observers:
            observer.set_params(params)

    def set_model(self, model):
        """Sets the model variable, and in the list of observers.
        
        Parameters
        ----------
        model : Estimator or subclass instance 
        
        """
        self.model = model
        for observer in self.observers:
            observer.set_model(model)

    def on_batch_begin(self, batch, log=None):
        """Calls the `on_batch_begin` methods of its observers.

        Parameters
        ----------
        batch : int
            Current training batch

        log: dict
            Currently no data is set to this parameter for this class. This may
            change in the future.
        """
        log = log or {}
        for observer in self.observers:
            observer.on_batch_begin(batch, log)

    def on_batch_end(self, batch, log=None):
        """Calls the `on_batch_end` methods of its observers.
        
        Parameters
        ----------
        batch : int
            Current training batch
        
        log: dict
            Dictionary containing the data, cost, batch size and current weights
        """
        log = log or {}
        for observer in self.observers:
            observer.on_batch_end(batch, log)

    def on_epoch_begin(self, epoch, log=None):
        """Calls the `on_epoch_begin` methods of its observers.

        Parameters
        ----------        
        epoch: integer
            Current training epoch

        log: dict
            Currently no data is passed to this argument for this method
            but that may change in the future.
        """
        log = log or {}
        for observer in self.observers:
            observer.on_epoch_begin(epoch, log)

    def on_epoch_end(self, epoch, log=None):
        """Calls the `on_epoch_end` methods of its observers.
        This function should only be called during train mode.

        Parameters
        ----------
        epoch: int
            Current training epoch
        
        log: dict
            Metric results for this training epoch, and for the
            validation epoch if validation is performed.
        """
        log = log or {}
        for observer in self.observers:
            observer.on_epoch_end(epoch, log)

    def on_train_begin(self, log=None):
        """Calls the `on_train_begin` methods of its observers.

        Parameters
        ----------
        log: dict
            Currently no data is passed to this argument for this method
                but that may change in the future.
        """
        for observer in self.observers:
            observer.on_train_begin(log)

    def on_train_end(self, log=None):
        """Calls the `on_train_end` methods of its observers.

        Parameters
        ----------
        log: dict
            Currently no data is passed to this argument for this method
                but that may change in the future.
        """
        for observer in self.observers:
            observer.on_train_end(log)

    def __iter__(self):
        return iter(self.observers)

# --------------------------------------------------------------------------- #
#                             CALLBACK CLASS                                  #
# --------------------------------------------------------------------------- #
class Observer(ABC, BaseEstimator):
    """Abstract base class used to build new observers."""
    def __init__(self):
        """Observer class constructor."""
        self.params = None
        self.model = None

    def set_params(self, params):
        """Sets parameters from estimator.

        Parameters
        ----------
        params : dict
            Dictionary containing estimator parameters
        """ 
        self.params = params

    def set_model(self, model):
        """Stores model in Observer object.

        Parameters
        ----------
        model : Estimator
            Estimator object
        """
        self.model = model

    def on_batch_begin(self, batch, log=None):
        """Logic executed at the beginning of each batch.

        Parameters
        ----------
        batch : int
            Current training batch
        
        log: dict
            Dictionary containing the data, cost, batch size and current weights
        """        
        pass

    def on_batch_end(self, batch, log=None):   
        """Logic executed at the end of each batch.
        
        Parameters
        ----------
        batch : int
            Current training batch
        
        log: dict
            Dictionary containing the data, cost, batch size and current weights
        """                
        pass

    def on_epoch_begin(self, epoch, log=None):
        """Logic executed at the beginning of each epoch.
        
        Parameters
        ----------
        epoch : int
            Current epoch
        
        log: dict
            Dictionary containing the data, cost, batch size and current weights
        """                
        pass

    def on_epoch_end(self, epoch, log=None):
        """Logic executed at the end of each epoch.
        
        Parameters
        ----------
        epoch : int
            Current epoch
        
        log: dict
            Dictionary containing the data, cost, batch size and current weights
        """                      
        pass

    def on_train_begin(self, log=None):
        """Logic executed at the beginning of training.
        
        Parameters
        ----------        
        log: dict
            Dictionary containing the data, cost, batch size and current weights
        """                      
        pass

    def on_train_end(self, log=None):
        """Logic executed at the end of training.
        
        Parameters
        ----------        
        log: dict
            Dictionary containing the data, cost, batch size and current weights
        """               
        pass
# --------------------------------------------------------------------------- #
#                             PERFORMANCE BASE                                #
# --------------------------------------------------------------------------- #
class PerformanceObserver(Observer):
    """Base class for performance observers."""

    def __init__(self, metric='val_score', epsilon=1e-3, patience=5): 
        super(PerformanceObserver, self).__init__()       
        self.name = "Performance Base Observer"
        self.metric = metric                
        self.epsilon = epsilon
        self.patience = patience     

    @property
    def stabilized(self):
        return self._stabilized   
       
    def _validate(self):     
        if 'val' in self.metric and self.val_size == 0.0:   
            msg = "The val_size parameter must be greater than zero if the metric is {m}".format(m=self.metric)
            raise ValueError(msg)
        validate_zero_to_one(param=self.epsilon, param_name='epsilon',
                             left='closed', right='closed')       
        validate_int(param=self.patience, param_name='patience',
                     minimum=0, left='open', right='open')

    def on_train_begin(self, log=None):                
        """Sets key variables at beginning of training.        
        
        Parameters
        ----------
        log : dict
            Contains no information
        """
        super(PerformanceObserver, self).on_train_begin(log=log)        
        log = log or {}        
        self._validate()
        # Private variables
        self._baseline = None        
        # If the metric is not available in the log, we fallback to 'train_cost'        
        self._fallback_metric = 'train_cost'
        self._iter_no_improvement = 0
        self._stabilized = False
        self._significant_improvement = False
        self._critical_points = []

        # If the metric is a score, determine what constitutes a better
        # and best score. This can be obtained from the scorer object on 
        # the model. 
        if 'score' in self.metric:
            try:
                self._best = self.model.scorer.best
                self._better = self.model.scorer.better
        # If no scorer object on the estimator, then we will assume a greater 
        # score is better and the maximum score is best. This is consistent 
        # with default scorers for regression (R2) and classification (accuracy).                 
            except:
                self._best = np.max
                self._better = np.greater
        # Otherwise, the metric is cost and best and better costs are min and
        # less, respectively
        else:
            self._best = np.min            
            self._better = np.less            

        # Validation
        validate_metric(self.metric)
        validate_zero_to_one(param=self.epsilon, param_name='epsilon',
                             left='open', right='open')
        validate_int(param=self.patience, param_name='patience')

        # log data
        self.performance_log_ = {}

    def _update_log(self, epoch, log):
        """Creates log dictionary of lists of performance results."""
        log['epoch'] = epoch
        log['baseline']= self._baseline
        log['relative_change'] = self._relative_change
        log['significant_improvement'] = self._significant_improvement
        log['iter_no_improvement']= self._iter_no_improvement
        log['stabilized'] = self._stabilized
        for k,v in log.items():
            self.performance_log_.setdefault(k,[]).append(v)
        return log

    def _metric_improved(self, current):
        """Returns true if the direction and magnitude of change indicates improvement"""        
        return self._better(current, self._baseline)

    def _significant_relative_change(self, current):   
        """Returns true if relative change is greater than epsilon."""     
        self._relative_change = abs(current-self._baseline) / abs(self._baseline)
        return self._relative_change > self.epsilon                

    def _process_improvement(self, current, log=None):
        """Sets values of parameters and attributes if improved."""
        self._iter_no_improvement = 0            
        self._stabilized = False
        self._baseline = current
        self._best_results = log

    def _process_no_improvement(self, current, log=None):
        """Sets values of parameters and attributes if no improved."""    
        self._iter_no_improvement += 1  
        if self._iter_no_improvement == self.patience:
            self._stabilized = True
            # We reset iter_no_improvement and baseline to better of the 
            # current value and prior baseline. This gives the estimator
            # another 'patience' epochs to achieve real improvement from
            # new baseline.  
            self._iter_no_improvement = 0
            self._baseline = self._best((current, self._baseline)) 
        else:
            self._stabilized = False               

    def _get_current_value(self, log):
        """Obtain the designated metric or fallback metric from the log."""
        current = log.get(self.metric)
        if current is None:
            if self.metric != self._fallback_metric:
                current = log.get(self._fallback_metric)
                if current is None:
                    msg = "Metrics {m} and {fbm} are not available in the log.\
                        Check dimensions of input data to confirm that there\
                            is adequate data for the metric.".format(
                                m=self.metric, fbm=self._fallback_metric
                            )
                    raise Exception(msg)
                else:
                    msg = "Metric {m} was not available in the log. Using {fbm}\
                        metric instead.".format(m=self.metric, fbm=self._fallback_metric)
                    warnings.warn(message=msg, category=RuntimeWarning)
            else:
                msg = "Metric {m} was not available in the log. Check dimensions\
                    of input data to ensure that {m} can be computed.".format(m=self.metric)
                raise Exception(msg)    
            
        return current

    def on_epoch_end(self, epoch, log=None):
        """Logic executed at the end of each epoch.
        
        Parameters
        ----------
        epoch : int
            Current epoch
        
        log: dict
            Dictionary containing the data, cost, batch size and current weights
        """                  
        log = log or {}   
        
        # Initialize state variables        
        self._significant_improvement = False
        self._relative_change = 0
        
        # Obtain current performance
        current = self._get_current_value(log)

        # Handle first iteration as an improvement by default
        if self._baseline is None:                            
            self._significant_improvement = True
            self._process_improvement(current, log)    

        # Otherwise, evaluate the direction and magnitude of the change        
        else:
            self._significant_improvement = self._metric_improved(current) and \
                self._significant_relative_change(current)

            if self._significant_improvement:
                self._process_improvement(current, log)
            else:
                self._process_no_improvement(current, log)

        # Log results and critical points
        log = self._update_log(epoch, log)
        self._critical_points.append(log)



        
