from .CommonFunction import *


def CalcFeatureRatio(rawDataObj, protClustObj):
    """
    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :return: ds_protClust object
    """
    metaDf = rawDataObj.GetMetadataDf().copy()
    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy()

    bgRatioSer = pd.Series()  # feature -> featureValue -> featureValueRatio
    for featureName in metaDf.columns:
        bgRatioSer[featureName] = (metaDf[featureName].value_counts() / metaDf.shape[0])

    clustDi = {}

    for clusIdx in range(1, np.max(predLi) + 1):
        boolMask = (predLi == clusIdx)
        clustDi[clusIdx] = {}
        for featureName in metaDf.columns:
            featValueRatioSer = metaDf[featureName][boolMask].value_counts() / metaDf[boolMask].shape[0]
            # index: feature value, data: ratio in the cluster
            for featureValue in bgRatioSer[featureName].index:
                try:
                    featValueRatioSer[featureValue] = featValueRatioSer[featureValue] / bgRatioSer[featureName][
                        featureValue]
                except:
                    featValueRatioSer.at[featureValue] = 0
            clustDi[clusIdx][featureName] = featValueRatioSer
        clustDi[clusIdx] = pd.Series(clustDi[clusIdx])

    clustSer = pd.Series(clustDi)

    protClustObj.clustScoringObj.clustFeatureValueRatioSer = clustSer

    return protClustObj
