# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 12:49:33 2021

@author: mschwed
"""


import re
from fuzzywuzzy import fuzz



def clean_companynames(company_name_stripped):

    # Strip company name from essentials
    company_name_stripped = re.sub('[^a-zA-Z0-9 ]+','',
        company_name_stripped.lower()) # strip of every non-alphabet character
    company_name_stripped = re.sub('\s\s+',' ',
        company_name_stripped) # remove double spaces
    
    #########################
    ## 1) REPLACE shortcuts #
    #########################
    # Replace "amer" with "america"
    if 'amer' in company_name_stripped:
        company_name_stripped = re.sub(' amer |^amer | amer$',' america ',
            company_name_stripped)
    
    # Replace "assn" with "association"
    if 'assn' in company_name_stripped:
        company_name_stripped = re.sub(' assn |^assn | assn$',' association ',
            company_name_stripped)
    
    # Replace "ctrs" with "centers"
    if 'ctrs' in company_name_stripped:
        company_name_stripped = re.sub(' ctrs |^ctrs | ctrs$',' ',
            company_name_stripped)
        
    # Replace "svcs" and svc"
    if 'svcs' in company_name_stripped:
        company_name_stripped = re.sub(' svcs |^svcs | svcs$',' services ',
            company_name_stripped)
    if 'svc' in company_name_stripped:
        company_name_stripped = re.sub(' svc |^svc | svc$',' service ',
            company_name_stripped)
    
    
    ########################
    ## 2) REMOVE stopwords #
    ########################
    # Remove "and"
    if 'and' in company_name_stripped:
        company_name_stripped = re.sub(' and |^and | and$',' ',
            company_name_stripped)
    
    # Remove "corporation" and "corp" and "co" and "cp"
    if 'corporation' in company_name_stripped:
        company_name_stripped = re.sub(
            ' corporation |^corporation | corporation$',' ',
            company_name_stripped)
    if 'corp' in company_name_stripped:
        company_name_stripped = re.sub(' corp |^corp | corp$',' ',
            company_name_stripped)
    if 'company' in company_name_stripped:
        company_name_stripped = re.sub(' company |^company | company$',' ',
            company_name_stripped)
    if 'co' in company_name_stripped:
        company_name_stripped = re.sub(' co |^co | co$',' ',
            company_name_stripped)
    if 'cp' in company_name_stripped:
        company_name_stripped = re.sub(' cp |^cp | cp$',' ',
            company_name_stripped)
    
    # Remove "development" and "dev"
    if 'development' in company_name_stripped:
        company_name_stripped = re.sub(
            ' development |^development | development$',' ',
            company_name_stripped)
    if 'dev' in company_name_stripped:
        company_name_stripped = re.sub(' dev |^dev | dev$',' ',
            company_name_stripped)
    
    # Remove "group"
    if 'group' in company_name_stripped:
        company_name_stripped = re.sub(' group |^group | group$',' ',
            company_name_stripped)
    
    # Remove "holdings" and "holding" and "hldg" and "hldgs"
    if 'holdings' in company_name_stripped:
        company_name_stripped = re.sub(' holdings |^holdings | holdings$',' ',
            company_name_stripped)
    if 'holding' in company_name_stripped:
        company_name_stripped = re.sub(' holding |^holding | holding$',' ',
            company_name_stripped)
    if 'hldg' in company_name_stripped:
        company_name_stripped = re.sub(' hldg |^hldg | hldg$',' ',
            company_name_stripped)
    if 'hldgs' in company_name_stripped:
        company_name_stripped = re.sub(' hldgs |^hldgs | hldgs$',' ',
            company_name_stripped)
    
    # Remove "incorporated" and "inc"
    if 'incorporated' in company_name_stripped:
        company_name_stripped = re.sub(
            ' incorporated |^incorporated | incorporated$',' ',
            company_name_stripped)
    if 'inc' in company_name_stripped:
        company_name_stripped = re.sub(' inc |^inc | inc$',' ',
            company_name_stripped)
    
    # Remove "investment" and "invt"
    if 'investment' in company_name_stripped:
        company_name_stripped = re.sub(
            ' investment |^investment | investment$',' ',company_name_stripped)
    if 'invt' in company_name_stripped:
        company_name_stripped = re.sub(' invt |^invt | invt$',' ',
            company_name_stripped)
    
    # Remove "limited" and "ltd"
    if 'limited' in company_name_stripped:
        company_name_stripped = re.sub(' limited |^limited | limited$',' ',
            company_name_stripped)
    if 'ltd' in company_name_stripped:
        company_name_stripped = re.sub(' ltd |^ltd | ltd$',' ',
            company_name_stripped)
    
    # Remove "llc"
    if 'llc' in company_name_stripped:
        company_name_stripped = re.sub(' llc |^llc | llc$',' ',
            company_name_stripped)
    
    # Remove "old" and "new"
    if 'old' in company_name_stripped:
        company_name_stripped = re.sub(' old |^old | old$',' ',
            company_name_stripped)
    if 'new' in company_name_stripped:
        company_name_stripped = re.sub(' new |^new | new$',' ',
            company_name_stripped)
    
    # Remove "plc"
    if 'plc' in company_name_stripped:
        company_name_stripped = re.sub(' plc |^plc | plc$',' ',
            company_name_stripped)
        
    # Remove "the"
    if 'the' in company_name_stripped:
        company_name_stripped = re.sub(' the |^the | the$',' ',
            company_name_stripped)
    
    # Remove "trust" and "tr"
    if 'trust' in company_name_stripped:
        company_name_stripped = re.sub(' trust |^trust | trust$',' ',
            company_name_stripped)
    if 'tr' in company_name_stripped:
        company_name_stripped = re.sub(' tr |^tr | tr$',' ',
            company_name_stripped)
    
    if 'sa' in company_name_stripped:
        company_name_stripped = re.sub(' sa |^sa | sa$',' ',
            company_name_stripped)
        
    if 'pac' in company_name_stripped:
        company_name_stripped = re.sub(' pac |^pac | pac$',' ',
            company_name_stripped)
    
    # Remove trailing or leading blanks
    company_name_stripped = re.sub('^\s+','',company_name_stripped)
    company_name_stripped = re.sub('\s+$','',company_name_stripped)
    
    return company_name_stripped


def clean_name(string):
    # strip of every non-alphabet character
    clean = re.sub('[^a-zA-Z0-9 ]+','', string.lower())
    # customized stuff
    clean = clean_companynames(clean)
    return clean


def name_match(inputs):
    chunk, compustat = inputs
    matched = []
    for name_tup in chunk:
        matches = [(name_tup[1], fuzz.ratio(name_tup[0], x[0]), x[1], x[2])
            for x in compustat]
        matches = list(sorted(matches, key=lambda x: (-x[1], x[0])))
        matched.append(matches[0])
    return matched