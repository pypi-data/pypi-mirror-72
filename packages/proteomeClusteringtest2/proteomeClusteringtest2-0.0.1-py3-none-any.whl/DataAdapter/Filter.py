import numpy as np
import pandas as pd
import copy
from .CommonFunction import GenerateStat, PrintStat


def FilterByRank(rawDataObj, topNum, methodStr='SD'):
    """
    Select topNum number of features.

    :param rawDataObj: ds_InputRawData 
    :type rawDataObj: object
    :param methodStr: 'SD' or 'MAD'
    :type methodStr: str
    :param topNum: Select topNum feature
    :type topNum: int
    :return: Return **ds_InputRawData** object without changing raw object
    :rtype: object
    """

    print('Before filtering:')
    PrintStat(rawDataObj)

    proteinRatioDf = rawDataObj.GetProtRatioDf()
    filterMethodSer = 'FilterByRank_'

    if methodStr == 'SD':
        filterMethodSer = filterMethodSer + 'SD_' + str(topNum)
        proteinRatioSD = np.std(proteinRatioDf, axis=0)
        filteredProtRatioDf = proteinRatioDf[proteinRatioSD.sort_values(ascending=False).head(topNum).index]
    elif methodStr == 'MAD':
        filterMethodSer = filterMethodSer + 'MAD_' + str(topNum)
        proteinRatioMAD = proteinRatioDf.apply(lambda x: x.mad())
        filteredProtRatioDf = proteinRatioDf[proteinRatioMAD.sort_values(ascending=False).head(topNum).index]
    else:
        print('Error: method is either \'SD\' or \'MAD\'.')
        filterMethodSer = ''
        filteredProtRatioDf = pd.DataFrame()

    ds_FilterDataObj = copy.deepcopy(rawDataObj)
    ds_FilterDataObj.SetProtRatioDf(protRatioDf=filteredProtRatioDf)
    ds_FilterDataObj.filterMethodStr = filterMethodSer

    print('After filtering')
    ds_FilterDataObj = GenerateStat(ds_FilterDataObj)
    print('Filter method: ' + filterMethodSer + '\n')

    return ds_FilterDataObj


def FilterByCutoff(rawDataObj, cutOff, methodStr='SD'):
    """
    Select features that SD or MAD are higher than **cutOff**.

    :param rawDataObj: ds_InputRawData 
    :type rawDataObj: object
    :param methodStr: 'SD' or 'MAD'
    :type methodStr: str
    :param cutOff: Select feature that SD or MAD are higher than this.
    :type cutOff: int
    :return: Return **ds_InputRawData** object without changing raw object
    :rtype: object
    """

    print('Before filtering:')
    PrintStat(rawDataObj)

    proteinRatioDf = rawDataObj.GetProtRatioDf()
    filterMethodStr = 'FilterByCutoff_'

    if methodStr == 'SD':
        filterMethodStr = filterMethodStr + 'SD_' + str(cutOff)
        proteinRatioSD = np.std(proteinRatioDf, axis=0)
        filteredProtRatioDf = proteinRatioDf[proteinRatioSD[proteinRatioSD > cutOff].index]
    elif methodStr == 'MAD':
        filterMethodStr = filterMethodStr + 'MAD_' + str(cutOff)
        proteinRatioMAD = proteinRatioDf.apply(lambda x: x.mad())
        filteredProtRatioDf = proteinRatioDf[proteinRatioMAD[proteinRatioMAD > cutOff].index]
    else:
        print('Error: method is either \'SD\' or \'MAD\'.')
        filterMethodStr = ''
        filteredProtRatioDf = pd.DataFrame()

    ds_FilterDataObj = copy.deepcopy(rawDataObj)
    ds_FilterDataObj.SetProtRatioDf(protRatioDf=filteredProtRatioDf)
    ds_FilterDataObj.filterMethodStr = filterMethodStr

    print('After filtering:')
    ds_FilterDataObj = GenerateStat(ds_FilterDataObj)
    print('Filter method: ' + filterMethodStr + '\n')

    return ds_FilterDataObj


def FilterByTopPercentage(rawDataObj, topPercentage, methodStr='SD'):
    """
    Select topPercentage(float) of features.

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object
    :param methodStr:  'SD' or 'MAD'
    :type methodStr: str
    :param topPercentage:  0 <= topPercentage <= 1
    :type topPercentage: float
    :return: Return **ds_InputRawData** object without changing raw object
    :rtype: object
    """

    print('Before filtering:')
    PrintStat(rawDataObj)

    proteinRatioDf = rawDataObj.GetProtRatioDf()
    filterMethodStr = 'FilterByTopPercentage_'
    topNum = int(topPercentage * proteinRatioDf.shape[1])

    if methodStr == 'SD':
        filterMethodStr = filterMethodStr + 'SD_' + str(topPercentage)
        proteinRatioSD = np.std(proteinRatioDf, axis=0)
        filteredProtRatioDf = proteinRatioDf[proteinRatioSD.sort_values(ascending=False).head(topNum).index]
    elif methodStr == 'MAD':
        filterMethodStr = filterMethodStr + 'MAD_' + str(topPercentage)
        proteinRatioMAD = proteinRatioDf.apply(lambda x: x.mad())
        filteredProtRatioDf = proteinRatioDf[proteinRatioMAD.sort_values(ascending=False).head(topNum).index]
    else:
        print('Error: method is either \'SD\' or \'MAD\'.')
        filterMethodStr = ''
        filteredProtRatioDf = pd.DataFrame()

    ds_FilterDataObj = copy.deepcopy(rawDataObj)
    ds_FilterDataObj.SetProtRatioDf(protRatioDf=filteredProtRatioDf)
    ds_FilterDataObj.filterMethodStr = filterMethodStr

    print('After filtering:')
    ds_FilterDataObj = GenerateStat(ds_FilterDataObj)
    print('Filter method: ' + filterMethodStr + '\n')

    return ds_FilterDataObj


def FilterByGeneList(rawDataObj, geneLi):
    """
    Select features in geneList.

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object
    :param geneLi: A list of gene name.
    :type geneLi: list
    :return: Return **ds_InputRawData** object without changing raw object
    :rtype: object
    """

    print('Before filtering:')
    PrintStat(rawDataObj)

    proteinRatioDf = rawDataObj.GetProtRatioDf()
    filterMethodStr = 'FilterByGeneList'

    if geneLi == '' or geneLi == np.nan:
       print('Error.\nGeneList cannot be null.\n')
       return 0

    elif all([gene in list(proteinRatioDf.columns) for gene in geneLi]) and geneLi != '':
        filteredProtRatioDf = proteinRatioDf[geneLi]

    else:
        print('Error.\nGene in geneList must be involved in protein ratio.\n')
        return 0

    ds_FilterDataObj = copy.deepcopy(rawDataObj)
    ds_FilterDataObj.SetProtRatioDf(protRatioDf=filteredProtRatioDf)
    ds_FilterDataObj.filterMethodStr = filterMethodStr

    print('After filtering:')
    ds_FilterDataObj = GenerateStat(ds_FilterDataObj)
    print('Filter method: ' + filterMethodStr + '\n')

    return ds_FilterDataObj