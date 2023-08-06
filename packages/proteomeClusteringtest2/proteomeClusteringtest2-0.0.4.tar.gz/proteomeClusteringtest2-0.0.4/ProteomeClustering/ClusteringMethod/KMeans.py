from sklearn import cluster, metrics, datasets
from nltk.cluster import KMeansClusterer, euclidean_distance
from .CommonFunction import *
import numpy as np


def KmeansClust_sklearn(rawDataObj, protClustObj):
    """
    K means clustering 

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object 
    :param protClustObj: ds_ProtClust
    :type protClustObj: object
    :returns: predArr 

    .. note::
        The parameter in protClustObj.clustParamObj.__kwargs must include 'clustNum', 'seed' \n
        distance measure only euclidean distance
    """
    k = protClustObj.clustParamObj.GetParam('clustNum')
    seed = protClustObj.clustParamObj.GetParam('seed')
    dataArr = rawDataObj.GetProtRatioDf().values

    kmeans_fit = cluster.KMeans(n_clusters=k, random_state=seed).fit(dataArr)
    predArr = kmeans_fit.labels_

    return predArr


def KmeansClust_nltk(rawDataObj, protClustObj):
    """
    Nltk K means clustering 

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object 
    :param protClustObj: ds_ProtClust
    :type protClustObj: object
    :returns:   predArr 

    .. note::
        The parameter in protClustObj.clustParamObj.__kwargs must include 'clustNum', 'distance'\n
        accepted distance : 'euclidean', 'manhattan', 'cosine', 'pcc';
    """
    k = protClustObj.clustParamObj.GetParam('clustNum')
    dist = protClustObj.clustParamObj.GetParam('kmeansDisatance')
    distance = GetDistance(dist)
    dataArr = rawDataObj.GetProtRatioDf().values

    clusterer = KMeansClusterer(num_means=k, distance=distance, repeats=1)
    predArr = np.array(clusterer.cluster(dataArr, True))

    return predArr
