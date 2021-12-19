# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 12:48:26 2021

@author: mschwed
"""

homedir = 'D:/Users/mschwede/Dropbox/PAC/'
import os
os.chdir(homedir)
import sys
if 'code/' not in sys.path:
    sys.path.append('code/')
import pandas as pd
from joblib import Parallel, delayed 
import _functions_match as f
import time

    
# Compustat company files
compustatna_file = 'input/compustat/company.csv'
compustatglobal_file = 'input/compustat/g_company.csv'

# Donation files
cmte_file = 'output/raw_imported/cmte.dta'
pac2pac_file = 'output/raw_imported/pac2pac.dta'


#-----------------------------------------------------#
# A) Import name and year from donation and compustat #
#-----------------------------------------------------#
# Ultorgs
cmte = pd.read_stata(cmte_file)
ultorgs = cmte[['ultorg']].drop_duplicates()
ultorgs = list(set(cmte['ultorg'].values))
ultorgs = [(f.clean_name(x), x) for x in ultorgs if x != '']

# Orgs from pac2pac
pac2pac = pd.read_stata(pac2pac_file)
donors = pac2pac[['donorcmte']].drop_duplicates()
donors = list(set(pac2pac['donorcmte'].values))
donors = [(f.clean_name(x), x) for x in donors if x != '']

# Compustat
na = pd.read_csv(compustatna_file, sep='\t', low_memory=False)
g = pd.read_csv(compustatglobal_file, sep='\t', low_memory=False)
compustat = pd.concat([na, g]).drop_duplicates()
assert len(compustat['gvkey'].unique()) == len(compustat)
compustat = list(set([(f.clean_name(row['conm']), row['conm'], row['gvkey'])
    for _, row in compustat.iterrows()]))

# Note: This doesn't take into account possible time dimension of valid names

    
#----------------------#
# B) Run name matching #
#----------------------#
# Ultorgs (takes about 20 min with 24 workers on 24 cores)
print('Working on ultorgs name matching...')
start = time.time()
n = 1500
chunks = [(ultorgs[i:i+n], compustat) for i in range(0, len(ultorgs), n)]
results = Parallel(n_jobs=24, verbose=10)(
    delayed(f.name_match)(x) for x in chunks)
results = [x for y in results for x in y]
matched = pd.DataFrame(
    data=results, columns=['ultorg','fuzz','conm','gvkey']
)
matched.to_stata('output/name_matched/matched_ultorg.dta', write_index=False)
end = time.time()
print('This took', end-start, 'seconds')

# Donors (takes about 10 min with 24 workers on 24 cores)
print('Working on donors name matching...')
start = time.time()
n = 800
chunks = [(donors[i:i+n], compustat) for i in range(0, len(donors), n)]
results = Parallel(n_jobs=24, verbose=10)(
    delayed(f.name_match)(x) for x in chunks)
results = [x for y in results for x in y]
matched = pd.DataFrame(
    data=results, columns=['donor','fuzz','conm','gvkey']
)
matched.to_stata('output/name_matched/matched_donor.dta', write_index=False)
end = time.time()
print('This took', end-start, 'seconds')