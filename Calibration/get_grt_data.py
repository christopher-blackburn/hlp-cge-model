'''
------------------------------------------------
Download the relevant data
------------------------------------------------
'''

# Download the government response tracker dataset
grt_data = pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv')

# Download the 2019 OES data
oes_data = pd.read_excel('https://github.com/cblackburn-bea/Datasets/raw/master/Data/nat4d_M2018_dl.xlsx')

# Download the Dingel and Neiman WFH data
wfh_data = pd.read_csv('https://github.com/jdingel/DingelNeiman-workathome/raw/master/onet_to_BLS_crosswalk/output/onet_teleworkable_blscodes.csv')

# Penn World Table
pwt_data = pd.read_excel('https://www.rug.nl/ggdc/docs/pwt91.xlsx',sheet_name ='Data')

'''
------------------------------------------------
The GRT data
------------------------------------------------
'''
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