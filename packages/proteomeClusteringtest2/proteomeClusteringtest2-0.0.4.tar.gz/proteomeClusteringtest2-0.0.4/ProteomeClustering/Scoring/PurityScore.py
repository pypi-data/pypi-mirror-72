from .CommonFunction import *


def CalcPurityScore(rawDataObj, protClustObj):
    """
    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :return: ds_protClust object
    """
    metaDf = rawDataObj.GetMetadataDf().copy()
    predLi = np.array(protClustObj.clustResultObj.sampleClustSer).copy()
    purity = 0
    for clusIdx in range(1, np.max(predLi) + 1):
        boolMask = (predLi == clusIdx)
        maxClusterPurity = 0

        for featureName in metaDf.columns:
            clusterPurity = _ChooseLargestFeature(metaDf[featureName][boolMask].value_counts())
            if clusterPurity > maxClusterPurity:
                maxClusterPurity = clusterPurity
        purity += maxClusterPurity

    purity /= metaDf.shape[0]
    protClustObj.clustScoringObj.purity = purity

    return protClustObj


def _ChooseLargestFeature(featureSer):
    tempNum = 0
    result = 0
    featureSer = featureSer.rename(index=str)
    for name in featureSer.index.values:
        if float(featureSer[name]) > tempNum:
            tempNum = float(featureSer[name])
            result = float(featureSer[name])
    return result