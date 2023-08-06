from .CommonFunction import *


def CalcGiniScore(rawDataObj, protClustObj):
    """
    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :return: ds_protClust object
    """

    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy()

    counts = np.unique(predLi, return_counts=True)[1]
    gini = 0
    for i in range(len(counts)):
        for j in range(len(counts)):
            gini += np.abs(counts[i] - counts[j])
    gini /= (2 * len(counts))
    gini /= np.sum(counts)

    protClustObj.clustScoringObj.giniScore = gini

    return protClustObj

