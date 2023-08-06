from .CommonFunction import *

import numpy.linalg as LA


def CalcSeparationIndex(rawDataObj, protClustObj):
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

    protClustObj.clustScoringObj.separationIndex = _Processing(rawDataArr, centerArr, utilityArr, m=2)

    return protClustObj


def _Processing(dataArr, centerArr, utilityArr, m=2):
    """
    Calculate the separation index
    :param: dataArr: np.array. Shape [data_num feature_num]
    :param: centerArr: np.array. Center of the clusters, dimension [cluster_num, feature_num]
    :param: utilityArr: np.array. Utility matrix, shape [cluster_num, data_num]
    :return: flaot partition index
    """

    sampleNum = dataArr.shape[0]  # (data_num, feature_num)
    clusterNum = centerArr.shape[0]  # (cluster_num, feature_num)

    compact = 0
    dist2Center = []
    for i in range(clusterNum):
        for j in range(i + 1, clusterNum):
            dist2Center.append(LA.norm(centerArr[i] - centerArr[j]))

        w = np.power(utilityArr[i], m)
        comp_clus = 0
        for k in range(sampleNum):
            comp_clus += w[k] * LA.norm(dataArr[k] - centerArr[i])
        compact += comp_clus

    dist2Center = np.array(dist2Center)
    S = (compact / (sampleNum * np.min(dist2Center)))

    return S
