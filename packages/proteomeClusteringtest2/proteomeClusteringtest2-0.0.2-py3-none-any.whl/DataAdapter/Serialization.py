import pickle

def DumpRawDataObj(rawDataObj,file):
	"""
	Dumping the rawDataObj into .pickle file

	:param rawDataObj: ds_InputRawData
	:type rawDataObj: object
	:returns: file
	"""
	with open(file, 'wb') as f:
		pickle.dump(rawDataObj, f, pickle.HIGHEST_PROTOCOL)
		print('.....Successfully dump raw data object at {}\n'.format(file))

def DumpProtClustObj(protClustObj,file):
	"""
	Dumping the protClustObj into .pickle file

	:param protClustObj: ds_InputRawData
	:type protClustObj: object
	:returns: file
	"""
	with open(file, 'wb') as f:
		pickle.dump(protClustObj, f, pickle.HIGHEST_PROTOCOL)
		print('.....Successfully dump protein cluster object at {}\n'.format(file))

def LoadRawDataObj(file):
	"""
	Loading a .pickle file to fast create a rawDataObj

	:param file:
	:type file: .pickle
	:returns: rawDataObj
	"""
	with open(file, 'rb') as f:
		rawDataObj = pickle.load(f)
		print('.....Successfully read raw data object from {}\n'.format(file))
	return rawDataObj

def LoadProtClustObj(file):
	"""
	Loading a .pickle file to fast create a protClustObj

	:param file:
	:type file: .pickle
	:returns: protClustObj
	"""
	with open(file, 'rb') as f:
		protClustObj = pickle.load(f)
		print('.....Successfully read protein cluster object from {}\n'.format(file))
	return protClustObj