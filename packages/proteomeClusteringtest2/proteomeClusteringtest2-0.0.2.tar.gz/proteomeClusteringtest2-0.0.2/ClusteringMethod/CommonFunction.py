import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.spatial import distance


def GetDistance(dist):
	distanceDict = {
					'euclidean':distance.euclidean,
					'cosine':distance.cosine,
					'manhattan':distance.cityblock,
					'pcc':distance.correlation
					}
	return distanceDict[dist]

def GeneratePairwiseDistMat(dataDf=pd.DataFrame(), distanceStr='correlation'):
	"""
	2020/01/10
	Generate pairwise distances between observations for "Hierarchical.py".
	Support Hierarchical.hclust()

	:param dataDf:  (DataFrame) proteinRatio
	:param distanceLi: (String)
	:return:
	"""
	distanceArr = squareform(pdist(X=dataDf, metric=distanceStr))
	return distanceArr
