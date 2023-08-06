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


### DataAdapter###

def PreprocessRawData_RemoveNa():
    """
    ReadFilesPath will check the number of patients is equal in protein ratio and metadata, remove continuous columns of
    metadataDf and set missing value into NA, if you want to remove missing value, you can use RemoveProtWithNa function
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)

    print(protDataObj.GetProtRatioDf())
    print(protDataObj.GetMetadataDf())


def PreprocessRawData_Imputation():
    """
    Besides remove missing value, you can also choose to impute missing value, there are three functions ImputeMin,
    ImputeAverage and ImputeKnn.
    """

    #####   InputRawData test
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    #protDataObj = DataAdapter.ImputeMin(protDataObj, percentage=0.1)
    #protDataObj = DataAdapter.ImputeAverage(protDataObj, percentage=0.1)
    protDataObj = DataAdapter.ImputeKnn(protDataObj, n_neighbors=5, weightStr='uniform', percentage=0.1)

    print(protDataObj.GetProtRatioDf())
    print(protDataObj.GetMetadataDf())


def PreprocessRawData_Log():
    """
    Before we run clustering, you can use RatioToLogRatio() to change your protein ratio data into log ratio or use
    LogRatioToRatio() to change log ratio data into ratio data.
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.LogRatioToRatio(protDataObj)
    protDataObj = DataAdapter.RatioToLogRatio(protDataObj)

    print(protDataObj.GetProtRatioDf())
    print(protDataObj.GetMetadataDf())


def PreprocessRawData_Normalize():
    """
    Before we run clustering, you can use ZscoreNmlz() to z-score your protein ratio data.

    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.ZscoreNmlz(protDataObj)

    print(protDataObj.GetProtRatioDf())
    print(protDataObj.GetMetadataDf())


def PreprocessRawData_Filter():
    """
        Before we run clustering, you can useFilterByRank(),  FilterByCutoff() or  FilterByTopPercentage() to
        select features.

    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, 0.5, methodStr='SD')
    #protDataObj = DataAdapter.FilterByTopPercentage(protDataObj, 0.1, methodStr='SD')
    #protDataObj = DataAdapter.FilterByRank(protDataObj, 1000, methodStr='SD')

    print(protDataObj.GetProtRatioDf())
    print(protDataObj.GetMetadataDf())



### Clustering###

def Clustering_Hierarchical():
    """
    Build a new object protClustObj to save the clustering result and then run hierarchical clustering
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()

    protClustObj.clustParamObj.SetParam(method="hierarchicalClust", linkage="average",
                                            distance="euclidean", clustNum=5)
    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    print(protClustObj.clustResultObj.sampleClustSer)


def Clustering_KMeans():
    """
    Build a new object protClustObj to save the clustering result and then run K-means clustering.
    'kmeansClust_sklearn' can only use euclidean distance,  'kmeansClust_nltk' can use euclidean, manhattan, and cosine.
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    seed = random.randint(1, 10000)
    protClustObj.clustParamObj.SetParam(method="kmeansClust_sklearn", seed=seed, clustNum=5)
    #protClustObj.clustParamObj.SetParam(method="kmeansClust_nltk", kmeansDisatance="manhattan", clustNum=5)
    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    print(protClustObj.clustResultObj.sampleClustSer)


def Clustering_Gaussian():
    """
    Build a new object protClustObj to save the clustering result and then run Gaussian Model clustering.
    covType(covariance_type) can choose 'full', 'tied', 'diag' or 'spherical'
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()

    protClustObj.clustParamObj.SetParam(method="gaussianEMClust", clustNum=5, covType='full')
    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    print(protClustObj.clustResultObj.sampleClustSer)


def Clsutering_ConsensusHierarchical():
    """
    Build a new object protClustObj to save the clustering result and then run Consensus Hierarchical clustering.
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='hierarchicalClust',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean',
                                        ccLinkage='ward')

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    print(protClustObj.clustResultObj.sampleClustSer)


def Clsutering_ConsensusKmeans():
    """
    Build a new object protClustObj to save the clustering result and then run Consensus Kmeans clustering.
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(ccMethod='kmeansClust_nltk', method="consensusClust",
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean')

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)
    print(type(protClustObj))
    print(protClustObj.clustResultObj.sampleClustSer)


### Scoring ###

def Scoring_CalGiniScore():
    """
    Calculate the gini score of a consensus kmeans clutsering result.

    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                    minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean', )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    Scoring.CalcGiniScore(protDataObj, protClustObj)
    print("giniScore: " + str(protClustObj.clustScoringObj.giniScore))


def Scoring_CalEveryScore():
    """
    Use CalEveryScore to calculate every scoring function we have, some are only related to clustering result like gini
    score and sihouette score, others are related to clustering result and meta data.

    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean')

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    Scoring.CalcEveryScore(protDataObj, protClustObj)

    # print scoring results
    print("partitionIndex: "+str(float(protClustObj.clustScoringObj.partitionIndex)))
    print("purity: " + str(protClustObj.clustScoringObj.purity))
    print("separation index: " + str(protClustObj.clustScoringObj.separationIndex))
    print("giniScore: " + str(protClustObj.clustScoringObj.giniScore))
    print("silhScore: " + str(protClustObj.clustScoringObj.silhScore))
    print("clustSilhScoreSer: " + str(protClustObj.clustScoringObj.clustSilhScoreSer))
    print("sampleSilhScoreSer: " + str(protClustObj.clustScoringObj.sampleSilhScoreSer))
    print("clustFeatureEntropySer: "+str(protClustObj.clustScoringObj.clustFeatureEntropySer))
    print("featureAriDi: " + str(protClustObj.clustScoringObj.featureAriDi))
    print("featureAmiDi: " + str(protClustObj.clustScoringObj.featureAmiDi))
    print("featureEntropyDi: " + str(protClustObj.clustScoringObj.featureEntropyDi))
    print("featureMaxFscoreDi: " + str(protClustObj.clustScoringObj.featureMaxFscoreDi))
    print("featureVscoreDi: " + str(protClustObj.clustScoringObj.featureVscoreDi))
    print("clustFeatureValueRatioSer: "+str(protClustObj.clustScoringObj.clustFeatureValueRatioSer))
    print("featurePairedFscoreDi: " + str(protClustObj.clustScoringObj.featurePairedFscoreDi))







### Visualization ###

def Visualization_CombineFig():
    """
    choose two interested features in metadata to see the connection between features and clustering result by the
    diverge bar, stacked bar and scatter plot together.
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean', )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    ### draw combine figure, choose two metadata feature to compare, needs to count entropy first
    protClustObj = Scoring.CalcClustFeatureEntropy(protDataObj, protClustObj)
    protClustObj = Scoring.CalcFeatureEntropy(protDataObj, protClustObj)
    currentFeatureSer = protDataObj.GetMetadataDf()['Stage']
    compareFeatureSer = protDataObj.GetMetadataDf()['pathology_N_stage']
    Visualization.DrawCombinedFig(protClustObj, currentFeatureSer, compareFeatureSer,  figTitleStr='Combined Figure',
                    figSizeLi=[15, 4], dpi=96, wSpace=0.7, pathStr='combinFig.png',
                    colorsStr='Set1', orderLi=['stacked', 'scatter', 'diverge'])


def Visualization_Featureplot():
    """
    You can also draw diverge bar, stacked bar and scatter plot separately.
    Diverge bar is to see the difference of entropy between each cluster
    Stacked bar is to see the number the feature values between each cluster
    Scatter plot is to see two features' distribution between each cluster
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean')

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    ### draw feature plot, choose two metadata feature to compare, needs to count entropy first
    protClustObj = Scoring.CalcClustFeatureEntropy(protDataObj, protClustObj)
    protClustObj = Scoring.CalcFeatureEntropy(protDataObj, protClustObj)
    currentFeatureSer = protDataObj.GetMetadataDf()['Stage']
    compareFeatureSer = protDataObj.GetMetadataDf()['pathology_N_stage']

    ### draw scatterplot, stackedbar, divergebar , respectively
    Visualization.DrawDivergeBar(protClustObj, currentFeatureSer, figSizeLi=[5, 4], dpi=96, path='divergebar.png')
    Visualization.DrawStackedBar(protClustObj, currentFeatureSer, color="Set1", edgeColor='white', width=0.5,
                   legendSize=10, figSizeLi=[5, 4], path='stackedbar.png', dpi=96)
    Visualization.DrawScatterPlot(protClustObj, currentFeatureSer, compareFeatureSer, color='Set1',
                    labelSize=10, path='scatterplot.png', figSizeLi=[5,4], dpi=96)


def Visualization_MetaColorMap():
    """
    Draw MetaColorMap that shows the distribution of each feature values in every clusters, the default is to choose all
    of the features, you can also use a list or csv file to choose which features you want to put in.

    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean', )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    ###draw MetaColorMap, show each samples' metadata feature

    labelLi = ['Gender', 'pathology_T_stage', 'pathology_N_stage', 'Stage', 'Integrated.Phenotype', 'CIN']
    Visualization.MetaColorMap(protDataObj, protClustObj, selectFeatureSer=labelLi, path='meta_colorbar.png')


def Visualization_SilhouettePlot():
    """
    Draw sihouette plot to see each cluster distance silhouette score, to make sure the clustering result is reasonable.
    Need to calculate silhouette score first
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean', )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    Scoring.CalcEveryScore(protDataObj, protClustObj)

    # draw sihouette plot
    Visualization.DrawSilhouettePlot(protDataObj, protClustObj, path='silhou.png')


def Visualization_SampleOverlap():
    """
    Draw a heat map about the sample overlap between two clustering results, to see each cluster is similar or not.

    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    # clustering result 1
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean' )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    # clustering result 2
    protClustObj2 = ds_ProtClust()
    protClustObj2.clustParamObj.SetParam(method="hierarchicalClust", linkage="complete",distance="cosine", clustNum=5)
    protClustObj2 = ClusteringMethod.Clustering(protDataObj, protClustObj2)

    print('ARI: '+str(adjusted_rand_score(protClustObj.clustResultObj.sampleClustSer.tolist(),
                                  protClustObj2.clustResultObj.sampleClustSer.tolist())))

    Visualization.FindSampleOverlapHeatmap(protClustObj, protClustObj2, path='SampleOverlap.png')

def Visualization_Heatmap():
    """
        Draw a heat map of ratio table, you can sort the data first.

    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    # sort protein data
    protDataObj = DataAdapter.SortByRow(protDataObj)


    # clustering
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean' )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    Visualization.DrawHeatMap(protDataObj, protClustObj, colorStr="coolwarm", clustColorStr='Set1', wSpace=0.02, figSizeLi=[20, 20],
                path=None, dpi=96)

def Visualization_CorrelationHeatmap():

    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean' )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    #Scoring.CalcEveryScore(protDataObj, protClustObj)
    Visualization.DrawPatientToPatientCorrHeatmap(protDataObj, protClustObj, path="corHeatmap.png",
                                                  colorsStr="coolwarm", figSizeLi=[10, 10], dpi=96)


def Visualization_PCA():
    """
    Draw a PCA plot to see the clustering result in a 2D plot.

    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean' )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    Visualization.PlotPca(protDataObj, protClustObj, dpi=96, path='PCA.png')


def Visualization_TSNE():
    """
    Draw a TSNE plot to see the clustering result in a 2D plot.
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean' )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    Visualization.PlotTsne(protDataObj, protClustObj, perplexity=30, dpi=96, figSizeLi=[6.4, 4.8], pointSize=6,
                           path='TSNE.png')

def Visualization_MosaicPlot():
    """
        Draw a mosaic plot to see the relation of a feature and clustering result .

    """
    protDataObj = DataAdapter.ReadFilesPath("Example/pancan32/pancan11_RGB/pancan11protRatio.csv",
                                            "Example/pancan32/pancan11_RGB/pancan11metadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=8, maxK=8, resample=0.8, resample_times=1000, ccDistance='manhattan')

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    Scoring.CalcFeatureAriScore(protDataObj, protClustObj)
    Visualization.DrawMosaicPlot(protDataObj, protClustObj, 'Cancer_Type', path='Mosaic.png')
Visualization_MosaicPlot()
### Statistics ###

def Statistics_Wilcon():
    """
    Run rank sum test to each cluster to see the p-value of each feature. the result can then be used to GO term and
    pathway analysis
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean' )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)
    clustNum = 5
    Statistics.RunWilconTest(protDataObj, protClustObj, clustNum, 'consensusClust')


def Statistics_GSEA():
    """
    Turn the ratio table and the clustering result into a gct and a cls file(GSEA format)
    :return:
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)

    Statistics.GenerateGctFile(protDataObj, path='GSEAGeneTable.gct')

    protClustObj = ds_ProtClust()

    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean')

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    Statistics.GenerateClsFile(protClustObj, path='GSEASampleClust.cls')



def Characterization_Characterize():
    """
    Compare odd ratio between each cluster and feature.
    Need to run scoring function first.
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean', )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)

    Scoring.CalcEveryScore(protDataObj, protClustObj)
    cutoffUpper = 2.0
    cutoffLower = 0.5
    Characterization.Characterize(protClustObj, cutoffUpper, cutoffLower)


def DumpObject():
    """
    After you finish clustering, you can save ds_ProtClust and ds_InputRawData object as pkl files to use next file.
    """
    protDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
    protDataObj = DataAdapter.RemoveProtWithNa(protDataObj)
    protDataObj = DataAdapter.FilterByCutoff(protDataObj, methodStr='MAD', cutOff=0.5)
    protClustObj = ds_ProtClust()
    protClustObj.clustParamObj.SetParam(method="consensusClust", ccMethod='kmeansClust_nltk',
                                        minK=5, maxK=8, resample=0.8, resample_times=1000, ccDistance='euclidean', )

    protClustObj = ClusteringMethod.Clustering(protDataObj, protClustObj)
    DataAdapter.DumpRawDataObj(protDataObj, 'colonCancer.pkl')
    DataAdapter.DumpProtClustObj(protClustObj, 'colonCancer_consensus.pkl')


def LoadObject():
    """
    Load the pkl file into ds_ProtClust and ds_InputRawData object
    """
    protDataObj = DataAdapter.LoadRawDataObj('colonCancer.pkl')
    protClustObj = DataAdapter.LoadProtClustObj('colonCancer_consensus.pkl')

    print(protDataObj.GetProtRatioDf())
    print(protClustObj.clustResultObj.sampleClustSer)
