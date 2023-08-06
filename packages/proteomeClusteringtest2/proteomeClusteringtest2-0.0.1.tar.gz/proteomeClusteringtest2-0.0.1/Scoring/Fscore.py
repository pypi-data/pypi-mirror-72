from .CommonFunction import *


def CalcFeatureMaxFscore(rawDataObj, protClustObj):
    """
    傳入inputRawData和protClust及clustering結果，計算各個metadata feauture的Fscore並儲存至ds_protClust object中的featureMaxFscoreDi dictionary

    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :param predLi: clutering result list，大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :return: ds_protClust object
    """
    metaColNameLi = rawDataObj.GetMetadataDf().columns.values
    metaDf = rawDataObj.GetMetadataDf().copy()
    predLi = protClustObj.clustResultObj.sampleClustSer.copy()
    #predLi=list(TurnClustToNumSer(rawDataObj.GetMetadataDf().index.values, protClustObj))
    protClustObj.clustScoringObj.featureMaxFscoreDi = dict()
    for colNameStr in metaColNameLi:
        trueLi = TurnLabelToNum(metaDf[colNameStr])
        predLi = TurnLabelToNum(predLi)
        maxFscore=GetMaxFscore(trueLi, predLi)
        protClustObj.clustScoringObj.featureMaxFscoreDi.update({colNameStr: maxFscore})

    return protClustObj

# 傳入clustering 結果 & class label (both are list)，計算Fscore
# trueLi --> 大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
def GetMaxFscore(trueLi, predLi):

    """
    傳入clustering 結果 & class label (both are list)，計算Fscore

    :param trueLi: feature class list,大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :param predLi: clutering result list，大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :return: float Fscore
    """
    finalMaxFscore=0

    for predNum in range(len(set(predLi))):

        maxFscore=0


        for trueNum in range(len(set(trueLi))):
            recall=_ComputeRecall(trueLi, predLi, trueNum, predNum)
            precision=_ComputePrecision(trueLi, predLi, trueNum, predNum)

            if recall==0 and precision==0:
                localFscore=0
            else:
                localFscore=2*(precision*recall)/( precision+recall)

            if localFscore>=maxFscore :
                maxFscore=localFscore

        truecount = _CountTrueNum(predLi, predNum)
        finalMaxFscore+=(maxFscore * ( truecount/ len(predLi)))

    return finalMaxFscore


def _ComputeRecall(trueLi, predLi, trueNum, predNum):
    """
    compute recall for computing Fscore   TP/(TP+FN)

    :param trueLi: feature class list,大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :param predLi: clutering result list，大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :param trueNum: int, represent current class
    :param predNum: int, represent current cluster
    :return: float recall
    """
    truePositive=0
    falseNagetive=0
    for lens in range(len(trueLi)):
        if predLi[lens]==predNum and trueLi[lens]==trueNum:
            truePositive+=1
        elif trueLi[lens]==trueNum:
            falseNagetive+=1

    return truePositive/(truePositive+falseNagetive)


def _ComputePrecision(trueLi, predLi, trueNum, predNum):
    """
    compute precision for computing Fscore   TP/(TP+FP)

    :param trueLi: feature class list,大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :param predLi: clutering result list，大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :param trueNum: int, represent current class
    :param predNum: int, represent current cluster
    :return: float precision
    """
    truePosive = 0
    falsePositive = 0
    for lens in range(len(trueLi)):
        if predLi[lens] == predNum and trueLi[lens] == trueNum:
            truePosive += 1
        elif predLi[lens] == predNum:
            falsePositive += 1

    return truePosive / (truePosive + falsePositive)


def _CountTrueNum(trueLi, trueNum):
    """
    count the number of current class

    :param trueLi: feature class list,大小與sample數一樣，如 0, 0, 1, 1, 2, 0, 2 數字代表cluster index
    :param trueNum: int, represent current class
    :return: int, the number of current class
    """
    count=0
    for lens in range(len(trueLi)):
        if trueLi[lens]==trueNum:
            count+=1
    return count