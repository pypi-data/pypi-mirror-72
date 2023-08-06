import Scoring
import ClusteringMethod
import Characterization
import DataAdapter
import Visualization  
from DataStructure import ds_InputRawData
from DataStructure import ds_ProtClust
import time
def ClusteringTest():
	# rawDataObj = DataAdapter.LoadRawDataObj('./rawData.pickle')
	# protClustObj = DataAdapter.LoadProtClustObj('./protClust.pickle')
	# print(protClustObj.clustResultObj.characterRatioDf)
	rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv","Example/colonCancerMetadata.csv")
	# rawDataObj = DataAdapter.ReadFilesPath("~/Desktop/pancan11protRatio.csv","~/Desktop/pancan11metadata.csv")
	protClustObj = ds_ProtClust()

	# protClustObj.clustParamObj.SetParam(method='kmeansClust_nltk',clustNum=5,kmeansDisatance='pcc',repeats=10)
	# protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
	# protClustObj = Scoring.CalcEveryScore(rawDataObj,protClustObj)
	# Characterization.PrintParagraph(rawDataObj,protClustObj)

	# protClustObj.clustParamObj.SetParam(method='kmeansClust_nltk',clustNum=5,kmeansDisatance='euclidean',repeats=1)
	# protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
	# protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)

	# protClustObj.clustParamObj.SetParam(method='kmeansClust_nltk',clustNum=5,kmeansDisatance='euclidean',repeats=10)
	# protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
	# protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)

	# protClustObj = Characterization.Characterize(protClustObj,2,0.5)
	# Characterization.PrintParagraph(rawDataObj,protClustObj)

	# protClustObj.clustParamObj.SetParam(method='kmeansClust_sklearn',clustNum=5,seed=10)
	# protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
	# protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)
	# protClustObj = Characterization.Characterize(protClustObj,2,0.5)
	#
	# protClustObj.clustParamObj.SetParam(method='hierarchicalClust_scipy',clustNum=5,linkage='ward',distance='cosine')
	# protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
	# protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)
	# protClustObj = Characterization.Characterize(protClustObj,2,0.5)
	
	# protClustObj.clustParamObj.SetParam(method='hierarchicalClust',clustNum=5,linkage='average',distance='euclidean')
	# protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
	# protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)
	# protClustObj = Characterization.Characterize(protClustObj,2,0.5)
	
	# protClustObj.clustParamObj.SetParam(method='consensusClust',ccMethod='hierarchicalClust',resample=0.8,ccLinkage='ward',ccDistance='euclidean',minK=4,maxK=6,resample_times=10)
	# protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
	# Visualization.DrawConsensusClustCDF(protClustObj)

	protClustObj.clustParamObj.SetParam(method='consensusClust', ccMethod='hierarchicalClust', resample=0.8,
										ccLinkage='single',ccFinalLinkage='average', ccDistance='euclidean',ccFinalDistance='pcc',
										minK=4, maxK=6, resample_times=10)
	protClustObj = ClusteringMethod.Clustering(rawDataObj, protClustObj)
	# Visualization.DrawConsensusClustCDF(protClustObj)

	# protClustObj.clustParamObj.SetParam(method='consensusClust', ccMethod='hierarchicalClust', resample=0.8,
	# 									ccLinkage='average',ccDistance='euclidean', minK=4, maxK=6, resample_times=10)
	# protClustObj = ClusteringMethod.Clustering(rawDataObj, protClustObj)
	# Visualization.DrawConsensusClustCDF(protClustObj)
	# protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)
	# protClustObj = Characterization.Characterize(protClustObj, 2, 0.5)

	protClustObj.clustParamObj.SetParam(method='consensusClust',ccMethod='hierarchicalClust_scipy',resample=0.8,ccLinkage='ward',ccDistance='cosine',ccFinalDistance='correlation',minK=4,maxK=6,resample_times=10)
	protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
	# Visualization.DrawConsensusClustCDF(protClustObj)
	# protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)
	# protClustObj = Characterization.Characterize(protClustObj,2,0.5)
	#
	# protClustObj.clustParamObj.SetParam(method='consensusClust',ccMethod='kmeansClust_nltk',resample=0.8,ccDistance='pcc',minK=2,maxK=6,resample_times=10)
	# protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
	#
	# protClustObj.clustParamObj.SetParam(method='consensusClust', ccMethod='kmeansClust_sklearn', resample=0.8,
	# 									 minK=2, maxK=6, resample_times=10)
	# protClustObj = ClusteringMethod.Clustering(rawDataObj, protClustObj)
	# Visualization.DrawConsensusClustCDF(protClustObj)
	# protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)
	# protClustObj = Characterization.Characterize(protClustObj,2,0.5)

	# DataAdapter.DumpRawDataObj(rawDataObj,'./rawData.pickle')
	# DataAdapter.DumpProtClustObj(protClustObj,'./protClust.pickle')

def ReadClustResult(path):
	import pandas as pd
	rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
	protClustObj = ds_ProtClust()
	input_file = pd.read_csv(path,header=None)
	protClustObj = ClusteringMethod.ReadClustSeries(input_file[1],rawDataObj,protClustObj)
	protClustObj = Scoring.CalcFeatureRatio(rawDataObj,protClustObj)
	protClustObj = Characterization.Characterize(protClustObj,2,0.5)
	protClustObj = Characterization.Characterize(protClustObj,3/2,2/3)

def Kmeans_test():
	from sklearn.metrics.cluster import adjusted_rand_score
	import numpy as np
	from scipy import stats
	rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv","Example/colonCancerMetadata.csv")
	protClustObj = ds_ProtClust()

	nltk_kmeans = []
	sklearn_kmeans = []
	nltk_kmeans_ari = []
	sklearn_kmeans_ari = []
	hclust = []
	hclust_ari = []
	ccMatrix = []
	ccMatrix_ari = []

	for i in range(100):
		protClustObj.clustParamObj.SetParam(method='consensusClust',ccMethod='kmeansClust_sklearn',resample=0.8,minK=5,maxK=5,resample_times=1000)
		protClustObj,mk = ClusteringMethod.Clustering(rawDataObj,protClustObj)
		mk = np.array(mk)
		mk = mk.flatten()
		# sklearn_kmeans.append(protClustObj.clustResultObj.sampleClustSer)
		sklearn_kmeans.append(mk)

		protClustObj.clustParamObj.SetParam(method='consensusClust',ccMethod='kmeansClust_nltk',resample=0.8,ccDistance='euclidean',minK=5,maxK=5,resample_times=1000)
		protClustObj,mk = ClusteringMethod.Clustering(rawDataObj,protClustObj)
		# nltk_kmeans.append(protClustObj.clustResultObj.sampleClustSer)
		mk = np.array(mk)
		mk = mk.flatten()
		nltk_kmeans.append(mk)

		# protClustObj.clustParamObj.SetParam(method='consensusClust',ccMethod='hierarchicalClust',resample=0.8,ccLinkage='ward',ccDistance='euclidean',minK=5,maxK=6,resample_times=1)
		# protClustObj,mk = ClusteringMethod.Clustering(rawDataObj,protClustObj)
		# # hclust.append(protClustObj.clustResultObj.sampleClustSer)
		# mk = np.array(mk)
		# mk = mk.flatten()
		# hclust.append(mk)
	
	for i in range(100):
		for j in range(100):
			ccMatrix =  round(stats.pearsonr(sklearn_kmeans[i], nltk_kmeans[j])[0],2)
			# ccMatrix = round(adjusted_rand_score(sklearn_kmeans[i],nltk_kmeans[j]),2)
			ccMatrix_ari.append(ccMatrix)
	# for i in range(10):
	# 	for j in range(i+1,10):

	# 		# sklean_ari = round(adjusted_rand_score(sklearn_kmeans[i],sklearn_kmeans[j]),2)
	# 		# nltk_ari = round(adjusted_rand_score(nltk_kmeans[i],nltk_kmeans[j]),2)
	# 		# sklearn_kmeans_ari.append(sklean_ari)
	# 		# nltk_kmeans_ari.append(nltk_ari)
	# 		h_ari = round(adjusted_rand_score(hclust[i],hclust[j]),2)
	# 		hclust_ari.append(h_ari)
	# 		# print("Cluster 1 : {}, Cluster 2 : {} , ARI score : {}".format(i,j,ari))
	# print(sklearn_kmeans_ari)
	# print('\n\n\n')
	# print(nltk_kmeans_ari)

	with open('./kmeans_ari2.txt','w') as of:
		# of.write("sklearn kmeans ari :\n")
		# of.write(str(sklearn_kmeans_ari))
		# of.write("nltk kmeans ari :\n")
		# of.write(str(nltk_kmeans_ari))
		of.write("sklearn & nltk consensus matrix ari :\n")
		of.write(str(ccMatrix_ari))
	of.close()
	
def hierarchicalClustTest():

	from sklearn.metrics.cluster import adjusted_rand_score
	import numpy as np
	from scipy import stats
	rawDataObj = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv","Example/colonCancerMetadata.csv")
	protClustObj = ds_ProtClust()

	scipy_distance = ['euclidean','correlation','cosine','cityblock']
	sklearn_distance = ['euclidean','pcc','cosine','manhattan']
	linkage = ['ward','complete','average','single']
	ari = []
	for i in range(4):
		if(linkage[i] == 'ward'):
				protClustObj.clustParamObj.SetParam(method='hierarchicalClust',clustNum=5,linkage=linkage[i],distance='euclidean')
				protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
				a = protClustObj.clustResultObj.sampleClustSer
				p = "ward_euclidean_hierarchicalClust"
				Visualization.PlotPca(rawDataObj,protClustObj,path=p)
				protClustObj.clustParamObj.SetParam(method='hierarchicalClust_scipy',clustNum=5,linkage=linkage[i],distance='euclidean')
				protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
				b = protClustObj.clustResultObj.sampleClustSer
				p = "ward_euclidean_hierarchicalClust_scipy"
				colorLi = ['#2ca02c','#d62728','#ff7f0e','#9467bd','#1f77b4']
				Visualization.PlotPca(rawDataObj,protClustObj,path=p,colorLi=colorLi)
				ari.append(round(adjusted_rand_score(a,b),2))
		# else:
		# 	for j in range(4):
		# 			protClustObj.clustParamObj.SetParam(method='hierarchicalClust_scipy',clustNum=5,linkage=linkage[i],distance=scipy_distance[j])
		# 			protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
		# 			a = protClustObj.clustResultObj.sampleClustSer
		# 			p = linkage[i]+'_'+scipy_distance[j]+"hierarchicalClust_scipy"
		# 			Visualization.PlotPca(rawDataObj,protClustObj,path=p)
		# 			protClustObj.clustParamObj.SetParam(method='hierarchicalClust',clustNum=5,linkage=linkage[i],distance=sklearn_distance[j])
		# 			protClustObj = ClusteringMethod.Clustering(rawDataObj,protClustObj)
		# 			b = protClustObj.clustResultObj.sampleClustSer
		# 			p = linkage[i]+'_'+sklearn_distance[j]+"_hierarchicalClust"
		# 			Visualization.PlotPca(rawDataObj,protClustObj,path=p)
		# 			ari.append(round(adjusted_rand_score(a,b),2))
	print(ari)

def consensusKMTest():
	from sklearn.metrics.cluster import adjusted_rand_score
	rawDataObj1 = DataAdapter.ReadFilesPath("Example/colonCancerProtRatio.csv", "Example/colonCancerMetadata.csv")
	rawDataObj2 = DataAdapter.ReadFilesPath("~/Desktop/pancan11protRatio.csv","~/Desktop/pancan11metadata.csv")
	protClustObj = ds_ProtClust()

	ari_list = []
	# dist = 'euclidean'
	# dist = 'pcc'
	# dist = 'cosine'
	# dist = 'manhattan'
	dist = ['euclidean','pcc','cosine','manhattan']
	for i in range(4):

		protClustObj.clustParamObj.SetParam(method='consensusClust', ccMethod='kmeansClust_nltk', resample=0.8,
											ccDistance=dist[i], minK=5, maxK=5, resample_times=100)
		protClustObj = ClusteringMethod.Clustering(rawDataObj1, protClustObj)
		a = protClustObj.clustResultObj.sampleClustSer
		ari_list.append(a)
	nltk_kmeans_ari = []
	for i in range(4):
		for j in range(i+1,4):
			nltk_ari = round(adjusted_rand_score(ari_list[i],ari_list[j]),2)
			nltk_kmeans_ari.append(nltk_ari)
	print(nltk_kmeans_ari)




ClusteringTest()
# ReadClustResult('~/Downloads/colon_ward_hierarchical.csv')
# Kmeans_test()
# hierarchicalClustTest()
# consensusKMTest()
