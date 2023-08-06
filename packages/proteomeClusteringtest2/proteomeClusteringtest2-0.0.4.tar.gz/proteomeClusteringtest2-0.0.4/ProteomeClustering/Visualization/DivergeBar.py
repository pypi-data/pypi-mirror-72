from .CommonFunction import *
import matplotlib.pyplot as plt


def DrawDivergeBarForCombineFig(protClustObj, currentFeatureSer, axes):
    """
    draw a diverge bar of the entropy/backgroundEntropy of each cluster

    :param currentFeatureSer: the Series includes each sample's feature value. ['white','black','white']
    :param axes: the postion of the bar plot in the combineFig
    :return: axes, the postion of the bar plot in the combineFig
    """
    center = 1 #the center of the score(since the average distribute of every feature value's entropy/backgroundEntropy is 1)
    currentFeatureName = currentFeatureSer.name
    sampleClustSer = protClustObj.clustResultObj.sampleClustSer
    scoringLi = _GetEntropyFromProtClust(protClustObj, sampleClustSer, currentFeatureName)
    clustXaxisLi = GetClustXaxisLi(sampleClustSer)
    ##### maybe run different scoring results beside entropy,so here need to extend
    # ScoringLi =__divideBackground(clustNumSer, currentFeautreSer)

    maxValue, minValue = _DetermineMaxMinValue(scoringLi)
    yAxisRange = _DetermineYaxisRange(maxValue, minValue, center)
    entropyLineColor = _DetermineLineColor(scoringLi, center)

    # Draw plot
    # plt.figure(figsize=(14,10), dpi= 80)
    axes.vlines(x=GetXlabelPositionLi(sampleClustSer), ymin=center, ymax=scoringLi, color=entropyLineColor, alpha=1,
                linewidth=15)

    axes.set_ylim(center - yAxisRange, center + yAxisRange)
    axes.set_ylabel('entropy')
    axes.set_xlabel('cluster')
    axes.set_xticks(GetXlabelPositionLi(sampleClustSer))
    axes.set_xticklabels(clustXaxisLi)
    axes.grid(linestyle='--', alpha=0.5)
    axes.axhline(y=center, color='black', linestyle='solid')
    axes.set_title('Diverge Bar')
    return axes


def DrawDivergeBar(protClustObj, currentFeatureSer, figSizeLi=[5, 4], dpi=100, path='divergebar.png'):
    """
    draw a diverge bar of the entropy/backgroundEntropy of each cluster

    :param currentFeatureSer: the Series includes each sample's feature value. ['white','black','white']
    :param figSizeLi: the width and high of the figure
    :param dpi: Dots Per Inch in the figure
    :return: fig, the diverge bar subplot fig
    """
    center = 1  #the center of the score(since the average distribute of every feature value's entropy/backgroundEntropy is 1)
    currentFeatureName = currentFeatureSer.name
    clustNumSer = protClustObj.clustResultObj.sampleClustSer
    clustXaxisLi = GetClustXaxisLi(clustNumSer)
    scoringLi = _GetEntropyFromProtClust(protClustObj, clustNumSer, currentFeatureName)
    fig, axes = plt.subplots(1, 1, figsize=(figSizeLi[0], figSizeLi[1]), dpi=dpi)
    ##### maybe run different scoring results beside entropy,so here need to extend
    # ScoringLi =__divideBackground(clustNumSer, currentFeautreSer)

    maxValue, minValue = _DetermineMaxMinValue(scoringLi)
    yAxisRange = _DetermineYaxisRange(maxValue, minValue, center)
    entropyLineColor = _DetermineLineColor(scoringLi, center)

    # Draw plot

    axes.vlines(x=GetXlabelPositionLi(clustNumSer), ymin=center, ymax=scoringLi, color=entropyLineColor, alpha=1,
                linewidth=15)

    axes.set_ylim(center - yAxisRange, center + yAxisRange)
    axes.set_ylabel('entropy')
    axes.set_xlabel('cluster')
    axes.set_xticks(GetXlabelPositionLi(clustNumSer))
    axes.set_xticklabels(clustXaxisLi)
    axes.grid(linestyle='--', alpha=0.5)
    axes.axhline(y=center, color='black', linestyle='solid')
    axes.set_title('Diverge Bar')

    fig.savefig(path, bbox_inches="tight")

    return fig


def _DetermineLineColor(scoringLi, center):
    """
    determine the color of the line in the diverge bar, if > center is green, otherwise is red

    :param scoringLi: a scoring list contain score each cluster
    :param center: the y-axis center
    :return: color list (green of red)
    """
    colorLi = ['red' for i in range(len(scoringLi))]
    for i in range(len(scoringLi)):
        if scoringLi[i] > center:
            colorLi[i] = 'green'

    return colorLi


def _DetermineYaxisRange(maxValue, minValue, center=1):
    """
    use max value and min value to determine the range of the y-axis of the diverge plot

    :param maxValue: the max value  of the Scoring list
    :param minValue: the minimum value
    :param center: the y-axis center
    :return: float, the range for y-axis, will later set into (center+range, center-range) in DrawDivergeBar function
    """
    maxRange = abs(maxValue - center)
    minRange = abs(minValue - center)

    if maxRange >= minRange:
        return maxRange + 0.1
    elif maxRange < minRange:
        return minRange + 0.1


def _DetermineMaxMinValue(ScoringLi):
    """
    determine the max value and minimum value of the Scoring list

    :param ScoringLi: a scoring list contain score each cluster
    :return: max value, min value
    """
    maxValue = ScoringLi[0]
    minValue = ScoringLi[0]
    for i in range(len(ScoringLi)):
        if ScoringLi[i] < minValue:
            minValue = ScoringLi[i]
        elif ScoringLi[i] > maxValue:
            maxValue = ScoringLi[i]

    return maxValue, minValue


def _GetEntropyFromProtClust(protClustObj, clustNumSer, currentFeatureName):
    """
    get entropy series from protClustObj in order to draw diverge bar

    :param protClustObj: ds_protClust object
    :param clustNum:int, the number of clusters
    :param currentFeatureName: string ,the feature name
    :return: entropy list
    """
    clustNum = len(set(clustNumSer))
    scoreLi = [0.0 for x in range(clustNum)]
    scoreCount = 0
    for currentClustCount in protClustObj.clustScoringObj.clustFeatureEntropySer.index.values:
        scoreLi[scoreCount] = protClustObj.clustScoringObj.clustFeatureEntropySer[currentClustCount][
                                  currentFeatureName] / protClustObj.clustScoringObj.featureEntropyDi[
                                  currentFeatureName]
        scoreCount += 1

    return scoreLi
