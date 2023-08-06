import pandas as pd


def Characterize(protClustObj, cutoffUpper, cutoffLower):
    """
    Compare feature odds ratio between clusters and background(Metadata)

    :param protClustObj: ds_ProtClust
    :type protClustObj: object
    :param cutoffUpper: to get the feature which odds ratio is higher than ceiling threshold
    :type cutoffUpper: int
    :param cutoffLower: to get the feature which odds ratio is lower than bottom threshold
    :type cutoffLower: int
    :returns: protClustObj (ds_ProtClust) with new characterRatioDf, characterFeatureDf
    """
    assert cutoffUpper > 0, 'threshold should >0'
    up_threshold = cutoffUpper
    assert cutoffLower > 0, 'threshold should >0'
    down_threshold = cutoffLower

    if protClustObj.clustScoringObj.clustFeatureValueRatioSer.empty:
        print('please run scoring function first')
    else:
        count = 1
        outputRatioDi = {}
        outputFeatureDi = {}
        clustSer = protClustObj.clustResultObj.clustSampleSer.values # use to get the amount of sample in each cluster
        for cluster in protClustObj.clustScoringObj.clustFeatureValueRatioSer:
            name = "cluster {} ( sample amount :{} )".format(count,len(clustSer[count-1]))
            characterRatioLi = []
            characterFeatureLi = []
            labelNameLi = []
            for label in cluster:
                temp1 = label[label >= up_threshold]
                temp2 = label[label > 0][label <= down_threshold]
                ratio = ';'.join([str(i) for i in temp1] + [str(i) for i in temp2])
                feature = ';'.join([str(i) for i in temp1.index] + [str(i) for i in temp2.index])
                if len(ratio) > 0:
                    characterRatioLi.append(ratio)
                    characterFeatureLi.append(feature)
                else:
                    characterRatioLi.append('NA')
                    characterFeatureLi.append('NA')
                labelNameLi.append(label.name)
            outputRatioDi.update({name: characterRatioLi})
            outputFeatureDi.update({name: characterFeatureLi})
            count += 1
        outcomeRatioDf = pd.DataFrame.from_dict(outputRatioDi)
        outcomeFeatureDf = pd.DataFrame.from_dict(outputFeatureDi)
        outcomeRatioDf.index = labelNameLi
        outcomeFeatureDf.index = labelNameLi
        outcomeRatioDf = outcomeRatioDf.T
        outcomeFeatureDf = outcomeFeatureDf.T
    PrintDescription(outcomeRatioDf, outcomeFeatureDf, cutoffUpper, cutoffLower)

    protClustObj.clustResultObj.characterRatioDf = protClustObj.clustResultObj.characterRatioDf.append(outcomeRatioDf)
    protClustObj.clustResultObj.characterFeatureDf = protClustObj.clustResultObj.characterFeatureDf.append(
        outcomeFeatureDf)
    return protClustObj


def PrintDescription(ratioDf, featureDf, cutoffUpper, cutoffLower):
    """
    log the feature filtered by threshold for each cluster

    :param ratioDf: odds ratio of each feature in each cluster
    :type ratioDf: pd.DataFrame
    :param feature: each cluster remained feature after filtering
    :type feature: pd.DataFrame
    :param cutoffUpper: to get the feature which odds ratio is higher than ceiling threshold
    :type cutoffUpper: int
    :param cutoffLower: to get the feature which odds ratio is lower than bottom threshold
    :type cutoffLower: int
    """
    if ratioDf.empty or featureDf.empty:
        print('run Characterization first')
    else:
        print("Characterization (ratio) ...")
        print(ratioDf)
        print("Characterization (feature) ...")
        print(featureDf)
        print("\n Description of each cluster (odds ratio >= {})\n".format(cutoffUpper))
        for i in ratioDf.index:
            print(i)
            for j in ratioDf.columns:
                ratioLi = ratioDf.loc[i, j].split(';')
                featureLi = featureDf.loc[i, j].split(';')
                for k in range(len(featureLi)):
                    if featureLi[k] != 'NA' and float(ratioLi[k]) > cutoffUpper:
                        print("{0:25} : {1:20}, odds ratio: {2:5.2f}".format(j, featureLi[k], float(ratioLi[k])))
            print('\n')

        print("\n Description of each cluster (odds ratio <= {})\n".format(cutoffLower))
        for i in ratioDf.index:
            print(i)
            for j in ratioDf.columns:
                ratioLi = ratioDf.loc[i, j].split(';')
                featureLi = featureDf.loc[i, j].split(';')
                for k in range(len(featureLi)):
                    if featureLi[k] != 'NA' and float(ratioLi[k]) < cutoffLower:
                        print("{0:25} : {1:20}, odds ratio: {2:5.2f}".format(j, featureLi[k], float(ratioLi[k])))
            print('\n')
