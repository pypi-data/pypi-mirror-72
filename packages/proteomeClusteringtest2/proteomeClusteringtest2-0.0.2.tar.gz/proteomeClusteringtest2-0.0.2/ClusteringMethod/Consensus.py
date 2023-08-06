import numpy as np
from itertools import combinations
import bisect
from sklearn import cluster, metrics, datasets
from sklearn.cluster import AgglomerativeClustering
from nltk.cluster import KMeansClusterer, euclidean_distance
from .CommonFunction import *
import scipy.cluster as sc
import scipy.cluster.hierarchy as sch

class ConsensusClust:
    """

    :param cluster: clustering method
    :type cluster: string
    :param minK: smallest number of clusters to try
    :type minK: int
    :param maxK: biggest number of clusters to try   minK = 5, maxK = 6 -> iteration = 2 , cluster number = 5 or 6minK = 5, maxK = 5 -> iteration = 1 , cluster number = 5
    :type maxK: int
    :param resample_times: number of resamplings for each cluster number
    :type resample_times: int
    :param resample_proportion: percentage to sample
    :type resample_proportion: float
    :param **kwargs: more parameter for other cluster method
    :type **kwargs: dict
    
    .. note::
        Mk: consensus matrices for each k (shape =(K,data.shape[0],data.shape[0]))\n
        Ak: area under CDF for each number of clusters\n
        deltaK: changes in areas under CDF\n
        bestK: number of clusters that was found to be best
    """
    def __init__(self, cluster, minK, maxK, resample_times=100, resample_proportion=0.8, **kwargs):
        assert 0 <= resample_proportion <= 1, "proportion has to be between 0 and 1"
        self.cluster_ = cluster
        self.resample_proportion_ = resample_proportion
        self.L_ = minK
        self.K_ = maxK+1
        self.H_ = resample_times
        self.Mk = None
        self.Ak = None
        self.CDF = None
        self.deltaK = None
        self.bestK = None
        self.karg = kwargs

    def _InternalResample(self, dataArr, proportion):
        """
        :param dataArr: target data for clustering
        :type dataArr: list
        :param proportion: percentage to sample
        :type proportion: float
        """
        resampled_indices = np.random.choice(
            range(dataArr.shape[0]), size=int(dataArr.shape[0] * proportion), replace=False)
        return resampled_indices, dataArr[resampled_indices, :]

    def fit(self, dataArr, verbose=False):
        """
        Fits a consensus matrix for each number of clusters

        :param dataArr: target data for clustering
        :type dataArr: list
        :param verbose: should print or not
        :type verbose: bool
        """
        Mk = np.zeros((self.K_ - self.L_, dataArr.shape[0], dataArr.shape[0]))
        Is = np.zeros((dataArr.shape[0],) * 2)
        for k in range(self.L_, self.K_):  # for each number of clusters
            i_ = k - self.L_
            if verbose:
                print("At k = %d, aka. iteration = %d" % (k, i_))
            for h in range(self.H_):  # resample H times
                if verbose:
                    print("\tAt resampling h = %d, (k = %d)" % (h, k))
                resampled_indices, resample_data = self._InternalResample(
                    dataArr, self.resample_proportion_)

                if self.cluster_ == cluster.KMeans:
                    Mh = self.cluster_(n_clusters=k).fit_predict(resample_data)
                elif self.cluster_ == KMeansClusterer:
                    dist = self.karg['distance'] if self.karg.get('distance') else 'euclidean'
                    distance = GetDistance(dist)
                    Mh = self.cluster_(num_means=k, distance=distance, repeats=1, avoid_empty_clusters=True).cluster(resample_data, True)
                    Mh = np.array(Mh)
                elif self.cluster_ == AgglomerativeClustering:
                    distance = self.karg['distance'] if self.karg.get('distance') else 'euclidean'
                    linkage = self.karg['linkage'] if self.karg.get('linkage') else 'ward'
                    if distance == 'pcc':
                        resample_data = GeneratePairwiseDistMat(dataDf=resample_data, distanceStr='correlation')
                        distance = 'precomputed'
                    Mh = self.cluster_(n_clusters=k, affinity=distance, linkage=linkage).fit_predict(resample_data)

                elif self.cluster_ == sc.hierarchy.cut_tree:
                    distance = self.karg['distance'] if self.karg.get('distance') else 'euclidean'
                    linkage = self.karg['linkage'] if self.karg.get('linkage') else 'ward'
                    disMat = sch.distance.pdist(resample_data, distance)
                    tree = sch.linkage(disMat, method=linkage)
                    clustered = self.cluster_(tree, k)
                    clustered.shape = (1,len(resample_data))
                    Mh = clustered[0]

                else:
                    print('please provide available clutering mothod')
                    break
                # find indexes of elements from same clusters with bisection
                # on sorted array => this is more efficient than brute force search
                id_clusts = np.argsort(Mh)
                sorted_ = Mh[id_clusts]
                id_clusts2 = []
                for i in range(len(id_clusts)):
                    id_clusts2.append(resampled_indices[id_clusts[i]])
                for i in range(k):  # for each cluster
                    ia = bisect.bisect_left(sorted_, i)
                    ib = bisect.bisect_right(sorted_, i)
                    is_ = id_clusts2[ia:ib]
                    ids_ = np.array(list(combinations(is_, 2))).T
                    # sometimes only one element is in a cluster (no combinations)
                    if ids_.size != 0:
                        Mk[i_, ids_[0], ids_[1]] += 1
                        Mk[i_, ids_[1], ids_[0]] += 1
                # increment counts

                ids_2 = np.array(list(combinations(resampled_indices, 2))).T
                Is[ids_2[0], ids_2[1]] += 1
                Is[ids_2[1], ids_2[0]] += 1
            Mk[i_] /= Is + 1e-8   # consensus matrix
            Mk[i_, range(dataArr.shape[0]), range(
                dataArr.shape[0])] = 1  # always with self
            Is.fill(0)  # reset counter

        self.Mk = Mk
        # fits areas under the CDFs
        self.Ak = np.zeros(self.K_ - self.L_)
        self.CDF = {}
        for i, m in enumerate(Mk):
            m2 = []
            for f in range(len(m)):
                for k in range(len(m)):
                    if(f<k):
                        m2.append(m[f][k])
            bins = [i/100 for i in range(101)]
            hist, bins = np.histogram(m2,bins=bins, density=True)
            self.Ak[i] = np.sum(h * (b - a)
                                for b, a, h in zip(bins[1:], bins[:-1], np.cumsum(hist)))
            cdfLi = []
            for b,a,h in zip(bins[1:], bins[:-1], np.cumsum(hist)):
                cdfLi.append(h*(b-a))
            index = i+self.L_
            self.CDF.update({index:cdfLi})
        # fits differences between areas under CDFs

        self.deltaK = np.array([(Ab - Aa) / Aa if i > 2 else Aa
                                for Ab, Aa, i in zip(self.Ak[1:], self.Ak[:-1], range(self.L_, self.K_ - 1))])
        self.bestK = np.argmax(self.deltaK) + \
                     self.L_ if self.deltaK.size > 0 else self.L_
        return self

    def Predict(self):
        """
        For best cluster number (determined in fit function), Predict cluster index of samples based on consensus matrix
        """
        assert self.Mk is not None, "First run fit"
        if self.cluster_ == cluster.KMeans:
            predArr = self.cluster_(n_clusters=self.bestK).fit_predict(
                1 - self.Mk[self.bestK - self.L_])
        elif self.cluster_ == KMeansClusterer:
            # nltk kmeans
            # dist = self.karg['distance'] if self.karg.get('distance') else 'euclidean'
            # distance = GetDistance(dist)
            # predArr = self.cluster_(num_means=self.bestK, distance=distance, repeats=300,avoid_empty_clusters=True).cluster( 1 - self.Mk[self.bestK - self.L_], True)

            # sklearn kmeans
            predArr = cluster.KMeans(n_clusters=self.bestK).fit_predict(
                1 - self.Mk[self.bestK - self.L_])

        elif self.cluster_ == AgglomerativeClustering:
            # distance = 'euclidean'
            # # distance = self.karg['distance'] if self.karg.get('distance') else 'euclidean'
            # linkage = 'ward'
            distance = self.karg['finaldistance'] if self.karg.get('finaldistance') else 'euclidean'
            data = 1 - self.Mk[self.bestK - self.L_]
            if distance == 'pcc':
                data = GeneratePairwiseDistMat(dataDf=1 - self.Mk[self.bestK - self.L_], distanceStr='correlation')
                distance = 'precomputed'
            linkage = self.karg['finallinkage'] if self.karg.get('finallinkage') else 'ward'
            predArr = self.cluster_(n_clusters=self.bestK, affinity=distance, linkage=linkage).fit_predict(data)
        else:
            distance = self.karg['finaldistance'] if self.karg.get('finaldistance') else 'euclidean'
            linkage = self.karg['finallinkage'] if self.karg.get('finallinkage') else 'ward'
            disMat = sch.distance.pdist(1 - self.Mk[self.bestK - self.L_], distance)
            tree = sch.linkage(disMat, method=linkage)
            clustered = self.cluster_(tree, self.bestK)
            clustered.shape = (1, self.Mk[self.bestK - self.L_].shape[0])
            predArr = clustered[0]
        return np.array(predArr)


