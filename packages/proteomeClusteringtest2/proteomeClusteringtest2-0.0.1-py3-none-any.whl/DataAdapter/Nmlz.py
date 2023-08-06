

import pandas as pd
from sklearn import preprocessing
from .CommonFunction import PrintStat


def ZscoreNmlz(rawDataObj):
    """
    Z-score normalization for each patient (SD for all the proteins to 1 & mean to 0).
    
    Should perform this step for log ratio.

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object
    :return: ds_InputRawData
    :rtype: object
    """

    print('Before normalization')
    PrintStat(rawDataObj)

    protRatioDf = rawDataObj.GetProtRatioDf()
    protRatioNmlzDf = pd.DataFrame(preprocessing.scale(protRatioDf, axis=1), index=protRatioDf.index,
                                   columns=protRatioDf.columns)
    rawDataObj.SetProtRatioDf(protRatioNmlzDf)

    print('After normalization')
    PrintStat(rawDataObj)

    return rawDataObj