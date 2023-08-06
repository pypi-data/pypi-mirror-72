from .CommonFunction import *

import numpy.linalg as LA


def CalcPartitionIndex(rawDataObj, protClustObj):
    """
    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :return: ds_protClust object
    """
    rawDataArr = rawDataObj.GetProtRatioDf().values.copy()
    
    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy()

    clusterNum = len(np.unique(np.array(predLi)))
    centerArr = GetClusterCenter(rawDataArr, predLi, clusterNum)

    utilityArr = GetUtilityMatrix(rawDataArr, centerArr, 'euclidean')

    protClustObj.clustScoringObj.partitionIndex = _Processing(rawDataArr, centerArr, utilityArr, m=2)

    return protClustObj


def _Processing(dataArr, centerArr, utilityArr, m=2):
    """
    Calculate the partition index
    :param: dataArr: np.array. Shape [data_num feature_num]
    :param: centerArr: np.array. Center of the clusters, dimension [cluster_num, feature_num]
    :param: utilityArr: np.array. Utility matrix, shape [cluster_num, data_num]
    :return: flaot partition index
    """
    sampleNum = dataArr.shape[0]  # (data_num, feature_num)
    clusterNum = centerArr.shape[0]  # (cluster_num, feature_num)
    SC = 0

    sampleNumInClus = utilityArr.sum(axis=1).reshape(-1)  # number of samples in each cluster

    for i in range(clusterNum):
        dist2Center = 0
        for j in range(clusterNum):
            dist2Center += LA.norm(centerArr[i] - centerArr[j])

        w = np.power(utilityArr[i], m)

        compact = 0
        for k in range(sampleNum):
            compact += w[k] * LA.norm(dataArr[k] - centerArr[i])

        SC += (compact / (sampleNumInClus[i] * dist2Center))

    return SC
