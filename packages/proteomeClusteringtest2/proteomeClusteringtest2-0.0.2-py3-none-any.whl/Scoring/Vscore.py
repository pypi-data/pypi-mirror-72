
import numpy as np
import pandas as pd
from .CommonFunction import *
from sklearn.metrics.cluster import v_measure_score






def CalcFeatureVscore(rawDataObj, protClustObj, beta=1.0):
    """
    傳入inputRawData和protClust、beta及clustering結果，計算各個metadata feauture的Vscore並儲存至ds_protClust object中的featureVscoreDi dictionary

    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :param predLi: clutering result list，大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :param beta: weights of the harmonic mean of homogeneity and completeness, default=1
    :return: ds_protClust object
    """

    metaColNameLi = rawDataObj.GetMetadataDf().columns.values
    metaDf = rawDataObj.GetMetadataDf().copy()
    predLi = protClustObj.clustResultObj.sampleClustSer.copy()
    #predLi=list(TurnClustToNumSer(rawDataObj.GetMetadataDf().index.values, protClustObj))
    protClustObj.clustScoringObj.featureVscoreDi = dict()
    for colNameStr in metaColNameLi:


        trueLi = TurnLabelToNum(metaDf[colNameStr])
        predLi = TurnLabelToNum(predLi)

        protClustObj.clustScoringObj.featureVscoreDi.update({colNameStr: v_measure_score(trueLi, predLi, beta)})




    return protClustObj
