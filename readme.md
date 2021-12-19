This repository contains Python code that transforms bulk PAC data from the [Center for Responsive politics](https://www.opensecrets.org) into GVKey-quarter level data ready to be used in further analyses.

In the last step I use a Stata do file for convenience, but this could of course be done in Python too.

The structure of the code is as follows:
 - `code/1_prepare_data.py` (a) imports all firm names and GVKeys from WRDS Compustat and (b) imports and cleans the raw PAC data from the CRP.
 - `code/2_match_companynames.py` matches the company names of the two data sets. I use [FuzzyWuzzy](https://pypi.org/project/fuzzywuzzy/) to string match the company names.
 - `code/3_create_final_dataset.do` merges the files into a final data set.

To run this code, you will need to first obtain the following input files:
 - the `company` and `g_company` file from WRDS
 - the `CampaignFinXX.zip` files from the CRP.
I provided a bit more information about these input files in the readme files of the respective input folders.

Contents of requirements.txt
`fuzzywuzzy==0.17.0
`joblib==0.14.0`
`pandas==1.1.5`

Use at your own responsibility.