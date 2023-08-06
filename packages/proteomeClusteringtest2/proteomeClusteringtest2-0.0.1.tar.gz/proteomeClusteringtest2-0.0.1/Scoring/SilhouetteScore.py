from .CommonFunction import *

from sklearn.metrics import silhouette_score, silhouette_samples


def CalcSilhScore(rawDataObj, protClustObj):
    """
    Calculate the silhouette score and save it in protClustObj.clustScoringObj.silhScore

    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :return: ds_protClust object
    """
    rawDataArr = rawDataObj.GetProtRatioDf().values.copy()
    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy()
    protClustObj.clustScoringObj.silhScore = silhouette_score(rawDataArr, predLi, sample_size=96)

    return protClustObj


def CalcSampleSilhScore(rawDataObj, protClustObj):
    """
    Calculate the silhouette score for each sample

    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :return:
    """

    protRatioArr = rawDataObj.GetProtRatioDf().values.copy()
    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy()

    samSilhArr = silhouette_samples(protRatioArr, predLi)
    samSilhSer = pd.Series(samSilhArr, index=rawDataObj.GetMetadataDf().index)
    protClustObj.clustScoringObj.sampleSilhScoreSer = samSilhSer

    return protClustObj


def CalcClustSilhScore(rawDataObj, protClustObj):
    """
    Calculate the silhouette score for each cluster, which is the average for the samples in the cluster

    :param rawDataObj:
    :param protClustObj:
    :return:
    """
    protRatioArr = rawDataObj.GetProtRatioDf().values.copy()
    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy()
    samSilhArr = silhouette_samples(protRatioArr, predLi)

    clustSilhSer = pd.Series()
    for clustIdx in range(1, np.max(predLi) + 1):
        clustSilhSer.at[clustIdx] = np.mean(samSilhArr[predLi == clustIdx])
    protClustObj.clustScoringObj.clustSilhScoreSer = clustSilhSer
    return protClustObj