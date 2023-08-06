########subplot#################
import numpy as np
import pandas as pd
import matplotlib.colors
import seaborn as sns
import matplotlib.pyplot as plt
from .CommonFunction import *


#    def sort_cluster(self,df,label):
#        df.sort_values(by=label,axis=1,inplace=True)
# labels:cluster numbers
# hls gist_rainbow Set1
def MetaColorMap(rawDataObj, protClustObj, path=None, selectFeatureSer=None, clustColor='Set1', figSizeLi=[10, 5],
                 xlabelSizeStr='large', ylabelSizeStr='small', ylabelDist=50, dpi=96):
    '''
    draw a figure about different feature value in meta data

    :param rawDataObj: ds_inputRawData object
    :param protClustObj: ds_protClust object
    :param path: the directory to save the figure, if none, the figure will only show in the program
    :param clustColor: the color palette used in the figure, default is Set1 in matplotlib
    :param figSizeLi: the width and high of the figure, default is 10 and 5
    :param xlabelSizeStr: x label font size
    :param ylabelSizeStr: y label font size
    :param ylabelDist: y label distance
    :return:
    '''

    metaDataDf=rawDataObj.GetMetadataDf ().copy()
    if selectFeatureSer is None:
        labelSer = rawDataObj.GetMetadataDf ().columns.values
    elif type(selectFeatureSer) is str:

        labelSer = pd.read_csv(selectFeatureSer, header=None, index_col=False)
        labelSer = labelSer.transpose()[0]

    else :
        labelSer=selectFeatureSer

    metaDataDf = metaDataDf[labelSer]
    # sort metadata by cluster

    clustNumSer = protClustObj.clustResultObj.sampleClustSer
    metaDataDf.insert(0,'clusterList', clustNumSer)

    ###sort same cluster together###
    metaDataDf.sort_values (by='clusterList', axis=0, inplace=True)
    countCol = metaDataDf.shape[1]  # how many columns in a row
    lenEachClustLi = GetlenEachClustLi (protClustObj)
    #metaDataDf = metaDataDf.drop (columns=['clusterNumList'])







    fig, axes = plt.subplots (countCol, 1, figsize=(figSizeLi[0], figSizeLi[1]), gridspec_kw={'hspace': 0.01, 'wspace': 0})

    for rowLabel in range (countCol):
        currentColSer = metaDataDf.iloc[:, rowLabel].copy()
        featureValueNum = len (set (currentColSer))
        currentColSer = currentColSer.astype ('str')
        #currentColSer = np.ma.masked_where (currentColSer == 'NA', currentColSer, False)
        # don't know how to name  1: Stage IV,stage III...      2: 6,6,7,7,3,4,1

        labelContentAr, contentOrderAr = np.unique (currentColSer, return_inverse=True)
        currentColSer = __ConvertToStr (labelContentAr, currentColSer)

        currentColSer =np.ma.array(currentColSer,mask=np.isnan(currentColSer))
        # use contentOrderAr draw color bar

        barContentAr = currentColSer.reshape (currentColSer.shape)

        pltColors = sns.color_palette (clustColor, featureValueNum)

        # add dimension of barContentAr. axis=0 means row; axis=1 means column
        barContentAr = np.expand_dims (barContentAr, axis=0)
        # map the color and the content order
        cmap = matplotlib.colors.ListedColormap (pltColors)
        # set mask color
        cmap.set_bad('white')
        norm = matplotlib.colors.BoundaryNorm (np.arange (featureValueNum + 1) - 0.5, featureValueNum)

        # remove xlabel, yticklabels, xticklabels; set ylabel as row label

        axes[rowLabel].set_ylabel (metaDataDf.columns.values[rowLabel], rotation=0, horizontalalignment='center', size=ylabelSizeStr,
                                   labelpad=ylabelDist)

        axes[rowLabel].set_yticks ([])
        axes[rowLabel].set_xticks ([])

        axes[rowLabel].imshow (barContentAr, cmap=cmap, norm=norm, aspect='auto')


        # x-axis,y-axis,width,length
    axes[countCol-1 ].set_xlabel ('Samples', position=(0.98, 0.1, 3, 10), size=xlabelSizeStr)

    if path==None:
        plt.show()
    else :
        fig.savefig (path,bbox_inches="tight", dpi=dpi)


def __ConvertToStr(labelContentAr, currentColSer):
    resultSer = currentColSer.copy ()
    #labelContentAr = labelContentAr[~labelContentAr.mask]
    #print(currentColSer[~currentColSer.mask])
    intNum = 0.0


    for label in labelContentAr:

        for data in range (len (currentColSer)):
            if currentColSer[data] == 'NA':
                resultSer[data] = float ('nan')
            elif label == currentColSer[data]:
                resultSer[data] = float(intNum)

        intNum += 1
    resultSer=resultSer.astype('float')
    return resultSer

def __xtickLen(lenEachClustLi):
    result=[]
    sum=0
    for k in lenEachClustLi:
        sum = sum + k/2
        result.append(sum)
        sum=sum+k/2
    return result


