# Data handling
import pandas as pd
import numpy as np

# Visualization
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def PlotTsne(rawDataObj, protClustObj, perplexity=30, dpi=96, figSizeLi=[6.4, 4.8], pointSize=6, colorLi=None, path=None):
    """
    2020/02/03
    Plot TSNE in 2D
    拿rawDataObj.__protRatioDf轉成Tsne空間(只取前二維)畫成散佈點圖。
    拿protClustObj.clustResultObj.sampleClustSer來著色。

    :param rawDataObj: ds_InputRawData
    :param protClustObj: ds_ProtClust
    :param perplexity:
    :param dpi: Resolution of the figure. (default = 96)
    :param figSizeLi: Figure's width, height in inches. (default = [6.4, 4.8])
    :param pointSize: The marker size in points**2. (default = 6)
    :param colorLi: The marker color. List of Hex color codes. (default = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
    :param path: If is null then show the plot. Else store to that path.
    :return:
    """
    protRatioDf = rawDataObj.GetProtRatioDf()
    clusterArr = np.array(protClustObj.clustResultObj.sampleClustSer)
    coordinateDf = _ConvertProtRatioToTsneSpace(protRatioDf, perplexity)

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


def _ConvertProtRatioToTsneSpace(protRatioDf, perplexity):
    """
    2020/02/03
    Called by PlotTsne()

    :param protRatioDf: pd.Dataframe()
    :return: 2D coordinate of TSNE
    """
    n_components = 2
    names = ['tsne1', 'tsne2']
    matrix = TSNE(n_components=n_components, perplexity=perplexity).fit_transform(protRatioDf)
    coordinateDf = pd.DataFrame(matrix)
    coordinateDf.rename({i: names[i] for i in range(n_components)}, axis=1, inplace=True)
    coordinateDf.index = protRatioDf.index

    return coordinateDf
