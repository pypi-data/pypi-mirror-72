from sklearn.cluster import AgglomerativeClustering
from .CommonFunction import GeneratePairwiseDistMat
import scipy.cluster as sc
import scipy.cluster.hierarchy as sch

def HierarchicalClust(rawDataObj, protClustObj):
    """
    Agglomerative Hierarchical clustering

    :param rawDataObj: ds_InputRawData
    :type rawDataObj: object 
    :param protClustObj: ds_ProtClust
    :type protClustObj: object
    :returns: predArr 

    .. note::
        The parameter in protClustObj.clustParamObj.__kwargs must include 'clustNum', 'linkage', 'distance'\n
        accepted linkage : 'ward', 'complete', 'average', 'single' \n
        accepted distance : 'euclidean', 'l1', 'l2', 'manhattan', 'cosine', 'pcc', 'precomputed' \n

    .. warning::
        if linkage is 'ward' then only 'euclidean accepted' \n
    """
    k = protClustObj.clustParamObj.GetParam('clustNum')
    linkage = protClustObj.clustParamObj.GetParam('linkage')
    distance = protClustObj.clustParamObj.GetParam('distance')
    dataArr = rawDataObj.GetProtRatioDf().values

    if distance == 'pcc':
        """
        2020/01/10
        For PCC distance
        """
        dataArr = GeneratePairwiseDistMat(dataDf=dataArr, distanceStr='correlation')
        # dataArr is pairwise distance metric
        distance = 'precomputed'

    clustering = AgglomerativeClustering(n_clusters=k, affinity=distance, linkage=linkage,
                                         compute_full_tree='auto', connectivity=None, distance_threshold=None,
                                         memory=None).fit(dataArr)
    predArr = clustering.labels_
    return predArr

def HierarchicalClust_Scipy(rawDataObj,protClustObj):
    """
        Hierarchical clustering Scipy \n
        Support ward linkage with other distance measures besides 'euclidean' distance

        :param rawDataObj: ds_InputRawData
        :type rawDataObj: object
        :param protClustObj: ds_ProtClust
        :type protClustObj: object
        :returns: predArr

        .. note::
            The parameter in protClustObj.clustParamObj.__kwargs must include 'clustNum', 'linkage', 'distance'\n
            accepted linkage : 'ward', 'complete', 'average', 'single' \n
            accepted distance : 'euclidean','correlation','cosine','cityblock' \n

        """
    k = protClustObj.clustParamObj.GetParam('clustNum')
    linkage = protClustObj.clustParamObj.GetParam('linkage')
    distance = protClustObj.clustParamObj.GetParam('distance')
    dataArr = rawDataObj.GetProtRatioDf().values

    disMat = sch.distance.pdist(dataArr,distance)
    tree = sch.linkage(disMat,method=linkage) 
    clustered = sc.hierarchy.cut_tree(tree,k)
    clustered.shape = (1,len(dataArr))
    predArr = clustered[0]

    return predArr
