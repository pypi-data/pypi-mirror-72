# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:48:37 2019

@author: tea9262
"""
import pandas as pd


#####the Params that needed in clustering

class ds_ClustParam:


    def __init__(self):
        self.__kwargs = {}

    def SetParam(self, **kwargs):
        self.__kwargs.clear()
        self.__kwargs.update(kwargs)

    def GetParam(self, key):

        if(self.__kwargs.get(key)):
            return self.__kwargs[key]
        else:
            return 0
        # assert self.__kwargs.get(key) is not None , 'the parameter {} is not provided'.format(key)
        # return self.__kwargs[key]

    def GetParamLi(self):

        return self.__kwargs.keys()
        




class ds_ClustResult:

    def __init__(self):


        self.utilityMatrixDf = pd.DataFrame()  # sample vs cluster
        self.dendrogramSer = pd.Series()  # format to be determined
        self.clustSampleSer = pd.Series()
        self.sampleClustSer = pd.Series()
        self.clustNum =  None
        self.characterRatioDf = pd.DataFrame()
        self.characterFeatureDf = pd.DataFrame()
        self.cdfLi = None

class ds_ClustScoring:

    def __init__(self):
        self.partitionIndex = 0
        self.separationIndex = 0
        self.silhScore = 0  # silhouette
        self.purity = 0  # Purity
        self.giniScore = 0

        self.bicScore = 0

        self.clustSilhScoreSer = pd.Series()  # silhouette score for each cluster
        self.sampleSilhScoreSer = pd.Series()  # silhouette score for each sample (or patient)

        self.featureAriDi = dict()  # key: feature, value: ARI
        self.featureAmiDi = dict()  # key: feature, value: AMI
        self.featureEntropyDi = dict()  # key: feature, value: entropy
        self.featureMaxFscoreDi = dict()  # key: feature, value: max fscore calculated with single sample
        self.featureVscoreDi = dict()  # key: feature, value: Vscore
        self.featurePairedFscoreDi = dict()  # key: feature, value: paired fscore based on sample pairs

        self.clustFeatureValueRatioSer = pd.Series()  # Series (each cluster)->Dictionary(each feature,dictionary->(each feature value,ratio))
        self.clustFeatureEntropySer = pd.Series()  # Series(each cluster)->Dictionary(each feature,entropy)

class ds_ProtClust:
    def __init__(self):

        self.clustParamObj = ds_ClustParam()
        self.clustResultObj = ds_ClustResult()
        self.clustScoringObj = ds_ClustScoring()


    



