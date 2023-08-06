from .CommonFunction import *
import scipy.stats as ss


def CalcFeatureEntropy(rawDataObj, protClustObj):
    """
    Calculate the entropy of each feature in metadata and save it in protClustObj.clustScoringObj.featureEntropyDi.\n
    No clustering result is required.

    :param rawDataObj:
    :param protClustObj:
    :return:
    """
    metaDf = rawDataObj.GetMetadataDf().copy()
    featureEntropyDi = {}

    for featureName in metaDf.columns:
        featureEntropyDi[featureName] = _ComputeEntropy(metaDf[featureName])

    protClustObj.clustScoringObj.featureEntropyDi = featureEntropyDi
    return protClustObj


def CalcClustFeatureEntropy(rawDataObj, protClustObj):
    """
    Calculate the feature entropy of each class and save it in protClustObj.clustScoringObj.clustFeatureEntropySer

    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :return: ds_protClust object
    """
    metaDf = rawDataObj.GetMetadataDf()
    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy()

    clustSer = pd.Series()
    for clustIdx in range(1, np.max(predLi) + 1):
        clustDf = metaDf[predLi == clustIdx]
        clustSer.at[clustIdx] = pd.Series()
        for featureName in metaDf.columns:
            clustSer[clustIdx].at[featureName] = _ComputeEntropy(clustDf[featureName])

    protClustObj.clustScoringObj.clustFeatureEntropySer = clustSer
    return protClustObj


def _ComputeEntropy(featureSer):
    """
    compute entropy of a certain feature for a certain cluster

    :param featureSer {pd.Series}: the elements are feature values in a cluster. ex: {'patient name1': 'feature value 1', ...}
    :return: entropy {float}
    """
    countArr = featureSer.value_counts().values
    countArr = countArr / np.sum(countArr)
    return ss.entropy(countArr, base=2)
