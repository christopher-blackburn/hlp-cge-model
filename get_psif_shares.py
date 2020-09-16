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

