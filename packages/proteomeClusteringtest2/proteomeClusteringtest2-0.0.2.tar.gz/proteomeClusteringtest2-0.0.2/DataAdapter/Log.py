
import math
from .CommonFunction import *

def LogRatioToRatio(rawDataObj):
    """

    :param rawDataObj: ds_InputRawData 
    :type rawDataObj: object
    :return: ds_InputRawData
    :rtype: object
    """

    print('Before changing to original ratio')
    PrintStat(rawDataObj)

    logRatioDf = rawDataObj.GetProtRatioDf()
    ratioDf = logRatioDf.applymap(lambda x: 2 ** x)
    rawDataObj.SetProtRatioDf(ratioDf)
    rawDataObj.numericalFormatStr = 'Original'

    print('After changing to original ratio')
    PrintStat(rawDataObj)

    return rawDataObj


def RatioToLogRatio(rawDataObj):
    """
    
    :param rawDataObj: ds_InputRawData 
    :type rawDataObj: object
    :return: ds_InputRawData
    :rtype: object
    """

    print('Before changing to log ratio')
    PrintStat(rawDataObj)

    ratioDf = rawDataObj.GetProtRatioDf()
    logRatio = ratioDf.applymap(lambda x: math.log2(x))
    rawDataObj.SetProtRatioDf(logRatio)
    rawDataObj.numericalFormatStr = 'Log'

    print('After changing to log ratio')
    PrintStat(rawDataObj)

    return rawDataObj