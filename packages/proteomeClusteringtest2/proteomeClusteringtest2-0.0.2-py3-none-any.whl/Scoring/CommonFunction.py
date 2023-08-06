import math
from collections import Counter
import pandas as pd
import numpy as np 
import scipy.spatial as spatial #for partition index and seperation index


def ConvertPredLiStartZero(predLi):
    '''
    predLi is sampleClustSer ([1, 2, 2, 3, 3, 4], sometimes for the convenience need to convert it to [0, 1, 1, 2, 2 ,3]

    :param predLi: sampleClustSer's list [1, 2, 2, 3, 3, 4]
    :return: list [0, 1, 1, 2, 2 ,3]
    '''
    resultLi=[]
    predRangeDict = {}
    count = 0
    for i in set(predLi):
        predRangeDict[i] = count
        count+=1

    for i in range(len(predLi)):
        resultLi.append(predRangeDict[predLi[i]])

    return resultLi


#for partition index and seperation index
def GetClusterCenter(dataArr, predLi, num):
    '''
    Get the center of each cluster.

    :param dataArr: np.array, data values, shape [data_num, feature_num]
    :param: predLi: list, dimension [data_num, ], the number in preds starts from 0, no integer is skipped
    :param: num: int, number of clusters
    :return: center: np.array, center of the clusters, dimension [cluster_num, feature_num] 
    '''
    centerArr = np.zeros((num,dataArr.shape[1]))
    clusMemCountArr = np.zeros(num)
    predFromZeroLi = ConvertPredLiStartZero(predLi)
    for i in range(len(predFromZeroLi)):
        centerArr[predFromZeroLi[i]] += dataArr[i]
        clusMemCountArr[predFromZeroLi[i]] += 1

    centerArr = np.divide(centerArr.T,clusMemCountArr).T
    return centerArr

#for partition index and seperation index
def GetUtilityMatrix(dataArr, centerArr, distanceMetric):
    '''
    Get the utility Matrix for the clustering results.
    The membership value is inversely proportional to distance (distance from the data point to each center) square.

    :param: dataArr: np.array. Shape [data_num feature_num]
    :param: center: np.array. Center of the clusters, dimension [cluster_num, feature_num]
    :param: distanceMetric: string. The distance metric. Possible values: euclidean, cityblock, cosine, correlation
    :return: np.array. Shape [cluster_num, data_num]
    '''
    num = centerArr.shape[0]

    distanceMatrixArr = spatial.distance.cdist(dataArr, centerArr, metric=distanceMetric)
    distanceMatrixArr = distanceMatrixArr/(np.sum(distanceMatrixArr,axis=1).reshape(-1,1))
   
    with np.errstate(divide='ignore', invalid='ignore'):
        utilityArr = 1/np.square(distanceMatrixArr)
        utilityArr[distanceMatrixArr == 0] = 1

    utilityArr = utilityArr/(np.sum(utilityArr,axis=1).reshape(-1,1)) #[data_num, cluster_num]

    return utilityArr.T

def ComputeEntropy(featureLi, unit='shannon'):
    '''
    compute entropy of data(meta data feature)

    :param featureLi: label list or number list, len is same as sample numbers
    :param unit: the log base of computing entropy. shannon=2, natural=e, hartley=10
    :return: float entropy
    '''



    base = {
        'shannon': 2.,
        'natural': math.exp(1),
        'hartley': 10.
    }

    if len(featureLi) <= 1:
        return 0

    counts = Counter()

    for d in featureLi:
        counts[d] += 1

    ent = 0

    probs = [float(c) / len(featureLi) for c in counts.values()]
    for p in probs:
        if p > 0.:
            ent -= p * math.log(p, base[unit])

    return ent



def TurnLabelToNum(featureLi):
    '''
    change feature value list into number list, in order to compute scores ex: ['black','black','red','yellow'] -> [0,0,1,2]

    :param featureLi: feature value list
    :return: number list
    '''
    listNum=0
    for label in set(featureLi):

        for i in range(len(featureLi)):
            if featureLi[i]==label:
                featureLi[i]=listNum
        listNum=listNum+1


    return list(featureLi)



def TurnClustToNumSer(sampleNameLi, protClustObj):
    '''
    change clustSampleSer in clustDataObj var into a numlist for the following figure

    :param sampleNameLi: the name list that needed to transfer
    :param protClustObj: ds_protClust object
    :return: numlist
    '''

    clustSampleSer= protClustObj.clustResultObj.clustSampleSer

    numSer = pd.Series([0 for x in range(len(sampleNameLi))],index=sampleNameLi)

    for col in range(len(clustSampleSer)):
        for row in range(len(clustSampleSer[col])):

            for num in range(len(sampleNameLi)):
                if clustSampleSer[col][row] == sampleNameLi[num]:
                    numSer[num] = col
    return numSer



def GetlenEachClustLi(protDataObj):
    '''
    count length of each cluster in protDataObj.clustSampleSer

    :param protDataObj:
    :return: lentgth list. Example:[7,9,7] for 3 clusters
    '''

    clustSampleLi = list(protDataObj.clustResultObj.clustSampleSer)
    lenLi = [0 for x in range(len(clustSampleLi))]
    for col in range(len(clustSampleLi)):
        lenLi[col]=len(clustSampleLi[col])

    return lenLi

