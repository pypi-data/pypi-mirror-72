# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:21:40 2019

@author: tea9262
"""
import pandas as pd


# the Protein ratio table and clinical metadata after normalized and imputation
class ds_InputRawData:
    """


    :param protRatioDf:
    :type protRatioDf: pd.DataFrame
    :param metadataDf:
    :type metadataDf: pd.DataFrame

    :ivar __protRatioDf: This is where we store protRatioDf.
    :vartype __protRatioDf: pd.DataFrame
    :ivar __metadataDf: This is where we store metadataDf.
    :vartype __metadataDf: pd.DataFrame
    :ivar filterMethodStr: Method of filter. Saved by function in :py:mod:`~DataAdapter.Filter` module.
    :vartype filterMethodStr: string
    :ivar numericalFormatStr: Original or Log ratio.
    :vartype numericalFormatStr: string
    :ivar patientNameLi: patients' name list.
    :vartype patientNameLi: list
    :ivar patientNum: Number of patients.
    :vartype patientNum: int
    :ivar featureNum: Number of features.
    :vartype featureNum: int
    :ivar metadataFreqDi: Frequency of metadata.
    :vartype metadataFreqDi: dictionary
    """

    def __init__(self, protRatioDf, metadataDf):
        self.__protRatioDf = protRatioDf
        self.__metadataDf = metadataDf
        self.filterMethodStr = ''  # Saved by Filter()
        self.numericalFormatStr = ''  # Original or Log
        self.patientNameLi = []  # Saved by ReadFilesPath()
        self.patientNum = 0  # Saved by _GenerateStat(), called by ReadFilesPath()
        self.featureNum = 0  # Saved by _GenerateStat(), called by ReadFilesPath()
        self.metadataFreqDi = {}  # Saved by _GenerateStat(), called by ReadFilesPath().
                                  # {'status': {'dead': 5, 'alive':10}, ...}

    def GetProtRatioDf(self):
        """
        :return: Print protein ratio (patients and proteins as rows and columns).
        :rtype: pd.DataFrame
        """
        return self.__protRatioDf

    def GetMetadataDf(self):
        """
        :return: Print metadata (patients and metadata as rows and columns).
        :rtype: pd.DataFrame
        """
        return self.__metadataDf

    def SetProtRatioDf(self, protRatioDf):
        """
        Store protRatioDf in ds_InputRawData manually.

        :param protRatioDf:
        :type protRatioDf: pd.DataFrame
        """

        self.__protRatioDf = protRatioDf

    def SetMetadataDf(self, metadataDf):
        """
        Store metadataDf in ds_InputRawData manually.

        :param metadataDf:
        :type metadataDf: pd.DataFrame
        """

        self.__metadataDf = metadataDf
