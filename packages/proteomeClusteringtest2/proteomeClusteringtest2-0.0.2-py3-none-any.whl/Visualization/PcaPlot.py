# Data handling
import pandas as pd
import numpy as np

# Visualization
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def PlotPca(rawDataObj, protClustObj, dpi=96, figSizeLi=[6.4, 4.8], pointSize=6, colorLi=None, path=None):
    """
    2020/02/03
    Plot PCA in 2D.
    拿rawDataObj.__protRatioDf轉成PCA空間(只取PC1，PC2)畫成散佈點圖。
    拿protClustObj.clustResultObj.sampleClustSer來著色。

    :param rawDataObj: ds_InputRawData
    :param protClustObj: ds_ProtClust
    :param dpi: Resolution of the figure. (default = 96)
    :param figSizeLi: Figure's width, height in inches. (default = [6.4, 4.8])
    :param pointSize: The marker size in points**2. (default = 6)
    :param colorLi: The marker color. List of Hex color codes. (default = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    :param path: If is null then show the plot. Else store to that path.
    :return:
    """

    # Input
    protRatioDf = rawDataObj.GetProtRatioDf()
    clusterArr = np.array(protClustObj.clustResultObj.sampleClustSer)
    coordinateDf = _ConvertProtRatioToPcaSpace(protRatioDf)

    # Variable for figure
    coordinateDf["cluster_labels"] = clusterArr
    clusterUnique = np.unique(clusterArr)
    xlabelStr = coordinateDf.columns[0]
    ylabelStr = coordinateDf.columns[1]

    # Match cluster number and color number
    if colorLi is None:
        colorLi = [None]*len(clusterUnique)
    if len(colorLi) < len(clusterUnique):
        print('Error. Number of colors should be less than Number of clusters.')
        return 0

    # Plot
    plt.figure(dpi=dpi, figsize=figSizeLi, clear=True)  # figure's parameter
    plt.grid(b=True)

    for i in range(len(clusterUnique)):
        plt.scatter(data=coordinateDf[coordinateDf["cluster_labels"] == clusterUnique[i]],
                    x=xlabelStr, y=ylabelStr,
                    label=i + 1,
                    s=pointSize ** 2,
                    c=colorLi[i])

    plt.legend(loc='best')
    plt.title('Plot')
    plt.xlabel(xlabelStr)
    plt.ylabel(ylabelStr)

    if path is None:
        plt.show()
    else:
        plt.savefig('{}.png'.format(path), bbox_inches='tight')
        plt.close()


def _ConvertProtRatioToPcaSpace(protRatioDf):
    """
    2020/02/03
    Called by PlotPca().
    Convert protRatioDf to PCA space.
    Only PC1 and PC2.

    :param protRatioDf: pd.Dataframe()
    :return: 2D coordinate of PCA
    """
    n_components = 2
    pca = PCA(n_components=n_components)
    pca.fit(protRatioDf)
    x_nameStr = 'PC1(' + str(round(pca.explained_variance_ratio_[0] * 100, 1)) + '%)'
    y_nameStr = 'PC2(' + str(round(pca.explained_variance_ratio_[1] * 100, 1)) + '%)'
    columnNamesLi = [x_nameStr, y_nameStr]
    coordinateArr = pca.fit_transform(protRatioDf)
    coordinateDf = pd.DataFrame(coordinateArr, index=protRatioDf.index, columns=columnNamesLi)

    return coordinateDf
