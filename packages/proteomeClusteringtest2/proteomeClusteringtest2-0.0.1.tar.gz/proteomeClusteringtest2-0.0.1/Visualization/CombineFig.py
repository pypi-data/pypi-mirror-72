# -*- coding: utf-8 -*-


from .CommonFunction import *
from .StackedBar import *
from .DivergeBar import *
from .ScatterPlot import *


def DrawCombinedFig(protClustObj, currentFeatureSer, compareFeatureSer, figTitleStr='Combined Figure',
                    figSizeLi=[15, 4], dpi=100, wSpace=0.7
                    , pathStr='combinFig.png', colorsStr='Set1', orderLi=['stacked', 'scatter', 'diverge']):
    """
    draw a combined figure included stacked, scatter, and diverge figure of clustering result

    :param protClustObj: ds_protClust object
    :param figSizeLi: the width and high of the figure
    :param currentFeatureSer: the Series includes each sample's feature value. ['white','black','white']
    :param compareFeatureSer: the Series includes you want to compare with currentFeatureSer
    :param pathStr: string, the name of the figure
    :param dpi: int, figure dpi
    :param wSpace: the width space between different figures
    :param orderLi: the string list include what plot you want to show in a CombineFig and the position of each plots
    :return: fig, the combination of subplots
    """

    clustNumSer = protClustObj.clustResultObj.sampleClustSer

    subplotNum = len(orderLi)
    fig, axes = plt.subplots(1, subplotNum, figsize=(figSizeLi[0] * subplotNum, figSizeLi[1]), gridspec_kw={'wspace': wSpace},
                             dpi=dpi)

    ######setting the order of plots######

    for orderNum in range(subplotNum):
        try:
            if orderLi[orderNum] != 'stacked' and orderLi[orderNum] != 'scatter' and orderLi[orderNum] != 'diverge':
                raise RuntimeError('use wrong plot name :' + orderLi[orderNum])
            elif len(set(orderLi)) < len(orderLi):
                raise RuntimeError('can not draw same plot twice')
            elif orderLi[orderNum] == 'stacked':

                axes[orderNum] = DrawStackedBarForCombineFig(clustNumSer, currentFeatureSer, axes[orderNum], color=colorsStr,
                                                          edgecolor='white',
                                                          width=0.5)

            elif orderLi[orderNum] == 'scatter':

                axes[orderNum] = DrawScatterPlotForCombineFig(clustNumSer, currentFeatureSer, compareFeatureSer,
                                                           axes[orderNum], color=colorsStr)

            elif orderLi[orderNum] == 'diverge':
                # scoringLi, scoreCenter = __DetermineScoreMethod(scoreMethod, protClustObj, clustNumber, currentFeatureName)
                axes[orderNum] = DrawDivergeBarForCombineFig(protClustObj, currentFeatureSer, axes[orderNum])

        except RuntimeError as e:
            print(e)

    #####use bbox_inches="tight" to make sure the completeness of legends in subplots#####
    fig.suptitle(figTitleStr, fontsize=16, x=0.5, y=1.5)
    fig.savefig(pathStr, bbox_inches="tight")

    return fig


def _GetEntropyFromProtClust(protClustObj, clustNum, currentFeatureName):
    """
    get entropy series from protClustObj in order to draw diverge bar

    :param protClustObj: ds_protClust object
    :param clustNum:int, the number of clusters
    :param currentFeatureName: string ,the feature name
    :return: entropy list
    """
    scoreLi = [0.0 for x in range(clustNum)]
    for currentClust in range(clustNum):
        scoreLi[currentClust] = protClustObj.clustScoringObj.clustFeatureEntropySer[currentClust][currentFeatureName] / \
                                protClustObj.clustScoringObj.featureEntropyDi[currentFeatureName]

    return scoreLi
