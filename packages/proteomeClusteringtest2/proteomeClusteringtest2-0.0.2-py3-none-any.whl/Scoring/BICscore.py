from .CommonFunction import *
from collections import Counter
from scipy.spatial import distance

def CalcBicScore(rawDataObj, protClustObj):
    """
    Calculate Bayesian information criterion score to estimate cluster number

    :param rawDataObj: ds_inputRawData object
    :type rawDataObj: object
    :param protClustObj: ds_protClust object
    :type protClustObj: object
    :return: ds_protClust object
    :rtype: object
    """

    rawDataArr = rawDataObj.GetProtRatioDf().values.copy()
    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy() # cluster result
    clusterNum = len(np.unique(np.array(predLi))) # cluster number
    centerArr = GetClusterCenter(rawDataArr, predLi, clusterNum) # cluster center
    clusterSizeLi = list(Counter(predLi).values())
    # print(rawDataArr); print(predLi); print(clusterNum); print(centerArr); print(clusterSizeLi);print('\n\n\n')

    protClustObj.clustScoringObj.bicScore = \
        _Processing(rawDataArr=rawDataArr, centerArr=centerArr, predLi=predLi, clusterNum=clusterNum, clusterSizeLi=clusterSizeLi)

    return protClustObj


def _Processing(rawDataArr, centerArr, predLi, clusterNum, clusterSizeLi):
    """
    reference: https://stats.stackexchange.com/questions/90769/using-bic-to-estimate-the-number-of-k-in-kmeans

    :param rawDataArr: Protein ratio. Shape [data_num feature_num]
    :type rawDataArr: np.array
    :param centerArr: Center of the clusters, dimension [cluster_num, feature_num]
    :type centerArr np.array
    :param predLi: sampleClustSer's list [1, 2, 2, 3, 3, 4]
    :type predLi: list
    :param clusterNum: Number of cluster.
    :type clusterNum: int
    :param clusterSizeLi: List of each cluster size.
    :type clusterSizeLi: list
    :return: BIC score
    :rtype: float
    """

    rawDataSize, rawDataDim = rawDataArr.shape

    # compute variance for all clusters beforehand
    cl_var = (1.0 / (rawDataSize - clusterNum) / rawDataDim) * sum([sum(distance.cdist(rawDataArr[np.where(predLi == (i+1))],[centerArr[i]], 'euclidean') ** 2) for i in range(clusterNum)])
    const_term = 0.5 * clusterNum * np.log(rawDataSize) * (rawDataDim + 1)

    BIC = np.sum([clusterSizeLi[i] * np.log(clusterSizeLi[i]) -
                  clusterSizeLi[i] * np.log(rawDataSize) -
                  ((clusterSizeLi[i] * rawDataDim) / 2) * np.log(2 * np.pi * cl_var) -
                  ((clusterSizeLi[i] - 1) * rawDataDim / 2) for i in range(clusterNum)]) - const_term

    return BIC
