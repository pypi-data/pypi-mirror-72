import pandas as pd
import math
from collections import Counter


def GetlenEachClustLi(protClustObj):
    """
    used in heatmap and metacolormap plot, get the sample number of each cluster

    :param protClustObj:
    :return: int list, for example, [20, 20, 20, 20, 16] for 5 clsuters and 96 samples
    """

    clustSampleLi = list(protClustObj.clustResultObj.clustSampleSer)
    lenLi = [0 for x in range(len(clustSampleLi))]
    for col in range(len(clustSampleLi)):
        lenLi[col] = len(clustSampleLi[col])

    return lenLi


def CountFeatureValueNum(metaSer, featureValue):
    """
    count how many a feature value(input) in the series

    :param metaSer: the meata data feature series in specific cluster
    :param featureValue: the feature value that wanted to count
    :return: int, number of the featureValue
    """
    count = 0
    for i in range(len(metaSer)):
        if metaSer[i] == featureValue:
            count = count + 1
    return count


def GetXlabelPositionLi(sampleClustSer):
    """
    Get the x label position to draw diverge and stacked plot

    :param sampleClustSer: series, show each sample belongs to which cluster
    :return: x label position list
    """
    xLabelLi = []
    for index in range(len(set(sampleClustSer))):
        xLabelLi.append(index)

    return xLabelLi


def GetEntropy(featureLi, unit='shannon'):
    """
    compute entropy of data(meta data feature)

    :param featureLi: label list or number list, len is same as sample numbers
    :param unit: the log base of computing entropy. shannon=2, natural=e, hartley=10
    :return: float entropy
    """

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


def GetClustXaxisLi(clustNumSer):
    """
    get the x axis label list used in stacked, scatter, diverge plot (cluster 1, 2, 3, 4, 5...)

    :param clustNumSer:
    :return: string list,
    """
    clustXaxisLi = []
    #####build index list of entropy table
    for index in set(clustNumSer):
        # clustXaxisLi.append("cluster" + str(index))
        clustXaxisLi.append(str(index))
    return clustXaxisLi
