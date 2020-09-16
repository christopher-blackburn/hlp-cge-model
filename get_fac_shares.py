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