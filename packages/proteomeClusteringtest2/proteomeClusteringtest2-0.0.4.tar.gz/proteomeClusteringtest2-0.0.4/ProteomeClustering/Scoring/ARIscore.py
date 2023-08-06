from .CommonFunction import *


from sklearn.metrics import adjusted_rand_score

def CalcFeatureAriScore(rawDataObj, protClustObj):
    """
    傳入inputRawData和protClust、beta及clustering結果，計算各個metadata feauture的ARI並儲存至ds_protClust object中的featureVscoreDi dictionary

    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :return: ds_protClust object
    """

    metaColName = rawDataObj.GetMetadataDf().columns.values
    metaDf = rawDataObj.GetMetadataDf().copy()
    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy()

    protClustObj.clustScoringObj.featureAriDi = dict()
    for colName in metaColName:
        
        trueLi = TurnLabelToNum(metaDf[colName])

        predLi = TurnLabelToNum(predLi)

        protClustObj.clustScoringObj.featureAriDi.update({colName: adjusted_rand_score(trueLi, predLi)})
    return protClustObj
