def GenerateGctFile(rawDataObj, path='GSEAGeneTable.gct'):
    """
    generate the gct file(protein ratio table) used by Gene Set Enrichment Analysis

    :param rawDataObj: ds_InputRawData
    :param path: str, the path to save the gct file
    :return: None
    """

    genetableDf = rawDataObj.GetProtRatioDf().T.copy()
    gct = open(path, 'w')
    gct.writelines('#1.2\n')
    gct.writelines(str(genetableDf.shape[0]) + '\t' + str(genetableDf.shape[1]) + '\n')
    gct.close()

    # insert name and description column labels
    descriptionLi = ['na' for x in range(genetableDf.shape[0])]
    genetableDf.insert(0, 'Description', descriptionLi)
    genetableDf.insert(0, 'Name', genetableDf.index.values)
    genetableDf.to_csv(path, mode='a', sep='\t', index=None)


def GenerateClsFile(protClustObj, path='GSEASampleClust.cls'):
    """
    generate the cls file(subtype of samples) used by Gene Set Enrichment Analysis

    :param protClustObj: ds_ProtClust
    :param path: str, the path to save the cls file
    :return: None
    """
    clustLi = protClustObj.clustResultObj.sampleClustSer.tolist()
    cls = open(path, 'w')

    cls.writelines(str(len(clustLi)) + '\t' + str(len(set(clustLi))) + '\t1\n')

    cls.writelines('#\t')
    for element in set(clustLi):
        cls.write('\t')
        cls.write(str(element))
    cls.write('\n')

    for element in clustLi:
        cls.write(str(element))
        cls.write('\t')

    cls.close()
