'''Download the 2014 WIOT from the WIOD Website'''

import pandas as pd 
import numpy as np
from numpy.linalg import inv

def calibrate():
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

    
    # Extract the final expenditure columns as a matrix
    F = wiod_HH2014.iloc[:,2:].values

    # Create a vector of ones of the same dimension
    i = np.ones((1,F.shape[0]))

    # Compute total HH expenditures in each region
    F_total = np.dot(i,F)

    # Diagonalize and invert the matrix
    Pi_f = np.transpose(np.dot(F,inv(np.diag(F_total[0]))))

    print('Successfully computed the expenditure share matrix!')


    '''
    ----------------------------------------------------
    Extract the intermediate transaction matrix for each region
    ----------------------------------------------------
    '''
    # Create a list of variable names that are not intermediate spending
    final_use_vars = ['CONS_h','CONS_np','CONS_g','GFCF','INVEN']

    # Extract the columns with the Chinese data
    chn_cols = wiod_2014.columns[(wiod_2014=='CHN').any(axis=0)]
    usa_cols = wiod_2014.columns[(wiod_2014=='USA').any(axis=0)]

    # Create a function to remove non-intermediate columns from the data
    def int_cols(col_list):
        int_col_list = []
        for col in list(col_list)[1:]:
            i=0
            for use in final_use_vars:
                if use in col:
                    i+=1
            if i==0:
                int_col_list.append(col)
        return int_col_list
        

    # Remove non-intermediate spending columns
    chn_int_cols = int_cols(chn_cols)
    usa_int_cols = int_cols(us_cols)
    row_int_cols = int_cols(row_cols)[3:-1]

    # Extract the intermediate spending data from the WIOT
    chn_int_cols.extend(['Industry Code','Country'])
    wiod_int_chn2014 = wiod_2014[chn_int_cols]
    wiod_int_chn2014 = wiod_int_chn2014[wiod_int_chn2014['Country'] != 'TOT'].drop([0,1,2])

    usa_int_cols.extend(['Industry Code','Country'])
    wiod_int_usa2014 = wiod_2014[usa_int_cols]
    wiod_int_usa2014 = wiod_int_usa2014[wiod_int_usa2014['Country'] != 'TOT'].drop([0,1,2])

    row_int_cols.extend(['Industry Code','Country'])
    wiod_int_row2014 = wiod_2014[row_int_cols]
    wiod_int_row2014 = wiod_int_row2014[wiod_int_row2014['Country'] != 'TOT'].drop([0,1,2])

    # Collapse the data into spending by region
    wiod_int_chn2014['Source Region'] = wiod_int_chn2014['Country'].apply(lambda x: row_map(x))
    wiod_int_usa2014['Source Region'] = wiod_int_usa2014['Country'].apply(lambda x: row_map(x))
    wiod_int_row2014['Source Region'] = wiod_int_row2014['Country'].apply(lambda x: row_map(x))

    wiod_int_chn2014 = wiod_int_chn2014.groupby(['Source Region','Industry Code']).sum().reset_index()
    wiod_int_usa2014 = wiod_int_usa2014.groupby(['Source Region','Industry Code']).sum().reset_index()
    wiod_int_row2014 = wiod_int_row2014.groupby(['Source Region','Industry Code']).sum().reset_index()


    '''
    ----------------------------------------
    Collapse the ROW data by columns
    ----------------------------------------
    '''

    # Extract the names of each industry of the row data
    int_col_names = list(wiod_int_row2014.columns)[2:58]

    # Loop through the intermediates and aggregate everything 
    for int_name in int_col_names:
        for col in list(wiod_int_row2014.columns)[58:-1]:
            if int_name in col:
                wiod_int_row2014[int_name] = wiod_int_row2014[int_name] + wiod_int_row2014[col]
                
    # Extract only the relevant columns from the ROW data
    int_col_names.extend(['Source Region','Industry Code'])
    wiod_int_row2014 = wiod_int_row2014[int_col_names]

    # Merge the datasets together (remember, respect order: CHN,ROW,USA)
    del wiod_int_chn2014['Country']
    del wiod_int_usa2014['Country']

    wiod_int2014 = pd.merge(wiod_int_chn2014,wiod_int_row2014,on=['Source Region','Industry Code'],how='inner')
    wiod_int2014 = pd.merge(wiod_int2014,wiod_int_usa2014,on=['Source Region','Industry Code'],how='inner')

    '''
    --------------------------------------------------------------------------------
    Extract the intermediate transactions matrix and compute the shares matrix
    --------------------------------------------------------------------------------
    Special Notes:
    --------------
    There are some values in the matrix that are 0 and this causes an issue 
    with the invertibility of the total expenditure matrix. For instance,
    C33 - Repair and Installation of Machinery and Equipment amounts to 0.
    To circumvent this issue, I replace 0 values with 1. This allows the matrix
    to be inverted but it does not change intermediate spending. 

    '''
    # Extract the intermediate expenditure columns as a matrix
    X = wiod_int2014.iloc[:,2:].values

    # Create a vector of ones of the same dimension
    i = np.ones((1,X.shape[0]))

    # Compute total intermediate purchases in each region-sector
    X_total = np.dot(i,X)

    # Replace 0s with 1s
    X_total[X_total ==0] = 1.0

    # Diagonalize and invert the matrix
    Pi_x = np.transpose(np.dot(X,inv(np.diag(X_total[0]))))

    print('Successfully computed the expenditure share matrix!')

    # Load the socioeconomic accounts data
    wiod_socio_data = pd.read_excel('http://www.wiod.org/protected3/data16/SEA/WIOD_SEA_Nov16.xlsx',sheet_name='DATA',header=0)

    print('Successfully downloaded SEA data for WIOD!')

    # Load the exchange rate data to convert into US$$$$
    wiod_exch_data = pd.read_excel('http://www.wiod.org/protected3/data16/EXR_WIOD_Nov16.xlsx',sheet_name='EXR',header=3)

    print('Successfully downloaded exchange rate data for WIOD!')

    # Only keep 2014
    wiod_socio_data2014 = wiod_socio_data[['country','variable','code',wiod_socio_data.columns[-1]]]
    wiod_exch_data2014 = wiod_exch_data[['Acronym','_2014']]

    # Rename the columns for the exchange rate data
    wiod_exch_data2014.columns = ['country','exch_rate']

    # Merge the data together 
    wiod_exp_data2014 = pd.merge(wiod_socio_data2014,wiod_exch_data2014,on='country',how='inner',validate='m:1')
    wiod_exp_data2014.head()

    # Extract the Chinese expenditure data
    chn_exp_data2014 = wiod_exp_data2014[wiod_exp_data2014['country'] == 'CHN']

    # Extract the US expenditure data 
    usa_exp_data2014 = wiod_exp_data2014[wiod_exp_data2014['country'] == 'USA']

    # Extract the ROW expenditure data
    row_exp_data2014 = wiod_exp_data2014[(wiod_exp_data2014['country'] != 'USA') & (wiod_exp_data2014['country'] != 'CHN')]

    '''
    ------------------------------------------------
    China factor cost shares
    ------------------------------------------------
    '''
    # Value added
    chn_va_data2014 = chn_exp_data2014[chn_exp_data2014['variable'] == 'VA']
    chn_va_data2014.columns = ['country','variable','code','va','exch_rate']

    # Gross output 
    chn_go_data2014 = chn_exp_data2014[chn_exp_data2014['variable'] == 'GO']
    chn_go_data2014.columns = ['country','variable','code','go','exch_rate']

    # Capital compensation
    chn_cap_data2014 = chn_exp_data2014[chn_exp_data2014['variable'] == 'CAP']
    chn_cap_data2014.columns = ['country','variable','code','cap','exch_rate']

    # Merge the data together 
    chn_data2014 = pd.merge(chn_va_data2014,chn_go_data2014,on=['country','code'],how='inner',validate='1:1')
    chn_data2014 = pd.merge(chn_data2014,chn_cap_data2014,on=['country','code'],how='inner',validate='1:1')

    # Compute the share parameters
    chn_data2014['alpha'] = chn_data2014['cap']/chn_data2014['va']
    chn_data2014['eta'] = chn_data2014['va']/chn_data2014['go']

    # Extract the parameter vectors
    chn_alpha_j = chn_data2014['alpha'].values 
    chn_eta_j = chn_data2014['eta'].values

    '''
    ------------------------------------------------
    "ROW" factor cost shares
    ------------------------------------------------
    Special Note:
    -------------
    This isn't entirely the rest of the world
    '''
    # Multiply times the exchange rate
    row_exp_data2014['exp_us'] = row_exp_data2014[wiod_socio_data.columns[-1]]*row_exp_data2014['exch_rate']

    # Collapse the data across industries
    row_exp_data2014 = row_exp_data2014.groupby(['variable','code']).sum().reset_index()


    # Value added
    row_va_data2014 = row_exp_data2014[row_exp_data2014['variable'] == 'VA']
    row_va_data2014.columns = ['variable','code','2014','exch_rate','va']

    # Gross output 
    row_go_data2014 = row_exp_data2014[row_exp_data2014['variable'] == 'GO']
    row_go_data2014.columns = ['variable','code','2014','exch_rate','go']

    # Capital compensation
    row_cap_data2014 = row_exp_data2014[row_exp_data2014['variable'] == 'CAP']
    row_cap_data2014.columns = ['variable','code','2014','exch_rate','cap']

    # Merge the data together 
    row_data2014 = pd.merge(row_va_data2014,row_go_data2014,on=['code'],how='inner',validate='1:1')
    row_data2014 = pd.merge(row_data2014,row_cap_data2014,on=['code'],how='inner',validate='1:1')

    # Compute the share parameters
    row_data2014['alpha'] = row_data2014['cap']/row_data2014['va']
    row_data2014['eta'] = row_data2014['va']/row_data2014['go']


    # Extract the parameter vectors
    row_alpha_j = row_data2014['alpha'].values
    row_eta_j = row_data2014['eta'].values

    '''
    ------------------------------------------------
    USA factor cost shares
    ------------------------------------------------
    '''
    # Value added
    usa_va_data2014 = usa_exp_data2014[usa_exp_data2014['variable'] == 'VA']
    usa_va_data2014.columns = ['country','variable','code','va','exch_rate']

    # Gross output 
    usa_go_data2014 = usa_exp_data2014[usa_exp_data2014['variable'] == 'GO']
    usa_go_data2014.columns = ['country','variable','code','go','exch_rate']

    # Capital compensation
    usa_cap_data2014 = usa_exp_data2014[usa_exp_data2014['variable'] == 'CAP']
    usa_cap_data2014.columns = ['country','variable','code','cap','exch_rate']

    # Merge the data together 
    usa_data2014 = pd.merge(usa_va_data2014,usa_go_data2014,on=['country','code'],how='inner',validate='1:1')
    usa_data2014 = pd.merge(usa_data2014,usa_cap_data2014,on=['country','code'],how='inner',validate='1:1')

    # Compute the share parameters
    usa_data2014['alpha'] = usa_data2014['cap']/usa_data2014['va']
    usa_data2014['eta'] = usa_data2014['va']/usa_data2014['go']

    # Extract the parameter vectors
    usa_alpha_j = usa_data2014['alpha'].values 
    usa_eta_j = usa_data2014['eta'].values

    # Sum the value added by country
    usa_va = usa_va_data2014['va'].sum()

    # Compute the Domar weights
    usa_go_data2014['domar'] = usa_go_data2014['go']/usa_va
    usa_domar = usa_go_data2014['domar'].values



    print('Successfully calibrated factor shares!')

    # Extract only the value added from the WIOD dataset
    wiod_va2014 = wiod_2014.T.reset_index()

    # Keep the relevant columns 
    wiod_va2014 = wiod_va2014[['index',0,1,2472]][4:]

    # Rename the columns for convenience
    wiod_va2014.columns = ['industry','description','country','va']

    '''
    ------------------------------------------------
    CHINA
    ------------------------------------------------
    '''

    # Extract the Chinese data
    chn_va2014 = wiod_va2014[wiod_va2014['country'] == 'CHN'][0:56]

    # Compute GDP
    chn_va2014['gdp'] = chn_va2014['va'].sum()

    # Compute value added contributions of each industry
    chn_va2014['upsilon'] = chn_va2014['va']/chn_va2014['gdp']

    '''
    ------------------------------------------------
    US
    ------------------------------------------------
    '''
    # Extract the US data
    usa_va2014 = wiod_va2014[wiod_va2014['country'] == 'USA'][0:56]

    # Compute GDP
    usa_va2014['gdp'] = usa_va2014['va'].sum()

    # Compute value added contributions of each industry
    usa_va2014['upsilon'] = usa_va2014['va']/usa_va2014['gdp']


    '''
    ------------------------------------------------
    ROW
    ------------------------------------------------
    '''
    # Extract the US data
    row_va2014 = wiod_va2014[(wiod_va2014['country'] != 'USA') & (wiod_va2014['country'] != 'CHN')][0:42*56]

    # Extract the main industry code
    row_va2014['industry_alt'] = row_va2014['industry'].apply(lambda x: x.split('.')[0])

    # Collapse the data by industry
    row_va2014 = row_va2014.groupby('industry_alt')['va'].sum().reset_index()

    # Compute ROW GDP
    row_va2014['gdp'] = row_va2014['va'].sum()

    # Compute value added contributions of each industry
    row_va2014['upsilon'] = row_va2014['va']/row_va2014['gdp']



    '''
    ------------------------------------------------
    Construct the Upsilon matrix
    ------------------------------------------------
    '''
    # Create the China upsilon entries
    chn_upsilon = np.pad(chn_va2014['upsilon'].values,(0,2*56),'constant').reshape((1,168))

    # Create the ROW upsilon entries
    row_upsilon = np.pad(row_va2014['upsilon'].values,(56,56),'constant').reshape((1,168))

    # Create the USA upsilon entries
    usa_upsilon = np.pad(usa_va2014['upsilon'].values,(2*56,0),'constant').reshape((1,168))

    # Create the Upsilon matrix 
    Upsilon = np.concatenate([chn_upsilon,row_upsilon,usa_upsilon])


    print('Successfully calibrated the value added shares matrix!')

    # Extract the final expenditure columns as a matrix
    X = wiod_int2014.iloc[:,2:].values

    '''
    ------------------------------------------------
    CHINA
    ------------------------------------------------
    '''

    # Extract the gross output vector for CHN
    chn_go2014 = chn_data2014['go'].values.reshape((56,1))

    '''
    ------------------------------------------------
    ROW
    ------------------------------------------------
    '''

    # Extract only the value added from the WIOD dataset
    wiod_va2014 = wiod_2014.T.reset_index()

    # Keep the relevant columns 
    wiod_go2014 = wiod_va2014[['index',0,1,2474]][4:]

    # Rename the columns for convenience
    wiod_go2014.columns = ['industry','description','country','go']

    # Extract the ROW data
    row_go2014 = wiod_go2014[(wiod_go2014['country'] != 'USA') & (wiod_go2014['country'] != 'CHN')][0:42*56]

    # Extract the main industry code
    row_go2014['industry_alt'] = row_go2014['industry'].apply(lambda x: x.split('.')[0])

    # Collapse the data by industry
    row_go2014 = row_go2014.groupby('industry_alt')['go'].sum().reset_index()

    # Extract the gross output vector 
    row_go2014 = row_go2014['go'].values.reshape((56,1))

    '''
    ------------------------------------------------
    USA
    ------------------------------------------------
    '''
    # Extract the gross output vector for USA
    usa_go2014 = usa_data2014['go'].values.reshape((56,1))

    '''
    ------------------------------------------------
    Construct the PsiX matrix
    ------------------------------------------------
    '''
    # Concatenate the gross output vectors
    py = np.concatenate([chn_go2014,row_go2014,usa_go2014])

    # Replace 0s with 1s (If GO is 0, then intermediate spending/purchases should also be 0.)
    py[py ==0] = 1.0

    # Diagonalize the matrix
    diag_py = np.diag(np.array(py).flatten())

    # Compute the PsiX matrix
    Psi_x = np.transpose(np.dot(np.transpose(X),inv(diag_py)))

    print('Successfully calibrated intermediate spending revenue shares!')

    # Add the gross output data to the consumption dataset
    py[py == 1.0] = 0 
    wiod_hh2014 = wiod_HH2014.copy()
    wiod_hh2014['go'] = pd.Series(py.flatten())

    # Compute the shares
    wiod_hh2014['CONSh_chn_share'] = wiod_hh2014['CONS_h.CHN']/wiod_hh2014['go']
    wiod_hh2014['CONSh_row_share'] = wiod_hh2014['CONS_h.ROW']/wiod_hh2014['go']
    wiod_hh2014['CONSh_usa_share'] = wiod_hh2014['CONS_h.USA']/wiod_hh2014['go']
    wiod_hh2014.fillna(0,inplace=True)

    # Extract the final spending revenue shares
    Psi_f = wiod_hh2014[['CONSh_chn_share','CONSh_row_share','CONSh_usa_share']].values

    print('Successfully calibrated final spending revenue shares!')

    

    # Download the government response tracker dataset
    grt_data = pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv')

    # Download the 2019 OES data
    oes_data = pd.read_excel('https://github.com/cblackburn-bea/Datasets/raw/master/Data/nat4d_M2018_dl.xlsx')

    # Download the Dingel and Neiman WFH data
    wfh_data = pd.read_csv('https://github.com/jdingel/DingelNeiman-workathome/raw/master/onet_to_BLS_crosswalk/output/onet_teleworkable_blscodes.csv')

    # Penn World Table
    pwt_data = pd.read_excel('https://www.rug.nl/ggdc/docs/pwt91.xlsx',sheet_name ='Data')

    print('Successfully downloaded data for labor supply shock calibration!')

    # Relevant columns
    grt_rel_cols = ['CountryName','CountryCode','RegionName','Date','StringencyIndex']

    # Extract the Chinese stringency data
    grt_chn_data = grt_data[grt_rel_cols][(grt_data['CountryCode']=='CHN') & grt_data['RegionName'].isnull()]


    # Extract the US stringency data
    grt_usa_data = grt_data[grt_rel_cols][(grt_data['CountryCode']=='USA') & grt_data['RegionName'].isnull()]

    # Extract the ROW stringency data
    grt_row_data = grt_data[grt_rel_cols][(grt_data['CountryCode']!='CHN') & (grt_data['CountryCode'] !='USA')]

    # Remove regional data in the ROW data
    grt_row_data = grt_row_data[grt_row_data['RegionName'].isnull()]
    grt_row_data.columns = ['countryname','countrycode','regionname','date','stringencyindex']

    # Extract the 2017 PWT
    pwt_data2017 = pwt_data[['countrycode','country','rgdpo']][pwt_data['year']==2017]

    # Drop the USA and CHN
    pwt_row_data2017 = pwt_data2017[(pwt_data2017['countrycode'] != 'CHN') & (pwt_data2017['countrycode'] != 'USA')]

    # Compute ROW GDP
    pwt_row_data2017['rgdpw'] = pwt_row_data2017['rgdpo'].sum()

    # Compute the share for each country
    pwt_row_data2017['gdp_share'] = pwt_row_data2017['rgdpo']/pwt_row_data2017['rgdpw']

    # Merge the ROW PWT data with the ROW GRT data
    grt_row_merge = pd.merge(grt_row_data,pwt_row_data2017,on='countrycode',how='left',validate='m:1')

    # Replace NaNs with 0
    grt_row_merge = grt_row_merge.fillna(0)

    # Compute the weighted-average stringency index for the ROW component
    wm = lambda x: np.average(x, weights=grt_row_merge.loc[x.index, 'gdp_share'])
    grt_row_data = grt_row_merge.groupby(['date']).agg(mean_stringency=('stringencyindex',wm)).reset_index()
    grt_row_data['mean_stringency_norm'] = grt_row_data['mean_stringency']/100


    # Extract the stringency data for CHN
    chn_string = list(grt_chn_data['StringencyIndex']/100)

    # Extract the stringency data for USA
    usa_string = list(grt_usa_data['StringencyIndex']/100)

    # Extract the stringency data for ROW
    row_string = list(grt_row_data['mean_stringency_norm'])


    import math

    # Keep the relevant OES data
    oes_data.columns = [title.lower() for title in oes_data.columns]
    oes_rel_cols = ['naics','naics_title','occ_code','occ_title','tot_emp']
    oes_data_subset = oes_data[oes_rel_cols][oes_data['occ_group']=='detailed']

    def naics3(x):
        if x in ['221100', '221200', '221300']:
            return x
        elif x in ['3250A1', '3250A2', '325400']:
            return x
        elif x in ['336100', '336200', '336300', '336400', '336500', '336600','336900']:
            return x
        elif x in ['541100','541500','541200','541600','541300','541700','541800','541900','541400']:
            return x
        elif x in ['561100', '561200', '561300', '561400', '561500', '561600','561700', '561900']:
            return x
        elif x in ['811100', '811200', '811300', '811400']:
            return x
        else:
            return str(x[0:3])

    # Extract the 3-digit NAICS code
    oes_data_subset['naics_3'] = oes_data_subset['naics'].apply(lambda x: naics3(x))

    # Change the column names of the WFH data
    wfh_data.columns = [title.lower() for title in wfh_data.columns]



    # Merge the telework data with the oes data
    oes_tel_data = pd.merge(oes_data_subset,wfh_data, on ='occ_code',how='left',validate='m:1')




    # Check for NaN values
    def nancheck(x):
        if np.isnan(x) == True:
            return 1
        else:
            return 0
    oes_tel_data['check'] = oes_tel_data['teleworkable'].apply(lambda x: nancheck(x))

    # Remove NaN values from the computation
    oes_tel_data = oes_tel_data[oes_tel_data['check'] == 0]




    # Replace missing values with 0
    def starcheck(x):
        if type(x) == str:
            return 0
        else:
            return x
    oes_tel_data['tot_emp'] = oes_tel_data['tot_emp'].apply(lambda x: starcheck(x))



    # Create function that assigns NACE codes to the naics codes
    def naics_to_nace(x):
        try:
            x_multi = math.floor(int(x)/10)
        except ValueError:
            x_multi = 0
        if x == '115':
            return 'A01'
        if x == '113':
            return 'A02'
        if x == '114':
            return 'A03'
        if x == '211' or x == '212' or x == '213':
            return 'B'    
        if x == '221100' or x == '221200':
            return 'D35+D36'
        if x == '221300':
            return 'E36'
        if x_multi == 23:
            return 'F'
        if x == '321':
            return 'C16'
        if x == '327':
            return 'C23'
        if x == '331':
            return 'C24'
        if x == '332':
            return 'C25'
        if x == '333':
            return 'C28'
        if x == '334':
            return 'C26'
        if x == '335':
            return 'C27'
        if x in ['336100', '336200', '336300', '336400', '336500', '336600']:
            return 'C29'
        if x == '336900':
            return 'C30'
        if x == '337':
            return 'C31_C32'
        if x == '339':
            return 'C31_C32'
        if x == '311':
            return 'C10_C12'
        if x == '312':
            return 'C10_C12'
        if x == '313':
            return 'C13_C15'
        if x == '314':
            return 'C13_C15'
        if x == '315' or x == '316':
            return 'C13_C15'
        if x == '322':
            return 'C17'
        if x == '323':
            return 'C18'
        if x == '324':
            return 'C19'
        if x in ['3250A1', '3250A2']:
            return 'C21'
        if x == '325400':
            return 'C21'
        if x == '326':
            return 'C22'
        if x_multi == 42:
            return 'G46'
        if x == '441':
            return 'G45'
        if x == '445':
            return 'G47'
        if x == '452':
            return 'G47'
        if x in ['442','443','444','446','447','448','451','453','454']:
            return 'G47'
        if x == '481':
            return 'H51'
        if x == '482':
            return 'H49'
        if x == '483':
            return 'H50'
        if x == '484':
            return 'H49'
        if x == '485':
            return 'H49'
        if x == '486':
            return 'H49'
        if x == '487':
            return 'H52'
        if x == '492':
            return 'H53'
        if x == '493':
            return 'H52'
        if x == '511':
            return 'J58'
        if x == '512':
            return 'J59_J60'
        if x == '517':
            return 'J61'
        if x == '515':
            return 'J59_J60'
        if x == '514':
            return 'J62_J63'
        if x == '521':
            return 'K64'
        if x == '523':
            return 'K66'
        if x == '524':
            return 'K65'
        if x == '525':
            return 'K65'
        if x == '531':
            return 'L68'
        if x == '532':
            return 'N77'
        if x == '541100':
            return 'M69_M70'
        if x == '541500':
            return 'J62_J63'
        if x == '541200':
            return 'M71'
        if x == '541600':
            return 'M69_M70'
        if x == '541300':
            return 'M71'
        if x == '541700':
            return 'M72'
        if x == '541800':
            return 'M73'
        if x == '541900':
            return 'M74_M75'
        if x == '541400':
            return 'M74_M75'
        if x == '551':
            return 'M69_M70'
        if x == '561300':
            return 'N78'
        if x == '561500':
            return 'N79'
        if x in ['561100', '561200','561400', '561600','561700', '561900']:
            return 'N80-N82'
        if x == '562':
            return 'E37-E39'
        if x_multi == 61:
            return 'P85'
        if x == '621' or x == '622' or x == '623':
            return 'Q86'
        if x == '624':
            return 'Q87_Q88'
        if x == '711':
            return 'R90_R92'
        if x == '713':
            return 'R93'
        if x == '721':
            return 'I'
        if x == '722':
            return 'I'
        if x == '811300':
            return 'C33'
        if x == '811100':
            return 'G45'
        if x == '813':
            return 'S94'
        if x in ['811200','811400']:
            return 'S95'
        if x == '812':
            return 'S96'
        if x == '814':
            return 'T'
        if x == '999':
            return 'O84'
        

    # Convert the NAICS to the NACE Codes     
    oes_tel_data['nace'] = oes_tel_data['naics_3'].apply(lambda x: naics_to_nace(x))

    # Drop none-types
    oes_tel_data = oes_tel_data[oes_tel_data['nace'] != None]

    # Sum to compute total employment by NACE category
    oes_tot_emp = oes_tel_data.groupby(['nace','occ_code','teleworkable'])['tot_emp'].sum().reset_index()

    # Compute total employment in each industry
    oes_tot_emp_ind = oes_tot_emp[['nace','tot_emp']].groupby('nace').sum().reset_index()

    # Compute the employment shares of each industry
    oes_tot_emp = pd.merge(oes_tot_emp,oes_tot_emp_ind,on=['nace'],how='left',validate='m:1')
    oes_tot_emp['share'] = oes_tot_emp['tot_emp_x']/oes_tot_emp['tot_emp_y']


    # Compute the percentage of workers in each industry who are not capable of teleworking
    oes_tot_emp['tel_emp_share'] = oes_tot_emp['teleworkable']*oes_tot_emp['share']
    oes_tel_cap = oes_tot_emp[['nace','tel_emp_share']].groupby('nace').sum().reset_index()
    oes_tel_cap['non_tel_cap'] = 1-oes_tel_cap['tel_emp_share']

    ''' Aggregate to WIOD industries where necessary'''
    def convertnace(x):
        if x[0] == 'N':
            return 'N'
        elif x[0] == 'Q':
            return 'Q'
        elif x[0] == 'R' or x[0] == 'S':
            return 'R_S'    
        else: 
            return x

    oes_tel_cap['nace_2'] = oes_tel_cap['nace'].apply(lambda x: convertnace(x))

    oes_tel_cap = oes_tel_cap.groupby('nace_2')['non_tel_cap'].mean().reset_index()

    # Add Fishing and Aquaculture
    fish_val = oes_tel_cap[oes_tel_cap['nace_2'].isin(['A01','A02'])]['non_tel_cap'].mean()
    fish = pd.Series({'nace_2':'A03','non_tel_cap':fish_val})

    fish.name = 2
    oes_tel_cap = oes_tel_cap.append(fish).sort_index()


    # Add C20 
    chem_val = oes_tel_cap[oes_tel_cap['nace_2'] == 'C21']['non_tel_cap'].mean()
    chem = pd.Series({'nace_2':'C20','non_tel_cap':chem_val})
    chem.name = 9
    oes_tel_cap = oes_tel_cap.append(chem).sort_index()

    # Add T and U
    t_val = 0
    t = pd.Series({'nace_2':'T','non_tel_cap':t_val})
    u = pd.Series({'nace_2':'U','non_tel_cap':t_val})


    t.name = 52
    u.name = 53
    oes_tel_cap = oes_tel_cap.append(t).sort_index()
    oes_tel_cap = oes_tel_cap.append(u).sort_index()


    # Extract the first 90 days from the China GRT data
    chn_q1_grt = chn_string[0:91]

    # Compute the mean
    chn_q1_grtmean = np.mean(chn_q1_grt)

    # Compute the maximum
    chn_q1_grtmax = np.max(chn_q1_grt)

    # Multiply the telework capacity vector and extract the data
    chn_shock_mean = np.array(oes_tel_cap['non_tel_cap']*chn_q1_grtmean).reshape((56,1)) 
    chn_shock_max = np.array(oes_tel_cap['non_tel_cap']*chn_q1_grtmax).reshape((56,1))

    row_shock_null = np.array(oes_tel_cap['non_tel_cap']*0).reshape((56,1)) 
    usa_shock_null = np.array(oes_tel_cap['non_tel_cap']*0).reshape((56,1)) 

    Xi_j_mean = np.concatenate((chn_shock_mean,row_shock_null,usa_shock_null),axis=0)
    Xi_j_max = np.concatenate((chn_shock_max,row_shock_null,usa_shock_null),axis=0)


    print('Successfully calibrated labor shocks for 2020Q1!')

    print('***MODEL CALIBRATED***')

    return [Pi_f, Pi_x, chn_alpha_j, chn_eta_j, row_alpha_j, row_eta_j, usa_alpha_j, usa_eta_j, Upsilon, Psi_x, Psi_f,Xi_j_mean,Xi_j_max,usa_domar]

#Model = calibrate()


