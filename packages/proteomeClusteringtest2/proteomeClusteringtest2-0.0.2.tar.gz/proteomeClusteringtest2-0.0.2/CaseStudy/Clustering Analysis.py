import numpy as np
import pandas as pd
from ProteomeClustering import DataAdapter
from ProteomeClustering import ClusteringMethod
from ProteomeClustering import Characterization
from ProteomeClustering import Statistics
from ProteomeClustering import Visualization
from ProteomeClustering import CaseStudy
from ProteomeClustering import Scoring
from ProteomeClustering.DataStructure import ds_InputRawData
from ProteomeClustering.DataStructure import ds_ProtClust
from scipy import stats
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics.cluster import v_measure_score

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from sklearn import metrics
from pandas.core.frame import DataFrame
import random


def MakeClusterResultCsvIntoObject(path='../../pathway_ontology_analysis/clustering_data/differentfilter_4/filter1.csv'):
    '''
    use csv file as a clustering result
    :param path:
    :return:
    '''
    protClustObj = ds_ProtClust()

    protClustObj.clustResultObj.sampleClustSer = pd.read_csv(path, header=None, index_col=0)

    protClustObj.clustResultObj.sampleClustSer = protClustObj.clustResultObj.sampleClustSer.iloc[:, 0]
    print(protClustObj.clustResultObj.sampleClustSer)
    return protClustObj

def SampleOverlap(resampleTimes=30):
    """
    find
    :param resampleTimes: the number to run clustering, to find the 5 similar clustering we want
    :return:
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    successCount = 0
    protClustObj = DataAdapter.LoadProtClustObj("consensusProtClust.pkl")
    protClustObj1 = [ds_ProtClust() for x in range(resampleTimes)]
    # protClustObj2 = [ds_ProtClust() for x in range(resampleTimes)]
    for num1 in range(resampleTimes):
        protClustObj1[num1].clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
                                                   covType='full')
        # protClustObj1[num1].clustParamObj.SetParam(method="hierarchicalClust", linkage="ward",
        #                                    distance="euclidean", clustNum=5)

        # protClustObj1[num1].clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_sklearn",
        #                                           clustNum=5, resample=0.8, minK=5, maxK=6, resample_times=10,
        #                                           ccDistance='euclidean')
        protClustObj1[num1] = ClusteringMethod.Clustering(protDataObj, protClustObj1[num1])

        print(adjusted_rand_score(protClustObj1[num1].clustResultObj.sampleClustSer.tolist(),
                                  protClustObj.clustResultObj.sampleClustSer.tolist()))

        ratioTable = Visualization.FindSampleOverlapHeatmap(protClustObj, protClustObj1[num1])
        xAxisLi = [x for x in range((len(ratioTable)))]
        yAxisLi = [x for x in range((len(ratioTable)))]

        if _IsPassOverLapBar(xAxisLi, yAxisLi, ratioTable) & _IsPassSampleNumBar(protClustObj1[num1]):
            successCount += 1
            sns.heatmap(ratioTable, cmap="Reds", linewidths=.5, annot=True, xticklabels=[x for x in set(xAxisLi)],
                        yticklabels=[x for x in set(yAxisLi)], vmin=0, vmax=1, cbar=False)
            plt.savefig("fig/successSampleOverlap" + str(successCount) + ".png")
            plt.cla()
            protClustObj1[num1].clustResultObj.sampleClustSer.to_csv("fig/PassOverLap" + str(successCount) + "_1.csv")
            DataAdapter.DumpProtClustObj(protClustObj1[num1], "fig/PassOverLap" + str(successCount) + "_1.pkl")
            # protClustObj2[num1].clustResultObj.sampleClustSer.to_csv("fig/PassOverLap" + str(successCount) + "_2.csv")
            # DataAdapter.DumpProtClustObj(protClustObj2[num1], "fig/PassOverLap" + str(successCount) + "_2.pkl")


def _IsPassOverLapBar(xAxisLi, yAxisLi, ratioTable, OverlapBar=0.4):
    """
    to test if each cluster has the similarity >overlapBar(default=0.3)
    :param xAxisLi:
    :param yAxisLi:
    :param ratioTable:
    :param OverlapBar:
    :return:
    """
    if not xAxisLi or not yAxisLi:
        return True
    sampleOverlapScore = 0
    tempI = -1
    tempK = -1
    for i in xAxisLi:

        for k in yAxisLi:
            if ratioTable[i][k] > sampleOverlapScore:
                sampleOverlapScore = ratioTable[i][k]
                tempI = i
                tempK = k
    ####
    if sampleOverlapScore <= OverlapBar:
        return False
    xAxisLi.remove(tempI)
    yAxisLi.remove(tempK)
    return _IsPassOverLapBar(xAxisLi, yAxisLi, ratioTable)


def _IsPassSampleNumBar(protClustObj, SampleNumBar=8):
    """
    to test if each cluster has enough samples(default>8)
    :param protClustObj:
    :param SampleNumBar:
    :return:
    """
    sampleLi1 = protClustObj.clustResultObj.sampleClustSer.tolist()
    for i in set(sampleLi1):
        count = 0
        for k in range(len(sampleLi1)):
            if sampleLi1[k] == i:
                count += 1
        print(count)
        if count < SampleNumBar:
            return False
    return True



def DifferentKmeansClusteringTest(resampleTimes=30,
                                  kmeanclusterfile="KmeansClusterFile.csv"):
    '''
    runt same clustering method multiple times to see if the clustering method is stable
    :param resampleTimes:
    :param kmeanclusterfile:
    :return:
    '''
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)


    ARITable = pd.DataFrame([[0.0 for x in range(resampleTimes)]] * resampleTimes)
    MaskTable = pd.DataFrame([[True for x in range(resampleTimes)]] * resampleTimes)
    logProtObj = [ds_ProtClust() for x in range(resampleTimes)]
    giniLi = [0.0 for x in range(resampleTimes)]

    gct = open(kmeanclusterfile, 'w')
    for num1 in range(resampleTimes):
        seed = random.randint(1, 100000)

        # logProtObj[num1].clustParamObj.SetParam(method="kmeansClust_sklearn", clustNum=5,
        #                                        seed=seed)
        #logProtObj[num1+15].clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
        #                                        covType='full')

        logProtObj[num1].clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_nltk",
                                                clustNum=5, resample=0.8, minK=5, maxK=6, resample_times=100,
                                                ccDistance='euclidean')

        logProtObj[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj[num1])
        Scoring.CalcGiniScore(protDataObj, logProtObj[num1])
        giniLi[num1] = logProtObj[num1].clustScoringObj.giniScore
        gct.writelines(str(logProtObj[num1].clustResultObj.sampleClustSer.tolist()) + '\n')

    gct.close()

    ariScatterLi = []
    giniScatterLi = []
    histogramLi = []

    num2 = 0
    for num1 in range(resampleTimes):

        for num2 in range(num1):
            score = adjusted_rand_score(logProtObj[num1].clustResultObj.sampleClustSer.tolist()
                                        , logProtObj[num2].clustResultObj.sampleClustSer.tolist())
            ariScatterLi.append(score)
            giniScatterLi.append(_ChooseLargeGini(giniLi, num1, num2))
            ARITable[num1][num2] = score
            MaskTable[num1][num2] = False
            histogramLi.append(score)

    '''
    ### histogram of ARI and Gini Score
    sns.distplot(histogramLi, bins=5, hist_kws=dict(edgecolor="black", linewidth=2))
    plt.xlim(0, 1.0)
    plt.show()
    sns.distplot(giniLi, bins=5, hist_kws=dict(edgecolor="black", linewidth=2))
    plt.xlim(0, 1.0)
    plt.show()
    '''

    '''
    ### heatmap of resample times ari
    # fig, axes = plt.subplots(1, 1, figsize=(50, 50))
    # sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, vmax=1, ax=axes)
    # g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, vmax=1, fmt='.2f', xticklabels=1, yticklabels=1)
    # fig.savefig('differentkmeans.png', dpi=300)
    # g.set(xticklabels=[x for x in range(1, resampleTimes+1)],yticklabels=[x for x in range(1, resampleTimes+1)])
    # plt.show()
    # print(ARITable)
    '''
    '''
    ### scatter plot of gini and ARI Score
    fig, axes = plt.subplots(1, 1, dpi=300)
    scatterDataDf = pd.DataFrame(list(zip(ariScatterLi, giniScatterLi)), columns=['ARI', 'Average Gini Score'])
    sns.scatterplot(x='ARI', y='Average Gini Score', data=scatterDataDf, ax=axes)
    axes.set_xlim([0, 1])
    axes.set_ylim([0, 1])

    fig.savefig('Con100 30Scatter.png')
    '''

def _ChooseLargeGini(giniLi, num1, num2):
    '''
    if giniLi[num1]<= giniLi[num2]:
        return giniLi[num2]
    else:
        return giniLi[num1]
    to draw a scatter plot of gini and ari needs to calculate average gini score
    '''
    return (giniLi[num1] + giniLi[num2]) / 2


def DifferentFilterClusteringTest(filterLi=None, kmeanclusterfile="FilterClusterFile.csv"):
    """

    :param filterLi:
    :param kmeanclusterfile:
    :return:
    """

    if filterLi is None:
        filterLi = [
            # ['cutoff','MAD', 0.5], ['cutoff','MAD', 0.75],['cutoff','MAD',0.9],['cutoff','MAD', 1.0],
            # ['cutoff', 'SD',0.5], ['cutoff','SD', 0.75],['cutoff','SD',0.9],['cutoff','SD', 1.0],
            # ['rank','MAD', 400], ['rank','MAD', 600], ['rank','MAD', 800], ['rank','MAD', 1000], ['rank','MAD', 1200],
            ['rank', 'SD', 400], ['rank', 'SD', 600], ['rank', 'SD', 800], ['rank', 'SD', 1000], ['rank', 'SD', 1200]
        ]

    SD = ['400', '600', '800', '1000', '1200']

    geneNumDf = pd.DataFrame({"MAD": SD, 'geneNum': [0 for x in range(len(filterLi))]})

    rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")

    # print(nonlogDataObj.GetProtRatioDf(filter=1))

    ARITable = pd.DataFrame([[0.0 for x in range(len(filterLi))]] * len(filterLi))
    logProtObj = [ds_ProtClust() for x in range(len(filterLi))]
    MaskTable = pd.DataFrame([[True for x in range(len(filterLi))]] * len(filterLi))

    gct = open(kmeanclusterfile, 'w')
    num1 = 0
    for func, method, cutoff in filterLi:

        if func == 'cutoff':
            rawDataObj = DataAdapter.FilterByCutoff(rawDataObj, method=method, cutOff=cutoff)

        elif func == 'rank':
            rawDataObj = DataAdapter.FilterByRank(rawDataObj, method=method, topNum=cutoff)

        rawDataObj.GetProtRatioDf().to_csv(func + method + str(cutoff) + ".csv")

        logProtObj[num1].clustParamObj.SetParam(method="consensusClustering", ccMethod="kmeans",
                                                clustNum=5, resample=0.9, minK=5, maxK=9, resample_times=1000)

        logProtObj[num1] = ClusteringMethod.clustering(rawDataObj, logProtObj[num1])
        geneNumDf['geneNum'][num1] = len(rawDataObj.GetProtRatioDf().columns.values)

        gct.writelines(str(logProtObj[num1].clustResultObj.sampleClustSer.tolist()) + '\n')

        num1 += 1

    gct.close()

    smallScore = 100.0
    number1 = 0
    number2 = 0
    histogramLi = []
    for num1 in range(len(filterLi)):

        for num2 in range(len(filterLi)):
            score = adjusted_rand_score(logProtObj[num1].clustResultObj.sampleClustSer.tolist()
                                        , logProtObj[num2].clustResultObj.sampleClustSer.tolist())
            ARITable[num1][num2] = score
            histogramLi.append(score)
            MaskTable[num1][num2] = False
            if score < smallScore:
                smallScore = score
                number1 = num1 + 1
                number2 = num2 + 1

    # show gene numbers barchart, distribution histogram and overlap heatmap

    sns.barplot(x="MAD", y='geneNum', data=geneNumDf)
    plt.show()
    sns.distplot(histogramLi)
    plt.show()
    sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, vmax=1, xticklabels=SD,
                yticklabels=SD)
    print(smallScore, number1, number2)
    plt.show()
    print(ARITable)


def silhouettePlotTest():
    rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")

    rawDataObj = DataAdapter.FilterByCutoff(rawDataObj, methodStr='MAD', cutOff=0.5)


    # protClustObj=GetSampleClust(protClustObj)
    #protClustObj.clustResultObj.sampleClustSer = pd.read_csv("kmeans1.csv", index_col=0, header=None)
    #protClustObj.clustResultObj.sampleClustSer = protClustObj.clustResultObj.sampleClustSer.iloc[:, 0]

    # protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="average",
    #                                   distance="euclidean", clustNum=5)
    # protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_nltk",
    #                                       clustNum=5, resample=0.8, minK=5, maxK=5, resample_times=1000,
    #                                       ccDistance='pcc')
    # protClustObj = ClusteringMethod.Clustering(rawDataObj, protClustObj)
    protClustObj2 = DataAdapter.LoadProtClustObj("hierarchical_cos_complete.pkl")
    protClustObj = DataAdapter.LoadProtClustObj("new.pkl")
    # protClustObj = DataAdapter.LoadProtClustObj("fig/dif_clust/consensus_nltk_euclidean.pkl")
    # print(protClustObj.clustResultObj.sampleClustSer.tolist())
    print(adjusted_rand_score(protClustObj2.clustResultObj.sampleClustSer.tolist()
                              , protClustObj.clustResultObj.sampleClustSer.tolist()))
    # protClustObj1 = DataAdapter.LoadProtClustObj("PassOverLap1_1.pkl")
    # protClustObj2 = DataAdapter.LoadProtClustObj("PassOverLap1_2.pkl")

    # compute silhouette_score
    Scoring.CalcEveryScore(rawDataObj, protClustObj2)

    # Scoring.CalcSampleSilhScore(rawDataObj, protClustObj)
    # Scoring.CalcSilhScore(rawDataObj, protClustObj)
    # Scoring.CalcClustSilhScore(rawDataObj, protClustObj)
    '''
    # print scoring results
    #print("partitionIndex: "+protClustObj.clustScoringObj.partitionIndex)
    #print("separationIndex: " + protClustObj.clustScoringObj.separationIndex )
    #print("silhScore: " + protClustObj.clustScoringObj.silhScore)
    print("purity: " + str(protClustObj.clustScoringObj.purity))
    print("separation index: "+str(protClustObj.clustScoringObj.separationIndex))
    print("giniScore: " + str(protClustObj.clustScoringObj.giniScore))
    print("silhScore: " + str(protClustObj.clustScoringObj.silhScore))
    print("clustSilhScoreSer: " + str(protClustObj.clustScoringObj.clustSilhScoreSer))
    print("sampleSilhScoreSer: " + str(protClustObj.clustScoringObj.sampleSilhScoreSer))
    print("featureAriDi: " + str(protClustObj.clustScoringObj.featureAriDi))
    print("featureAmiDi: " + str(protClustObj.clustScoringObj.featureAmiDi))
    print("featureEntropyDi: " + str(protClustObj.clustScoringObj.featureEntropyDi))
    print("featureMaxFscoreDi: " + str(protClustObj.clustScoringObj.featureMaxFscoreDi))
    print("featureVscoreDi: " + str(protClustObj.clustScoringObj.featureVscoreDi))
    print("featurePairedFscoreDi: " + str(protClustObj.clustScoringObj.featurePairedFscoreDi))
    '''

    # draw sihouette plot
    Visualization.DrawSilhouettePlot(rawDataObj, protClustObj2)


def DifferentClusteringResult(differentclusterfile="fig/dif_clust/DifferentClusterFile.csv"):
    """
    run different clustering methods listed in csv file and save them as .pkl files
    :param differentclusterfile:
    :return:
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    parameter = pd.read_csv('different clustering result parameter.csv', header=None, index_col=0)

    parameter = parameter.T
    parameter.reset_index(drop=True, inplace=True)
    print(parameter['linkage'])
    print(parameter)

    resultCount = len(parameter['method'])
    protClustObj = [ds_ProtClust() for x in range(resultCount)]
    for num in range(resultCount):
        ##protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="average",
        #                                    distance="euclidean", clustNum=5)
        protClustObj[num].clustParamObj.SetParam(method=parameter['method'][num], distance=parameter['distance'][num],
                                                 ccMethod=parameter['ccMethod'][num], linkage=parameter['linkage'][num],
                                                 clustNum=5, resample=float(parameter['resample'][num]),
                                                 resample_times=int(parameter['resample_times'][num])
                                                 , minK=5, maxK=5, ccDistance=parameter['ccDistance'][num]
                                                 , ccLinkage=parameter['ccLinkage'][num])

        # protClustObj.clustParamObj.SetParam(method="selfOrganizingMapClust", dimension=5,
        #                                   clustNum=5, learnRate=0.1, sigma=3, epochNum=800)
        protClustObj[num] = ClusteringMethod.Clustering(protDataObj, protClustObj[num])

        DataAdapter.DumpProtClustObj(protClustObj[num], _NameDifferentClusteringResult(parameter, num))
        gct = open(differentclusterfile, 'a')
        gct.writelines(str(protClustObj[num].clustResultObj.sampleClustSer.tolist())[1:-1] + '\n')

        gct.close()


def DifferentClusteringResult_giniARIScatterPlot():
    """
    use .pkl files to draw histogram, scatterplot and heatmap
    :return:
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    parameter = pd.read_csv('different clustering result parameter.csv', header=None, index_col=0)

    parameter = parameter.T
    parameter.reset_index(drop=True, inplace=True)
    resultCount = len(parameter['method'])
    # DataAdapter.DumpProtClustObj(protClustObj, "hierarchicalProtClust.pkl")
    # DataAdapter.DumpRawDataObj(protDataObj, "RawData.pkl")

    ARITable = pd.DataFrame([[0.0 for x in range(resultCount)]] * resultCount)
    MaskTable = pd.DataFrame([[True for x in range(resultCount)]] * resultCount)
    logProtObj = [ds_ProtClust() for x in range(resultCount)]
    giniLi = [0.0 for x in range(resultCount)]

    for num1 in range(resultCount):
        logProtObj[num1] = DataAdapter.LoadProtClustObj(_NameDifferentClusteringResult(parameter, num1))
        Scoring.CalcGiniScore(protDataObj, logProtObj[num1])
        giniLi[num1] = logProtObj[num1].clustScoringObj.giniScore

    ariScatterLi = []
    giniScatterLi = []
    histogramLi = []

    for num1 in range(resultCount):

        for num2 in range(num1):
            score = adjusted_rand_score(logProtObj[num1].clustResultObj.sampleClustSer.tolist()
                                        , logProtObj[num2].clustResultObj.sampleClustSer.tolist())
            if score < 0.05:
                score = 0.00
            ariScatterLi.append(round(score, 2))
            giniScatterLi.append(_ChooseLargeGini(giniLi, num1, num2))
            ARITable[num1][num2] = round(score, 2)
            MaskTable[num1][num2] = False
            histogramLi.append(score)

    sns.distplot(histogramLi, bins=5, hist_kws=dict(edgecolor="black", linewidth=2))
    print(len(histogramLi))
    plt.xlim(0, 1.2)
    plt.show()
    sns.distplot(giniLi, bins=4, hist_kws=dict(edgecolor="black", linewidth=2))
    plt.xlim(0, 1.0)
    plt.show()
    # plt.show()
    print(ARITable)
    # fig, axes = plt.subplots(1, 1, dpi=300)
    # scatterDataDf = pd.DataFrame(list(zip(ariScatterLi,giniScatterLi)), columns=['ari', 'average gini'])
    # sns.scatterplot(x='ari', y='average gini', data=scatterDataDf, ax=axes)
    g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmax=1, fmt='.2f', xticklabels=1,
                    yticklabels=1)
    g.set(xticklabels=[x for x in range(1, resultCount + 1)], yticklabels=[x for x in range(1, resultCount + 1)])
    plt.show()
    # axes.set_xlim([0,1])
    # axes.set_ylim([0, 1])
    # axes.set_xticklabels([x for x in range(1, resultCount)])
    # axes.set_yticklabels([x for x in range(1,resultCount)])
    # fig.savefig('fig/dif_clust/difClust_scatergini.png')


def DifferentClusteringResult_separationGiniScatterPlot():
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    parameter = pd.read_csv('different clustering result parameter.csv', header=None, index_col=0)

    parameter = parameter.T
    parameter.reset_index(drop=True, inplace=True)
    resultCount = len(parameter['method'])
    # DataAdapter.DumpProtClustObj(protClustObj, "hierarchicalProtClust.pkl")
    # DataAdapter.DumpRawDataObj(protDataObj, "RawData.pkl")
    nameLi = []

    logProtObj = [ds_ProtClust() for x in range(resultCount)]
    silhoLi = [0.0 for x in range(resultCount)]
    separationLi = [0.0 for x in range(resultCount)]
    giniLi = [0.0 for x in range(resultCount)]

    for num1 in range(resultCount):
        logProtObj[num1] = DataAdapter.LoadProtClustObj(_NameDifferentClusteringResult(parameter, num1))
        Scoring.CalcSeparationIndex(protDataObj, logProtObj[num1])
        separationLi[num1] = round(logProtObj[num1].clustScoringObj.separationIndex, 3)
        Scoring.CalcSilhScore(protDataObj, logProtObj[num1])
        silhoLi[num1] = round(logProtObj[num1].clustScoringObj.silhScore, 3)
        Scoring.CalcGiniScore(protDataObj, logProtObj[num1])
        giniLi[num1] = round(logProtObj[num1].clustScoringObj.giniScore, 3)
        nameLi.append(_NameDifferentClusteringResult(parameter, num1).split("/", 2)[2].split(".", 1)[0])

    sns.distplot(separationLi, bins=5, hist_kws=dict(edgecolor="black", linewidth=2))
    plt.xlim(0, 1.0)
    plt.show()
    sns.distplot(silhoLi, bins=5, hist_kws=dict(edgecolor="black", linewidth=2))
    plt.show()
    '''
    shortNameDf = pd.read_csv('shorthand name list.csv', header=None)
    sihouDf = DataFrame({'name':shortNameDf[1],'Silhouette Score':silhoLi})
    #giniDf = DataFrame({'name': shortNameDf[1], 'Gini Score': giniLi})
    #giniDf = giniDf.sort_values(by=['Gini Score'])
    sihouDf = sihouDf.sort_values(by=['Silhouette Score'])
    fig, axes = plt.subplots(1, 1, dpi=300)
    #sns.barplot(y='name',x='Gini Score',data=giniDf,ax=axes)
    sns.barplot(y='name', x='Silhouette Score', data=sihouDf, ax=axes)
    axes.set_yticklabels(sihouDf['name'], fontdict={'fontsize':5.0})
    #fig.savefig('fig/dif_clust/difClust_giniBarplot.png')
    fig.savefig('fig/dif_clust/difClust_silhouetteBarplot.png')


    #print("test: "+str(stats.mannwhitneyu(histogramLi,[0.96,1],use_continuity=False, alternative='two-sided')))
    #sns.distplot(giniLi)
    #plt.show()
    #sns.distplot(silhoLi, bins=5, hist_kws=dict(edgecolor="black", linewidth=2))
    #plt.show()
    fig, axes = plt.subplots(1, 1, dpi=300)
    scatterDataDf = pd.DataFrame(list(zip(silhoLi,giniLi)), columns=['Silhouette Score', 'Gini Score'])
    sns.scatterplot(x='Silhouette Score', y='Gini Score', data=scatterDataDf, ax=axes)
    #axes.set_xlim([0,1])
    axes.set_ylim([0, 1])

    fig.savefig('fig/dif_clust/difClust_separationGiniScatter.png')
    print(giniLi)
    print(silhoLi)
    #pd.Series(nameLi).to_csv('n.csv')
    '''


def PCA_TSNETEST():
    """
    find
    :param resampleTimes: the number to run clustering, to find the 5 similar clustering we want
    :return:
    """
    rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")

    rawDataObj = DataAdapter.FilterByCutoff(rawDataObj, methodStr='MAD', cutOff=0.5)
    # clust1 = DataAdapter.LoadProtClustObj('new.pkl')
    # clust2 = DataAdapter.LoadProtClustObj('hierarchical_cos_complete.pkl')
    clust1 = ds_ProtClust()
    clust2 = ds_ProtClust()
    clust1.clustResultObj.sampleClustSer = pd.read_csv(
        '../../pathway_ontology_analysis/clustering_data/differentfilter_4/filter1.csv', header=None, index_col=0)
    clust2.clustResultObj.sampleClustSer = pd.read_csv(
        '../../pathway_ontology_analysis/clustering_data/differentfilter_4/filter2.csv', header=None, index_col=0)
    clust2.clustResultObj.sampleClustSer = clust2.clustResultObj.sampleClustSer.iloc[:, 0]
    clust1.clustResultObj.sampleClustSer = clust1.clustResultObj.sampleClustSer.iloc[:, 0]

    # protClustObj2 = DataAdapter.LoadProtClustObj("consensusProtClust.pkl")
    # protClustObj = DataAdapter.LoadProtClustObj("hierarchicalProtClust.pkl")
    # protClustObj = DataAdapter.LoadProtClustObj("hierarchical_cos_complete.pkl")
    # protClustObj = DataAdapter.LoadProtClustObj("PassOverLap1_1.pkl")
    # print(protClustObj.clustResultObj.sampleClustSer.tolist())
    print(adjusted_rand_score(clust1.clustResultObj.sampleClustSer.tolist()
                              , clust2.clustResultObj.sampleClustSer.tolist()))
    # protClustObj1 = DataAdapter.LoadProtClustObj("PassOverLap1_1.pkl")
    # protClustObj2 = DataAdapter.LoadProtClustObj("PassOverLap1_2.pkl")

    # compute silhouette_score

    # Scoring.CalcEveryScore(rawDataObj, protClustObj)
    Visualization.PlotPca(rawDataObj, clust1, dpi=300, path='fig/MADTOP400_PCA.png')
    Visualization.PlotPca(rawDataObj, clust2, dpi=300, path='fig/MADTOP1200_PCA.png',
                          colorLi=['#9467bd', '#d62728', '#2ca02c', '#1f77b4', '#ff7f0e'])
    '''
    for count in range(1, 100):
        Visualization.PlotTsne(rawDataObj, protClustObj, dpi=300, perplexity=8,
                               path='fig/goterm/0.26/gaussian/gaussianTSNE_'+str(count)+'.png')
    #ratioTable = Visualization.FindSampleOverlapHeatmap(protClustObj, protClustObj1)
    #DataAdapter.DumpProtClustObj(protClustObj1, 'hierarchical_cos_complete.pkl')

    ##   '#d62728' red, '#9467bd' purple, '#2ca02c' green,'#1f77b4' blue, '#ff7f0e'orange
    '''



def TestConHierarchicalInstability():
    # parameter = pd.read_csv('TestConHierarchicalInstability.csv', header=None, index_col=0)
    parameter = pd.read_csv('TestConHCpccInstability.csv', header=None, index_col=0)
    parameter = parameter.T
    parameter.reset_index(drop=True, inplace=True)
    print(parameter['linkage'])
    print(parameter)

    resultCount = len(parameter['resample'])

    for num in range(resultCount):
        TestConHierachical(float(parameter['resample'][num]), int(parameter['resample_times'][num]),
                           parameter['ccDistance'][num], parameter['ccLinkage'][num])


def TestConHierachical(resam, resample_times, ccDistance, ccLinkage, resample=30):
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    protClustObj = [ds_ProtClust() for x in range(resample)]
    ARITable = pd.DataFrame([[0.0 for x in range(resample)]] * resample)
    MaskTable = pd.DataFrame([[True for x in range(resample)]] * resample)
    # conprotObj = DataAdapter.LoadProtClustObj('fig/dif_clust/hierarchical_euclidean_complete.pkl')
    # conprotObj =[ds_ProtClust() for x in range(resample)]

    for i in range(resample):
        protClustObj[i].clustParamObj.SetParam(method="consensusClust", clustNum=5, ccMethod='hierarchicalClust',
                                               minK=5, maxK=5,
                                               resample=resam, resample_times=resample_times, ccDistance=ccDistance,
                                               ccLinkage=ccLinkage)
        protClustObj[i] = ClusteringMethod.Clustering(protDataObj, protClustObj[i])

        # conprotObj[i].clustParamObj.SetParam(method="hierarchicalClust", clustNum=5, minK=5,
        #                                     maxK=5, distance='pcc', linkage='average')
        # conprotObj[i] = ClusteringMethod.Clustering(protDataObj, conprotObj[i])
    # protClustObj.clustResultObj.sampleClustSer.to_csv("SOMresult.csv")
    # DataAdapter.DumpProtClustObj(protClustObj, "SOMProtClust.pkl")
    # print(adjusted_rand_score(
    #        conprotObj.clustResultObj.sampleClustSer.tolist(),
    #        protClustObj[i].clustResultObj.sampleClustSer.tolist()))

    # Scoring.CalcGiniScore(protDataObj, protClustObj)
    # print("gini: "+str(protClustObj.clustScoringObj.giniScore))

    for num1 in range(resample):
        for num2 in range(num1):
            score = adjusted_rand_score(
                protClustObj[num1].clustResultObj.sampleClustSer.tolist(),
                protClustObj[num2].clustResultObj.sampleClustSer.tolist())
            ARITable[num1][num2] = round(score, 2)
            MaskTable[num1][num2] = False

    fig, ax = plt.subplots(figsize=(18, 10))
    g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, fmt='.2f',
                    xticklabels=1, yticklabels=1, vmax=1, ax=ax)
    # plt.show()
    g.set(xticklabels=[x for x in range(1, resample + 1)], yticklabels=[x for x in range(1, resample + 1)])

    # fig.savefig('fig/conHierarchical/'+str(resam)+'_'+str(resample_times)+'_'+ccDistance+'_'+ccLinkage+'.png',dpi=300)
    fig.savefig(
        'fig/conHierarchical/pcc/' + str(resam) + '_' + str(
            resample_times) + '_' + ccDistance + '_' + ccLinkage + '.png',
        dpi=300)
    # fig.cla()


def ConHCpccCompare():
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")

    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = [ds_ProtClust() for x in range(3)]
    protClustObj[0] = DataAdapter.LoadProtClustObj("fig/dif_clust/consensus_hierarchical_pcc_average.pkl")
    protClustObj[1] = DataAdapter.LoadProtClustObj("fig/dif_clust/consensus_hierarchical_pcc_complete.pkl")
    protClustObj[2] = DataAdapter.LoadProtClustObj("fig/dif_clust/consensus_hierarchical_pcc_single.pkl")

    #####   compute and draw ARI heatmap
    ARITable = pd.DataFrame([[0.0 for x in range(len(protClustObj))]] * len(protClustObj))
    MaskTable = pd.DataFrame([[True for x in range(len(protClustObj))]] * len(protClustObj))
    giniLi = [0.0 for x in range(3)]
    for num1 in range(len(protClustObj)):

        for num2 in range(num1):
            score = adjusted_rand_score(protClustObj[num1].clustResultObj.sampleClustSer.tolist()
                                        , protClustObj[num2].clustResultObj.sampleClustSer.tolist())

            if score < 0.05:
                score = 0.00
            ARITable[num1][num2] = score
            MaskTable[num1][num2] = False
        Scoring.CalcGiniScore(protDataObj, protClustObj[num1])
        giniLi[num1] = round(protClustObj[num1].clustScoringObj.giniScore, 3)
    '''
    ### draw ari heatmap
    #g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmax=1, fmt='.2f', xticklabels=1,
    #                yticklabels=1)
    #g.set(xticklabels=['average','complete','single'], yticklabels=['average','complete','single'])
    #plt.show()

    ### draw pca
    for num1 in range(len(protClustObj)):
        Visualization.PlotPca(protDataObj, protClustObj[num1], dpi=300, path='fig/conHierarchical/pcc/'+str(num1+1)+'.png')


    giniDf = DataFrame({'Cluster Method': ['ConHC_pcc_aver','ConHC_pcc_comp','ConHC_pcc_single'], 'Gini Score': giniLi})
    giniDf = giniDf.sort_values(by=['Gini Score'])
    fig, axes = plt.subplots(1, 1, dpi=300)
    sns.barplot(x='Cluster Method', y='Gini Score', data=giniDf, ax=axes)
    axes.set_xticklabels(giniDf['Cluster Method'])

    fig.savefig('fig/conHierarchical/pcc/gini Barplot.png')
    '''
    ### draw sampleoverlap heatmap
    # for num1 in range(len(protClustObj)-1):
    Visualization.FindSampleOverlapHeatmap(protClustObj[0], protClustObj[1],
                                           path='fig/conHierarchical/pcc/sampleoverlap_ConHC_average_complete.png',
                                           dpi=300)

    #######


def _NameDifferentClusteringResult(parameter, num):
    if parameter['method'][num] == 'hierarchicalClust':
        return 'fig/dif_clust/hierarchical_' + parameter['distance'][num] + '_' + parameter['linkage'][num] + '.pkl'
    elif parameter['method'][num] == 'consensusClust':
        if parameter['ccMethod'][num] == 'hierarchicalClust':
            return 'fig/dif_clust/consensus_hierarchical_' + parameter['ccDistance'][num] + '_' + \
                   parameter['ccLinkage'][num] + '.pkl'
        else:
            return 'fig/dif_clust/consensus_nltk_' + parameter['ccDistance'][num] + '.pkl'


def GoTermVennTest(path1, path2, subtype1, subtype2, process="biological", figPath='fig/GoTermVenn/0.7/'):
    node1 = path1 + '/cluster' + str(subtype1) + "_up/" + process + "/cluster" + str(subtype1) + "up.txt"
    node2 = path2 + '/cluster' + str(subtype2) + "_up/" + process + "/cluster" + str(subtype2) + "up.txt"
    return CaseStudy.DrawGoTermOverlapVenn(node1, node2, figPath + str(subtype1) + '_' + str(subtype2) + '.png')





def GSEATest():
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")

    rawDataObj = DataAdapter.FilterByCutoff(protDataObj, method='MAD', cutOff=0.5)

    Statistics.GenerateGctFile(protDataObj, path='GSEAGeneTable.gct')

    protClustObj = ds_ProtClust()

    protClustObj.clustParamObj.SetParam(filter="median", method="hierarchical", linkage="ward",
                                        distance="euclidean", clustNum=5)

    protClustObj = ClusteringMethod.clustering(rawDataObj, protClustObj)

    Statistics.GenerateClsFile(protClustObj)
    # protClustObj.clustResultObj.sampleClustSer.to_csv ("colon_consensus.csv")

    # temp = protClustObj.clustResultObj.sampleClustSer.tolist ()

def GoTermTest(choseGoNum=10):
    upOrDown = "up"
    process = "biological"
    clustNum = 5
    # aabb=Characterization.findGoTermOverlap()
    CaseStudy.DrawGoTermHeatMap(goTerm1ClustLi=[1, 2, 3, 4, 5], goTerm2ClustLi=[1, 2, 3, 4, 5], choseGoNum=choseGoNum,
                                goTerm1Str="consensus nltk euclidean",
                                goTerm2Str="filtermad0.5_colon_hierachical_0.05", upOrDownStr=upOrDown,
                                processStr=process, clusterNum=clustNum, dpi=300)


def NetworkTest(sub=5):
    # for subtype in range(1, sub + 1):
    subtype1 = 4
    # subtype2 = 4
    node1 = "D:\pathway_ontology_analysis/network analysis/networkanalyst/consensus nltk euclidean/" + "consensus2_node_table.csv"
    node2 = "D:\pathway_ontology_analysis/network analysis/networkanalyst/hierarchical_cosine/" + "hierarchical4_node_table.csv"
    CaseStudy.DrawNetworkOverlapGeneVenn(node1, node2, subtype1, 5)
    CaseStudy.DrawNetworkOverlapGeneVenn(node1, node2, subtype1, 2)




