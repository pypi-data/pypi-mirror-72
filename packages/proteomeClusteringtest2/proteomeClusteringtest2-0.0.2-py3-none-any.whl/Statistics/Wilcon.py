import pandas as pd
from scipy.stats import mannwhitneyu


def RunWilconTest(filterRatioCsv, clusterCsv, clusterNum, fileName):
    """
    execute wilcoxon rank test to generate the genes' p-value file(to see if they pass the wilcon test) each subtype

    :param filterRatioCsv: the or the ratio table csv file that used to run wilcoxon rank test
    :param clusterCsv: the csv file that represent each sample's subtype
    :param clusterNum: the number of clusters
    :param fileName: the filename of the wilcoxon rank test results
    :return: None
    """
    if isinstance(filterRatioCsv, str):
        filterRatioDf = pd.read_csv(filterRatioCsv, index_col=0)
    else :
        filterRatioDf = filterRatioCsv.GetProtRatioDf().copy()

    if isinstance(clusterCsv, str):
        clusteringResultSer = pd.read_csv(clusterCsv, index_col=0, header=None)
        clusteringResultSer = clusteringResultSer.iloc[:, 0]
    else :
        clusteringResultSer = clusterCsv.clustResultObj.sampleClustSer

    # print(clusteringResultSer.tolist())

    for Num in range(clusterNum):
        clusterLi, nonclusterLi = _GetclusterLi(clusteringResultSer, Num + 1)
        clustfilterRatioDf = filterRatioDf.T[clusterLi]
        nonclusterfilterRatioDf = filterRatioDf.T[nonclusterLi]
        count = 0
        resultDf = pd.DataFrame()
        for geneStr in clustfilterRatioDf.index:
            count += 1
            stat, pval = mannwhitneyu(clustfilterRatioDf.T[geneStr], nonclusterfilterRatioDf.T[geneStr],
                                      use_continuity=False, alternative='greater')
            ser = pd.Series({'gene': geneStr, 'p-value': pval, 'u-stat':stat})
            resultDf = resultDf.append(ser, ignore_index=True)
        resultDf.sort_values(by='p-value', ascending=False, inplace=True)
        resultDf = resultDf[::-1]
        resultDf.to_csv(fileName + "_pval_" + str(Num + 1) + ".csv")
        print(resultDf)

    # wilcoxon()


def _GetclusterLi(clusteringResultSer, subtype):
    """
    get the current subtype's samples list and rest samples list, in order to run wilcoxon rank test

    :param clusteringResultSer: the series that represent each sample's subtype
    :param subtype:int, the current subtype
    :return: current subtype's samples list and rest samples list
    """
    clusterLi = []
    nonclusterLi = []
    for k in clusteringResultSer.index:
        if clusteringResultSer[k] == subtype:
            clusterLi.append(k)
        else:
            nonclusterLi.append(k)

    return clusterLi, nonclusterLi
