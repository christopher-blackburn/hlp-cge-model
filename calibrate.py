'''This code calibrates the model and returns all matrices required for the simulation'''

import pandas as pd 

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

    print(Pi_x.shape)

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

    return [Pi_f, Pi_x, chn_alpha_j, chn_eta_j, row_alpha_j, row_eta_j, usa_alpha_j, usa_eta_j, Upsilon, Psi_x, Psi_f]

