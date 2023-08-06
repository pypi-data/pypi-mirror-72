def PrintParagraph(rawDataObj, protClustObj):
    """
    print some paragraph about the clustering result

    :param rawDataObj:
    :type rawDataObj: object
    :param protClustObj:
    :type  protClustObj: object
    """
    clustSer = protClustObj.clustResultObj.clustSampleSer.values
    clustNum = protClustObj.clustResultObj.clustNum

    print("\nClustering method \n")

    paramLi = list(protClustObj.clustParamObj.GetParamLi())
    methodStr = protClustObj.clustParamObj.GetParam('method')
    k = protClustObj.clustParamObj.GetParam('clustNum')
    print("\tThe clustering method used in this run is \"{}\".\n\tThe cluster number is \"{}\".".format(methodStr,clustNum))
    print("\tOther parameters used in this run :")
    for i in paramLi:
        if i not in ['method','clustNum']:
            print("\t\t{} : {}".format(i,protClustObj.clustParamObj.GetParam(i)))
    sampleStr = ""
    for i in range(1,clustNum+1):
        sampleStr += str(len(clustSer[i-1]))
        if i == clustNum-1:
            sampleStr += ' and '
        else:
            sampleStr += ', '

    print("\nClustering result \n")

    print("\tThe samples are clustered into {} clusters .".format(clustNum))
    print("\tThe number of sample in cluster1 to cluster{} are {}respectively.".format(clustNum,sampleStr))
    
    print("\nClustering scores \n")
    # print("\tpartitionIndex : {} , separationIndex : {} , silhScore : {} , purity : {} , giniScore : {}\n" \
                    # .format(protClustObj.clustScoringObj.partitionIndex,protClustObj.clustScoringObj.separationIndex,\
                        # protClustObj.clustScoringObj.silhScore,protClustObj.clustScoringObj.purity,protClustObj.clustScoringObj.giniScore))
    print("\tpartitionIndex : ",protClustObj.clustScoringObj.partitionIndex)
    print("\tseparationIndex : ",protClustObj.clustScoringObj.separationIndex)
    print("\tsilhScore : ",protClustObj.clustScoringObj.silhScore)
    print("\tpurity : ",protClustObj.clustScoringObj.purity)
    print("\tginiScore : ",protClustObj.clustScoringObj.giniScore)
        # print("There are {} samples in {}th cluster :\n {}\n".format(len(clustSer[i-1]),i,clustSer[i-1]))
    # print("Utility Matrix Data frame :\n{}".format(protClustObj.clustResultObj.utilityMatrixDf))
    # print("Sample Series for each cluster :\n{}".format(protClustObj.clustResultObj.clustSampleSer))
    # print("Cluster ID for each sample :\n{}".format(protClustObj.clustResultObj.sampleClustSer))

