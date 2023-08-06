from .CommonFunction import *
from scipy.spatial import distance
import DataStructure
import pandas as pd
def SortByRow(rawDataObj):
    """
    use euclidean distance to sort gene name in gene ratio table

    :param rawDataObj: ds_InputRawData, use GetProtRatioDf() and
    :return: rawDataObj
    """
    orderLi = []  # reindex gene name list
    geneNameLi = rawDataObj.GetProtRatioDf().columns.values.copy()
    heatMapRatioDf = rawDataObj.GetProtRatioDf().copy()
    # record euclidean score
    b_first = True
    for name1Str in geneNameLi:
        if b_first:
            orderChoseNameStr = name1Str #the gene that have the least distance with last gene
            orderLi.append(name1Str)
            b_first = False
        eucideanDistSer = pd.Series([100000.0 for i in range(len(geneNameLi))], index=geneNameLi)
        for name2Str in geneNameLi:
            if _IsNameExist(orderLi, name2Str):

                continue
            else:

                eucideanDistSer[name2Str] = distance.euclidean(heatMapRatioDf[orderChoseNameStr], heatMapRatioDf[name2Str])
        if len(orderLi) < len(geneNameLi):
            orderChoseNameStr = _FindLeastScoreName(eucideanDistSer)
            orderLi.append(orderChoseNameStr)

    # stdSer=stdSer.sort_values(ascending=False)
    heatMapRatioDf = heatMapRatioDf.T.reindex(orderLi)

    rawDataObj.SetProtRatioDf(heatMapRatioDf.T)
    return rawDataObj



def _IsNameExist(nameLi, nameStr):
    """
    find out whether the name in the list or not

    :param nameLi: gene/sample name list
    :param nameStr: gene/sample name
    :return: True or False
    """
    for listNameStr in nameLi:
        if nameStr == listNameStr:
            return True
    return False


def _FindLeastScoreName(stdSer):
    """
    find out which gene/sample's score is the least

    :param stdSer:
    :return: gene/sample name
    """
    tempScore = 100000.0
    for nameStr in stdSer.index:
        if stdSer[nameStr] < tempScore:
            tempScore = stdSer[nameStr]
            resultStr = nameStr

    return resultStr



def SortByColumn(rawDataObj):
    """
    use euclidean distance to sort sample name in gene ratio table

    :param rawDataObj: ds_InputRawData  use GetProtRatioDf()
    :type rawDataObj: object
    :return: rawDataObj
    """
    orderLi = []  # reindex gene name list
    geneNameLi = rawDataObj.GetProtRatioDf().T.columns.values.copy()
    heatMapRatioDf = rawDataObj.GetProtRatioDf().T.copy()
    # record euclidean score
    b_first = True
    for name1Str in geneNameLi:
        if b_first:
            orderChoseNameStr = name1Str
            orderLi.append(name1Str)
            b_first = False
        euclideanDistSer = pd.Series([100000.0 for i in range(len(geneNameLi))], index=geneNameLi)
        for name2Str in geneNameLi:
            if _IsNameExist(orderLi, name2Str):

                continue
            else:

                euclideanDistSer[name2Str] = distance.euclidean(heatMapRatioDf[orderChoseNameStr], heatMapRatioDf[name2Str])
        if len(orderLi) < len(geneNameLi):
            orderChoseNameStr = _FindLeastScoreName(euclideanDistSer)
            orderLi.append(orderChoseNameStr)

    heatMapRatioDf = heatMapRatioDf.T.reindex(orderLi)
    rawDataObj.SetProtRatioDf(heatMapRatioDf)
    return rawDataObj