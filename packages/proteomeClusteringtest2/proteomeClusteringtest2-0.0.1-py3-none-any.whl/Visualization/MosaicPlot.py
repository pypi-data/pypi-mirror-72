from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.colors
from pylab import *
import numpy as np
import pandas as pd




def DrawMosaicPlot(rawDataObj, protClustObj, FeatureStr, titleStr='Mosaic Plot', colorLi=None, figSizeLi=[10, 10],
                path=None, dpi=96, legenCol=6, legendLoc=[0.5, -0.1]):
    """
    Draw Mosaic plot to show the number of feature in each cluster

    :param rawDataObj: {ds_InputRawData }
    :param protClustObj: {ds_ProtClust }
    :param FeatureStr: the metadata feature you want to select (String)
    :param titleStr: the title of the plot (String)
    :param colorLi: the string of color set or the marker color, list of Hex color codes, default is 'paired'
    :param figSizeLi: the size of the plot (String)
    :param path: If is null then show the plot. Else store to that path.
    :param dpi: Resolution of the figure. (default = 96)
    :param legenCol: the number of value each column in legend
    :param legendLoc: the location of legend
    :return: figure
    """

    clustNumSer = protClustObj.clustResultObj.sampleClustSer.copy()

    metadataDf = rawDataObj.GetMetadataDf().copy()
    dataDf = pd.DataFrame({'Cluster':clustNumSer,FeatureStr:metadataDf[FeatureStr]})
    dataDf = dataDf.sort_values('Cluster')
    labelDict ={}
    colorDict ={}
    ### produce Dictionary tuple list to delete the content in the map
    for x in sorted(set(clustNumSer)):
        for y in sorted(set(metadataDf[FeatureStr])):
            labelDict.update({(str(x),y):''})


    ## colormap
    if colorLi==None or isinstance(colorLi,str):
        if isinstance(colorLi,str):
            colorSetStr = colorLi
        else:
            colorSetStr = 'Paired'
        colorLi=[]
        cmap = cm.get_cmap(colorSetStr, len(set(metadataDf[FeatureStr])))  # PiYG

        for i in range(cmap.N):
            rgb = cmap(i)[:3]  # will return rgba, we take only first 3 so we get rgb
            colorLi.append(matplotlib.colors.rgb2hex(rgb))


    colorDict = dict(zip(sorted(set(metadataDf[FeatureStr])), colorLi))
    print(colorDict)
    for x in sorted(set(clustNumSer)):
        for y in sorted(set(metadataDf[FeatureStr])):
            colorDict.update({(str(x),y):colorDict[y]})

    fig, axes = plt.subplots(1,1, figsize=(figSizeLi[0], figSizeLi[1]), dpi=dpi)

    #props = lambda key: {'color': '#ff7f0e' if '1' in key else ('gray' if 'luad' in key else 'blue')}
    props = lambda key:{'color':colorDict[key]}
    labelizer = lambda k: labelDict[k]
    a,b = mosaic(dataDf,['Cluster',FeatureStr], title=titleStr, properties=props, labelizer=labelizer, ax=axes, axes_label=True, gap=0.05)
    axes.set_yticklabels([])
    #print(dataDf[FeatureStr])

    leg = axes.legend(_BuildColorList(dataDf[FeatureStr].tolist()),loc='center', bbox_to_anchor=(legendLoc[0], legendLoc[1]),ncol=legenCol)

    #plt.xlabel('Cluster')

    if path is None:
        plt.show()
    else:
        plt.savefig('{}.png'.format(path), bbox_inches='tight')
        plt.close()

    return fig




def _BuildColorList(SearchLi):
    colLi = []
    for i in SearchLi:
        if i in colLi:
            continue
        else:
            colLi.append(i)
    return colLi