import numpy as np
import matplotlib.pyplot as plt


def SelfOrganizingMapClust(rawDataObj, protClustObj):
    """

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object 
    :param protClustObj: ds_ProtClust
    :type protClustObj: object
    :returns: predLi

    .. note::
        The parameters in protClustObj.clustParamObj.__kwargs must include 'dimension', 'learnRate', 'sigma', 'epochNum'\n
        Optional parameter: 'plotError'\n
        'dimension' can be a tuple for 2D maps, or an integer for 1-D maps.\n
        If 'plotError (bool)' is in the parameter list, the error history will be plotted.
    """
    dim = protClustObj.clustParamObj.GetParam('dimension')
    alpha = protClustObj.clustParamObj.GetParam('learnRate')
    sigma = protClustObj.clustParamObj.GetParam('sigma')
    epochNum = protClustObj.clustParamObj.GetParam('epochNum')

    rawDataArr = rawDataObj.GetProtRatioDf().values
    if isinstance(dim, int):
        som = SOM1D(dim)
    else:
        som = SOM2D(*dim)

    som.InitializeParams(rawDataArr)
    som.Fit(rawDataArr, alpha, sigma, epochNum)
    predLi = som.GetClustLabels(rawDataArr)
    errorHistory = som.GetErrorHistory()


    print('Error History')
    print(errorHistory)

    try:
        if protClustObj.clustParamObj.GetParam('plotError') == True:
            try:
                PlotErrorHistory(errorHistory, filename=protClustObj.clustParamObj.GetParam('filename'))
            except:
                PlotErrorHistory(errorHistory)
    except:
        pass

    return predLi


def PlotErrorHistory(errorLi, filename='SOM Error History.png'):
    """
    Plot the Error History

    :param errorLi:
    :type errorLi: list
    :return: None
    """
    plt.plot(errorLi)
    plt.xlabel('Epoch')
    plt.ylabel('Error')
    plt.title('SOM Error History')
    plt.savefig(filename)


class SOM2D(object):
    def __init__(self, xdim, ydim):
        self.__xdim = xdim  # number of nodes in x-dimension
        self.__ydim = ydim  # number of noder in y-dimension

        self.__nodeArr = np.array([])  # not initialized
        self.__alphaStart = 0
        self.__sigmaStart = 0
        self.__epochNum = 0
        self.__errorHistory = []
        self.__interval = 0  # interval of epochs to save the error history

    def InitializeParams(self, rawDataArr):
        """
        Initialize the nodes in self.__map with normal distribution

        :param rawDataArr: shape = (sampleNum, featureNum)
        :type rawDataArr: np.array
        """
        self.__nodeArr = np.random.normal(np.mean(rawDataArr), np.std(rawDataArr),
                                          size=(self.__xdim, self.__ydim, rawDataArr.shape[1]))

    def Fit(self, rawDataArr, alpha, sigma, epochNum, interval=1000):
        """
        Train the SOM on the given data for several iterations

        :param rawDataArr:  data to train on
        :type rawDataArr: np.array
        :param epochNum: number of iterations to train; if 0, epochs=len(data) and every data point is used once
        :type epochNum: int
        :param interval: interval of epochs to use for saving training errors
        :type interval: int
        """
        self.__interval = interval
        self.__alphaStart = alpha
        self.__sigmaStart = sigma
        self.__epochNum = epochNum

        for epoch in range(self.__epochNum):
            self.__TrainPerEpoch(rawDataArr, epoch)

    def GetClustLabels(self, rawDataArr):
        """
        Treat each unit in the nodeArr as a cluster. The best match unit is the cluster label for each data sample.
        The cluster index will be adjusted since some units are never used.

        :param rawDataArr:
        :type rawDataArr: np.array
        :return: clustLabels
        """
        clustLabels = []

        for dataSample in rawDataArr:
            x, y = self.__FindBestMatch(dataSample)
            clustLabels.append(x * self.__xdim + y)

        usedLabels = np.unique(clustLabels)
        transform = {usedLabels[i]: i for i in range(len(usedLabels))}
        clustLabels = [transform[clustLabels[i]] for i in range(len(clustLabels))]

        return np.array(clustLabels)

    def GetErrorHistory(self):
        return self.__errorHistory

    def __TrainPerEpoch(self, rawDataArr, currentEpoch):
        '''
        Update the SOM for one epoch. The training parameters are updated once in an epoch.

        :param rawDataArr: 
        :type rawDataArr: np.array
        :param currentEpoch: 
        :type currentEpoch: int
        '''
        alpha = self.__alphaStart / (1 + (currentEpoch / 0.5) ** 4)
        sigma = self.__sigmaStart / (1 + (currentEpoch / 0.5) ** 4)

        idxArr = np.random.choice(np.arange(rawDataArr.shape[0]), rawDataArr.shape[0], replace=False)

        # Traversing all data points in one epoch
        for dataidx in range(idxArr.shape[0]):
            self.__LearnOneSample(rawDataArr[dataidx], alpha, sigma)
        self.__errorHistory.append(self.__GetError(rawDataArr))

    def __GetError(self, rawDataArr):
        """
        get current error on all data samples

        :param rawDataArr: 
        :type rawDataArr: np.array
        """
        error = 0
        for dataSample in rawDataArr:
            error += np.min(np.sum((self.__nodeArr - dataSample) ** 2, axis=2))
        return error

    def __LearnOneSample(self, dataSample, alpha, sigma):
        '''
        Update the nodeArr based on one sample

        :param dataSample: one-dimension of a patient sample with different proteins
        :type dataSample: np.array
        :param alpha: current alpha
        :type alpha: float
        :param sigma: current sigma
        :type sigma: sigma
        :return: None
        '''
        xIdx, yIdx = self.__FindBestMatch(dataSample)
        distArr = self.__GetDist2BestMatch(xIdx, yIdx)
        h = np.exp(-(distArr / sigma) ** 2).reshape(self.__xdim, self.__ydim, 1)
        self.__nodeArr = self.__nodeArr - h * alpha * (self.__nodeArr - dataSample)

    def __FindBestMatch(self, dataSample):
        """
        Return the x-index and y-index for the best matching unit in the nodeArr

        :param dataSample: one-dimension of a patient sample with different proteins
        :type dataSample: np.array
        :return: xIdx {int}, y{int}
        """
        assert (dataSample.shape[0] == self.__nodeArr.shape[2])
        idx = np.argmin(np.sum((self.__nodeArr - dataSample) ** 2, axis=2))

        xIdx = int(idx / self.__nodeArr.shape[1])
        yIdx = idx % self.__nodeArr.shape[1]

        return xIdx, yIdx

    def __GetDist2BestMatch(self, xIdx, yIdx):
        """
        Return the distance matrix to the best match unit. The distance measure is Manhattan Distance

        :param xIdx: the x-index of the best match unit
        :type xIdx: int
        :param yIdx: the y-index of the best match unit
        :type yIdx: int
        """
        idxArr = np.array(list(np.ndindex(self.__xdim, self.__ydim))).reshape(self.__xdim, self.__ydim, 2)
        distArr = idxArr - np.array([xIdx, yIdx])
        distArr = np.sum(np.abs(distArr), axis=2)
        return distArr


class SOM1D(object):
    def __init__(self, dim):
        self.__dim = dim

        self.__nodeArr = np.array([])  # not initialized
        self.__alphaStart = 0
        self.__sigmaStart = 0
        self.__epochNum = 0
        self.__errorHistory = []
        self.__interval = 0  # interval of epochs to save the error history

    def InitializeParams(self, rawDataArr):
        """
        Initialize the nodes in self.__map with normal distribution

        :param rawDataArr: shape = (sampleNum, featureNum)
        :type rawDataArr: np.array
        """
        self.__nodeArr = np.random.normal(np.mean(rawDataArr), np.std(rawDataArr),
                                          size=(self.__dim, rawDataArr.shape[1]))

    def Fit(self, rawDataArr, alpha, sigma, epochNum, interval=1000):
        ''' Train the SOM on the given data for several iterations

        :param rawDataArr: data to train on
        :type rawDataArr: np.array
        :param epochNum: number of iterations to train; if 0, epochs=len(data) and every data point is used once
        :type epochNum: int
        :param interval: interval of epochs to use for saving training errors
        :type interval: int
        '''
        self.__interval = interval
        self.__alphaStart = alpha
        self.__sigmaStart = sigma
        self.__epochNum = epochNum

        for epoch in range(self.__epochNum):
            self.__TrainPerEpoch(rawDataArr, epoch)

    def GetClustLabels(self, rawDataArr):
        """
        Treat each unit in the nodeArr as a cluster. The best match unit is the cluster label for each data sample.
        The cluster index will be adjusted since some units are never used.

        :param rawDataArr:
        :type rawDataArr: np.array
        :return: clustLabels
        """
        clustLabels = []

        for dataSample in rawDataArr:
            idx = self.__FindBestMatch(dataSample)
            clustLabels.append(idx)

        usedLabels = np.unique(clustLabels)
        transform = {usedLabels[i]: i for i in range(len(usedLabels))}
        clustLabels = [transform[clustLabels[i]] for i in range(len(clustLabels))]

        return np.array(clustLabels)

    def GetErrorHistory(self):
        return self.__errorHistory

    def __TrainPerEpoch(self, rawDataArr, currentEpoch):
        '''
        Update the SOM for one epoch. The training parameters are updated once in an epoch.

        :param rawDataArr:
        :type rawDataArr: np.array
        :param currentEpoch: 
        :type currentEpoch: int
        '''
        alpha = self.__alphaStart / (1 + (currentEpoch / 0.5) ** 4)
        sigma = self.__sigmaStart / (1 + (currentEpoch / 0.5) ** 4)

        idxArr = np.random.choice(np.arange(rawDataArr.shape[0]), rawDataArr.shape[0], replace=False)

        # Traversing all data points in one epoch
        for dataidx in range(idxArr.shape[0]):
            self.__LearnOneSample(rawDataArr[dataidx], alpha, sigma)
        self.__errorHistory.append(self.__GetError(rawDataArr))

    def __GetError(self, rawDataArr):
        """
        get current error on all data samples

        :param rawDataArr:
        :type rawDataArr: np.array
        :return: error
        """
        error = 0
        for dataSample in rawDataArr:
            error += np.min(np.sum((self.__nodeArr - dataSample) ** 2, axis=1))
        return error

    def __LearnOneSample(self, dataSample, alpha, sigma):
        """
        Update the nodeArr based on one sample

        :param dataSample: one-dimension of a patient sample with different proteins
        :type dataSample: np.array
        :param alpha: current alpha
        :type alpha: float
        :param sigma: current sigma
        :type sigma: sigma
        :return: None
        """
        idx = self.__FindBestMatch(dataSample)
        distArr = self.__GetDist2BestMatch(idx)
        h = np.exp(-(distArr / sigma) ** 2).reshape(-1, 1)
        self.__nodeArr = self.__nodeArr - h * alpha * (self.__nodeArr - dataSample)

    def __FindBestMatch(self, dataSample):
        """
        Return the x-index and y-index for the best matching unit in the nodeArr

        :param dataSample: one-dimension of a patient sample with different proteins
        :type dataSample: np.array
        :return: xIdx {int}, y{int}
        """
        assert (dataSample.shape[0] == self.__nodeArr.shape[1])
        idx = np.argmin(np.sum((self.__nodeArr - dataSample) ** 2, axis=1))

        return idx

    def __GetDist2BestMatch(self, idx):
        """
        Return the distance matrix to the best match unit. The distance measure is Manhattan Distance

        :param idx: the index of the best match unit
        :type idx: int
        :return: distArr
        """
        idxArr = np.arange(self.__dim)
        distArr = np.abs(idxArr - idx)
        return distArr

