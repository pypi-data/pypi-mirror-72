#!/usr/bin/env python3

import pandas as pd
import numpy as np
# from scipy import stats
import math
from shizen_gengo.explore import explore_utils
from shizen_gengo.preprocess_text import text_utils
from shizen_gengo.preprocess_dataframe import dataframe_utils

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv("../local-data/raw/bat_sample2_original_headers.csv",
                  keep_default_na=True,
                  dtype=str,
                  encoding = "ISO-8859-1")
# replace an empty string and records with only spaces
# df = df.replace(r'^\s*$', np.nan, regex=True)
print(df.shape)

df['Customer Display Name'].reset_index().sample(5)
test = explore_utils.search(df, 'Customer Display Name', 'Ã¤').head() #sÃº
print(test[['Incident ID', 'Customer Display Name']])

tmp = df.copy()
tmp['name_cleaned'] = text_utils.remove_accented_chars(tmp['Customer Display Name'])
print(tmp[tmp['Incident ID']=='CH3270146']['name_cleaned'])
del tmp

#####
tmp = df.copy()
tmp['Customer Display Name'] = text_utils.remove_digits(tmp['Customer Display Name'])
print(tmp[tmp['Incident ID']=='CH4037102']['Customer Display Name'])

tmp['Customer Display Name'] = text_utils.remove_consecutive_spaces(tmp['Customer Display Name'])
print(tmp[tmp['Incident ID']=='CH4037102']['Customer Display Name'])
del tmp

######
tmp = df.copy()
tmp['Customer Display Name'] = text_utils.remove_repeating_letters(tmp['Customer Display Name'])
print(tmp[tmp['Incident ID'].isin(['CH3335178', 'CH4685020'])]['Customer Display Name'])
del tmp

####
tmp = df.copy()
print(type(tmp.columns))
tmp.columns = dataframe_utils.standardise_column_headers(tmp.columns)
print(type(tmp.columns))
print(tmp.columns)
del tmp
