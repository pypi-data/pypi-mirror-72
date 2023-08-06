import random
import matplotlib.pyplot as plt
from .CommonFunction import *
import seaborn as sns


def DrawScatterPlotForCombineFig(clustNumSer, currentFeatureSer, compareFeatureSer, axes, color='Set1', labelSize=10):
    """
    draw a scatter plot based on cluster, meta feature value and the feature you want to compare

    :param clustNumSer: the number Series represents the samples' cluster. [1,0,0,2] means 4 samples in different 3 clusters
    :param currentFeatureSer: the Series includes each sample's feature value. ['white','black','white']
    :param compareFeatureSer: the Series includes you want to compare with currentFeatureSer
    :param axes: the postion of the bar plot in the combineFig
    :param labelSize: the size of label font
    :param color: the color palette from matplotlib.pyplot used in the figure
    :return: axes, the position of the bar plot in the combineFig
    """
    clustXaxisLi = GetClustXaxisLi(clustNumSer)

    featureValueSetLi = (list(set(compareFeatureSer)))
    featureValueSetLi.sort(reverse=False)
    # scatterPlotDf=pd.concat([clustNumSer,currentFeautreSer],names=['clust','feature'])
    # scatterPlotDf=clustNumSer.to_frame().join(currentFeautreSer.to_frame())
    scatterPlotDf = pd.DataFrame(
        {'clust': clustNumSer, currentFeatureSer.name: currentFeatureSer, compareFeatureSer.name: compareFeatureSer})

    scatterPlotDf[compareFeatureSer.name ] = __TurnStrSerToIntLi(scatterPlotDf[compareFeatureSer.name])

    scatterPlotDf[compareFeatureSer.name ] = __TurnFeatureRandom(scatterPlotDf[compareFeatureSer.name])

    scatterPlotDf['clust'] = __TurnStrSerToIntLi(scatterPlotDf['clust'])

    scatterPlotDf['clust'] = __TurnFeatureRandom(scatterPlotDf['clust'])

    sns.scatterplot(x='clust', y=compareFeatureSer.name, hue=currentFeatureSer.name, hue_order=set(currentFeatureSer),
                   palette=sns.color_palette(color, len(set(currentFeatureSer))), data=scatterPlotDf, ax=axes)




    #####setting label and hide legend title
    handles, labels = axes.get_legend_handles_labels()
    axes.legend(handles=handles[1:], labels=labels[1:],loc='lower left', prop={'size': 10}, bbox_to_anchor=(0.0, 1.1, 0.4, 0.3))
    # axes.legend(set(currentFeautreSer), prop={'size': 10}, loc='lower right')
    axes.tick_params(labelsize=labelSize)
    axes.set_xlabel('')             ### x-axis title

    axes.set_xticks(GetXlabelPositionLi(clustNumSer))         ### x tick points

    axes.set_xticklabels(clustXaxisLi)          ### x tick label names

    axes.set_yticks(GetXlabelPositionLi(compareFeatureSer))

    axes.set_yticklabels(featureValueSetLi)
    axes.set_xlabel('cluster')
    axes.set_title(currentFeatureSer.name)

    return axes



def DrawScatterPlot(protClustObj, currentFeatureSer, compareFeatureSer, color='Set1',
                    labelSize=10, path='scatterplot.png', figSizeLi=[5,4], dpi=96):
    """
    draw a scatter plot based on cluster, meta feature value and the feature you want to compare

    :param currentFeatureSer: the Series includes each sample's feature value. ['white','black','white']
    :param compareFeatureSer: the Series includes you want to compare with currentFeatureSer
    :param figSizeLi: the width and high of the figure
    :param dpi: Dots Per Inch in the figure
    :param labelSize: the size of label font
    :return: plt, the figure of the scatter plot
    """
    clustNumSer = protClustObj.clustResultObj.sampleClustSer
    clustXaxisLi = GetClustXaxisLi(clustNumSer)

    featureValueSetLi = (list(set(compareFeatureSer)))
    featureValueSetLi.sort(reverse=False)
    # scatterPlotDf=pd.concat([clustNumSer,currentFeautreSer],names=['clust','feature'])
    # scatterPlotDf=clustNumSer.to_frame().join(currentFeautreSer.to_frame())
    fig, axes = plt.subplots (1, 1, figsize=(figSizeLi[0], figSizeLi[1]), dpi=dpi)

    scatterPlotDf = pd.DataFrame(
        {'clust': clustNumSer, currentFeatureSer.name: currentFeatureSer, compareFeatureSer.name: compareFeatureSer})

    scatterPlotDf[compareFeatureSer.name ] = __TurnStrSerToIntLi(scatterPlotDf[compareFeatureSer.name])

    scatterPlotDf[compareFeatureSer.name ] = __TurnFeatureRandom(scatterPlotDf[compareFeatureSer.name])

    scatterPlotDf['clust'] = __TurnStrSerToIntLi(scatterPlotDf['clust'])

    scatterPlotDf['clust'] = __TurnFeatureRandom(scatterPlotDf['clust'])

    sns.scatterplot(x='clust', y=compareFeatureSer.name, hue=currentFeatureSer.name, hue_order=set(currentFeatureSer),
                   palette=sns.color_palette(color, len(set(currentFeatureSer))), data=scatterPlotDf, ax=axes)




    #####setting label and hide legend title
    handles, labels = axes.get_legend_handles_labels()
    axes.legend(handles=handles[1:], labels=labels[1:],loc='lower left', prop={'size': 10}, bbox_to_anchor=(0.0, 1.1, 0.4, 0.3))
    # axes.legend(set(currentFeautreSer), prop={'size': 10}, loc='lower right')
    axes.tick_params(labelsize=labelSize)
    axes.set_xlabel('')             ### x-axis title

    axes.set_xticks(GetXlabelPositionLi(clustNumSer))         ### x tick points

    axes.set_xticklabels(clustXaxisLi)          ### x tick label names

    axes.set_yticks(GetXlabelPositionLi(compareFeatureSer))

    axes.set_yticklabels(featureValueSetLi)
    axes.set_xlabel('cluster')
    axes.set_title(currentFeatureSer.name)

    fig.savefig (path, bbox_inches="tight")

    return fig











def __TurnStrSerToIntLi(currentFeatureSer):
    """
    turn a string series into int [0,1,2,3,3,2....]

    :param currentFeatureSer: the Series includes each sample's feature value. ['white','black','white']
    :return: number list, [0,1,2,2]means 4 samples in different 3 different feature values
    """
    numLi = [0 for x in range(len(currentFeatureSer))]
    featureSetLi = (list(set(currentFeatureSer)))
    featureSetLi.sort(reverse=False)
    for k in range(len(currentFeatureSer)):

        num = 0
        for featureValue in featureSetLi:
            if currentFeatureSer[k] == featureValue:
                numLi[k] = num
            num += 1
    return numLi


def __TurnFeatureRandom(FeatureNumLi, ranges=0.2):
    """
    turn feature number list in to [0.12,1.15,1.98,2.2....],  in order to scatter the data points.

    :param FeatureNumLi: number list, [0,1,2,2]means 4 samples in different 3 different feature values
    :param ranges:the range to add or minus randomly, the smaller the concentrated the data points
    :return: FeatureNumLi [0.12,1.15,1.98,2.2....]
    """
    randNumLi = [0 for x in range(len(FeatureNumLi))]

    for num in range(len(FeatureNumLi)):
        randNumLi[num] = float(FeatureNumLi[num] + random.uniform(0 - ranges, 0 + ranges))

    return randNumLi

