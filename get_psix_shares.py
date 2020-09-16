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