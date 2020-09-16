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