from .Vscore import CalcFeatureVscore
from .Fscore import CalcFeatureMaxFscore
from .ARIscore import CalcFeatureAriScore
from .AMIscore import CalcFeatureAmiScore
from .PairedFscore import CalcFeaturePairedFscore
from .SilhouetteScore import CalcSilhScore, CalcSampleSilhScore, CalcClustSilhScore
from .PartitionIndex import CalcPartitionIndex
from .SeparationIndex import CalcSeparationIndex
from .GiniScore import CalcGiniScore
from .PurityScore import CalcPurityScore
from .FeatureRatio import CalcFeatureRatio
from .FeatureEntropy import CalcClustFeatureEntropy, CalcFeatureEntropy
from .BICscore import CalcBicScore


def CalcEveryScore(rawDataObj, protClustObj):
    '''
    Calculates all available scores and store them in protClustObj

    :param rawDataObj:
    :param protClustObj:
    :return:
    '''
    scoreOptionsLi = [CalcFeatureVscore, CalcFeatureMaxFscore, CalcFeatureAriScore, CalcFeatureAmiScore,
                      CalcFeaturePairedFscore, CalcSilhScore, CalcSampleSilhScore, CalcClustSilhScore,
                      CalcPartitionIndex,
                      CalcSeparationIndex, CalcGiniScore, CalcPurityScore, CalcFeatureRatio, CalcClustFeatureEntropy,
                      CalcFeatureEntropy,
                      CalcBicScore]

    for scoreOption in scoreOptionsLi:
        protClustObj = scoreOption(rawDataObj, protClustObj)

    return protClustObj
