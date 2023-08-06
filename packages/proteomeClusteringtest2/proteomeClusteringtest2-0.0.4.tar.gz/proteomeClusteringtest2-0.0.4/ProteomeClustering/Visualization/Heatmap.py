from sklearn.metrics import adjusted_rand_score

from .CommonFunction import *
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import matplotlib.colors
from scipy.spatial import distance
import math

def DrawHeatMap(rawDataObj, protClustObj, colorStr="coolwarm", clustColorStr='Set1', wSpace=0.02, figSizeLi=[20, 20],
                path=None, dpi=96):
    """
    draw a heat map based on rawDataObj filtered ratio table

    :param rawDataObj: ds_InputRawData
    :param protClustObj: ds_ProtClust
    :param colorStr: the matplotlib color set used in heatmap, default is "coolwarm"
    :param clustColorStr: (if hierarchical clustering) the matplotlib color set used in clustermap to show different subtypes, defalt is "Set1"
    :param wSpace: (if not hierarchical clustering) the width space between each subtype
    :param figSizeLi: the figure size of the heatmap
    :param path: the path to save heatmap figure
    :return: heatmap fig
    """

    clustNumSer = protClustObj.clustResultObj.sampleClustSer

    heatMapRatioDf = rawDataObj.GetProtRatioDf().copy()
    heatMapRatioDf['clusterNumList'] = clustNumSer

    lenEachClustLi = GetlenEachClustLi(protClustObj)

    ###sort same cluster together###
    heatMapRatioDf.sort_values(by='clusterNumList', axis=0, inplace=True)

    heatMapRatioDf = heatMapRatioDf.drop(columns=['clusterNumList'])
    sampleNameli = heatMapRatioDf.index.values
    # heatMapRatioDf = heatMapRatioDf[heatMapRatioDf.columns != 'clusterNumList']

    methodStr = protClustObj.clustParamObj.GetParam('method')

    if methodStr == 'hierarchicalClust':

        pltColors = sns.color_palette(clustColorStr, len(set(clustNumSer)))
        cmap = matplotlib.colors.ListedColormap(pltColors)
        rowClusterColor = clustNumSer.map(cmap)
        metricStr = protClustObj.clustParamObj.GetParam('distance')
        linkageStr = protClustObj.clustParamObj.GetParam('linkage')

        fig = sns.clustermap(heatMapRatioDf, row_colors=rowClusterColor, metric=metricStr, method=linkageStr,
                                   cmap=colorStr, xticklabels=False, yticklabels=False,
                                   figsize=(figSizeLi[0], figSizeLi[1]))
        ax = fig.ax_heatmap
        ax.set_xlabel("gene")
        ax.set_ylabel("sample")

    else:
        # print('only hierarchical clustering can show heatmap')

        ### draw heatmap
        fig, axes = plt.subplots(1, len(lenEachClustLi), figsize=(figSizeLi[0], figSizeLi[1]),
                                 gridspec_kw={'hspace': 0, 'wspace': wSpace, 'width_ratios': lenEachClustLi})
        heatMapStart = 0
        heatMapEnd = 0
        cbarAx = fig.add_axes([.905, .3, .05, .3])
        for i in range(len(lenEachClustLi)):
            heatMapEnd += lenEachClustLi[i]
            if i == len(lenEachClustLi) - 1:
                # (__SortSampleRatioDf(heatMapRatioDf.iloc[:, heatMapStart:heatMapEnd],sampleNameli[heatMapStart:heatMapEnd])

                sns.heatmap(heatMapRatioDf.T.iloc[:, heatMapStart:heatMapEnd],
                            ax=axes[i], xticklabels=False, yticklabels=False, cmap=colorStr, robust=True, cbar_ax=cbarAx)
            else:
                sns.heatmap(heatMapRatioDf.T.iloc[:, heatMapStart:heatMapEnd],
                            ax=axes[i], cbar=False, xticklabels=False, yticklabels=False, cmap=colorStr, robust=True)
            heatMapStart += lenEachClustLi[i]
            axes[i].set_xlabel('cluster' + str(i + 1))

        # confiugration: figure_size, color?, minmax, center,

    if path == None:
        plt.show()
    else:
        plt.savefig(path, dpi=dpi)
    return fig


def DrawPatientToPatientCorrHeatmap(rawDataObj, protClustObj, colorsStr="coolwarm", figSizeLi=[10, 10],
                                    path=None, dpi=96):
    """
    draw a heat map based on sample to sample correlation

    :param rawDataObj: ds_InputRawData
    :param protClustObj: ds_ProtClust
    :param colorsStr: the matplotlib color set used in heatmap, default is "coolwarm"
    :param figSizeLi: the figure size of the heatmap
    :param path: the path to save heatmap figure
    :return: heatmap fig
    """
    sampleNameli = rawDataObj.GetProtRatioDf().index.values
    distArr = [[0.0 for i in range(len(sampleNameli))] for k in range(len(sampleNameli))]
    clustNumSer = protClustObj.clustResultObj.sampleClustSer

    heatMapRatioDf = rawDataObj.GetProtRatioDf().copy()
    heatMapRatioDf['clusterNumList'] = clustNumSer

    ###sort same cluster together###
    heatMapRatioDf.sort_values(by='clusterNumList', axis=0, inplace=True)

    heatMapRatioDf = heatMapRatioDf.drop(columns=['clusterNumList'])
    sampleNameli = heatMapRatioDf.index.values
    col = 0

    for name1 in sampleNameli:
        row = 0
        for name2 in sampleNameli:
            distArr[col][row] = sc.spatial.distance.euclidean(heatMapRatioDf.T[name1], heatMapRatioDf.T[name2])
            #if distArr[col][row]!=0:
            #    distArr[col][row] = math.log2(distArr[col][row])
            row += 1
        col += 1
    plt.figure(figsize=(figSizeLi[0], figSizeLi[1]))

    sns.heatmap(distArr, xticklabels=False, yticklabels=False, cmap=colorsStr, robust=True, square=True,vmin=0)
    print(distArr)
    if path is None:
        plt.show()
    else:
        plt.savefig(path, dpi=dpi)
    return plt
