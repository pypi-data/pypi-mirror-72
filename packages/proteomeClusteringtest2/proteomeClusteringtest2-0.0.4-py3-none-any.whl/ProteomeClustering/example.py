# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 14:19:08 2019

@author: tea9262
"""
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet, fcluster
from scipy.spatial.distance import pdist
from matplotlib import pyplot as plt

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


def ScoringMethodTest():
    protRatioExample = pd.read_csv("Example/protRatio.csv", index_col=0)
    protMetaExample = pd.read_csv("Example/protMeta.csv", index_col=0)
    rawDataObj = ds_InputRawData(protRatioExample, protMetaExample)
    protClustObj = ds_ProtClust()

    protClustObj.clustParamObj.SetParam(filter="median", method="hierachical", clusterNum=5, linkage="single",
                                        distance="Euclidean")
    ##### Scoring function Example

    # V-score

    protClustObj = Scoring.CalcFeatureVscore(rawDataObj, protClustObj)

    print("protVscoreDi: ")
    print(protClustObj.clustScoringObj.featureVscoreDi)

    # F-score

    protClustObj = Scoring.CalcFeatureMaxFscore(rawDataObj, protClustObj)

    print("FeatureMaxFscoreDi: ")
    print(protClustObj.clustScoringObj.featureMaxFscoreDi)


def HierachicalClusteringTest():
    rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    rawDataObj = DataAdapter.FilterByCutoff(rawDataObj, methodStr='MAD', cutOff=0.5)
    print(rawDataObj.GetProtRatioDf())
    rawDataObj.GetProtRatioDf().to_csv("colon_ratio.csv")
    protClustObj = ds_ProtClust()

    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_sklearn",
                                        clustNum=5, resample=0.9, minK=5, maxK=6, resample_times=1000)
    # protClustObj.clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
    #                                    covType='full')
    # protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="average",
    #                                    distance="pcc", clustNum=5)
    protClustObj = ClusteringMethod.Clustering(rawDataObj, protClustObj)
    protClustObj.clustResultObj.sampleClustSer.to_csv("colon_consensus.csv")
    temp = protClustObj.clustResultObj.sampleClustSer.tolist()
    # save protclust and rawdata obj pickle files
    DataAdapter.DumpProtClustObj(protClustObj, "consensusProtClust.pkl")
    DataAdapter.DumpRawDataObj(rawDataObj, "consensusRawData.pkl")

    protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="ward",
                                        distance="euclidean", clustNum=5)
    # protClustObj.clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
    #                                    covType='spherical')
    # protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_nltk",
    # ccDistance='cosine', clustNum=5, resample=0.8, minK=5, maxK=6, resample_times=1000)
    protClustObj = ClusteringMethod.Clustering(rawDataObj, protClustObj)

    # save protclust and rawdata obj pickle files
    DataAdapter.DumpProtClustObj(protClustObj, "hierarchicalProtClust.pkl")
    DataAdapter.DumpRawDataObj(rawDataObj, "hierarchicalRawData.pkl")
    protClustObj.clustResultObj.sampleClustSer.to_csv("colon_hierachical.csv")
    print(v_measure_score(temp, protClustObj.clustResultObj.sampleClustSer.tolist()))
    print(adjusted_rand_score(temp, protClustObj.clustResultObj.sampleClustSer.tolist()))


def nonLogClusteringTest(distanceLinkageLi=None, path="Example/colonCancerProtRatio.csv"):
    if distanceLinkageLi is None:
        distanceLinkageLi = [['euclidean', 'ward'], ['manhattan', 'complete'], ['cosine', 'average']
            , ['euclidean', 'complete'], ['cosine', 'complete']]

    logRatio = pd.read_csv(path, index_col=0)
    nonlogRatio = np.power(2, logRatio)

    protMetaExample = pd.read_csv("Example/colonCancerMetadata.csv", index_col=0)
    logDataObj = ds_InputRawData(logRatio, protMetaExample)
    # logDataObj = DataAdapter.FilterByRank (logDataObj, method = 'SD', topNum=1600)
    logDataObj = DataAdapter.FilterByCutoff(logDataObj, method='MAD', cutOff=0.5)
    logProtObj = ds_ProtClust()
    nonlogDataObj = ds_InputRawData(nonlogRatio, protMetaExample)
    nonlogDataObj = DataAdapter.FilterByCutoff(nonlogDataObj, method='MAD', cutOff=0.5)
    nonlogProtObj = ds_ProtClust()
    # print(logDataObj.GetProtRatioDf(filter=1))
    # print(nonlogDataObj.GetProtRatioDf(filter=1))

    ARITable = pd.DataFrame([[0.0 for x in range(len(distanceLinkageLi))]] * len(distanceLinkageLi))

    row = 0

    for dis, link in distanceLinkageLi:
        logProtObj.clustParamObj.SetParam(method="hierarchical", linkage=link,
                                          distance=dis, clustNum=5)

        logProtObj = ClusteringMethod.clustering(logDataObj, logProtObj)
        # print (logProtObj.clustResultObj.sampleClustSer)
        col = 0
        for dis2, link2 in distanceLinkageLi:
            nonlogProtObj.clustParamObj.SetParam(method="hierarchical", linkage=link2,
                                                 distance=dis2, clustNum=5)

            nonlogProtObj = ClusteringMethod.clustering(nonlogDataObj, nonlogProtObj)

            ARITable[row][col] = adjusted_rand_score(logProtObj.clustResultObj.sampleClustSer.tolist()
                                                     , nonlogProtObj.clustResultObj.sampleClustSer.tolist())
            # ARITable[row][col] = v_measure_score (logProtObj.clustResultObj.sampleClustSer.tolist ()
            #                                          , nonlogProtObj.clustResultObj.sampleClustSer.tolist ())

            col += 1
        row += 1
    sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True)

    plt.show()
    print(ARITable)


def VisualizationMethodTest():
    rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    rawDataObj = DataAdapter.FilterByCutoff(rawDataObj, method='MAD', cutOff=0.5)
    rawDataObj = DataAdapter.SortByRow(rawDataObj)
    rawDataObj = DataAdapter.SortByColumn(rawDataObj)
    # rawDataObj = DataAdapter.SortByColumn(rawDataObj)

    protClustObj = ds_ProtClust()

    # protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="ward", distance="euclidean", clustNum=5)

    # protClustObj.clustParamObj.SetParam (method="consensusClustering", ccMethod="kmeans",
    #                                     clustNum=5, resample=0.8, minK=5, maxK=6, resample_times=1000)
    protClustObj = ClusteringMethod.Clustering(rawDataObj, protClustObj)

    ### draw heatmap of protein ratio table and Patient To Patient Correlation heatmap
    # Visualization.DrawHeatMap (rawDataObj, protClustObj,path='ratioheatmap50.png')
    Visualization.DrawPatientToPatientCorrHeatmap(rawDataObj, protClustObj, path="sideHeatmap.png")

    ### draw combine figure, choose two metadata feature to compare, needs to count entropy first
    protClustObj = Scoring.CalcClustFeatureEntropy(rawDataObj, protClustObj)
    protClustObj = Scoring.CalcFeatureEntropy(rawDataObj, protClustObj)
    currentFeatureSer = rawDataObj.GetMetadataDf()['Stage']
    compareFeatureSer = rawDataObj.GetMetadataDf()['pathology_N_stage']
    # print(protClustObj.clustScoringObj.clustFeatureEntropySer)
    # print(protClustObj.clustScoringObj.featureEntropyDi)
    Visualization.DrawCombinedFig(protClustObj, currentFeatureSer, compareFeatureSer, pathStr='combinFig.png')

    ### draw scatterplot, stackedbar, divergebar , respectively
    Visualization.DrawDivergeBar(protClustObj, currentFeatureSer)
    Visualization.DrawStackedBar(protClustObj, currentFeatureSer)
    Visualization.DrawScatterPlot(protClustObj, currentFeatureSer, compareFeatureSer)

    ###draw MetaColorMap, show each samples' metadata feature

    labelLi = ['Gender', 'pathology_T_stage', 'pathology_N_stage', 'Stage', 'Integrated.Phenotype', 'CIN']
    Visualization.MetaColorMap(rawDataObj, protClustObj, selectFeatureSer=labelLi, path='meta_colorbar.png')


def GoTermTest(choseGoNum = 10):

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
        #subtype2 = 4
        node1 = "D:\pathway_ontology_analysis/network analysis/networkanalyst/consensus nltk euclidean/"+"consensus2_node_table.csv"
        node2 = "D:\pathway_ontology_analysis/network analysis/networkanalyst/hierarchical_cosine/"+ "hierarchical4_node_table.csv"
        CaseStudy.DrawNetworkOverlapGeneVenn(node1, node2, subtype1, 5)
        CaseStudy.DrawNetworkOverlapGeneVenn(node1, node2, subtype1, 2)


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
    #protClustObj2 = [ds_ProtClust() for x in range(resampleTimes)]
    for num1 in range(resampleTimes):
        protClustObj1[num1].clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
                                                   covType='full')
        #protClustObj1[num1].clustParamObj.SetParam(method="hierarchicalClust", linkage="ward",
        #                                    distance="euclidean", clustNum=5)


        #protClustObj1[num1].clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_sklearn",
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
                        yticklabels=[x for x in set(yAxisLi)], vmin=0, vmax=1,cbar=False)
            plt.savefig("fig/successSampleOverlap"+str(successCount)+".png")
            plt.cla()
            protClustObj1[num1].clustResultObj.sampleClustSer.to_csv("fig/PassOverLap"+str(successCount)+"_1.csv")
            DataAdapter.DumpProtClustObj(protClustObj1[num1], "fig/PassOverLap"+str(successCount)+"_1.pkl")
            #protClustObj2[num1].clustResultObj.sampleClustSer.to_csv("fig/PassOverLap" + str(successCount) + "_2.csv")
            #DataAdapter.DumpProtClustObj(protClustObj2[num1], "fig/PassOverLap" + str(successCount) + "_2.pkl")


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


def DifferentKmeansClusteringTest_conHC(resampleTimes=30,
                                 dis='single'):
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)



    ARITable = pd.DataFrame([[0.0 for x in range(resampleTimes)]] * resampleTimes)
    MaskTable = pd.DataFrame([[True for x in range(resampleTimes)]] * resampleTimes)
    logProtObj = [ds_ProtClust() for x in range(resampleTimes)]
    logProtObj2 = [ds_ProtClust() for x in range(resampleTimes)]
    logProtObj3 = [ds_ProtClust() for x in range(resampleTimes)]
    giniLi = [0.0 for x in range(resampleTimes)]
    silhoLi = [0.0 for x in range(resampleTimes)]
    separationLi = [0.0 for x in range(resampleTimes)]
    histogramLi = []


    for num1 in range(resampleTimes):
        #logProtObj[num1].clustParamObj.SetParam(method="kmeansClust_sklearn", clustNum=5,
        #                                        seed=seed)
        #logProtObj[num1].clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
        #                                        covType='full')
        #logProtObj[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj[num1])
        '''
        logProtObj[num1].clustParamObj.SetParam(method="consensusClust", minK=5, maxK=5, ccMethod='hierarchicalClust',
                                               ccDistance='pcc', ccLinkage='average', resample_times=1000,resample=0.8)
        logProtObj[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj[num1])

        logProtObj2[num1].clustParamObj.SetParam(method="consensusClust", minK=5, maxK=5, ccMethod='hierarchicalClust',
                                                ccDistance='pcc', ccLinkage='complete', resample_times=1000,
                                                resample=0.8)
        logProtObj2[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj2[num1])

        logProtObj3[num1].clustParamObj.SetParam(method="consensusClust", minK=5, maxK=5, ccMethod='hierarchicalClust',
                                                ccDistance='pcc', ccLinkage='single', resample_times=1000,
                                                resample=0.8)
        logProtObj3[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj3[num1])


        DataAdapter.DumpProtClustObj(logProtObj[num1],'fig/conHierarchical/re1000/average/conHC_pcc'+str(num1)+'.pkl')
        DataAdapter.DumpProtClustObj(logProtObj2[num1],
                                     'fig/conHierarchical/re1000/complete/conHC_pcc' + str(num1) + '.pkl')

        #

        '''
        # DataAdapter.DumpProtClustObj(logProtObj[num1],
        #                             'fig/instableKmeanGaussian/gaussian/full/' + str(num1) + '.pkl')
        logProtObj[num1] = DataAdapter.LoadProtClustObj(
            'fig/conHierarchical/re1000/' + dis + '/conHC_pcc' + str(num1) + '.pkl')
        Scoring.CalcSeparationIndex(protDataObj, logProtObj[num1])
        separationLi[num1] = logProtObj[num1].clustScoringObj.separationIndex
        Scoring.CalcSilhScore(protDataObj, logProtObj[num1])
        silhoLi[num1] = logProtObj[num1].clustScoringObj.silhScore
        Scoring.CalcGiniScore(protDataObj, logProtObj[num1])
        giniLi[num1] = logProtObj[num1].clustScoringObj.giniScore





    n, bins, patches = plt.hist(giniLi, bins=4, range=(0.7, 0.75), rwidth=0.9, weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.xticks([0.7,0.7125, 0.725,0.7375,0.75], fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Gini Index', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/conHierarchical/pcc/' + dis + '/gini'), bbox_inches='tight')
    print(n)
    plt.show()

    n, bins, patches = plt.hist(separationLi, bins=4, range=(0.38, 0.5), rwidth=0.9, weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.yticks(fontsize=16)
    plt.xticks([ 0.38, 0.41,0.44, 0.47, 0.5], fontsize=16)
    plt.xlabel('Separation Index', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/conHierarchical/pcc/' + dis + '/separation'),
                bbox_inches='tight')
    print(n)
    plt.show()

    n, bins, patches = plt.hist(silhoLi, bins=4, rwidth=0.9, range=(-0.02, 0.06), weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.yticks(fontsize=16)
    plt.xticks([ -0.02, 0, 0.02,0.04, 0.06], fontsize=16)
    plt.xlabel('Silhouette Score', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/conHierarchical/pcc/' + dis + '/silhouette'),
                bbox_inches='tight')
    print(n)
    plt.show()


def DifferentKmeansClusteringTest(resampleTimes=30,
                                  kmeanclusterfile="KmeansClusterFile.csv",dis='full'):
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    # print(protDataObj.GetProtRatioDf(filter=1))
    # print(nonlogDataObj.GetProtRatioDf(filter=1))
    protClustObj = ds_ProtClust()
    # protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="ward",
    #                                    distance="euclidean", clustNum=5)
    # protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)
    # protClustObj.clustResultObj.sampleClustSer.to_csv("colon_hierarchical.csv")
    # DataAdapter.DumpProtClustObj(protClustObj, "hierarchicalProtClust.pkl")
    # DataAdapter.DumpRawDataObj(protDataObj, "RawData.pkl")

    #consensus_nltkclusterfile = "consensus_nltkclusterfileClusterFile.csv"

    ARITable = pd.DataFrame([[0.0 for x in range(resampleTimes)]] * resampleTimes)
    MaskTable = pd.DataFrame([[True for x in range(resampleTimes)]] * resampleTimes)
    logProtObj = [ds_ProtClust() for x in range(resampleTimes)]
    logProtObj2 = [ds_ProtClust() for x in range(resampleTimes)]
    logProtObj3 = [ds_ProtClust() for x in range(resampleTimes)]
    giniLi = [0.0 for x in range(resampleTimes)]
    silhoLi = [0.0 for x in range(resampleTimes)]
    separationLi = [0.0 for x in range(resampleTimes)]
    histogramLi = []

    gct = open(kmeanclusterfile, 'w')
    for num1 in range(resampleTimes):

        #logProtObj[num1].clustParamObj.SetParam(method="kmeansClust_sklearn", clustNum=5,
        #                                        seed=seed)
        #logProtObj[num1].clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
        #                                        covType='full')
        #logProtObj[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj[num1])
        '''
        logProtObj[num1].clustParamObj.SetParam(method="consensusClust", minK=5, maxK=5, ccMethod='hierarchicalClust',
                                               ccDistance='pcc', ccLinkage='average', resample_times=1000,resample=0.8)
        logProtObj[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj[num1])

        logProtObj2[num1].clustParamObj.SetParam(method="consensusClust", minK=5, maxK=5, ccMethod='hierarchicalClust',
                                                ccDistance='pcc', ccLinkage='complete', resample_times=1000,
                                                resample=0.8)
        logProtObj2[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj2[num1])

        logProtObj3[num1].clustParamObj.SetParam(method="consensusClust", minK=5, maxK=5, ccMethod='hierarchicalClust',
                                                ccDistance='pcc', ccLinkage='single', resample_times=1000,
                                                resample=0.8)
        logProtObj3[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj3[num1])


        DataAdapter.DumpProtClustObj(logProtObj[num1],'fig/conHierarchical/re1000/average/conHC_pcc'+str(num1)+'.pkl')
        DataAdapter.DumpProtClustObj(logProtObj2[num1],
                                     'fig/conHierarchical/re1000/complete/conHC_pcc' + str(num1) + '.pkl')
        
        #

        '''
        #DataAdapter.DumpProtClustObj(logProtObj[num1],
        #                             'fig/instableKmeanGaussian/gaussian/full/' + str(num1) + '.pkl')
        logProtObj[num1] = DataAdapter.LoadProtClustObj(
            'fig/instableKmeanGaussian/gaussian/'+dis+'/' + str(num1) + '.pkl')
        Scoring.CalcSeparationIndex(protDataObj, logProtObj[num1])
        separationLi[num1] = logProtObj[num1].clustScoringObj.separationIndex
        Scoring.CalcSilhScore(protDataObj, logProtObj[num1])
        silhoLi[num1] = logProtObj[num1].clustScoringObj.silhScore
        Scoring. CalcGiniScore(protDataObj, logProtObj[num1])
        giniLi[num1] =  logProtObj[num1].clustScoringObj.giniScore
        gct.writelines(str(logProtObj[num1].clustResultObj.sampleClustSer.tolist()) + '\n')

    gct.close()

    num2 = 0
    for num1 in range(resampleTimes):

        for num2 in range(num1):
            score = adjusted_rand_score(logProtObj[num1].clustResultObj.sampleClustSer.tolist()
                                        , logProtObj[num2].clustResultObj.sampleClustSer.tolist())
            # ariScatterLi.append(score)
            # giniScatterLi.append(_ChooseLargeGini(giniLi, num1, num2))
            ARITable[num1][num2] = score
            MaskTable[num1][num2] = False
            histogramLi.append(score)

    n, bins, patches = plt.hist(histogramLi, bins=5, range=(0, 1), rwidth=0.9, weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Adjuested Rand Index', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/displot/instableKmeanGaussian/gaussian/'+dis+'/ari'), bbox_inches='tight')
    print(n)
    plt.show()

    
    n, bins, patches = plt.hist(giniLi, bins=6, range=(0, 0.6), rwidth=0.9, weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Gini Index', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/displot/instableKmeanGaussian/gaussian/'+dis+'/gini'), bbox_inches='tight')
    print(n)
    plt.show()

    n, bins, patches = plt.hist(separationLi, bins=4, range=(0.2, 0.6), rwidth=0.9, weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.yticks(fontsize=16)
    plt.xticks([0.2, 0.3, 0.4, 0.5, 0.6], fontsize=16)
    plt.xlabel('Separation Index', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/displot/instableKmeanGaussian/gaussian/'+dis+'/separation'), bbox_inches='tight')
    print(n)
    plt.show()

    n, bins, patches = plt.hist(silhoLi, bins=5, rwidth=0.9, range=(0, 0.15), weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.yticks(fontsize=16)
    plt.xticks([0, 0.03, 0.06, 0.09, 0.12,0.15], fontsize=16)
    plt.xlabel('Silhouette Score', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/displot/instableKmeanGaussian/gaussian/'+dis+'/silhouette'), bbox_inches='tight')
    print(n)
    plt.show()
    ariScatterLi = []
    giniScatterLi = []
    histogramLi = []

    


    '''
    #sns.distplot(histogramLi, bins=5, hist_kws=dict(edgecolor="black", linewidth=2))
    #plt.xlim(0, 1.0)
    #plt.show()
    #sns.distplot(giniLi, bins=5, hist_kws=dict(edgecolor="black", linewidth=2))
    #plt.xlim(0, 1.0)
    #plt.show()
    #sns.set(font_scale=2)
    fig, axes = plt.subplots(1, 1, figsize=(50, 50))
    #sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, vmax=1, ax=axes)
    g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, vmax=1, fmt='.2f', xticklabels=1, yticklabels=1)
    fig.savefig('differentkmeans.png', dpi=300)
    g.set(xticklabels=[x for x in range(1, resampleTimes+1)],yticklabels=[x for x in range(1, resampleTimes+1)])
    plt.show()
    #print(ARITable)
    #fig, axes = plt.subplots(1, 1, dpi=300)
    #scatterDataDf = pd.DataFrame(list(zip(ariScatterLi,giniScatterLi)), columns=['ARI', 'Average Gini Score'])
    #sns.scatterplot(x='ARI', y='Average Gini Score', data=scatterDataDf, ax=axes)
    #axes.set_xlim([0,1])
    #axes.set_ylim([0, 1])

    #fig.savefig('Con100 30Scatter.png')
    '''



def DifferentKmeansClusteringTest_original(resampleTimes=30,dir='kmeans/', dis='euclidean'):
    protDataObj = DataAdapter.ReadFilesPath("Example/pancan32/pancan11_RGB/pancan11protRatio.csv",
                                            "Example/pancan32/pancan11_RGB/pancan11metadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)

    #ARITable = pd.DataFrame([[0.0 for x in range(resampleTimes)]] * resampleTimes)
    #MaskTable = pd.DataFrame([[True for x in range(resampleTimes)]] * resampleTimes)
    logProtObj = [ds_ProtClust() for x in range(resampleTimes)]
    #logProtObj2 = [ds_ProtClust() for x in range(resampleTimes)]
    #logProtObj3 = [ds_ProtClust() for x in range(resampleTimes)]
    giniLi = [0.0 for x in range(resampleTimes)]
    silhoLi = [0.0 for x in range(resampleTimes)]
    separationLi = [0.0 for x in range(resampleTimes)]
    histogramLi = []
    metahisLi = []

    for num1 in range(resampleTimes):


        #logProtObj[num1].clustParamObj.SetParam(method="kmeansClust_nltk", clustNum=8,
        #                                        kmeansDisatance=dis)
        #logProtObj[num1].clustParamObj.SetParam(method="gaussianEMClust", clustNum=8,
        #                                        covType=dis)
        #logProtObj[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj[num1])
        #DataAdapter.DumpProtClustObj(logProtObj[num1],'fig/pancan/instableKmeanGaussian1000/'+dir+dis+'/'+str(num1)+'.pkl')
        logProtObj[num1] = DataAdapter.LoadProtClustObj('fig/pancan/instableKmeanGaussian1000/'+dir+dis+'/'+
                                                        str(num1)+'.pkl')

        Scoring.CalcFeatureAriScore(protDataObj, logProtObj[num1])
        #print(logProtObj[num1].clustScoringObj.featureAriDi['Cancer_Type'])
        metahisLi.append(logProtObj[num1].clustScoringObj.featureAriDi['Cancer_Type'])
        #Visualization.DrawMosaicPlot(protDataObj, logProtObj[num1], 'Cancer_Type')


        Scoring.CalcSeparationIndex(protDataObj, logProtObj[num1])
        separationLi[num1] = logProtObj[num1].clustScoringObj.separationIndex
        Scoring.CalcSilhScore(protDataObj, logProtObj[num1])
        silhoLi[num1] = logProtObj[num1].clustScoringObj.silhScore
        Scoring.CalcGiniScore(protDataObj, logProtObj[num1])
        giniLi[num1] = logProtObj[num1].clustScoringObj.giniScore


    '''
    num2 = 0
    for num1 in range(resampleTimes):

        for num2 in range(num1):
            score = adjusted_rand_score(logProtObj[num1].clustResultObj.sampleClustSer.tolist()
                                        , logProtObj[num2].clustResultObj.sampleClustSer.tolist())
            
            ARITable[num1][num2] = score
            MaskTable[num1][num2] = False
            histogramLi.append(score)
    '''
    n, bins, patches = plt.hist(metahisLi, bins=5, range=(0.4,0.65), rwidth=0.9, weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.xticks([0.4, 0.45, 0.5, 0.55, 0.6,0.65], fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Adjuested Rand Index', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/pancan/displot/instableKmeanGaussian/'+ dir+ dis + '/ari_metadata'),
                bbox_inches='tight')
    print(n)
    plt.show()


    '''
    n, bins, patches = plt.hist(histogramLi, bins=5, range=(0, 1), rwidth=0.9, weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Adjuested Rand Index', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/pancan/displot/instableKmeanGaussian/'+dir+dis+'/ari'), bbox_inches='tight')
    print(n)
    plt.show()
    '''
    n, bins, patches = plt.hist(giniLi, bins=4, range=(0.1, 0.5), rwidth=0.9, weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.xticks([0.1, 0.2, 0.3, 0.4, 0.5], fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Gini Index', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/pancan/displot/instableKmeanGaussian/'+dir+dis+'/gini'), bbox_inches='tight')
    print(n)
    plt.show()

    n, bins, patches = plt.hist(separationLi, bins=4, range=(0.2, 0.4), rwidth=0.9, weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.yticks(fontsize=16)
    plt.xticks([0.2, 0.25, 0.3, 0.35,0.40], fontsize=16)
    plt.xlabel('Separation Index', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/pancan/displot/instableKmeanGaussian/'+dir+dis+'/separation'), bbox_inches='tight')
    print(n)
    plt.show()

    n, bins, patches = plt.hist(silhoLi, bins=3, rwidth=0.9, range=(0.05, 0.2), weights=None, edgecolor='black',
                                color='#87CEFA')
    plt.yticks(fontsize=16)
    plt.xticks([0.05, 0.1, 0.15, 0.2], fontsize=16)
    plt.xlabel('Silhouette Score', fontsize=20)
    plt.ylabel('Number', fontsize=20)
    plt.savefig('{}.png'.format('fig/pancan/displot/instableKmeanGaussian/kmeans/'+dis+'/silhouette'), bbox_inches='tight')
    print(n)
    plt.show()
    ariScatterLi = []
    giniScatterLi = []
    histogramLi = []


    '''
    fig, axes = plt.subplots(1, 1, figsize=(50, 50))
    #sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, vmax=1, ax=axes)
    g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, vmax=1, fmt='.2f', xticklabels=1, yticklabels=1)
    fig.savefig('fig/pancan/displot/instableKmeanGaussian/kmeans/differentkmeans.png', dpi=300)
    g.set(xticklabels=[x for x in range(1, resampleTimes+1)],yticklabels=[x for x in range(1, resampleTimes+1)])
    plt.show()
    #print(ARITable)
    '''
#DifferentKmeansClusteringTest_original(resampleTimes=1000,dir='kmeans/',dis='euclidean')







def _ChooseLargeGini(giniLi, num1, num2):
    '''
    if giniLi[num1]<= giniLi[num2]:
        return giniLi[num2]
    else:
        return giniLi[num1]
    '''
    return (giniLi[num1]+giniLi[num2])/2


def DifferentFilterClusteringTest(filterLi=None, kmeanclusterfile="FilterClusterFile.csv"):
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

    protClustObj = ds_ProtClust()
    protClustObj2 = ds_ProtClust()
    protClustObj.clustResultObj.sampleClustSer = pd.read_csv('../../pathway_ontology_analysis/clustering_data/differentfilter_4/filter1.csv',header=None, index_col=0)
    protClustObj2.clustResultObj.sampleClustSer = pd.read_csv(
        '../../pathway_ontology_analysis/clustering_data/differentfilter_4/filter2.csv', header=None, index_col=0)
    protClustObj2.clustResultObj.sampleClustSer =protClustObj2.clustResultObj.sampleClustSer.iloc[:,0]
    protClustObj.clustResultObj.sampleClustSer = protClustObj.clustResultObj.sampleClustSer.iloc[:,0]
    print(protClustObj2.clustResultObj.sampleClustSer)
    # protClustObj=GetSampleClust(protClustObj)
    #protClustObj.clustResultObj.sampleClustSer = pd.read_csv("kmeans1.csv", index_col=0, header=None)
    #protClustObj.clustResultObj.sampleClustSer = protClustObj.clustResultObj.sampleClustSer.iloc[:, 0]

    #protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="average",
    #                                   distance="euclidean", clustNum=5)
    #protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_nltk",
    #                                       clustNum=5, resample=0.8, minK=5, maxK=5, resample_times=1000,
    #                                       ccDistance='pcc')
    #protClustObj = ClusteringMethod.Clustering(rawDataObj, protClustObj)
    #protClustObj2 = DataAdapter.LoadProtClustObj("hierarchical_cos_complete.pkl")
    #protClustObj = DataAdapter.LoadProtClustObj("new.pkl")
    #protClustObj = DataAdapter.LoadProtClustObj("fig/dif_clust/consensus_nltk_euclidean.pkl")
    #print(protClustObj.clustResultObj.sampleClustSer.tolist())
    print(adjusted_rand_score(protClustObj2.clustResultObj.sampleClustSer.tolist()
                                        , protClustObj.clustResultObj.sampleClustSer.tolist()))
    # protClustObj1 = DataAdapter.LoadProtClustObj("PassOverLap1_1.pkl")
    # protClustObj2 = DataAdapter.LoadProtClustObj("PassOverLap1_2.pkl")

    # compute silhouette_score
    Scoring.CalcEveryScore(rawDataObj, protClustObj2)
    
    #Scoring.CalcSampleSilhScore(rawDataObj, protClustObj)
    #Scoring.CalcSilhScore(rawDataObj, protClustObj)
    #Scoring.CalcClustSilhScore(rawDataObj, protClustObj)
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
    protDataObj = DataAdapter.ReadFilesPath("Example/pancan32/PANCAN_TOP10.csv", "Example/pancan32/PANCAN_TOP10_metadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    #protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    #protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    parameter = pd.read_csv('different clustering result parameter.csv',header=None, index_col=0)

    parameter = parameter.T
    parameter.reset_index(drop=True, inplace=True)
    print(parameter['linkage'])
    print(parameter)

    resultCount=len(parameter['method'])
    protClustObj = [ds_ProtClust() for x in range(resultCount)]
    for num in range(resultCount):
        ##protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="average",
        #                                    distance="euclidean", clustNum=5)
        protClustObj[num].clustParamObj.SetParam(method=parameter['method'][num], distance=parameter['distance'][num],
                                            ccMethod=parameter['ccMethod'][num], linkage= parameter['linkage'][num],
                                        clustNum=11, resample=float(parameter['resample'][num]),
                                            resample_times=int(parameter['resample_times'][num])
                                            , minK=11, maxK=11,  ccDistance=parameter['ccDistance'][num]
                                                 ,ccLinkage=parameter['ccLinkage'][num])

        # protClustObj.clustParamObj.SetParam(method="selfOrganizingMapClust", dimension=5,
        #                                   clustNum=5, learnRate=0.1, sigma=3, epochNum=800)
        protClustObj[num] = ClusteringMethod.Clustering(protDataObj, protClustObj[num])


        DataAdapter.DumpProtClustObj(protClustObj[num], _NameDifferentClusteringResult(parameter, num,dir='pancan32/top10'))
        gct = open(differentclusterfile, 'a')
        gct.writelines(str(protClustObj[num].clustResultObj.sampleClustSer.tolist())[1:-1]+'\n')

        gct.close()

    



def DifferentClusteringResult_giniARIScatterPlot():
    protDataObj = DataAdapter.ReadFilesPath("Example/pancan32/pancan11_RGB/pancan11protRatio.csv",
                                            "Example/pancan32/pancan11_RGB/pancan11metadata.csv")
    # protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)

    parameter = pd.read_csv('different clustering result parameter.csv', header=None, index_col=0)

    parameter = parameter.T
    parameter.reset_index(drop=True, inplace=True)
    #resultCount = len(parameter['method'])
    resultCount = 8
    # DataAdapter.DumpProtClustObj(protClustObj, "hierarchicalProtClust.pkl")
    # DataAdapter.DumpRawDataObj(protDataObj, "RawData.pkl")



    ARITable = pd.DataFrame([[0.0 for x in range(resultCount)]] * resultCount)
    MaskTable = pd.DataFrame([[True for x in range(resultCount)]] * resultCount)
    logProtObj = [ds_ProtClust() for x in range(resultCount)]
    giniLi = [0.0 for x in range(resultCount)]
    ariScatterLi = []
    giniScatterLi = []
    histogramLi = []
    '''
    for num1 in range(resultCount):
        logProtObj[num1] = DataAdapter.LoadProtClustObj(_NameDifferentClusteringResult(parameter, num1,dir='pancan'))
        Scoring. CalcGiniScore(protDataObj, logProtObj[num1])
        giniLi[num1] =  logProtObj[num1].clustScoringObj.giniScore

    
    '''
    logProtObj[0] = DataAdapter.LoadProtClustObj('fig/pancan/kmeans_euclidean.pkl')
    logProtObj[1] = DataAdapter.LoadProtClustObj('fig/pancan/kmeans_manhattan.pkl')
    logProtObj[2] = DataAdapter.LoadProtClustObj('fig/pancan/kmeans_cosine.pkl')
    logProtObj[3] = DataAdapter.LoadProtClustObj('fig/pancan/kmeans_pcc.pkl')
    logProtObj[4] = DataAdapter.LoadProtClustObj('fig/pancan/gaussian_full.pkl')
    logProtObj[5] = DataAdapter.LoadProtClustObj('fig/pancan/gaussian_tied.pkl')
    logProtObj[6] = DataAdapter.LoadProtClustObj('fig/pancan/gaussian_diag.pkl')
    logProtObj[7] = DataAdapter.LoadProtClustObj('fig/pancan/gaussian_spherical.pkl')
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

    '''
    sns.distplot(histogramLi, bins=5,  hist_kws=dict(edgecolor="black", linewidth=2))
    print(len(histogramLi))
    plt.xlim(0,1.0)
    plt.show()
    sns.distplot(giniLi, bins=4, hist_kws=dict(edgecolor="black", linewidth=2))
    plt.xlim(0, 1.0)
    plt.show()
    #plt.show()
    print(ARITable)
    '''
    #fig, axes = plt.subplots(1, 1, dpi=300)
    #scatterDataDf = pd.DataFrame(list(zip(ariScatterLi,giniScatterLi)), columns=['ari', 'average gini'])
    #sns.scatterplot(x='ari', y='average gini', data=scatterDataDf, ax=axes)  [x for x in range(1, resultCount+1)]
    g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmax=1, fmt='.2f', xticklabels=1, yticklabels=1)
    g.set(xticklabels=['KM_eu','KM_man','KM_cos','KM_pcc','GMM_full','GMM_tied','GMM_diag','GMM_spher']
          ,yticklabels=['KM_eu','KM_man','KM_cos','KM_pcc','GMM_full','GMM_tied','GMM_diag','GMM_spher'])
    g.set_xticklabels(g.get_xticklabels(),rotation=45)
    g.set_yticklabels(g.get_yticklabels(), rotation=45)
    plt.show()
    #axes.set_xlim([0,1])
    #axes.set_ylim([0, 1])
    #axes.set_xticklabels([x for x in range(1, resultCount)])
    #axes.set_yticklabels([x for x in range(1,resultCount)])
    #fig.savefig('fig/dif_clust/difClust_scatergini.png')




def DifferentClusteringResult_separationGiniScatterPlot():
    protDataObj = DataAdapter.ReadFilesPath("Example/pancan32/pancan11_RGB/pancan11protRatio.csv", "Example/pancan32/pancan11_RGB/pancan11metadata.csv")
    #protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)

    parameter = pd.read_csv('different clustering result parameter.csv', header=None, index_col=0)

    parameter = parameter.T
    parameter.reset_index(drop=True, inplace=True)
    resultCount = len(parameter['method'])
    # DataAdapter.DumpProtClustObj(protClustObj, "hierarchicalProtClust.pkl")
    # DataAdapter.DumpRawDataObj(protDataObj, "RawData.pkl")
    nameLi=[]

    ariLi = [0.0 for x in range(resultCount)]
    pancanClustObj = DataAdapter.LoadProtClustObj('Example/pancan32/pancan11_RGB/pancan11_label.pkl')
    pancanClustObj.clustResultObj.sampleClustSer = pancanClustObj.clustResultObj.sampleClustSer.sort_index()
    logProtObj = [ds_ProtClust() for x in range(resultCount)]
    silhoLi = [0.0 for x in range(resultCount)]
    separationLi = [0.0 for x in range(resultCount)]
    giniLi = [0.0 for x in range(resultCount)]

    for num1 in range(resultCount):
        logProtObj[num1] = DataAdapter.LoadProtClustObj(_NameDifferentClusteringResult(parameter, num1,dir='pancan'))
        Scoring. CalcSeparationIndex(protDataObj, logProtObj[num1])
        separationLi[num1] = round(logProtObj[num1].clustScoringObj.separationIndex,3)
        #Scoring.CalcSilhScore(protDataObj, logProtObj[num1])
        #silhoLi[num1] = round(logProtObj[num1].clustScoringObj.silhScore,3)
        Scoring.CalcGiniScore(protDataObj, logProtObj[num1])
        giniLi[num1] = round(logProtObj[num1].clustScoringObj.giniScore,3)
        nameLi.append(_NameDifferentClusteringResult(parameter, num1).split("/", 2)[2].split(".",1)[0])
        Scoring.CalcFeatureAriScore(protDataObj, logProtObj[num1])
        ariLi[num1] = logProtObj[num1].clustScoringObj.featureAriDi['Cancer_Type']


    shortNameDf = pd.read_csv('shorthand name list.csv', header=None)
    clustLi =['HC' for x in range(13)]+['ConHC' for x in range(13)]+['ConKM' for x in range(4)]\
             +['KM' for x in range(4)]+['GMM' for x in range(4)]
    colorLi = ['#ff7f0e' for x in range(13)]+['#1f77b4' for x in range(13)]+['#d62728' for x in range(4)]\
             +['#9467bd' for x in range(4)]+['#2ca02c' for x in range(4)]

    #sihouDf = DataFrame({'name':shortNameDf[1],'Silhouette Score':silhoLi})
    #giniDf = DataFrame({'name': shortNameDf[1], 'Gini Score': giniLi})
    ariDf =  DataFrame({'name':shortNameDf[1],'ARI':ariLi,'Clust':clustLi,'color':colorLi})
    #giniDf = giniDf.sort_values(by=['Gini Score'])
    #sihouDf = sihouDf.sort_values(by=['Silhouette Score'])
    ariDf = ariDf.sort_values(by=['ARI'])
    fig, axes = plt.subplots(1, 1, dpi=300)
    #sns.barplot(y='name',x='Gini Score',data=giniDf,ax=axes)
    sns.barplot(y='name', x='ARI', data=ariDf, ax=axes,palette=ariDf['color'])
    axes.set_yticklabels(ariDf['name'], fontdict={'fontsize':5.0})
    #fig.savefig('fig/dif_clust/difClust_giniBarplot.png')
    fig.savefig('fig/pancan/compare11label_ariBarplot.png')

    '''
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







def DifferentClusteringResult_ARIBarplot():
    #protDataObj = DataAdapter.ReadFilesPath("Example/pancan32/pancan11_RGB/pancan11protRatio.csv", "Example/pancan32/pancan11_RGB/pancan11metadata.csv")

    #protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    parameter = pd.read_csv('different clustering result parameter.csv', header=None, index_col=0)

    parameter = parameter.T
    parameter.reset_index(drop=True, inplace=True)
    resultCount = len(parameter['method'])
    nameLi=[]

    ariLi = [0.0 for x in range(resultCount)]
    logProtObj = [ds_ProtClust() for x in range(resultCount)]
    silhoLi = [0.0 for x in range(resultCount)]
    separationLi = [0.0 for x in range(resultCount)]
    giniLi = [0.0 for x in range(resultCount)]

    for num1 in range(resultCount):
        logProtObj[num1] = DataAdapter.LoadProtClustObj(_NameDifferentClusteringResult(parameter, num1,dir='dif_clust'))
        #Scoring. CalcSeparationIndex(protDataObj, logProtObj[num1])
        #separationLi[num1] = round(logProtObj[num1].clustScoringObj.separationIndex,3)
        #Scoring.CalcSilhScore(protDataObj, logProtObj[num1])
        #ariLi[num1] = round(logProtObj[num1].clustScoringObj.silhScore,3)
        Scoring.CalcGiniScore(protDataObj, logProtObj[num1])
        ariLi[num1] = round(logProtObj[num1].clustScoringObj.giniScore,3)
        nameLi.append(_NameDifferentClusteringResult(parameter, num1).split("/", 2)[2].split(".",1)[0])
        #Scoring.CalcFeatureAriScore(protDataObj, logProtObj[num1])
        #ariLi[num1] = logProtObj[num1].clustScoringObj.featureAriDi['Cancer_Type']
        #Scoring.CalcFeatureMaxFscore(protDataObj, logProtObj[num1])
        #ariLi[num1] = logProtObj[num1].clustScoringObj.featureMaxFscoreDi['Cancer_Type']
    shortNameDf = pd.read_csv('shorthand name list.csv', header=None)
    clustLi = ['HC' for x in range(13)] + ['ConHC' for x in range(13)] + ['ConKM' for x in range(4)]
    colorLi = ['#ff7f0e' for x in range(13)] + ['#1f77b4' for x in range(13)] + ['#d62728' for x in range(4)] \

    # sihouDf = DataFrame({'name':shortNameDf[1],'Silhouette Score':silhoLi})
    # giniDf = DataFrame({'name': shortNameDf[1], 'Gini Score': giniLi})
    ariDf = DataFrame({'name': shortNameDf[1], 'ARI': ariLi, 'Clust': clustLi, 'color': colorLi})

    # giniDf = giniDf.sort_values(by=['Gini Score'])
    # sihouDf = sihouDf.sort_values(by=['Silhouette Score'])
    ariDf = ariDf.sort_values(by=['ARI'])
    fig, axes = plt.subplots(1, 1, dpi=300)
    # sns.barplot(y='name',x='Gini Score',data=giniDf,ax=axes)
    sns.barplot(y='name', x='ARI', data=ariDf, ax=axes, palette=ariDf['color'])
    #handles, labels = axes.get_legend_handles_labels()
    #axes.legend(handles=handles[0:], labels=labels[0:])
    axes.set_yticklabels(ariDf['name'], fontdict={'fontsize': 5.0})
    axes.set_xlabel('Gini Index')

    # fig.savefig('fig/dif_clust/difClust_giniBarplot.png')
    fig.savefig('fig/dif_clust/giniBarplot.png')






def PCA_TSNETEST(dis,pkl):
    """
    find
    :param resampleTimes: the number to run clustering, to find the 5 similar clustering we want
    :return:
    """
    #rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")

    #rawDataObj = DataAdapter.FilterByCutoff(rawDataObj, methodStr='MAD', cutOff=0.5)
    rawDataObj = DataAdapter.ReadFilesPath("Example/pancan32/pancan11_RGB/pancan11protRatio.csv",
                                            "Example/pancan32/pancan11_RGB/pancan11metadata.csv")
    rawDataObj = DataAdapter.RemoveProtWithNa(rawDataObj)
    clust = DataAdapter.LoadProtClustObj('fig/pancan/hierarchical_euclidean_average.pkl')
    clust1 = DataAdapter.LoadProtClustObj(pkl)

    Visualization.PlotPca(rawDataObj, clust, dpi=300, pointSize=4, path='fig/pancan/check/pca_' +'HC_eu_average')
    Visualization.PlotPca(rawDataObj, clust1, dpi=300, pointSize=4, path='fig/pancan/check/pca_' + dis)
    Scoring.CalcFeatureAriScore(rawDataObj, clust1)
    #Visualization.DrawMosaicPlot(rawDataObj, clust1, 'Cancer_Type', path='fig/dif_clust/pca/mosaic_' + dis,
    #                             figSizeLi=[20, 10], dpi=300)
    print(adjusted_rand_score(clust.clustResultObj.sampleClustSer, clust1.clustResultObj.sampleClustSer))

    # Visualization.PlotPca(rawDataObj, clust2, dpi=300, path='fig/MADTOP1200_PCA.png',
    #                      colorLi=['#9467bd', '#d62728',  '#2ca02c', '#1f77b4',  '#ff7f0e'] )
    #Visualization.PlotTsne(rawDataObj, clust1, dpi=300, perplexity=8, pointSize=1, path='fig/dif_clust/pca/tsne_' + dis)

    #Visualization.PlotPca(rawDataObj, clust2, dpi=300, path='fig/MADTOP1200_PCA.png',
    #                      colorLi=['#9467bd', '#d62728',  '#2ca02c', '#1f77b4',  '#ff7f0e'] )
    '''
    for count in range(1, 100):
        Visualization.PlotTsne(rawDataObj, protClustObj, dpi=300, perplexity=8,
                               path='fig/goterm/0.26/gaussian/gaussianTSNE_'+str(count)+'.png')
    #ratioTable = Visualization.FindSampleOverlapHeatmap(protClustObj, protClustObj1)
    #DataAdapter.DumpProtClustObj(protClustObj1, 'hierarchical_cos_complete.pkl')
    
    ##   '#d62728' red, '#9467bd' purple, '#2ca02c' green,'#1f77b4' blue, '#ff7f0e'orange
    '''

#PCA_TSNETEST(dis='HC_eu_single',pkl='fig/pancan/hierarchical_euclidean_single.pkl')
def TestSOM():

    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    protClustObj = ds_ProtClust()

    #conprotObj = DataAdapter.LoadProtClustObj('consensusProtClust.pkl')
    protClustObj.clustParamObj.SetParam(method="selfOrganizingMapClust", dimension=5,
                                           learnRate=0.01, sigma=0.5, epochNum=1000, plotError=True, filename='SOMplot')
    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    #protClustObj.clustResultObj.sampleClustSer.to_csv("SOMresult.csv")
    #DataAdapter.DumpProtClustObj(protClustObj, "SOMProtClust.pkl")
    #print(adjusted_rand_score(
    #        conprotObj.clustResultObj.sampleClustSer.tolist(),
    #        protClustObj.clustResultObj.sampleClustSer.tolist()))
    Scoring.CalcGiniScore(protDataObj, protClustObj)
    print("gini: "+str(protClustObj.clustScoringObj.giniScore))
    Visualization.PlotPca(protDataObj, protClustObj)

def TestConHierarchicalInstability():


    #parameter = pd.read_csv('TestConHierarchicalInstability.csv', header=None, index_col=0)
    parameter = pd.read_csv('TestConHCpccInstability.csv', header=None, index_col=0)
    parameter = parameter.T
    parameter.reset_index(drop=True, inplace=True)
    print(parameter['linkage'])
    print(parameter)

    resultCount = len(parameter['resample'])

    for num in range(resultCount):
        TestConHierachical(float(parameter['resample'][num]), int(parameter['resample_times'][num]), parameter['ccDistance'][num], parameter['ccLinkage'][num])

def TestConHierachical(resam, resample_times, ccDistance, ccLinkage, resample=30):

    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    protClustObj = [ds_ProtClust() for x in range(resample)]
    ARITable = pd.DataFrame([[0.0 for x in range(resample)]] * resample)
    MaskTable = pd.DataFrame([[True for x in range(resample)]] * resample)
    #conprotObj = DataAdapter.LoadProtClustObj('fig/dif_clust/hierarchical_euclidean_complete.pkl')
    #conprotObj =[ds_ProtClust() for x in range(resample)]

    for i in range(resample):
        protClustObj[i].clustParamObj.SetParam(method="consensusClust", clustNum=5,ccMethod='hierarchicalClust',minK=5,maxK=5,
                                           resample=resam, resample_times=resample_times, ccDistance=ccDistance, ccLinkage=ccLinkage)
        protClustObj[i] = ClusteringMethod.Clustering(protDataObj, protClustObj[i])

        #conprotObj[i].clustParamObj.SetParam(method="hierarchicalClust", clustNum=5, minK=5,
        #                                     maxK=5, distance='pcc', linkage='average')
        #conprotObj[i] = ClusteringMethod.Clustering(protDataObj, conprotObj[i])
    #protClustObj.clustResultObj.sampleClustSer.to_csv("SOMresult.csv")
    #DataAdapter.DumpProtClustObj(protClustObj, "SOMProtClust.pkl")
        #print(adjusted_rand_score(
        #        conprotObj.clustResultObj.sampleClustSer.tolist(),
        #        protClustObj[i].clustResultObj.sampleClustSer.tolist()))

    #Scoring.CalcGiniScore(protDataObj, protClustObj)
    #print("gini: "+str(protClustObj.clustScoringObj.giniScore))


    for num1 in range(resample):
        for num2 in range(num1):
            score = adjusted_rand_score(
                protClustObj[num1].clustResultObj.sampleClustSer.tolist(),
                protClustObj[num2].clustResultObj.sampleClustSer.tolist())
            ARITable[num1][num2] = round(score,2)
            MaskTable[num1][num2] = False

    fig, ax = plt.subplots(figsize=(18, 10))
    g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, fmt='.2f',
        xticklabels = 1, yticklabels = 1, vmax=1,ax=ax)
    #plt.show()
    g.set(xticklabels=[x for x in range(1, resample + 1)], yticklabels=[x for x in range(1, resample + 1)])

    #fig.savefig('fig/conHierarchical/'+str(resam)+'_'+str(resample_times)+'_'+ccDistance+'_'+ccLinkage+'.png',dpi=300)
    fig.savefig(
        'fig/conHierarchical/pcc/' + str(resam) + '_' + str(resample_times) + '_' + ccDistance + '_' + ccLinkage + '.png',
        dpi=300)
    #fig.cla()



def ConHCpccCompare(resample=30):
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")

    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = [ds_ProtClust() for x in range(3)]
    protClustObj[0] = DataAdapter.LoadProtClustObj("fig/dif_clust/consensus_hierarchical_pcc_average.pkl")
    protClustObj[1] = DataAdapter.LoadProtClustObj("fig/conHierarchical/re1000/complete/conHC_pcc23.pkl")
    protClustObj[2] = DataAdapter.LoadProtClustObj("fig/conHierarchical/re1000/single/conHC_pcc97.pkl")

    protClustObj_average = [ds_ProtClust() for x in range(resample)]
    protClustObj_complete = [ds_ProtClust() for x in range(resample)]
    protClustObj_single = [ds_ProtClust() for x in range(resample)]
    gini_average = [0.0 for x in range(resample)]
    gini_complete = [0.0 for x in range(resample)]
    gini_single = [0.0 for x in range(resample)]
    # conprotObj = DataAdapter.LoadProtClustObj('fig/dif_clust/hierarchical_euclidean_complete.pkl')
    # conprotObj =[ds_ProtClust() for x in range(resample)]
    '''
    for i in range(resample):
        protClustObj_average[i].clustParamObj.SetParam(method="consensusClust", clustNum=5, ccMethod='hierarchicalClust',
                                               minK=5, maxK=5,
                                               resample=0.8, resample_times=1000, ccDistance='pcc',
                                               ccLinkage='average')
        protClustObj_average[i] = ClusteringMethod.Clustering(protDataObj, protClustObj_average[i])

        protClustObj_complete[i].clustParamObj.SetParam(method="consensusClust", clustNum=5,
                                                       ccMethod='hierarchicalClust',
                                                       minK=5, maxK=5,
                                                       resample=0.8, resample_times=1000, ccDistance='pcc',
                                                       ccLinkage='complete')
        protClustObj_complete[i] = ClusteringMethod.Clustering(protDataObj, protClustObj_complete[i])

        protClustObj_single[i].clustParamObj.SetParam(method="consensusClust", clustNum=5,
                                                       ccMethod='hierarchicalClust',
                                                       minK=5, maxK=5,
                                                       resample=0.8, resample_times=1000, ccDistance='pcc',
                                                       ccLinkage='single')
        protClustObj_single[i] = ClusteringMethod.Clustering(protDataObj, protClustObj_single[i])


        Scoring.CalcGiniScore(protDataObj, protClustObj_average[i])
        gini_average[i] = round(protClustObj_average[i].clustScoringObj.giniScore, 3)

        Scoring.CalcGiniScore(protDataObj, protClustObj_complete[i])
        gini_complete[i] = round(protClustObj_complete[i].clustScoringObj.giniScore, 3)

        Scoring.CalcGiniScore(protDataObj, protClustObj_single[i])
        gini_single[i] = round(protClustObj_single[i].clustScoringObj.giniScore, 3)

    '''

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

    ### draw ari heatmap
    #sns.set(font_scale=2)
    #g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmax=1, fmt='.2f', xticklabels=1,
    #                yticklabels=1)
    #g.set(xticklabels=['Average', 'Complete', 'Single'], yticklabels=['Average', 'Complete', 'Single'])
    #plt.yticks(fontsize=16)
    #plt.xticks(fontsize=16)
    #plt.show()

    #Visualization.FindSampleOverlapHeatmap(protClustObj[0], protClustObj[1],
    #                                       path='fig/conHierarchical/pcc/sampleoverlap_ConHC_average_complete.png',
    #                                       dpi=300,xlabelStr='ConHC_average', ylabelStr='ConHC_complete')

    ### draw pca
    # for num1 in range(len(protClustObj)):
    Visualization.PlotPca(protDataObj, protClustObj[2], dpi=300, path='fig/conHierarchical/pcc/pca_single.png',
                          colorLi=['#9467bd', '#d62728','#2ca02c','#1f77b4','#ff7f0e'])
    ##   '#d62728' red, '#9467bd' purple, '#2ca02c' green,'#1f77b4' blue, '#ff7f0e'orange
    ### draw box plot
    '''
    clusterMethodLi = ['Complete' for x in range(resample)] + ['Average' for x in range(resample)] + ['Single' for x in
                                                                                                      range(resample)]
    giniDf = DataFrame({'Cluster Method': clusterMethodLi, 'Gini Index': gini_complete + gini_average + gini_single})
    print(giniDf['Cluster Method'])
    print(giniDf['Gini Index'])
    # giniDf = giniDf.sort_values(by=['Gini Score'])
    fig, axes = plt.subplots(1, 1, dpi=300)
    sns.boxplot(x='Cluster Method', y='Gini Index', data=giniDf, ax=axes)
    # axes.set_xticklabels(giniDf['Cluster Method'])
    plt.xlabel('Cluster Method', fontsize=20)
    plt.ylabel('Gini Index', fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # fig.savefig('fig/conHierarchical/pcc/gini boxplot_test.png')
    fig.savefig('boxplot', bbox_inches='tight')
    ### draw sampleoverlap heatmap
    # for num1 in range(len(protClustObj)-1):
    

    #######
    '''


def _NameDifferentClusteringResult(parameter, num, dir='dif_clust'):

    if parameter['method'][num]=='hierarchicalClust':
        return 'fig/'+dir+'/hierarchical_'+parameter['distance'][num]+'_'+parameter['linkage'][num]+'.pkl'
    elif parameter['method'][num]=='consensusClust':
        if parameter['ccMethod'][num]=='hierarchicalClust':
            return 'fig/'+dir+'/consensus_hierarchical_'+parameter['ccDistance'][num]+'_'+parameter['ccLinkage'][num]+'.pkl'
        else:
            return 'fig/'+dir+'/consensus_nltk_'+parameter['ccDistance'][num]+'.pkl'
    elif parameter['method'][num]=='kmeansClust_nltk':
        return 'fig/'+dir+'/kmeans_'+parameter['distance'][num]+'.pkl'
    elif parameter['method'][num]=='gaussianEMClust':
        return 'fig/'+dir+'/gaussian_'+parameter['distance'][num]+'.pkl'




def GoTermVennTest(path1,path2, subtype1,subtype2, process="biological",figPath='fig/GoTermVenn/0.7/'):


        node1 = path1 +'/cluster'+ str(subtype1) + "_up/"+process+"/cluster"+str(subtype1)+"up.txt"
        node2 = path2 +'/cluster'+ str(subtype2) + "_up/"+process+"/cluster"+str(subtype2)+"up.txt"
        return CaseStudy.DrawGoTermOverlapVenn(node1, node2, figPath+str(subtype1)+'_'+str(subtype2)+'.png')








def DifferentKmeansAndGaussianClusteringTest(resampleTimes=30,
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
    halfResmpleTimes = int(resampleTimes/2)
    gct = open(kmeanclusterfile, 'w')
    for num1 in range( halfResmpleTimes):
        seed = random.randint(1, 100000)

        logProtObj[num1].clustParamObj.SetParam(method="kmeansClust_nltk", clustNum=5, kmeansDisatance='euclidean')
        logProtObj[num1+halfResmpleTimes].clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
                                                covType='full')

        #logProtObj[num1].clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_nltk",
        #                                        clustNum=5, resample=0.8, minK=5, maxK=6, resample_times=100,
        #                                        ccDistance='euclidean')

        logProtObj[num1] = ClusteringMethod.Clustering(protDataObj, logProtObj[num1])
        Scoring.CalcGiniScore(protDataObj, logProtObj[num1])
        giniLi[num1] = logProtObj[num1].clustScoringObj.giniScore
        gct.writelines(str(logProtObj[num1].clustResultObj.sampleClustSer.tolist()) + '\n')

        logProtObj[num1+halfResmpleTimes] = ClusteringMethod.Clustering(protDataObj, logProtObj[num1+halfResmpleTimes])
        Scoring.CalcGiniScore(protDataObj, logProtObj[num1+halfResmpleTimes])
        giniLi[num1+halfResmpleTimes] = logProtObj[num1+halfResmpleTimes].clustScoringObj.giniScore
        gct.writelines(str(logProtObj[num1+halfResmpleTimes].clustResultObj.sampleClustSer.tolist()) + '\n')

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


    ### heatmap of resample times ari
    # fig, axes = plt.subplots(1, 1, figsize=(50, 50))
    tickLi=['KM1','KM2','KM3','KM4','KM5','KM6','KM7','KM8','KM9','KM10','KM11','KM12','KM13','KM14','KM15',
            'GMM1','GMM2','GMM3','GMM4','GMM5','GMM6','GMM7','GMM8','GMM9','GMM10','GMM11','GMM12','GMM13','GMM14','GMM15']
    # sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, vmax=1, ax=axes)
    g = sns.heatmap(ARITable, cmap="Reds", linewidths=.5, annot=True, mask=MaskTable, vmin=0, vmax=1, fmt='.2f', xticklabels=1, yticklabels=1)
    # fig.savefig('differentkmeans.png', dpi=300)
    #g.set(xticklabels=[x for x in range(1, resampleTimes+1)],yticklabels=[x for x in range(1, resampleTimes+1)])
    g.set(xticklabels=tickLi, yticklabels=tickLi)
    plt.show()
    # print(ARITable)

    '''
    ### scatter plot of gini and ARI Score
    fig, axes = plt.subplots(1, 1, dpi=300)
    scatterDataDf = pd.DataFrame(list(zip(ariScatterLi, giniScatterLi)), columns=['ARI', 'Average Gini Score'])
    sns.scatterplot(x='ARI', y='Average Gini Score', data=scatterDataDf, ax=axes)
    axes.set_xlim([0, 1])
    axes.set_ylim([0, 1])

    fig.savefig('Con100 30Scatter.png')
    '''














def PanCancerDesideK():
    protDataObj = DataAdapter.ReadFilesPath("Example/pancan32/pancan11_RGB/pancan11protRatio.csv", "Example/pancan32/pancan11_RGB/pancan11metadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)

    #protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    print(protDataObj.GetProtRatioDf())
    kLi=[3,4,5,6,7,8,9,10,11,12,13,14,15]
    silhoLi = [0.0 for x in range(len(kLi))]
    separationLi = [0.0 for x in range(len(kLi))]
    protClustObj = [ds_ProtClust() for x in range(len(kLi))]
    pancanClustObj = DataAdapter.LoadProtClustObj('Example/pancan32/pancan11_RGB/pancan11_label.pkl')
    pancan9Obj = DataAdapter.LoadProtClustObj('Example/pancan32/pancan11_RGB/pancan11_9cluster.pkl')
    pancanClustObj.clustResultObj.sampleClustSer = pancanClustObj.clustResultObj.sampleClustSer.sort_index()
    pancan9Obj.clustResultObj.sampleClustSer = pancan9Obj.clustResultObj.sampleClustSer.sort_index()
    print(adjusted_rand_score(pancanClustObj.clustResultObj.sampleClustSer.tolist(),
                              pancan9Obj.clustResultObj.sampleClustSer.tolist()))
    for i in range(len(kLi)):
        protClustObj[i].clustParamObj.SetParam(method="hierarchicalClust", linkage="ward",
                                        distance="euclidean", clustNum=kLi[i])
        protClustObj[i] = ClusteringMethod.Clustering(protDataObj, protClustObj[i])
        protClustObj[i].clustResultObj.sampleClustSer = protClustObj[i].clustResultObj.sampleClustSer.sort_index()
        print(adjusted_rand_score(pancanClustObj.clustResultObj.sampleClustSer.tolist(),
                                  protClustObj[i].clustResultObj.sampleClustSer.tolist()))
        ### count separation index and silhouette score
        Scoring.CalcSeparationIndex(protDataObj, protClustObj[i])
        separationLi[i] = round(protClustObj[i].clustScoringObj.separationIndex, 3)
        Scoring.CalcSilhScore(protDataObj, protClustObj[i])
        silhoLi[i] = round(protClustObj[i].clustScoringObj.silhScore, 3)


    # save protclust and rawdata obj pickle files
    #DataAdapter.DumpProtClustObj(protClustObj, "Example/pancan32/pancan10_ConKMProtClust.pkl")



    # draw plot order = [1, 2, 3],
    separationDf = DataFrame({'Cluster K': kLi, 'Separation Index': separationLi})
    sns.pointplot( x="Cluster K", y="Separation Index", data=separationDf, color=".3", ci=None)
    #plt.xlim(0, 1.0)
    plt.show()
    silhouDf = DataFrame({'Cluster K': kLi, 'Silhouette Score': silhoLi})
    sns.pointplot( x="Cluster K", y='Silhouette Score', data=silhouDf, color=".3", ci=None)
    plt.show()





def PanCancerClusteringTest():
    protDataObj = DataAdapter.ReadFilesPath("Example/pancan32/PANCAN_TOP10.csv", "Example/pancan32/PANCAN_TOP10_metadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    #rawDataObj = DataAdapter.FilterByCutoff(rawDataObj, methodStr='MAD', cutOff=0.5)
    print(protDataObj.GetProtRatioDf())
    protClustObj = ds_ProtClust()

    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_nltk", ccDistance="euclidean",
                                         resample=0.8, minK=10, maxK=14, resample_times=100)
    # protClustObj.clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
    #                                    covType='full')
    # protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="average",
    #                                    distance="pcc", clustNum=5)
    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    # save protclust and rawdata obj pickle files
    DataAdapter.DumpProtClustObj(protClustObj, "Example/pancan32/pancan10_ConKMProtClust.pkl")

    #protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="ward",
    #                                    distance="euclidean", clustNum=5)
    # protClustObj.clustParamObj.SetParam(method="gaussianEMClust", clustNum=5,
    #                                    covType='spherical')
    # protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod="kmeansClust_nltk",
    # ccDistance='cosine', clustNum=5, resample=0.8, minK=5, maxK=6, resample_times=1000)
    pancanClustObj = DataAdapter.LoadProtClustObj('Example/pancan32/pancan10_label.pkl')

    # save protclust and rawdata obj pickle files

    print(adjusted_rand_score(pancanClustObj.clustResultObj.sampleClustSer.tolist(), protClustObj.clustResultObj.sampleClustSer.tolist()))

#PanCancerDesideK()
#PanCancerClusteringTest()
#DifferentClusteringResult(differentclusterfile="fig/pancan/DifferentClusterFile.csv")



'''
InputRawDataTest()
ProtClustTest()
ClustFeatureRatioExample()
PortClustScoreExample()
ScoringMethodTest()
'''

# nonLogClusteringTest(path="Example/colonCancerProtRatio.csv")
#HierachicalClusteringTest()


#CaseStudy.FindGoTermOverlap(clusterNum=5,goTerm1Str="consensus nltk euclidean", processStr='biological',
#                                goTerm2Str="filtermad0.5_colon_hierachical_0.05")


GoTermTest( choseGoNum = 2000)
#NetworkTest(5)

#SampleOverlap(resampleTimes=30000)

# VisualizationMethodTest()


# GSEATest()

#DifferentKmeansClusteringTest(resampleTimes=30)
#TestConHierarchicalInstability()
#PCA_TSNETEST()
#protClustObj = DataAdapter.LoadProtClustObj("hierarchical_cos_complete.pkl")

#rawDataObj = DataAdapter.LoadRawDataObj("RawData.pkl")
#protClustObj.clustResultObj.sampleClustSer.to_csv('hierarchical0.7.csv')
#Statistics.RunWilconTest ("colon_ratio.csv", protClustObj1, 5, "colon_filter1")
#Statistics.RunWilconTest (rawDataObj, protClustObj, 5, "colon_consensus")
#Statistics.RunWilconTest ("colon_ratio.csv", "PassOverLap2_1.csv", 5, "colon_filter2")


#DifferentFilterClusteringTest()

#SampleOverlap_hierarchical()
# clustResultDf = pd.read_csv("DifferentClusterFile.csv",header=None).T
# print(adjusted_rand_score(clustResultDf[13],clustResultDf[14]))


#rawDataObj = DataAdapter.LoadRawDataObj("RawData.pkl")
#protClustObj1 = DataAdapter.LoadProtClustObj("PassOverLap1_1.pkl")
#protClustObj2 = DataAdapter.LoadProtClustObj("consensusProtClust.pkl")


#protClustObj2 = DataAdapter.LoadProtClustObj("hierarchicalProtClust.pkl")
#protClustObj3 = DataAdapter.LoadProtClustObj("hierarchical_cos_complete.pkl")
#protClustObj4 = DataAdapter.LoadProtClustObj("new.pkl")
'''
for i in protClustObj4.clustResultObj.sampleClustSer.index.values:
    if protClustObj4.clustResultObj.sampleClustSer[i]==6:
        protClustObj4.clustResultObj.sampleClustSer[i]=4

print(protClustObj4.clustResultObj.sampleClustSer)
DataAdapter.DumpProtClustObj(protClustObj4, 'new.pkl')
'''




#Visualization.FindSampleOverlapHeatmap(protClustObj4, protClustObj2, dpi=300)
#DataAdapter.DumpProtClustObj(protClustObj1[i],'fig/con vs hierarchical/overlap/'+str(i+1)+'.pkl')
#protClustObj = DataAdapter.LoadProtClustObj('consensusProtClust.pkl')
#protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)
#protClustObj = Characterization.Characterize(protClustObj,1.5,2/3)

#protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
#protDataObj = DataAdapter.ReadFilesPath("Example/seeds.csv", "Example/seedsMeta.csv")
#protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
#protClustObj = DataAdapter.LoadProtClustObj('consensusProtClust.pkl')


#DifferentClusteringResult()

#DifferentClusteringResult_giniARIScatterPlot()
#DifferentClusteringResult_separationGiniScatterPlot()
#DifferentClusteringResult_ARIBarplot()
'''
data = pd.read_csv('giniData.csv')
sns.barplot(x='gini score', y='difference between max and min cluster',data=data)
plt.savefig('difference.png',dpi=300)
plt.cla()
'''










'''
# go term overlap list


list1 = GoTermVennTest('Example/consensus nltk euclidean', 'Example/filtermad0.5_colon_hierachical_0.05',1,2, figPath='fig/GoTermVenn/0.4_new/')
list2 = GoTermVennTest('Example/consensus nltk euclidean', 'Example/filtermad0.5_colon_hierachical_0.05',1,4, figPath='fig/GoTermVenn/0.4_new/')
list3 = GoTermVennTest('Example/consensus nltk euclidean', 'Example/filtermad0.5_colon_hierachical_0.05',1,5, figPath='fig/GoTermVenn/0.4_new/')

#CaseStudy.DrawOverlapOverlapVenn(list1,list2,path='fig/GoTermVenn/0.7/2_1_3overlap.png')
CaseStudy.DrawOverlapOverlapVenn3(list1, list2, list3, 'fig/GoTermVenn/0.4_new/1_2_4_5overlap.png',node1='c2', node2='c4',node3='c5',dpi=300)
'''
'''
protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
#protDataObj = DataAdapter.ReadFilesPath("fig/spectra count/ratiotable.csv", "fig/spectra count/metadata.csv")
protDataObj = DataAdapter.ZscoreNmlz(protDataObj)
protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
#protDataObj = DataAdapter.FilterByRank(protDataObj, methodStr='MAD', topNum=1263)

protClustObj =ds_ProtClust()
protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='hierarchicalClust',minK=3,maxK=7,
                                           resample=0.8, resample_times=1000, ccDistance='pcc', ccLinkage='average')
protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)
for i in range(len(protClustObj.clustResultObj.clustSampleSer)):
    print(len(protClustObj.clustResultObj.clustSampleSer[i+1]))
#Statistics.GenerateGctFile(protDataObj)

'''


def MakeClusterResultCsvIntoObject(path='Example/pancan32/pancan11_RGB/pancan11 label.csv'):
    '''
    use csv file as a clustering result
    :param path:
    :return:
    '''
    protClustObj = ds_ProtClust()

    protClustObj.clustResultObj.sampleClustSer = pd.read_csv(path, index_col=0)
    protClustObj.clustResultObj.sampleClustSer['Cluster'] = [1 for x in range(127)] + [2 for x in range(747)]+ [3 for x in range(334)] + [4 for x in range(215)] + [5 for x in range(212)]+ [6 for x in range(454)]+ [7 for x in range(237)]+ [8 for x in range(195)]+ [9 for x in range(412)]+ [10 for x in range(130)]+ [11 for x in range(404)]
    protClustObj.clustResultObj.sampleClustSer = protClustObj.clustResultObj.sampleClustSer.iloc[:, 1]
    DataAdapter.DumpProtClustObj(protClustObj, 'Example/pancan32/pancan11_RGB/pancan11_label.pkl')
    print(protClustObj.clustResultObj.sampleClustSer)

'''
#MakeClusterResultCsvIntoObject()
protClustObj = ds_ProtClust()
protClustObj.clustResultObj.sampleClustSer = pd.read_csv('Example/pancan32/pancan11_RGB/pancan11_9cluster.csv', index_col=0)
protClustObj.clustResultObj.sampleClustSer = protClustObj.clustResultObj.sampleClustSer.iloc[:, 0]
DataAdapter.DumpProtClustObj(protClustObj, 'Example/pancan32/pancan11_RGB/pancan11_9cluster.pkl')
print(protClustObj.clustResultObj.sampleClustSer)

protDataObj = DataAdapter.ReadFilesPath("Example/pancan32/pancan11_RGB/pancan11protRatio.csv", "Example/pancan32/pancan11_RGB/pancan11metadata.csv")
protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
pancanClustObj = DataAdapter.LoadProtClustObj('Example/pancan32/pancan11_RGB/pancan11_label.pkl')
pancan9Obj = DataAdapter.LoadProtClustObj('Example/pancan32/pancan11_RGB/pancan11_9cluster.pkl')
protClustObj = DataAdapter.LoadProtClustObj('fig/pancan/consensus_nltk_pcc.pkl')
pancanClustObj.clustResultObj.sampleClustSer = pancanClustObj.clustResultObj.sampleClustSer.sort_index()
pancan9Obj.clustResultObj.sampleClustSer = pancan9Obj.clustResultObj.sampleClustSer.sort_index()
protClustObj.clustResultObj.sampleClustSer = protClustObj.clustResultObj.sampleClustSer.sort_index()
print(adjusted_rand_score(pancanClustObj.clustResultObj.sampleClustSer.tolist(),
                              pancan9Obj.clustResultObj.sampleClustSer.tolist()))
Visualization.FindSampleOverlapHeatmap(pancan9Obj,pancanClustObj)

protClustObj = DataAdapter.LoadProtClustObj('hierarchical_cos_complete.pkl')
protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")

protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
Scoring.CalcEveryScore(protDataObj,protClustObj)
Characterization.Characterize(protClustObj,1.5,2/3)
'''


#Diff()
