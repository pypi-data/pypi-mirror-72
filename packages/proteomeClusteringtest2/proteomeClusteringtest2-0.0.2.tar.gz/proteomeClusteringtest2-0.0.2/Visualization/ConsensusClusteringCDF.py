import matplotlib.pyplot as plt

def DrawConsensusClustCDF(protClustObj,path=None):
	cdfLi = protClustObj.clustResultObj.cdfLi
	# print(cdfLi)
	fig , ax = plt.subplots()
	x = [i/100 for i in range(1,101)]
	for key in cdfLi:
		plt.plot(x,cdfLi[key],label= key)
	plt.xlabel("Consensus Index")
	plt.ylabel("CDF")
	plt.title("Consensus CDF")
	plt.legend()
	# plt.show()
	# plt.savefig("cdf.png")
	if path is None:
		plt.show()
	else:
		plt.savefig('{}.png'.format(path), bbox_inches='tight')
		plt.close()