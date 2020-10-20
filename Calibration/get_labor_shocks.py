import math

'''
------------------------------------------------
Employment Shares and Telework data
------------------------------------------------
'''

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

labor_shock_mean = np.concatenate((chn_shock_mean,row_shock_null,usa_shock_null),axis=0)
labor_shock_max = np.concatenate((chn_shock_max,row_shock_null,usa_shock_null),axis=0)