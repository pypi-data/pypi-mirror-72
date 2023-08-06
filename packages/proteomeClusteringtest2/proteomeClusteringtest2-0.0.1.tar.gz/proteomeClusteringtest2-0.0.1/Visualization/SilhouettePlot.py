import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def DrawSilhouettePlot(rawDataObj, protClustObj, path=None):
    clusterResult = protClustObj.clustResultObj.sampleClustSer

    silhScore = protClustObj.clustScoringObj.silhScore
    sampleSilhScore = protClustObj.clustScoringObj.sampleSilhScoreSer

    clusterNum = np.max(clusterResult) + 1
    fig, ax1 = plt.subplots()
    ax1.set_xlim([np.min(sampleSilhScore.values) - 0.05, np.max(sampleSilhScore.values) + 0.05])
    ax1.set_ylim([0, len(clusterResult) + (clusterNum + 1) * 10])

    y_lower = 10
    for i in range(1, clusterNum):
        clusterSilhouetteScoreArr = sampleSilhScore[clusterResult == i].values
        clusterSilhouetteScoreArr.sort()
        clusterSize = clusterSilhouetteScoreArr.shape[0]
        y_upper = y_lower + clusterSize
        color = cm.nipy_spectral(float(i) / clusterNum)

        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, clusterSilhouetteScoreArr,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * clusterSize, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples
    ax1.set_title("The Silhouette plot for the various clusters.")
    ax1.set_xlabel("Silhouette Score")
    ax1.set_ylabel("Cluster Label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhScore, color="red", linestyle="--")
    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks(np.arange(0, np.max(sampleSilhScore.values) + 0.05, 0.1))
    if path is None:
        plt.show()
    else:
        plt.savefig(path)
