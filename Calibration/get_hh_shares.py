'''Download the 2014 WIOT from the WIOD Website'''

import pandas as pd 

# Download the 2014 WIOT from the WIOD website
wiod_2014 = pd.read_excel('http://www.wiod.org/protected3/data16/wiot_ROW/WIOT2014_Nov16_ROW.xlsb',header=2,engine='pyxlsb')
print('WIOT for 2014 Successfully downloaded!')

''' There are some special requirements here. 
    First, the excel file is actually a binary
    excel file. Pandas can read binary excel files,
    but you need to download the pyxlsb package. 
    
    To download use,
    
    pip3 install pyxlsb
    
    You may also need to upgrade pandas,
    
    pip3 install pandas --upgrade
    
    '''

'''
--------------------------
Get the relevant data
--------------------------
'''

pd.options.mode.chained_assignment = None 

# Extract the columns with the Chinese data
chn_cols = wiod_2014.columns[(wiod_2014=='CHN').any(axis=0)]

# Extract the columns with the US data
us_cols = wiod_2014.columns[(wiod_2014=='USA').any(axis=0)]

# Extract all others columns 
row_cols=[]
for col_name in wiod_2014.columns:
    if col_name in list(chn_cols)[1:] or col_name in list(us_cols)[1:]:
        pass
    else:
        row_cols.append(col_name)
    
# Rename the first 4 columns
wiod_2014.rename(columns={wiod_2014.columns[0]: 'Industry Code'}, inplace = True)
wiod_2014.rename(columns={wiod_2014.columns[1]: 'Industry Description'}, inplace = True)
wiod_2014.rename(columns={wiod_2014.columns[2]: 'Country'}, inplace = True)
wiod_2014.rename(columns={wiod_2014.columns[3]: 'Industry WIOD Code'}, inplace = True)
        
# Extract the data for each country
chn_cols_list = list(chn_cols)[1:]
chn_cols_list.extend(['Industry Code','Country'])
wiod_chn2014 = wiod_2014[chn_cols_list]
wiod_chn2014 = wiod_chn2014[wiod_chn2014['Country'] != 'TOT'].drop([0,1,2])

us_cols_list = list(us_cols)[1:]
us_cols_list.extend(['Industry Code','Country'])
wiod_usa2014 = wiod_2014[us_cols_list]
wiod_usa2014 = wiod_usa2014[wiod_usa2014['Country'] != 'TOT'].drop([0,1,2])

row_cols_list = list(row_cols)[4:-1]
row_cols_list.extend(['Industry Code','Country'])
wiod_row2014 = wiod_2014[row_cols_list]
wiod_row2014 = wiod_row2014[wiod_row2014['Country'] != 'TOT'].drop([0,1,2])


# Create a function to extract the appropriate columns (CONS_h)
def get_CONSH(col_list):
    return [col for col in col_list if 'CONS_h' in col]

# Get HH spending for the different countries
chn_HH = get_CONSH(wiod_chn2014.columns)
chn_HH.extend(['Industry Code','Country'])
usa_HH = get_CONSH(wiod_usa2014.columns)
usa_HH.extend(['Industry Code','Country'])
row_HH = get_CONSH(wiod_row2014.columns)
row_HH.extend(['Industry Code','Country'])
    
# Extract HH spending from each dataset
chn_HH2014 = wiod_chn2014[chn_HH]
usa_HH2014 = wiod_usa2014[usa_HH]
row_HH2014 = wiod_row2014[row_HH]

# Compute total HOUSEHOLD spending in ROW
row_HH2014['CONS_h.ROW'] = row_HH2014[get_CONSH(wiod_row2014)].sum(axis=1)
row_HH2014 = row_HH2014[['Industry Code','Country','CONS_h.ROW']]

# Compute total HOUSEHOLD spending in CHN
chn_HH2014.columns = ['CONS_h.CHN','Industry Code','Country']

# Compute total HOUSEHOLD spending in USA
usa_HH2014.columns = ['CONS_h.USA','Industry Code','Country']

# Create a function that maps countries into ROW or not
def row_map(x):
    if x == 'USA' or x=='CHN':
        return x
    else:
        return 'ROW'
    
# Collapse the data into spending by region-sector (Regions = CHN,USA,ROW)
chn_HH2014['Source Region'] = chn_HH2014['Country'].apply(lambda x: row_map(x))
chn_HH2014 = chn_HH2014[['Source Region','Industry Code','CONS_h.CHN']].groupby(['Source Region','Industry Code']).sum().reset_index()

usa_HH2014['Source Region'] = usa_HH2014['Country'].apply(lambda x: row_map(x))
usa_HH2014 = usa_HH2014[['Source Region','Industry Code','CONS_h.USA']].groupby(['Source Region','Industry Code']).sum().reset_index()

row_HH2014['Source Region'] = row_HH2014['Country'].apply(lambda x: row_map(x))
row_HH2014 = row_HH2014[['Source Region','Industry Code','CONS_h.ROW']].groupby(['Source Region','Industry Code']).sum().reset_index()


# Merge the datasets together
wiod_HH2014 = pd.merge(chn_HH2014,row_HH2014 ,on=['Source Region','Industry Code'],how='inner')
wiod_HH2014 = pd.merge(wiod_HH2014,usa_HH2014,on=['Source Region','Industry Code'],how='inner')

'''
----------------------------------------------------
Compute the expenditure share matrix
----------------------------------------------------
'''

import numpy as np
from numpy.linalg import inv

# Extract the final expenditure columns as a matrix
F = wiod_HH2014.iloc[:,2:].values

# Create a vector of ones of the same dimension
i = np.ones((1,F.shape[0]))

# Compute total HH expenditures in each region
F_total = np.dot(i,F)

# Diagonalize and invert the matrix
Pi_f = np.transpose(np.dot(F,inv(np.diag(F_total[0]))))

print('Successfully computed the expenditure share matrix!')