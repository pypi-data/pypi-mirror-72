import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def FindSampleOverlapHeatmap(protClustObj1, protClustObj2, path=None, colorStr='Blues', dpi=96, xlabelStr='Cluster1', ylabelStr='Cluster2'):
    """
    find each subtype's sample overlap between two clustering result.  intersection /union

    :param protClustObj1: ds_protClustObj1
    :param protClustObj2: ds_protClustObj2
    :return: overlap heatmap
    """
    clust1Li = protClustObj1.clustResultObj.sampleClustSer.tolist()
    clust2Li = protClustObj2.clustResultObj.sampleClustSer.tolist()
    clust1Ser = protClustObj1.clustResultObj.sampleClustSer
    clust2Ser = protClustObj2.clustResultObj.sampleClustSer
    clustNum1 = len(set(clust1Li))
    clustNum2 = len(set(clust2Li))
    samNumLi1 = [0 for x in range(len(set(clust1Li)))]
    samNumLi2 = [0 for x in range(len(set(clust2Li)))]
    ratioTable = pd.DataFrame([[0.0 for x in range(clustNum1)]] * clustNum2)
    for Num1 in range(clustNum1):
        c1Li = _GetClustLi(clust1Ser, Num1 + 1)
        for Num2 in range(clustNum2):
            c2Li = _GetClustLi(clust2Ser, Num2 + 1)
            count = 0

            union = set(c1Li).union(c2Li)
            intersection = set(c1Li).intersection(c2Li)

            if len(union) == 0:
                ratioTable[Num1][Num2] = 0
            else:
                ratioTable[Num1][Num2] = len(intersection) / len(union)
            samNumLi2[Num2] = clust2Li.count(Num2+1)
        samNumLi1[Num1] = clust1Li.count(Num1+1)

    __PrintSampleNum(samNumLi1,samNumLi2)
    sns.set(font_scale=2)
    sns.heatmap(ratioTable, cmap=colorStr, linewidths=.5, annot=True, xticklabels=[x  for x in set(clust1Ser)],
                yticklabels=[x  for x in set(clust2Ser)], vmin=0, vmax=1, fmt='.2f')
    plt.xlabel(xlabelStr)
    plt.ylabel(ylabelStr)
    if path is None:
        plt.show()

    else:
        plt.savefig(path, bbox_inches='tight',dpi=dpi)

    return ratioTable


def _GetClustLi(clusteringResultSer, subtypeNum):
    """
    Get the sample name list in subtype (param:Num)

    :param clusteringResultSer: clustering result series, contain each sample was clustered into which subtype
    :param subtypeNum: the number represent which subtype
    :return: sample name list
    """
    clusterLi = []

    for nameStr in clusteringResultSer.index:
        if clusteringResultSer[nameStr] == subtypeNum:
            clusterLi.append(nameStr)
        else:
            continue

    return clusterLi

def __PrintSampleNum(clust1Li, clust2Li):
    '''
    Print how many samples in each cluster subtypes

    :return: None
    '''
    print('Method1: \n')
    for num in range(len(set(clust1Li))):

        print("cluster" + str(num + 1) + ": " + str(clust1Li[num]))
    print('Method2: \n')
    for num in range(len(set(clust2Li))):
        print("cluster" + str(num + 1) + ": " + str(clust2Li[num]))