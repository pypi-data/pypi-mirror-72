#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ============================================================================ #
# Project : MLStudio                                                           #
# Version : 0.1.0                                                              #
# File    : data_manager.py                                                    #
# Python  : 3.8.2                                                              #
# ---------------------------------------------------------------------------- #
# Author  : John James                                                         #
# Company : DecisionScients                                                    #
# Email   : jjames@decisionscients.com                                         #
# URL     : https://github.com/decisionscients/MLStudio                        #
# ---------------------------------------------------------------------------- #
# Created       : Sunday, March 15th 2020, 6:52:47 pm                          #
# Last Modified : Sunday, March 15th 2020, 6:57:11 pm                          #
# Modified By   : John James (jjames@decisionscients.com)                      #
# ---------------------------------------------------------------------------- #
# License : BSD                                                                #
# Copyright (c) 2020 DecisionScients                                           #
# ============================================================================ #
#%%
"""Data manipulation functions."""
from abc import ABC, abstractmethod
from itertools import combinations_with_replacement
from math import ceil, floor

import numpy as np
from numpy.random import RandomState
import pandas as pd
from scipy.sparse import isspmatrix_coo, issparse, csr_matrix, hstack
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.utils import shuffle, check_array
from sklearn.preprocessing import LabelBinarizer, LabelEncoder

from mlstudio.utils.validation import check_X_y
# --------------------------------------------------------------------------- #
#                           DATA PREPARATION                                  #
# --------------------------------------------------------------------------- #

def check_coo(X):
    """Converts coo matrices to csr format."""
    if issparse(X):
        if isspmatrix_coo(X):
            X = X.tocsr()
    return X    
# --------------------------------------------------------------------------- #
def unpack_parameters(theta):
    """Unpacks the parameters theta and returns bias and weights."""
    if np.ndim(theta) == 0:
        bias = np.array([0])
        weights = np.array(theta)
    elif np.ndim(theta) == 1:
        bias = theta[0]
        weights = theta[1:]
    else:
        bias = theta[0,:]
        weights = theta[1:,:]
    return bias, weights
# --------------------------------------------------------------------------- #
def encode_labels(y):
    """Encodes labels to have values from 0 to n_classes - 1
    
    Parameters
    ----------
    y : array shape (n_samples,)
        Labels to encode

    Returns
    -------
    y : Encoded labels with values from 0 to n_classes - 1
    """
    classes = np.sort(np.unique(y))
    n_classes = len(classes)
    binary_classes = np.arange(n_classes)
    if np.array_equal(classes, binary_classes):
        return y
    else:
        encoder = LabelEncoder()
        return encoder.fit_transform(y)

# --------------------------------------------------------------------------- #
#                               TRANSFORMERS                                  #
# --------------------------------------------------------------------------- #
class AddBiasTerm(BaseEstimator, TransformerMixin):
    """Adds bias term of ones to matrix."""

    def fit(self, X, y=None):
        """Fits data to the transformer."""
        return self

    def _transform_numpy(self, X):
        """Adds bias term to numpy matrix."""
        return np.insert(X, 0, 1.0, axis=1)
    
    def _transform_csr(self, X):
        """Adds bias term to csr matrix."""
        X = check_coo(X)
        ones = np.ones((X.shape[0],1))
        bias_term = csr_matrix(ones, dtype=float)
        X = hstack((bias_term, X)) 
        X = check_coo(X)
        return X

    def transform(self, X, y=None):
        """Adds bias term to matrix and returns it to the caller."""
        X = check_array(X, accept_sparse=True, accept_large_sparse=True)
        if issparse(X):
            X = self._transform_csr(X)
        else:
            X = self._transform_numpy(X)
        return X        
    
    def inverse_transform(self, X):
        """Removes bias term from matrix and returns it to caller."""
        X = check_coo(X)
        return X[:,1:]
                        
# --------------------------------------------------------------------------- #
class ZeroBiasTerm(BaseEstimator, TransformerMixin):
    """Zeros out bias term in a parameters matrix or tensor."""

    def fit(self, X, y=None):
        """Fits data to the transformer."""
        return self

    def transform(self, X):
        """Zero out bias term in numpy matrix."""
        if np.ndim(X) == 1:
            X[0] = 0
        else:
            X[0,:] = np.zeros(shape=X.shape[1])
        return X
           

# --------------------------------------------------------------------------- #
class DataProcessor(ABC, BaseEstimator):
    """Prepares data for training.
    
    Parameters
    ----------
    val_size : float (default = 0.3)
        The proportion of data to be allocated to a validation set.

    random_state : int or None (default = None)
        The seed for pseudo randomization.
    
    """
    def __init__(self, estimator, random_state=None):        
        self.estimator = estimator
        self.random_state = random_state


    def fit(self, X, y=None):
        """Returns self."""
        return self

    @abstractmethod
    def transform(self, X, y=None):
        """Processes data and returns a dictionary to the calling object.
        
        Parameters
        ----------
        X : array_like of shape (n_samples,n_features)
            The matrix of inputs 

        y : array_like of shape(n_samples,)
            An array of target values.

        Returns
        -------
        dict : Dictionary containing transformed data.           

        """
        pass

    def fit_transform(self, X, y=None):
        """Calls fit and transform."""
        return self.fit(X, y).transform(X, y)        

# --------------------------------------------------------------------------- #
class RegressionDataProcessor(DataProcessor):
    """Prepares data for regression."""

    def transform(self, X, y):
        """Prepares data for regression."""
        X_train, y_train = check_X_y(X, y)
        X_train = AddBiasTerm().fit_transform(X_train)
        # Initialize data dictionary and n_features (including bias term)
        d = {}
        d['n_features_'] = X_train.shape[1]        
        # Return training and validation data if val_size is truthy
        if self.estimator.val_size:
            X_train, X_val, y_train, y_val = data_split(X=X_train, y=y_train, 
                        stratify=False, test_size=self.estimator.val_size, 
                        random_state=self.random_state)
            d['X_train_'] = X_train
            d['y_train_'] = y_train
            d['X_val_'] = X_val
            d['y_val_'] = y_val            
        # Otherwise return just training data
        else:             
            d['n_features_'] = X_train.shape[1]
            d['X_train_'] = X_train
            d['y_train_'] = y_train

        return d

# --------------------------------------------------------------------------- #
class LogisticRegressionDataProcessor(DataProcessor):
    """Prepares data for regression."""

    def transform(self, X, y):
        """Prepares data for regression."""
        # Check the data and add bias term
        X_train, y_train = check_X_y(X, y)
        X_train = AddBiasTerm().fit_transform(X_train)
        # Initialize data dictionary and n_features (including bias term)
        d = {}
        d['n_features_'] = X_train.shape[1]        
        # Return stratified training and validation data if val_size is truthy
        if self.estimator.val_size:
            X_train, X_val, y_train, y_val = data_split(X=X_train, y=y_train, 
                        stratify=True, test_size=self.estimator.val_size, 
                        random_state=self.random_state)
            d['X_train_'] = X_train
            d['y_train_'] = y_train
            d['X_val_'] = X_val
            d['y_val_'] = y_val            
        # Otherwise return just training data
        else:             
            d['n_features_'] = X_train.shape[1]
            d['X_train_'] = X_train
            d['y_train_'] = y_train

        return d
# --------------------------------------------------------------------------- #
class MulticlassDataProcessor(DataProcessor):
    """Prepares data for multi-class classification."""

    def transform(self, X, y):
        """Prepares data for multi-class classification."""
        if len(np.unique(y)) < 3:
            msg = "This data processor is for multi-class settings with classes\
                >2. Please use the LogisticRegressionDataProcessor instead."
            raise Exception(msg)

        # Check the data, add bias term, and encode y to values [0,n_classes - 1]
        X_train, y_train = check_X_y(X, y)
        X_train = AddBiasTerm().fit_transform(X_train)
        y_train = encode_labels(y_train)
        # Initialize data dict, n_features (including bias term) and n_classes
        d = {}
        d['n_features_'] = X_train.shape[1]  
        d['n_classes_'] = len(np.unique(y_train))
        # Return stratified training and validation data if val_size is truthy
        if self.estimator.val_size:
            X_train, X_val, y_train, y_val = data_split(X=X_train, y=y_train, 
                        stratify=True, test_size=self.estimator.val_size, 
                        random_state=self.random_state)
            d['X_train_'] = X_train
            d['y_train_'] = y_train            
            d['X_val_'] = X_val
            d['y_val_'] = y_val
        # Otherwise return training data
        else:
            d['X_train_'] = X_train
            d['y_train_'] = y_train        
        return d                               

# --------------------------------------------------------------------------- #
class NormScaler(TransformerMixin, BaseEstimator):
    """Scalers a vector to unit length.  

    Scaling a sample 'x' to 0-1 is calculated as:

        X_new = X/ X.norm

    Note: Works for dense matrices only.

    Attributes
    ----------
    r : float
        The magnitude of the vector

    """        

    def __init__(self, clip_norm=1):        
        self.clip_norm = clip_norm
        self.r_ = None

    def fit(self, X, y=None):
        """Computes the Frobenius norm of the input vector
        
        Parameters
        ----------
        X : array-like, shape [n_features,]
            The data used to compute the mean and standard deviation
            used for centering and scaling.

        y : Ignored

        """
        self.r_= np.linalg.norm(X)
        return self

    def transform(self, X):
        """Scales features to have a norm of 1

        Parameters
        ----------
        X : array-like, shape [n_features,]
            The data to scale

        Returns
        -------
        Xt : array-like of same shape as X
        """
        X = np.divide(X, self.r_) * self.clip_norm               
        return X

    def fit_transform(self, X):
        """Combines fit and transform methods.
        
        Parameters
        ----------
        X : array-like, shape [n_features,]
            The data to scale
        
        Returns
        -------
        Xt : array-like of same shape as X
        """
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X):
        """Inverses the standardization process.

        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The centered and scaled data.

        Returns
        -------
        array-like of same shape as X, with data returned to original
        un-standardized values.
        """
        X = X * self.r_ / self.clip_norm    
        return X
# --------------------------------------------------------------------------- #

class MinMaxScaler(TransformerMixin, BaseEstimator):
    """Scales each feature to values between 0 and 1.

    Scaling a sample 'x' to 0-1 is calculated as:

        X_new = (X - X_min) / (X_max-X_min)

    Note: Works for dense matrices only.

    Attributes
    ----------
    data_min_ : ndarray, shape (n_features)
        Per feature minimum seen in the data

    data_max_ : ndarray, shape (n_features)
        Per feature maximum seen in the data        

    data_range_ : ndarray, shape (n_features)
        Per feature range ``(data_max_ - data_min_)`` seen in the data

    """        

    def __init__(self):        
        pass

    def fit(self, X, y=None):
        """Computes the min and max on X for scaling.
        
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data used to compute the mean and standard deviation
            used for centering and scaling.

        y : Ignored

        """
        self.data_min_ = np.amin(X, axis=0)
        self.data_max_ = np.amax(X, axis=0)
        self.data_range_ = self.data_max_ - self.data_min_
        return self

    def transform(self, X):
        """Scales features to range 0 to 1.

        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data to center and scale.

        Returns
        -------
        Xt : array-like of same shape as X
        """
        X = X - self.data_min_
        X = np.divide(X, self.data_range_, 
                      out = np.zeros(X.shape,dtype=float), 
                      where = self.data_range_ != 0)        
        return X

    def fit_transform(self, X):
        """Combines fit and transform methods.
        
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data to center and scale.
        
        Returns
        -------
        Xt : array-like of same shape as X
        """
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X):
        """Inverses the standardization process.

        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The centered and scaled data.

        Returns
        -------
        array-like of same shape as X, with data returned to original
        un-standardized values.
        """
        X = X * self.data_range_
        X = X + self.data_min_
        return X
# --------------------------------------------------------------------------- #
class StandardScaler(TransformerMixin, BaseEstimator):
    """Standardizes data to a zero mean and unit variance.

    Standardizing a sample 'x' is calculated as:

        z = (x - u) / s
    where 'u' is either the mean of the training samples 'x', or zero of 
    'center=False' and 's' is the standard deviation of the training samples
    or one if 'scale=False'.

    Parameters
    ----------
    center : Bool, optional (default=True)
        If True, center the data by subtracting the means of the variables.

    scale : Bool, optional (default=True)
        If True, scale the data to a unit variance.

    Attributes
    ----------
    mean_ : array-like, shape (n_features)
        The mean value for each feature in the training set.
        Equal to zero if 'center=False'.

    std_ : array-like, shape (n_features)
        The standard deviation for each feature in the training set.
        Equal to one if 'scale=False'.
    """        

    def __init__(self, center=True, scale=True):
        self.center = center
        self.scale = scale
        self.mean_=0
        self.std_=1

    def fit(self, X, y=None):
        """Computes the mean and std for centering and scaling the data.
        
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data used to compute the mean and standard deviation
            used for centering and scaling.

        y : Ignored

        """
        if self.center:
            self.mean_ = np.mean(X,axis=0)
        if self.scale:
            self.std_ = np.std(X,axis=0)
        return self

    def transform(self, X):
        """Center and scale the data.

        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data to center and scale.

        Returns
        -------
        array-like of same shape as X, centered and scaled
        """
        z = (X-self.mean_)/self.std_
        return z

    def inverse_transform(self, X):
        """Inverses the standardization process.

        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The centered and scaled data.

        Returns
        -------
        array-like of same shape as X, with data returned to original
        un-standardized values.
        """
        X = X * self.std_
        X = X + self.mean_
        return X

    def fit_transform(self, X):
        """Calls fit and transform methods."""
        self.fit(X)
        return self.transform(X)

# --------------------------------------------------------------------------  #
#                           GRADIENT SCALING                                  #        
# --------------------------------------------------------------------------  #        
class GradientScaler(BaseEstimator, TransformerMixin):
    """Scales and/or normalizes exploding and vanishing gradients. 

    If the norm of the gradient is below the lower threshold, the gradient
    is rescaled to a unit vector. If it is greater than the upper threshold
    then the new gradient is given by:

    ..math:: \nabla_{new} = \frac{\text{upper_threshold}}{\lVert \nabla \rVert} \times \nabla
    
    Parameters
    ----------
    lower_threshold : float (default=1e-15)
        The lower threshold for the magnitude of the vector.

    upper_threshold : float (default=1e15)
        The upper threshold for the magnitude of the vector.   

    """

    def __init__(self, lower_threshold=1e-10, upper_threshold=1e10): 
        self.lower_threshold  = lower_threshold
        self.upper_threshold = upper_threshold
        self.normalizer_ = None

    def fit(self, X, y=None):
        """Fits the transformer to the data. """  
        self._r = np.linalg.norm(X)
        return self       

    def transform(self, X):
        """Transforms the data."""                
        if self._r < self.lower_threshold:
            X = X  * self.lower_threshold / self._r                        
        elif self._r > self.upper_threshold:
            X = X  * self.upper_threshold / self._r            
        return X
            
    def fit_transform(self, X):
        """Performs fit and transform."""
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X):
        """Apply the inverse transformation."""
        if self._r < self.lower_threshold:
            X = X  * self._r / self.lower_threshold                         
        elif self._r > self.upper_threshold:
            X = X  * self._r / self.upper_threshold                    
        return X

# --------------------------------------------------------------------------- #
#                            SHUFFLE DATA                                     #
# --------------------------------------------------------------------------- #
def shuffle_data(X, y=None, random_state=None):
    """ Random shuffle of the samples in X and y.
    
    Shuffles data

    Parameters
    ----------
    X : array_like of shape (m, n_features)
        Input data

    y : array_like of shape (m,)
        Target data    

    Returns
    -------
    Shuffled X, and y
    
    """    
    X, y = shuffle(X, y, random_state=random_state)
    return X, y

# --------------------------------------------------------------------------- #
#                              SAMPLE                                         #
# --------------------------------------------------------------------------- #    
def sampler(X, y, size=1, replace=True, random_state=None):
    """Generates a random sample of a given size from a data set.

        Parameters
    ----------
    X : array_like of shape (m, n_features)
        Input data

    y : array_like of shape (m,)
        Target data    

    size : int
        The size of the dataset.

    replace : Bool. 
        Whether to sample with or without replacement

    random_state : int
        random_state for reproducibility
    
    Returns
    -------
    X, y    : Random samples from data sets X, and y of the designated size.

    """
    import numpy as np

    nobs = X.shape[0]
    idx = np.random.choice(a=nobs, size=size, replace=True)
    return X[idx], y[idx]

# --------------------------------------------------------------------------- #
#                            SPLIT DATA                                       #
# --------------------------------------------------------------------------- #
def data_split(X, y, test_size=0.3, shuffle=False, stratify=False, random_state=None):
    """ Split the data into train and test sets 
    
    Splits inputs X, and y into training and test sets of proportions
    1-test_size, and test_size respectively.

    Parameters
    ----------
    X : array_like of shape (m, n_features)
        Input data

    y : array_like of shape (m,)
        Target data

    test_size : float, optional (default=0.3)
        The proportion of X, and y to be designated to the test set.

    shuffle : bool, optional (default=True)
        Bool indicating whether the data should be shuffled prior to split.

    stratify : bool, optional (default=False)
        If True, stratified sampling is performed. 

    random_state : int, optional (default=None)
        Random state variable

    Returns
    -------
    X_train : array-like
        Training data 

    X_test : array-like
        Test data

    y_train : array-like
        Targets for X_train

    y_test : array_like
        Targets for X_test 
    """
    if isspmatrix_coo(X):
        X = X.tocsr()
    if isspmatrix_coo(y):
        y = y.tocsr()
        
    if X.shape[0] != y.shape[0]:
        raise ValueError("X and y have incompatible shapes. Expected "
                         "X.shape[0]=y.shape[0] however X.shape[0] = %d "
                         " and y.shape[0] = %d." % (X.shape[0], y.shape[0]))

    if not stratify:
        if shuffle:
            X, y = shuffle_data(X, y, random_state)
        split_i = len(y) - int(len(y) // (1 / test_size))
        X_train, X_test = X[:split_i], X[split_i:]
        y_train, y_test = y[:split_i], y[split_i:]
    else:
        train_idx = []
        test_idx = []
        classes = np.unique(y)
        for k in classes:
            # Obtain the indices and number of samples for class k
            idx_k = np.array(np.where(y == k)).reshape(-1,1)  
            n_samples_k = idx_k.shape[0]
            # Compute number of training and test samples
            n_train_samples_k = ceil(n_samples_k * (1-test_size))
            n_test_samples_k = n_samples_k - n_train_samples_k
            # Shuffle the data
            if shuffle:
                if random_state:
                    np.random.random_state(random_state)
                np.random.shuffle(idx_k)
            # Allocate corresponding indices to training and test set indices
            train_idx_k = idx_k[0:n_train_samples_k]
            test_idx_k = idx_k[n_train_samples_k:n_train_samples_k+n_test_samples_k]
            # Maintain indices in a list
            train_idx.append(train_idx_k)
            test_idx.append(test_idx_k)
        # Concatenate all indices into a training and test indices
        train_idx = np.concatenate(train_idx).ravel()
        test_idx = np.concatenate(test_idx).ravel()
        # Slice and dice.
        y_train, y_test = y[train_idx], y[test_idx]
        X_train, X_test = X[train_idx], X[test_idx]

    return X_train, X_test, y_train, y_test

def batch_iterator(X, y=None, batch_size=None):
    """Batch generator.
    
    Creates an iterable of batches of the designated batch size.

    Parameters
    ----------
    X : array-like
        A features matrix of shape (m, n_features), where m is the number of 
        examples in X.
    
    y : array-like, optional (default=None)
        The target vector of shape (m,)

    batch_size : None or int, optional (default=None)
        The number of observations to be included in each batch. 

    Returns
    -------
    array-like
        Returns inputs in batches of batch_size. If batch_size
        is None, a single batch containing all data is generated.
    
    """
    n_samples = X.shape[0]
    if batch_size is None:
        batch_size = n_samples    
    for i in np.arange(0, n_samples, batch_size):
        if y is not None:
            yield X[i:i+batch_size], y[i:i+batch_size]
        else:
            yield X[i:i+batch_size]

def one_hot(x, n_classes=None, dtype='float32'):
    """Converts a vector of integers to one-hot encoding. 
    
    Creates a one-hot matrix for multi-class classification
    and categorical cross_entropy.

    Parameters
    ----------
    x : array-like of shape(n_observations,)
        Vector of integers (from 0 to num_classes-1) to be converted to one-hot matrix.
    n_classes : int
        Number of classes
    dtype : Data type to be expected, as a string
        ('float32', 'float64', 'int32', ...)

    Returns
    -------
    A binary one-hot matrix representation of the input. The classes axis
    is placed last.
    """
    x = np.array(x, dtype='int')
    if not n_classes:
        n_classes = np.amax(x) + 1
    one_hot = np.zeros((x.shape[0], n_classes))
    one_hot[np.arange(x.shape[0]), x] = 1
    return one_hot

def todf(x, stub):
    """Converts nested array to dataframe."""
    n = len(x[0])
    df = pd.DataFrame()
    for i in range(n):
        colname = stub + str(i)
        vec = [item[i] for item in x]
        df_vec = pd.DataFrame(vec, columns=[colname])
        df = pd.concat([df, df_vec], axis=1)
    return(df)  
