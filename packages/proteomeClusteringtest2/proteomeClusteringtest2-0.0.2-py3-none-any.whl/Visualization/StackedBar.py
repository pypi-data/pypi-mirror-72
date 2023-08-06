import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import math
from collections import Counter

from .CommonFunction import *


def DrawStackedBarForCombineFig(clustNumSer, currentFeatureSer, axes, color="Set1", edgecolor='white', width=0.5,
                                legendSize=10):
    """
    draw a stacked bar based on cluster and meta feature value

    :param clustNumSer: the number Series represents the samples' cluster. [1,0,0,2] means 4 samples in different 3 clusters
    :param currentFeatureSer: the Series includes each sample's feature value. ['white','black','white']
    :param axes: the postion of the bar plot in the combineFig
    :param color: the color set of different feature values
    :param edgecolor: the background color of the bar plot
    :param width: the width of each bar
    :param legendSize: the size of the legned
    :return: axes, the postion of the bar plot in the combineFig
    """


    clustXaxisLi=GetClustXaxisLi(clustNumSer)
    colors = sns.color_palette(color, len(set(currentFeatureSer)))

    featureValueMatrix = [[0 for x in range(len(set(clustNumSer)))] for y in range(len(set(currentFeatureSer)))]

    ##### for every predict cluster
    #for currentClust in range(len(set(clustNumSer))):
    clustCount=0
    for currentClust in set(clustNumSer):
        clusterFilter = (clustNumSer == currentClust)
        barClust = currentFeatureSer[clusterFilter]
        valueCount = 0
        # print(barClust.value_counts())
        ##### for every type in every meta data
        for value in (set(currentFeatureSer)):
            featureValueMatrix[valueCount][clustCount] = CountFeatureValueNum(barClust, value)
            valueCount += 1
            # else:
            #   Matrix[currentClust][valueCount]=0
    #      valueCount=valueCount+1
        clustCount+=1
    bars = [0 for x in range(len(set(clustNumSer)))]
    for i in range(len(set(currentFeatureSer))):
        axes.bar(clustXaxisLi, featureValueMatrix[i], bottom=bars, color=colors[i], edgecolor=edgecolor, width=width)
        bars = np.add(bars, featureValueMatrix[i]).tolist()
    axes.legend(set(currentFeatureSer), loc='lower left', prop={'size': legendSize}, bbox_to_anchor=(0.0, 1.1, 0.4, 0.3))
    axes.set_xlabel('cluster')
    axes.set_title(currentFeatureSer.name)

    return axes


def DrawStackedBar(protClustObj, currentFeatureSer, color="Set1", edgeColor='white', width=0.5,
                   legendSize=10, figSizeLi=[5, 4], path='stackedbar.png', dpi=72):
    """
    draw a stacked bar based on cluster and meta feature value

    :praram protClustObj: ds_protclustObj
    :param currentFeatureSer: the Series includes each sample's feature value. ['white','black','white']
    :param color: the color set of different feature values
    :param edgeColor: the background color of the bar plot
    :param width: the width of each bar
    :param figSizeLi: the width and high of the figure
    :param legendSize: the size of the legned
    :return: axes, the position of the bar plot in the combineFig
    """

    clustNumSer = protClustObj.clustResultObj.sampleClustSer
    clustXaxisLi = GetClustXaxisLi (clustNumSer)
    colors = sns.color_palette (color, len (set (currentFeatureSer)))
    fig, axes = plt.subplots (1, 1, figsize=(figSizeLi[0], figSizeLi[1]), dpi=dpi)
    featureValueMatrix = [[0 for x in range (len (set (clustNumSer)))] for y in range (len (set (currentFeatureSer)))]

    ##### for every predict cluster
    clustCount = 0
    for currentClust in set(clustNumSer):
        clusterFilter = (clustNumSer == currentClust)
        barClust = currentFeatureSer[clusterFilter]
        valueCount = 0
        # print(barClust.value_counts())
        ##### for every type in every meta data
        for value in (set (currentFeatureSer)):
            featureValueMatrix[valueCount][clustCount] = CountFeatureValueNum (barClust, value)
            valueCount += 1
            # else:
            #   Matrix[currentClust][valueCount]=0
    #      valueCount=valueCount+1
        clustCount+=1
    bars = [0 for x in range (len (set (clustNumSer)))]
    for i in range (len (set (currentFeatureSer))):
        axes.bar (clustXaxisLi, featureValueMatrix[i], bottom=bars, color=colors[i], edgecolor=edgeColor, width=width)
        bars = np.add (bars, featureValueMatrix[i]).tolist ()
    axes.legend (set (currentFeatureSer), loc='lower left', prop={'size': legendSize},
                 bbox_to_anchor=(0.0, 1.1, 0.4, 0.3))

    axes.set_title (currentFeatureSer.name)
    axes.set_xlabel('cluster')
    fig.savefig (path, bbox_inches="tight")

    return fig
