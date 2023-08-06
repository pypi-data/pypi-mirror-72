import pandas as pd
import copy
from .CommonFunction import GenerateStat, PrintStat

def RemoveProtWithNa(rawDataObj):
    """
    Removed rows (features) which contain missing data

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object
    :return: protRatioDropNaDf
    :rtype: pd.DataFrame
    """

    print('Before removing NA')
    PrintStat(rawDataObj)

    protRatioDf = rawDataObj.GetProtRatioDf()

    protRatioDropNaDf = protRatioDf.dropna(axis=1)

    dropNaDataObj = copy.deepcopy(rawDataObj)
    dropNaDataObj.SetProtRatioDf(protRatioDf=protRatioDropNaDf)

    print('After removing NA')
    impDataObj = GenerateStat(dropNaDataObj)

    return dropNaDataObj


def AssignNaStrToNotAvailableCell(metadataDf):
    """
    Assign missing value of metadataDf to 'NA'
    
    Called by ReadFilesPath()

    :param metadataDf: 
    :type metadataDf: pd.DataFrame
    :return: newMetadataDf
    :rtype: pd.DataFrame
    """
    newMetadataDf = metadataDf.fillna('NA')
    return newMetadataDf


def RemoveContinuousFeature(metadataDf, metadataCategoryDf=pd.DataFrame()):
    """
    Drop continuous features (columns) of metadataDf that depends on metadataCategoryDf or check whether its label count is over half of length.
    
    Called by ReadFilesPath()

    :param metadataDf: 
    :type metadataDf: pd.DataFrame
    :param metadataCategoryDf: Consist of whether each feature is categorical.
    :return: newMetadataDf
    :rtype: pd.DataFrame
    """

    if not metadataCategoryDf.empty:
        '''Depends on metadataCategoryDf'''
        CategoricalColumnLi = metadataCategoryDf.transpose().index[(metadataCategoryDf.transpose().iloc[:, 0] == 1)]
        newMetadataDf = metadataDf[CategoricalColumnLi]
    else:
        '''check whether its label count is over half of length'''
        columnLength = len(metadataDf)
        CategoricalColumnLi = []
        for x in metadataDf.columns:
            if len(metadataDf[x].unique()) < columnLength / 3:
                CategoricalColumnLi.append(x)
        newMetadataDf = metadataDf[CategoricalColumnLi]

    print('Categorical features:')
    print(CategoricalColumnLi)

    return newMetadataDf
