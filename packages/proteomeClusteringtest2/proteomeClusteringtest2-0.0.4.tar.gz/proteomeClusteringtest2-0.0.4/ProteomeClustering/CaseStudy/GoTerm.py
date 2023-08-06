import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os.path


def FindGoTermOverlap(upOrDownStr="up", processStr="biological", clusterNum=5, goTerm1Str="gene ontology",
                      goTerm2Str="gene ontology_consensus"):
    """
    find two clustering results' go terms overlap

    :param upOrDownStr: is set in file name, means the genes chose from rank sum test each subtype are based on > or < than rest subtypes. (although we not use down anymore)
    :param processStr: "biological", "cellular", or "molecular"
    :param clusterNum: the number of cluster
    :param goTerm1Str: go terms file name
    :param goTerm2Str: go terms file name

    :return: heatmap ratioDf

    """
    ratioDf = pd.DataFrame([[0.0 for x in range(clusterNum)]] * clusterNum)

    for col in range(clusterNum):
        path1Str = "Example/" + goTerm1Str + "/cluster" + str(col + 1) + "_" + upOrDownStr + "/" + processStr + "/cluster" + str(
            col + 1) + upOrDownStr + ".txt"

        if os.path.isfile(path1Str):
            goTerm1Df = pd.read_csv(path1Str, delimiter="\t")
        else:
            continue
        for row in range(clusterNum):
            path2Str = "Example/" + goTerm2Str + "/cluster" + str(
                row + 1) + "_" + upOrDownStr + "/" + processStr + "/cluster" + str(
                row + 1) + upOrDownStr + ".txt"
            if os.path.isfile(path2Str):
                goTerm2Df = pd.read_csv(path2Str, delimiter="\t")
            else:
                continue
            count = 0
            num = 0
            for goNameStr in goTerm1Df['geneSet']:
                num += 1

                for goName2Str in goTerm2Df['geneSet']:
                    if goNameStr == goName2Str:
                        count += 1
            totalGoTerm = _CountTotalGoTerm(goTerm1Df['geneSet'], goTerm2Df['geneSet'])
            ratioDf[col][row] = count / totalGoTerm
    print(ratioDf)

    __PrintgoTermNum(clusterNum, goTerm1Str, goTerm2Str, upOrDownStr=upOrDownStr, processStr=processStr)
    sns.heatmap(ratioDf, cmap="Reds", linewidths=.5, annot=True, vmin=0, vmax=1,
                xticklabels=[x + 1 for x in range(clusterNum)], yticklabels=[x + 1 for x in range(clusterNum)])
    plt.xlabel('ConKM_eu')
    plt.ylabel('HC_cos_comp')
    plt.savefig('Con_HC_0.4heatmap.png',dpi=300)

    return ratioDf


def _CountTotalGoTerm(goTerm1Ser, goTerm2Ser):
    """
    count the total number of two go terms without repeat
    :param goTerm1Ser: the gene set ID series of go term1. ex:[Go1,Go2,Go3]
    :param goTerm2Ser:the gene set ID series of go term2. ex:[Go1,Go2,Go3]
    :return: int, the number of two go terms
    """
    totalLi = goTerm1Ser.tolist()
    for name in goTerm2Ser:
        if _IsgoNameInOverlapLi(totalLi, name):
            continue
        else:
            totalLi.append(name)
    return len(totalLi)


def _IsgoNameInOverlapLi(geneSetLi, goName):
    """
    to judge if the gene set ID is in the go term list
    :param geneSetLi:a list contain gene set IDs
    :param goName: gene set ID
    :return: True/False
    """
    if geneSetLi == []:
        return False
    for name in geneSetLi:
        if name == goName:
            return True
    return False


def _FindGoTermOverlapLi(goTerm1Str, goTerm2Str, choseGoNum=50, upOrDownStr="up", processStr="biological",
                         clusterNum=5):
    """
    find the overlap Gene set list between (param: goTerm1Str) and (param: goTerm2Str),
    for each subtype we choose top (param: choseGoNum) overlap gene sets to the overlap list
    :param choseGoNum: the number of overlap gene sets we choose each subtype
    :param goTerm1Str: go terms file name
    :param goTerm2Str: go terms file name
    :param upOrDownStr: is set in file name, means the genes chose from rank sum test each subtype are based on > or <
    than rest subtypes. (although we not use down anymore)
    :param processStr: "biological", "cellular", or "molecular"
    :param clusterNum: the number of cluster
    :return: overlap list
    """
    overlapLi = []
    for col in range(clusterNum):
        path1Str = "Example/" + goTerm1Str + "/cluster" + str(col + 1) + "_" + upOrDownStr + "/" + processStr + "/cluster" + str(
            col + 1) + upOrDownStr + ".txt"

        if os.path.isfile(path1Str):
            goTerm1Df = pd.read_csv(path1Str, delimiter="\t")
        else:

            continue

        count = 0

        for goNameStr in goTerm1Df['geneSet']:
            if count >= choseGoNum:
                break
            elif _IsgoNameInOverlapLi(overlapLi, goNameStr):
                count += 1
                continue
            else:
                overlapLi.append(goNameStr)
                count += 1

    for col in range(clusterNum):
        path2Str = "Example/" + goTerm2Str + "/cluster" + str(
            col + 1) + "_" + upOrDownStr + "/" + processStr + "/cluster" + str(
            col + 1) + upOrDownStr + ".txt"
        if os.path.isfile(path2Str):
            goTerm2Df = pd.read_csv(path2Str, delimiter="\t")
        else:

            continue

        count = 0
        for goName2 in goTerm2Df['geneSet']:
            if count >= choseGoNum:
                break
            elif _IsgoNameInOverlapLi(overlapLi, goName2):
                count += 1
                continue
            else:
                overlapLi.append(goName2)
                count += 1

    print(overlapLi)

    print(len(overlapLi))
    return overlapLi


def _FindGoTermPValue(overlapLi, goTermClustLi, goTermStr, upOrDownStr="up", processStr="biological",
                      clusterNum=5):
    """
    base on overlapLi to find the gene sets' pvalue, in order to draw gene sets heatmap next step
    :param overlapLi: overlap Gene set list between (param: goTerm1Str) and (param: goTerm2Str)
    :param goTermClustLi: the correspond subtype order of the goTermStr, based on goTerm overlap heatmap.
    ex: two goTermStrs  have 5 subtype and goTermStr1_subtype1 similar to goTermStr2_subtype3, and the goTermClustLi
    of goTermStr1 is [1, 2, 3, 4, 5], than the goTermClustLi of goTermStr2 may be [3, 2, 1, 4 ,5]
    :param goTermStr: go terms file name
    :param upOrDownStr: is set in file name, means the genes chose from rank sum test each subtype are based on > or <
    than rest subtypes. (although we not use down anymore)
    :param processStr: "biological", "cellular", or "molecular"
    :param clusterNum: the number of cluster
    :return: pValueDf
    """
    pValueDf = pd.DataFrame([[1.0 for x in range(len(overlapLi))]] * clusterNum, columns=overlapLi)

    count = 0
    for runingClustering in range(clusterNum):
        pathStr = "Example/" + goTermStr + "/cluster" + str(
            runingClustering + 1) + "_" + upOrDownStr + "/" + processStr + "/cluster" \
               + str(runingClustering + 1) + upOrDownStr + ".txt"
        if os.path.isfile(pathStr):
            goTermDf = pd.read_csv(pathStr, delimiter="\t")
        else:
            count += 1
            continue

        goTerm2Num = goTermDf.shape[0]

        for nameStr in overlapLi:
            for i in range(goTerm2Num):

                if nameStr == goTermDf['geneSet'][i]:

                    goTermNameStr = goTermDf['geneSet'][i]
                    if goTermDf['pValue'][i] == 0:
                        pValueDf[goTermNameStr][_FindCorrespondRow(goTermClustLi, count)] = 1E-17

                    else:
                        pValueDf[goTermNameStr][_FindCorrespondRow(goTermClustLi, count)] = float(goTermDf['pValue'][i])
                        # print(goTerm['pValue'][i])
        count += 1
    return pValueDf


def DrawGoTermHeatMap(goTerm1Str, goTerm2Str, goTerm1ClustLi=None, goTerm2ClustLi=None, choseGoNum=50,
                      upOrDownStr="up", processStr="biological", clusterNum=5, dpi=96):
    """
    :param upOrDownStr: is set in file name, means the genes chose from rank sum test each subtype are based on > or <
    than rest subtypes. (although we not use down anymore)
    :param processStr: "biological", "cellular", or "molecular"
    :param clusterNum: the number of cluster
    :param goTerm1Str: go terms file name
    :param goTerm2Str: go terms file name
    :param goTerm1ClustLi:the correspond subtype order of the goTermStr, based on goTerm overlap heatmap.
    ex: two goTermStrs  have 5 subtype and goTermStr1_subtype1 similar to goTermStr2_subtype3, and the goTermClustLi
    of goTermStr1 is [1, 2, 3, 4, 5], than the goTermClustLi of goTermStr2 may be [3, 2, 1, 4 ,5]
    :param goTerm2ClustLi: same as above
    :param choseGoNum:  the number of overlap gene sets we choose each subtype
    :return:
    """
    if goTerm1ClustLi is None:
        goTerm1ClustLi = [x+1 for x in range(clusterNum)]
    if goTerm2ClustLi is None:
        goTerm2ClustLi = [x+1 for x in range(clusterNum)]
    overlapLi = _FindGoTermOverlapLi(choseGoNum=choseGoNum, upOrDownStr=upOrDownStr,
                                     processStr=processStr, clusterNum=clusterNum,
                                     goTerm1Str=goTerm1Str, goTerm2Str=goTerm2Str)

    goTermResultDf = _FindGoTermPValue(overlapLi, goTerm2ClustLi, goTermStr=goTerm2Str, upOrDownStr=upOrDownStr,
                                       processStr=processStr,
                                       clusterNum=clusterNum)
    goTermResultDf.to_csv(
        "Example/" + goTerm2Str + "/pValueTable_" + str(choseGoNum) + "_" + upOrDownStr + "_" + processStr + ".csv")

    goTermResultDf = np.log10(goTermResultDf)
    # clors=sns.palplot(sns.light_palette("red", reverse=True))
    fig, axes = plt.subplots(1, 1, figsize=(30, 3))
    mask = goTermResultDf == 0
    # yltick=__Setytick(goTerm1Clust, goTerm2Clust), xticklabels=goTermResultDf.columns
    sns.heatmap(goTermResultDf, cmap="Reds_r", mask=mask, linewidths=.5, ax=axes, xticklabels=False,
                yticklabels=goTerm2ClustLi)

    fig.savefig(
        "Example/" + goTerm2Str + "/pValueTable_" + str(choseGoNum) + "_" + upOrDownStr + "_" + processStr + ".png",
        bbox_inches="tight", dpi=dpi)

    goTermResultDf = _FindGoTermPValue(overlapLi, goTerm1ClustLi, goTermStr=goTerm1Str, upOrDownStr=upOrDownStr,
                                       processStr=processStr,
                                       clusterNum=clusterNum)
    goTermResultDf.to_csv(
        "Example/" + goTerm1Str + "/pValueTable_" + str(choseGoNum) + "_" + upOrDownStr + "_" + processStr + ".csv")

    goTermResultDf = np.log10(goTermResultDf)
    # clors=sns.palplot(sns.light_palette("red", reverse=True))
    fig, axes = plt.subplots(1, 1, figsize=(30, 3))
    mask = goTermResultDf == 0
    # RdYlBu
    sns.heatmap(goTermResultDf, cmap="Reds_r", mask=mask, ax=axes,xticklabels=False,
                yticklabels=goTerm1ClustLi)

    fig.savefig(
        "Example/" + goTerm1Str + "/pValueTable_" + str(choseGoNum) + "_" + upOrDownStr + "_" + processStr + ".png",
        bbox_inches="tight",dpi=dpi)




def __PrintgoTermNum(clusterNum, goTerm1Str, goTerm2Str, upOrDownStr="up", processStr="biological"):
    '''
    Print how many goterms in each cluster subtypes
    :param upOrDownStr: is set in file name, means the genes chose from rank sum test each subtype are based on > or <
    than rest subtypes. (although we not use down anymore)
    :param processStr: "biological", "cellular", or "molecular"
    :param clusterNum: the number of cluster
    :param goTerm1Str: go terms file name
    :param goTerm2Str: go terms file name
    :return: None
    '''
    print("Method " + goTerm1Str)
    for num in range(clusterNum):
        path1 = "Example/" + goTerm1Str + "/cluster" + str(num + 1) + "_" + upOrDownStr + "/" + processStr + "/cluster" + str(
            num + 1) + upOrDownStr + ".txt"
        if os.path.isfile(path1):
            goTerm1 = pd.read_csv(path1, delimiter="\t")
        else:
            print("cluster" + str(num + 1) + " has no gene set")
            continue
        print("cluster" + str(num + 1) + ": " + str(len(goTerm1['geneSet'])))

    print("Method " + goTerm2Str)
    for num in range(clusterNum):
        path2 = "Example/" + goTerm2Str + "/cluster" + str(num + 1) + "_" + upOrDownStr + "/" + processStr + "/cluster" + str(
            num + 1) + upOrDownStr + ".txt"
        if os.path.isfile(path2):
            goTerm2 = pd.read_csv(path2, delimiter="\t")
        else:
            print("cluster" + str(num + 1) + " has no gene set")
            continue
        print("cluster" + str(num + 1) + ": " + str(len(goTerm2['geneSet'])))

def _FindCorrespondRow(goTermClustLi, count):
    """
    put correspond goterm row in to right row
    :param goTermClustLi: the correspond subtype order of the goTermStr, based on goTerm overlap heatmap.
    ex: two goTermStrs  have 5 subtype and goTermStr1_subtype1 similar to goTermStr2_subtype3, and the goTermClustLi
    of goTermStr1 is [1, 2, 3, 4, 5], than the goTermClustLi of goTermStr2 may be [3, 2, 1, 4 ,5]
    :param count:int, current gene set position in gene set list
    :return: int, the row in gene sets heatmap
    """
    result = 0
    for go in goTermClustLi:
        if go == count + 1:
            return result

        result += 1