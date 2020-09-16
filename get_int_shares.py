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