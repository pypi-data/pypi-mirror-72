from sklearn.mixture import GaussianMixture


def GaussianEMClust(rawDataObj, protClustObj):
    """

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object 
    :param protClustObj: ds_ProtClust
    :type protClustObj: object
    :returns: predArr 

    .. note::
        The parameter in protClustObj.clustParamObj.__kwargs must include 'clustNum', 'covType'
    """
    clustNum = protClustObj.clustParamObj.GetParam('clustNum')
    covType = protClustObj.clustParamObj.GetParam('covType')
    dataArr = rawDataObj.GetProtRatioDf().values

    gaussianClusterer = GaussianMixture(n_components=clustNum, covariance_type=covType)
    predArr = gaussianClusterer.fit_predict(X=dataArr)

    return predArr
