import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3





def DrawNetworkOverlapGeneVenn(node1Csv, node2Csv, subtype, degreeCutOff=10):
    """
    draw venn diagram about the number of two subtypes' overlap genes

    :param node1Csv: str, cluster gene node csv path
    :param node2Csv: str, cluster gene node csv path
    :param subtype: number of clusters
    :param degreeCutOff: number of degree

    :return: None

    """
    node1Df = pd.read_csv (node1Csv, index_col=0)
    node2Df = pd.read_csv (node2Csv, index_col=0)
    count=0
    filterNode1Df=node1Df[node1Df.Degree>=degreeCutOff]
    filterNode2Df=node2Df[node2Df.Degree>=degreeCutOff]

    for name1 in filterNode1Df['Label']:
        for name2 in filterNode2Df['Label']:
            #if name1==name2 and name1!='Id':
            if name1 == name2 :
                count+=1
    fig, ax = plt.subplots (nrows=1, ncols=1)
    venn2 (subsets=(filterNode1Df.shape[0]-count,filterNode2Df.shape[0]-count,count ), set_labels=('ConKM', 'HC'),ax=ax)
    fig.savefig("vennfig_subtype"+str(subtype)+"_"+str(degreeCutOff),bbox_inches='tight')
    plt.close (fig)

    print("subtype"+str(subtype)+": ",filterNode1Df.shape[0],filterNode2Df.shape[0],count)




def DrawGoTermOverlapVenn(node1Csv, node2Csv, path, node1Name='ConKM', node2Name='HC',dpi=300):

    overlapLi=[]
    goTerm1Df = pd.read_csv(node1Csv, delimiter="\t")
    goTerm2Df = pd.read_csv(node2Csv, delimiter="\t")
    count = 0
    num = 0
    for goNameStr in goTerm1Df['geneSet']:
        num += 1

        for goName2Str in goTerm2Df['geneSet']:
            if goNameStr == goName2Str:
                count += 1
                overlapLi.append(goName2Str)



    # set font size
    font = {'family': 'sans',
            'weight': 'bold',
            'size': 22}
    matplotlib.rc('font', **font)
    fig, ax = plt.subplots(nrows=1, ncols=1,dpi=dpi)


    venn2(subsets=(len(goTerm1Df['geneSet']) - count, len(goTerm2Df['geneSet']) - count, count),
          set_labels=(node1Name, node2Name), ax=ax)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print(overlapLi)
    return overlapLi




def DrawOverlapOverlapVenn3(list1, list2, list3, path,node1='1', node2='3',node3='5',dpi=300):
    count1_2_3=0
    count1_2 = _CountTwoOverlap(list1,list2)
    count2_3 = _CountTwoOverlap(list2,list3)
    count1_3 = _CountTwoOverlap(list1,list3)
    overlapLi=[]
    for goNameStr in list1:


        for goName2Str in list2:
            for goName3Str in list3:

                if goNameStr == goName2Str == goName3Str:
                    count1_2_3 += 1
                    overlapLi.append(goName2Str)


    font = {'family': 'sans',
            'weight': 'bold',
            'size': 22}
    matplotlib.rc('font', **font)
    fig, ax = plt.subplots(nrows=1, ncols=1, dpi=dpi)

    venn3(subsets=(len(list1) - count1_2-count1_3 + count1_2_3, len(list2) - count2_3 - count1_2 + count1_2_3, count1_2-count1_2_3,
                   len(list3) - count2_3 - count1_3 + count1_2_3, count1_3-count1_2_3, count2_3-count1_2_3, count1_2_3),
          set_labels=(str(node1), str(node2), str(node3)), ax=ax)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)


def _CountTwoOverlap(list1, list2):
    count=0
    for name1 in list1:

        for name2 in list2:
            if name1==name2:
                count+=1

    return count