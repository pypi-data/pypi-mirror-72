#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : ML Studio                                                         #
# Version : 0.1.0                                                             #
# File    : regression.py                                                     #
# Python  : 3.8.3                                                             #
# --------------------------------------------------------------------------  #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/MLStudio                       #
# --------------------------------------------------------------------------  #
# Created       : Friday, April 10th 2020, 3:27:23 pm                         #
# Last Modified : Wednesday, June 10th 2020, 9:11:49 pm                       #
# Modified By   : John James (jjames@decisionscients.com)                     #
# --------------------------------------------------------------------------  #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
#%%
from collections import OrderedDict
import os
from pathlib import Path
import sys
homedir = str(Path(__file__).parents[4])
demodir = str(Path(__file__).parents[2])
sys.path.append(homedir)

import pandas as pd
import numpy as np
from sklearn.linear_model import SGDRegressor

from mlstudio.supervised.machine_learning.gradient_descent import GradientDescentRegressor
from mlstudio.supervised.core.scorers import R2
from mlstudio.supervised.core.objectives import MSE
from mlstudio.utils.data_manager import StandardScaler, data_split
from mlstudio.visual.animations import animate_optimization_regression


def get_data():
    """Obtains the Ames housing price data for modeling."""
    # ----------------------------------------------------------------------  #
    # Designate file locations
    datadir = os.path.join(homedir,"mlstudio/demo/data/Ames/")
    filepath = os.path.join(datadir, "train.csv")
    # ----------------------------------------------------------------------  #
    # Obtain and scale data
    cols = ["GrLivArea", "SalePrice"]
    df = pd.read_csv(filepath, nrows=500, usecols=cols)
    df_samples = df.head()
    X = np.array(df['GrLivArea']).reshape(-1,1)
    y = df['SalePrice']
    X_train, X_test, y_train, y_test = data_split(X,y, random_state=5)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test

def train_models(X, y):
    """Trains batch, stochastic and minibatch gradient descent."""    
    bgd = GradientDescentRegressor(theta_init=np.array([0,0]), epochs=500, 
                                   random_state=50,scorer=R2(),
                                   objective=MSE())
    sgd = GradientDescentRegressor(theta_init=np.array([0,0]), epochs=500, 
                                   batch_size=1, random_state=50, scorer=R2(),
                                   objective=MSE())
    mbgd = GradientDescentRegressor(theta_init=np.array([0,0]), epochs=500, 
                                    batch_size=64, random_state=50, scorer=R2(),
                                    objective=MSE())
    bgd.fit(X,y)
    sgd.fit(X,y)
    mbgd.fit(X,y)
    estimators = {'Batch Gradient Descent': bgd, 'Stochastic Gradient Descent': sgd,
            'Minibatch Gradient Descent': mbgd}
    return estimators

def append_filepath(filepath=None, appendage=None):
    """Appends the appendage to the filepath."""
    if filepath:
        base = os.path.basename(filepath)
        ext = os.path.splitext(base)[1]
        base = base + "_" + appendage + ext
        filepath = os.path.join(os.path.dirname(filepath), base)
    return filepath

def plot_optimization(estimators, max_frames=None, filepath=None, show=True):
    """Renders surface, scatterplot, and line plots."""        
    filepath = append_filepath(filepath, "optimization")
    # Render plot
    animate_optimization_regression(estimators=estimators, max_frames=max_frames, 
                                    filepath=filepath, show=show)

def regression_demo(max_frames=None, filepath=None, show=True):
    """Regression demo main processing function.
    
    Parameters
    ----------
    filepath:  str
        A relative or absolute filepath. 

    show: bool (default=True)
        Indicates whether to render the plot  
    
    """
     
    X_train, X_test, y_train, y_test = get_data()
    estimators = train_models(X_train, y_train)
    plot_optimization(estimators=estimators, max_frames=max_frames, 
                      filepath=filepath, show=show)

def main():
    filepath = os.path.join(demodir, 'figures/regression_demo.html')
    regression_demo(max_frames=100, filepath=filepath)

if __name__ == "__main__":
    main()
#%%

