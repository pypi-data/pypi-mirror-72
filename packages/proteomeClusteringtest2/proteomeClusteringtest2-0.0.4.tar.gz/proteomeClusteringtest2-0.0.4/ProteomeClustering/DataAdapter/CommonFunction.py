

def GenerateStat(rawDataObj):
    """
    Check and save numerical format of protRatio (Original or Log), patients number, features number, metadata frequency

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object:
    :return: ds_InputRawDataObj
    :rtype: object
    """

    protRatioDf = rawDataObj.GetProtRatioDf()
    metadataDf = rawDataObj.GetMetadataDf()

    # Check numerical format of protein ratio
    if any(protRatioDf < 0):
        # log
        rawDataObj.numericalFormatStr = 'Log'
    else:
        # original
        rawDataObj.numericalFormatStr = 'Original'

    # Save patientNum & featureNum
    rawDataObj.patientNum = protRatioDf.shape[0]
    rawDataObj.featureNum = protRatioDf.shape[1]

    # Save metadata frequency
    metadataDf = metadataDf.applymap(lambda x: x.lower() if type(x) == str else x)
    rawDataObj.metadataFreqDi = dict(metadataDf.apply(lambda x: _CountMetadataFreq(list(x))))

    # Print  metadata frequency
    PrintStat(rawDataObj)

    return rawDataObj


def _CountMetadataFreq(metadataLi):
    """
    Called by GenerateStat()

    :param metadataLi: 
    :type metadataLi: list
    :return:
    """
    metadtaFreq = dict((x, metadataLi.count(x)) for x in metadataLi)
    return metadtaFreq


def PrintStat(rawDataObj):
    """
    Print numerical format of protRatio (Original or Log), patients number, features number, metadata frequency

    :param rawDataObj:
    :type rawDataObj: object
    """

    numericalFormatStr = rawDataObj.numericalFormatStr
    patientNum = rawDataObj.patientNum
    featureNum = rawDataObj.featureNum
    metadataFreqDi = rawDataObj.metadataFreqDi

    print('Numerical format of protein ratio: ' + str(numericalFormatStr))
    print('Patients number: ' + str(patientNum))
    print('Feature number:' + str(featureNum))
    print('Metadata frequency: ' + str(metadataFreqDi) + '\n')