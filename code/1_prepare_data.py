# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 09:30:16 2021

@author: mschwed
"""

homedir = 'D:/Users/mschwede/Dropbox/PAC/'


import os
os.chdir(homedir)
import sys
if not 'code/' in sys.path:
    sys.path.append('code/')
import pandas as pd
import zipfile
from collections import defaultdict


# Input folder
donation_files = 'input/campaign_finance/'

# Output folder
output_folder = 'output/'


#-----------------------#
# A) Read from ZIP file #
#-----------------------#
# Years
years = ['00','02','04','06','08','10','12','14','16','18']

# Read from zip file
alldata = defaultdict(list)
for year in years:
    
    print('Reading files for year', year)
    
    # Which file
    file = donation_files + 'CampaignFin' + year + '.zip'
    
    # Read pac-to-can
    print('\t pacs...')
    cols = ['cycle','fecrecno','pacid','cid','amount','date','realcode',
            'type','di','feccandid']
    with zipfile.ZipFile(file,'r').open('pacs' + year + '.txt') as infile:
        pac2can = pd.read_csv(infile, sep=',', quotechar='|', names=cols,
                              low_memory=False)
    alldata['pac2can'].append(pac2can)
    
    # Read pac-to-pac
    print('\t pac_other...')
    cols = ['cycle','fecrecno','filerid','donorcmte','contriblendtrans',
            'city','state','zip','fecoccemp','primecode','date','amount',
            'recipid','party','otherid','recipcode','recipprimcode',
            'amend','report','pg','microfilm','type','realcode','source']
    with zipfile.ZipFile(file,'r').open('pac_other' + year + '.txt') as infile:
        pac2pac = pd.read_csv(infile, sep=',', quotechar='|', names=cols,
                              low_memory=False)
    alldata['pac2pac'].append(pac2pac)
    
    # Read candidate info
    print('\t cands...')
    cols = ['cycle','feccandid','cid','firstlastp','party','distidrunfor',
            'distidcurr','currcand','cyclecand','crpico','recipcode','nopacs']
    with zipfile.ZipFile(file,'r').open('cands' + year + '.txt') as infile:
        can = pd.read_csv(infile, sep=',', quotechar='|', names=cols,
                          low_memory=False)
    alldata['can'].append(can)
    
    # Read committee info
    print('\t committees...')
    cols = ['cycle','cmteid','pacshort','affiliate','ultorg','recipid',
            'recipcode','feccandid','party','primcode','source','sensitive',
            'foreign','active']
    with zipfile.ZipFile(file,'r').open('cmtes' + year + '.txt') as infile:
        cmte = pd.read_csv(infile, sep=',', quotechar='|', names=cols,
                           low_memory=False, encoding='cp1252')
    alldata['cmte'].append(cmte)
        
# Collect
pac2can = pd.concat(alldata['pac2can'])
pac2pac = pd.concat(alldata['pac2pac'])
cands = pd.concat(alldata['can'])
cmtes = pd.concat(alldata['cmte'])


#-----------------------------------#
# B) Keep relevant columns and rows #
#-----------------------------------#
### 1) Pac2can
# Drop realcode Z9 or Z4
# See: https://groups.google.com/forum/#!searchin/opensecrets-open-data/
# pac$20type|sort:relevance/opensecrets-open-data/VY2uXMaJlPg/apUYaY_opU8J
pac2can = pac2can[~pac2can['realcode'].str[:2].isin({'Z9','Z4','z9','z4'})]

# Take sum
pac2can = pac2can[pac2can['cid'].notna()]
summed = pac2can.groupby(['cycle','pacid','cid','date']).sum()['amount']
"""
There could be cases of the same cycle, committee, candidate, date, amount but
with different fec_record_id. We don't want to lose them.

A given committee can give to multiple candidates, and a given candidate can
receive from multiple committees.
"""
# Save to stata
summed.to_frame().to_stata(output_folder + 'pac2can.dta')

### 2) Pac2pac
# Drop realcode Z9 or Z4
# See: https://groups.google.com/forum/#!searchin/opensecrets-open-data/
# pac$20type|sort:relevance/opensecrets-open-data/VY2uXMaJlPg/apUYaY_opU8J
pac2pac = pac2pac[~pac2pac['realcode'].str[:2].isin({'Z9','Z4','z9','z4'})]

#Keep only those donations filed by donor (as in SAS file that created old data)
pac2pac = pac2pac[(pac2pac['filerid'].notna()) & (pac2pac['recipid'].notna())]
pac2pac = pac2pac[pac2pac['filerid'] != pac2pac['recipid']]
"""
Here is what I believe to be true:
- fec_filer_id and fec_cmte_id are the donor and recipient IDs, but it's
not clear which one is which
- crp_recip_id is the recipient ID: if candidate, then CID, if committee,
then fec_cmte_id
"""
# Take sum
summed = pac2pac.groupby(
    ['cycle','filerid','donorcmte','date','recipid','party']
).sum()['amount']
    
# Save
summed.to_frame().to_stata(output_folder + 'pac2pac.dta')

### 3) Candidate info
cands = cands.drop_duplicates(subset=['cycle','cid'])
cands = cands[['cycle','cid','firstlastp','party','distidrunfor']]
cands.to_stata(output_folder + 'can.dta', write_index=False)

### 4) Committee info
cmtes = cmtes[['cycle','cmteid','recipid','feccandid','ultorg']]
assert cmtes.duplicated(['cycle','cmteid']).astype(int).sum() == 0
cmtes.to_stata(output_folder + 'cmte.dta', write_index=False)