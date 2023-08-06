"""
Contain ReadFilesPath(), CheckRatioNotEmpty(), CheckMetadataNotEmpty
"""

import pandas as pd
import numpy as np
from DataStructure import ds_InputRawData
from .CommonFunction import GenerateStat, PrintStat
from .DataChecking import CheckFileExistence, CheckPatientNum
from .DataCleaning import RemoveContinuousFeature, AssignNaStrToNotAvailableCell, RemoveProtWithNa


def ReadFilesPath(protRatioPath, metadataPath, metadataCategoryPath=''):
    """
   
    :param protRatioPath: string of path of protein ratio file (protein and patient as row and column)
    :type protRatioPath: str
    :param metadataPath: string of path of metadata file (patient and metadata as row and column)
    :type metadataPath: str
    :param metadataCategoryPath: string of path of file that determines metadata are categorical or not.

        file content: row1 is feature labels, row2 is 0 (continuous) or 1 (categorical).
        ::
            +---------------+----------+----------+-----+
            | name          | feature1 | feature2 | ... /
            +============+============+===========+=====+
            | isCategorical | 0        | 1        | ... /
            +---------------+----------+----------+-----+

    :return: ds_InputRawData
    :rtype: object
    """

    # Input
    protRatioDf = pd.read_csv(protRatioPath, index_col=0)
    protRatioDf_transposed = protRatioDf.T  # Transpose protRatioDf (patient and protein as row and column)
    metadataDf = pd.read_csv(metadataPath, index_col=0)

    # Check path cannot be ""
    if len(metadataCategoryPath) != 0:
        metadataCategoryDf = pd.read_csv(metadataCategoryPath, index_col=0)
    else:
        metadataCategoryDf = pd.DataFrame()
    # Check pd.DataFrame() cannot be empty
    if not(CheckFileExistence(protRatioDf=protRatioDf_transposed, metadataDf=metadataDf)):
        return 0
    # Check number of patients is equal in protein ratio and metadata
    if not(CheckPatientNum(protRatioDf=protRatioDf_transposed, metadataDf=metadataDf)):
        return 0

    # Make lowercase
    metadataDf = metadataDf.applymap(lambda x: x.lower() if type(x) == str else x)
    # Drop continuous columns of metadataDf
    metadataDf = RemoveContinuousFeature(metadataDf=metadataDf, metadataCategoryDf=metadataCategoryDf)
    # Deal with metadata's missing value
    metadataDf = AssignNaStrToNotAvailableCell(metadataDf)

    # Create ds_InputRawData object
    rawDataObj = ds_InputRawData(protRatioDf_transposed, metadataDf)
    rawDataObj.patientNameLi = list(protRatioDf_transposed.columns[:])
    rawDataObj = GenerateStat(rawDataObj)

    if protRatioDf_transposed.isnull().values.any():
        print("Need call RemoveProtWithNa() or Impute later.\n")

    return rawDataObj


def CheckRatioNotEmpty(ds_InputRawDataObj):
    """
    Check protRatio is not empty.

    :param ds_InputRawDataObj:
    :type ds_InputRawData: object
    :return: True if protRatioDf is not empty.
    :rtype: bool
    """
    if ds_InputRawDataObj.GetProtRatioDf().empty:
        print('Protein ratio is empty.')
        return False
    else:
        return True


def CheckMetadataNotEmpty(ds_InputRawDataObj):
    """
    Check metadata is not empty

    :param ds_InputRawDataObj:
    :type ds_InputRawDataObj: object
    :return: True if metadataDf is not empty.
    :rtype: bool
    """
    if ds_InputRawDataObj.GetMetadataDf().empty:
        print('Metadata is empty.')
        return False
    else:
        return True




