"""
Contain ImputeMin(), ImputeAverage(), ImputeKnn(), _ImputeMinToSingleColumn()
"""

import pandas as pd
import numpy as np
import copy
from .CommonFunction import GenerateStat, PrintStat
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer


def ImputeMin(rawDataObj, percentage=0.1):
    """
    Impute missing value of protein using the min along each patient.

    :param rawDataObj: ds_InputRawData 
    :type rawDataObj: object
    :param percentage: Remove missing value require less percentage of all patients. (default = 0.1)
    :type percentage: float
    :return: Return ds_InputRawData
    :rtype: object
    """

    print('Before imputation')
    PrintStat(rawDataObj)

    protRatioDf = pd.DataFrame(rawDataObj.GetProtRatioDf())
    # Remove NA first
    protRatioDropNaDf = protRatioDf.dropna(axis=1, thresh=(1-percentage)*protRatioDf.shape[0])
    # Imputation
    impProtRatioDf = protRatioDropNaDf.apply(lambda x: _ImputeMinToSingleColumn(x))

    impDataObj = copy.deepcopy(rawDataObj)
    impDataObj.SetProtRatioDf(protRatioDf=impProtRatioDf)

    print('After imputation')
    impDataObj = GenerateStat(impDataObj)

    return impDataObj


def ImputeAverage(rawDataObj, percentage=0.1):
    """
    Impute missing value of protein using the mean along each patient.

    :param rawDataObj: ds_InputRawData 
    :type rawDataObj: object
    :param percentage: Remove missing value require less percentage of all patients. (default = 0.1)
    :type percentage: float
    :return: ds_InputRawData
    :rtype: object
    """

    print('Before imputation')
    PrintStat(rawDataObj)

    protRatioDf = rawDataObj.GetProtRatioDf()
    # Remove NA first
    protRatioDropNaDf = protRatioDf.dropna(axis=1, thresh=(1 - percentage) * protRatioDf.shape[0])
    # Imputation
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp.fit(protRatioDropNaDf)
    impProtRatioDf = pd.DataFrame(imp.transform(protRatioDropNaDf), index=protRatioDropNaDf.index, columns=protRatioDropNaDf.columns)

    impDataObj = copy.deepcopy(rawDataObj)
    impDataObj.SetProtRatioDf(protRatioDf=impProtRatioDf)

    print('After imputation')
    impDataObj = GenerateStat(impDataObj)

    return impDataObj


def ImputeKnn(rawDataObj, n_neighbors=5, weightStr='uniform', percentage=0.1):
    """
    Impute missing value of protein using KNN.

    :param rawDataObj: ds_InputRawData 
    :type rawDataObj: object
    :param n_neighbors: Number of neighboring samples to use for imputation. (default = 5)
    :type n_neighbors: int
    :param weightStr: Weight function used in prediction. Possible values:
        
        ‘uniform’ : uniform weights. All points in each neighborhood are weighted equally. (default)
        
        ‘distance’ : weight points by the inverse of their euclidean distance.
    
    :type weightStr: str
    :param percentage: Remove missing value require less percentage of all patients. (default = 0.1)
    :type percentage: int
    :return: ds_InputRawData
    :rtype: object
    """

    print('Before imputation')
    PrintStat(rawDataObj)

    protRatioDf = rawDataObj.GetProtRatioDf()
    # Remove NA first
    protRatioDropNaDf = protRatioDf.dropna(axis=1, thresh=(1 - percentage) * protRatioDf.shape[0])
    # Imputation
    imp = KNNImputer(missing_values=np.nan, n_neighbors=n_neighbors, weights=weightStr)
    impProtRatioDf = pd.DataFrame(imp.fit_transform(protRatioDropNaDf), index=protRatioDropNaDf.index, columns=protRatioDropNaDf.columns)

    impDataObj = copy.deepcopy(rawDataObj)
    impDataObj.SetProtRatioDf(protRatioDf=impProtRatioDf)

    print('After imputation')
    impDataObj = GenerateStat(impDataObj)

    return impDataObj


def _ImputeMinToSingleColumn(arr):
    """
    2020/02/11
    Called by ImputeMin()
    :param arr:
    :return:
    """

    min_ = np.nanmin(arr)
    arr.fillna(min_)

    return arr.fillna(min_)
