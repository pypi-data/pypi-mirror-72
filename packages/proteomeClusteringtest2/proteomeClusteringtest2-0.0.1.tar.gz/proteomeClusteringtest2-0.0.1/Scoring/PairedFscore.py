from .CommonFunction import *

from scipy.special import comb

def CalcFeaturePairedFscore(rawDataObj, protClustObj):
    """
    Calculate the PairedFscore for each label and the clustering results

    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :return: ds_protClust object
    """

    metaColName = rawDataObj.GetMetadataDf().columns.values.copy()
    metaDf = rawDataObj.GetMetadataDf().copy()
    predLi = protClustObj.clustResultObj.sampleClustSer.values.copy()

    protClustObj.clustScoringObj.featurePairedFscoreDi = dict()
    for colName in metaColName:
        trueLi = TurnLabelToNum(metaDf[colName])
        predLi = TurnLabelToNum(predLi)

        protClustObj.clustScoringObj.featurePairedFscoreDi.update({colName: _GetSinglePairedFscore(trueLi, predLi)})
    return protClustObj


def _GetTnTpFnFp(trueLi, predLi):
    """
    Calculate the TP, TN, FP, FN pairs

    :param trueLi: feature class list,大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :param predLi: clutering result list，大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :return: dict {'TP', 'FP', 'FN', 'FN'}
    """
    clustersArr = np.array(predLi)
    classesArr = np.array(trueLi)
    tp_plus_fp = comb(np.bincount(clustersArr), 2).sum()
    tp_plus_fn = comb(np.bincount(classesArr), 2).sum()
    A = np.c_[(clustersArr, classesArr)]
    tp = sum(comb(np.bincount(A[A[:, 0] == i, 1]), 2).sum()
             for i in set(clustersArr))
    fp = tp_plus_fp - tp
    fn = tp_plus_fn - tp
    tn = comb(len(A), 2) - tp - fp - fn
    return {'TP':tp,'FP':fp,'FN':fn,'TN':tn}

def _GetSinglePairedFscore(trueLi, predLi):
    """
    Calculate paried Fscore

    :param trueLi: feature class list,大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :param predLi: clutering result list，大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :return: float paired F score
    """
    pairNumDi = _GetTnTpFnFp(trueLi, predLi)
    return 2*pairNumDi['TP'] / (2*pairNumDi['TP'] + pairNumDi['FP'] + pairNumDi['FN'])


