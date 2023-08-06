"""
Contain CheckFileExistence(), CheckPatientNum()
"""


def CheckFileExistence(protRatioDf, metadataDf):
    """
    Check **protRatioDf** and **metadataDf** are not empty.

    :param protRatioDf: 
    :type protRatioDf: pd.DataFrame
    :param metadataDf: 
    :type metadataDf: pd.DataFrame
    :return: Return `True` if **protRatioDf** and **metadataDf** are not empty
    :rtype: bool
    """
    if protRatioDf.empty or metadataDf.empty:
        print('Protein ratio and metadata cannot be empty.')
        return False
    else:
        return True


def CheckPatientNum(protRatioDf, metadataDf):
    """
    Check number of patients is equal in **protRatioDf** and **metadataDf**.

    :param protRatioDf: 
    :type protRatioDf: pd.DataFrame
    :param metadataDf: 
    :type metadataDf: pd.DataFrame
    :return: Return `True` if number of patients is equal in **protRatioDf** and **metadataDf**
    :rtype: bool
    """
    if protRatioDf.shape[0] != metadataDf.shape[0]:
        print('Number of patients is not equal in protRatioDf and metadataDf.')
        return False
    else:
        return True
