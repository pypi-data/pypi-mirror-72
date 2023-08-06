import numpy as np
import pandas as pd
from sklearn import cluster, metrics, datasets
from .KMeans import *
from .Hierarchical import *
from .Consensus import *
from .GuassianModel import GaussianEMClust
from .SelfOrganizingMap import SelfOrganizingMapClust
from pylab import *

def Clustering(rawDataObj, protClustObj):
    """
    Top level of clustering to perform different cluster method including:\n
    KmeansClust_sklearn,  KmeansClust_nltk,  HierarchicalClust,
    ConsensusClust  ( KmeansClust_sklearn ),  ConsensusClust ( KmeansClust_nltk ),  ConsensusClust ( HierarchicalClust ),  ConsensusClust ( HierarchicalClust_Scipy ),
    GaussianEMClust,  SelfOrganizingMapClust

    :param rawDataObj:    use protein ratio dataframe to perform clustering
    :type rawDataObj: object
    :param protClustObj:  use cluster parameter saved in protClustObj.clustParamObj to perform clustering
    :type protClustObj: object
    :return protClustObj: protClustObj with saving utilityMatrixDf, clustSampleSer, sampleClustSer
    
    .. note::
        utilityMatrixDf : pandas dataframe (row is sample, column is cluster number, value is 1 if sample belongs cluster otherwise 0) \n
        clustSampleSer  : 2D pandas Series (1D is cluster number, 2D is sample) [[p1,p3,p4], [p2], [p5]] \n
        sampleClustSer  : pandas Series (size is sample amount; values are cluster ID) [1,2,1,2,2,3,2,1]
    
    """
    dataDf = rawDataObj.GetProtRatioDf()
    patientLi = list(dataDf.index)
    dataArr = dataDf.values
    methodStr = protClustObj.clustParamObj.GetParam('method')

    clusterResultLi = None
    CCCDF = None

    print('available parameter : {}'.format(list(protClustObj.clustParamObj.GetParamLi())))
    if methodStr == 'kmeansClust_sklearn':
        print('KmeansClust_sklearn starting ...')

        clusterResultLi = KmeansClust_sklearn(rawDataObj, protClustObj)
        print('KmeansClust_sklearn result :\n{}'.format(clusterResultLi))

    elif methodStr == 'kmeansClust_nltk':
        print('KmeansClust_nltk starting ...')

        clusterResultLi = KmeansClust_nltk(rawDataObj, protClustObj)
        print('KmeansClust_nltk result :\n{}'.format(clusterResultLi))

    elif methodStr == 'hierarchicalClust':
        print('HierarchicalClust starting ...')

        clusterResultLi = HierarchicalClust(rawDataObj, protClustObj)
        print('HierarchicalClust result :\n{}'.format(clusterResultLi))

    elif methodStr == 'hierarchicalClust_scipy':
        print('hierarchicalClust_scipy starting ...')

        clusterResultLi = HierarchicalClust_Scipy(rawDataObj,protClustObj)
        print('hierarchicalClust_scipy result :\n{}'.format(clusterResultLi))
        
    elif methodStr == 'consensusClust':
        print('ConsensusClust starting ...')

        ccMethodStr = protClustObj.clustParamObj.GetParam('ccMethod')
        rp = protClustObj.clustParamObj.GetParam('resample')
        minK = protClustObj.clustParamObj.GetParam('minK')
        maxK = protClustObj.clustParamObj.GetParam('maxK')
        resample_times = protClustObj.clustParamObj.GetParam('resample_times')
        if ccMethodStr == 'kmeansClust_sklearn':
            CC = ConsensusClust(cluster=cluster.KMeans, minK=minK, maxK=maxK, resample_times=resample_times,
                                resample_proportion=rp).fit(dataArr=dataArr)
            CC_predict = CC.Predict()
            print('ConsensusClust (KmeansClust_sklearn) result :\n{}'.format(CC_predict))

        elif ccMethodStr == 'kmeansClust_nltk':
            distance = protClustObj.clustParamObj.GetParam('ccDistance')
            CC = ConsensusClust(cluster=KMeansClusterer, minK=minK, maxK=maxK, resample_times=resample_times,
                                resample_proportion=rp, distance=distance).fit(dataArr=np.array(dataArr))
            CC_predict = CC.Predict()
            print('ConsensusClust (KmeansClust_nltk) result :\n{}'.format(CC_predict))

        elif ccMethodStr == 'hierarchicalClust':
            linkage = protClustObj.clustParamObj.GetParam('ccLinkage')
            distance = protClustObj.clustParamObj.GetParam('ccDistance')
            finallinkage = protClustObj.clustParamObj.GetParam('ccFinalLinkage') if protClustObj.clustParamObj.GetParam('ccFinalLinkage') else 'ward'
            finaldistance = protClustObj.clustParamObj.GetParam('ccFinalDistance') if protClustObj.clustParamObj.GetParam('ccFinalDistance') else 'euclidean'
            CC = ConsensusClust(cluster=AgglomerativeClustering, minK=minK, maxK=maxK, resample_times=resample_times,
                                resample_proportion=rp,
                                linkage=linkage,distance=distance,finallinkage=finallinkage,finaldistance=finaldistance).fit(dataArr=np.array(dataArr))
            CC_predict = CC.Predict()
            print('ConsensusClust (HierarchicalClust) result :\n{}'.format(CC_predict))

        elif ccMethodStr == 'hierarchicalClust_scipy':
            linkage = protClustObj.clustParamObj.GetParam('ccLinkage')
            distance = protClustObj.clustParamObj.GetParam('ccDistance')
            finallinkage = protClustObj.clustParamObj.GetParam('ccFinalLinkage') if protClustObj.clustParamObj.GetParam('ccFinalLinkage') else 'ward'
            finaldistance = protClustObj.clustParamObj.GetParam('ccFinalDistance') if protClustObj.clustParamObj.GetParam('ccFinalDistance') else 'euclidean'
            CC = ConsensusClust(cluster=sc.hierarchy.cut_tree, minK=minK, maxK=maxK, resample_times=resample_times,
                                resample_proportion=rp,
                                linkage=linkage, distance=distance, finallinkage=finallinkage, finaldistance=finaldistance).fit(dataArr=np.array(dataArr))
            CC_predict = CC.Predict()
            print('ConsensusClust (hierarchicalClust_scipy) result :\n{}'.format(CC_predict))

        else:
            CC_predict = None
            print('please provide available Clustering algorithm for ConsensusClust')  
        # X  = np.arange(len(CC.CDF[0]))
        # for i in CC.CDF:
        #     plot(CC.CDF[i])
        # show()
        CCCDF = CC.CDF
        clusterResultLi = CC_predict

    elif methodStr == 'gaussianEMClust':
        print('GaussianEMClust starting ...')

        clusterResultLi = GaussianEMClust(rawDataObj, protClustObj)
        print('GaussianMixture Clustering result :\n{}'.format(clusterResultLi))

    elif methodStr == 'selfOrganizingMapClust':
        print('SelfOrganizingMapClust starting')

        clusterResultLi = SelfOrganizingMapClust(rawDataObj, protClustObj)
        print('SelfOrganizingMapClust result :\n{}'.format(clusterResultLi))

    else:
        print('please provide available Clustering algorithm')
    clusterResultLi = [clust + 1 for clust in clusterResultLi]
    protClustObj.clustResultObj.utilityMatrixDf = _GetUtilityMatrixDf(clusterResultLi, patientLi)
    protClustObj.clustResultObj.clustSampleSer = _GetClustSampleSer(clusterResultLi, patientLi)
    protClustObj.clustResultObj.sampleClustSer = pd.Series(clusterResultLi, patientLi)
    protClustObj.clustResultObj.clustNum = max(clusterResultLi)
    protClustObj.clustResultObj.cdfLi = CCCDF
    return protClustObj

def ReadClustSeries(clusterResultLi,rawDataObj, protClustObj):
    """
    Saving a clustered result into data structure without performing clustering method

    :param clusterResultLi: the clustered result
    :type clusterResultLi: list
    :param rawDataObj: data structure to be saved
    :type rawDataObj: object
    :param protClustObj: data structure to be saved
    :type protClustObj: object

    """
    print(clusterResultLi)
    clusterResultLi = [clust + 1 for clust in clusterResultLi]
    dataDf = rawDataObj.GetProtRatioDf()
    patientLi = list(dataDf.index)
    protClustObj.clustResultObj.utilityMatrixDf = _GetUtilityMatrixDf(clusterResultLi, patientLi)
    protClustObj.clustResultObj.clustSampleSer = _GetClustSampleSer(clusterResultLi, patientLi)
    protClustObj.clustResultObj.sampleClustSer = pd.Series(clusterResultLi, patientLi)
    protClustObj.clustResultObj.clustNum = max(clusterResultLi)
    return protClustObj

def _GetUtilityMatrixDf(clusterResultLi, patientLi):
    """
    produce Utility Matrix Dataframe

    :param clusterResultLi: 
    :type clusterResultLi: list
    :param patientLi:
    :type patientLi: list
    :returns:  resultDf (pd.DataFrame())

    """
    resultDf = pd.DataFrame()
    clustNum = len(set(clusterResultLi))
    resultDf['sample'] = patientLi
    for i in range(1, clustNum + 1):
        clust = []
        for j in clusterResultLi:
            clust.append(1) if i == j else clust.append(0)
        resultDf['cluster' + str(i)] = clust
    resultDf = resultDf.set_index('sample')
    return resultDf


def _GetClustSampleSer(clusterResultLi, patientLi):
    """
    produce Cluster Sample Series
    :param clusterResultLi: 
    :type clusterResultLi: list
    :param patientLi:
    :type patientLi: list
    :returns: resultDf (pd.Series())
    """
    clustNum = len(set(clusterResultLi))
    index = [i for i in range(1, clustNum + 1)]
    data = [[] for i in range(clustNum)]
    for i in range(len(clusterResultLi)):
        data[clusterResultLi[i] - 1].append(patientLi[i])
    resultSer = pd.Series(data, index)
    return resultSer
