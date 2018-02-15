#################################################################
#################################################################
############### Clustergrammer 
#################################################################
#################################################################

#############################################
########## 1. Load libraries
#############################################
##### 1. General support #####
import requests
import os
import numpy as np
from IPython.display import display, IFrame
import tempfile
import scipy.stats as ss
import pandas as pd

##### 2. Other libraries #####

#######################################################
#######################################################
########## S1. Function
#######################################################
#######################################################

#############################################
########## 1. Run
#############################################

def run(dataset, normalization='rawdata', normalize_cols=False, log=False, z_score=False, nr_genes=1500):

	# Get tempfile
	(fd, filename) = tempfile.mkstemp()
	filename = filename+'.txt'
	try:
		# Get data
		data = dataset[normalization]

		# Normalize columns
		if normalize_cols:
			data = data/data.sum()

		# Log-transform
		if log:
			data = np.log10(data+1)

		# Get variable subset
		data = data.loc[data.var(axis=1).sort_values(ascending=False).index[:nr_genes]]

		# Z-score
		if z_score:
			data = data.apply(ss.zscore, axis=1)

		# Add metadata
		data.index = ['Gene: '+x for x in data.index]
		data.columns=pd.MultiIndex.from_tuples([tuple(['{key}: {value}'.format(**locals()) for key, value in rowData.items()]) for index, rowData in dataset['sample_metadata'].iterrows()])

		# Write file and get link
		data.to_csv(filename, sep='\t')
		clustergrammer_url = requests.post('http://amp.pharm.mssm.edu/clustergrammer/matrix_upload/', files={'file': open(filename, 'rb')}).text
	finally:
		os.remove(filename)
	return clustergrammer_url

#############################################
########## 2. Plot
#############################################

def plot(clustergrammer_url):
	return display(IFrame(clustergrammer_url, width="1000", height="1000"))
