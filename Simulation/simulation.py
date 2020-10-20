import os
from numpy.linalg import inv
import numpy as np 
import pandas as pd 

# Change to the directory with the calibration file
os.chdir('/Users/cblackburn/Downloads')

# Import the calibration function 
from calibrate import calibrate

def run_simulation(rho,epsilon,psi):

	# Calibrate the model
	Model = calibrate()

	# Specify elasticities of substitution (this will be a user input)
	#rho = 2.75
	#epsilon = 0.5
	#psi = 2

	# Extract the Model Components
	Pi_f = Model[0]
	Pi_x = Model[1]
	chn_alpha_j = Model[2]
	chn_eta_j = Model[3]
	row_alpha_j = Model[4]
	row_eta_j = Model[5]
	usa_alpha_j = Model[6]
	usa_eta_j = Model[7]
	Upsilon = Model[8]
	Psi_x = Model[9]
	Psi_f = Model[10]
	Xi_j_mean = Model[11]
	Xi_j_max = Model[12]
	usa_domar = Model[13]


	# Construct the alpha and eta matrices 
	alpha = np.concatenate((chn_alpha_j,row_alpha_j,usa_alpha_j),axis=0)
	alpha = np.diag(alpha)
	eta = np.concatenate((chn_eta_j,row_eta_j,usa_eta_j),axis=0)
	eta = np.diag(eta)

	# Diagonalize matrix for final good spending
	diag_Psi_f1 = np.diag(np.array(np.dot(Psi_f,np.ones((3,1)))).flatten())

	# Diagonalize matrix for intermediate inputs
	diag_Psi_x1 = np.diag(np.array(np.dot(Psi_x,np.ones((168,1)))).flatten())


	# Compute the price vector 
	M = np.matrix(np.dot(Psi_f,Upsilon) + Psi_x + (1-rho)*(diag_Psi_f1 - np.dot(Psi_f,Pi_f)) + (1-epsilon)*(diag_Psi_x1 -np.dot(Psi_x,Pi_x)),dtype='float')
	P = -1*np.matrix(np.dot(inv(np.eye(168) - M),(np.eye(168) - np.dot(Psi_f,Upsilon) - Psi_x)),dtype='float')

	# Kronecker product
	Pi_f1_kron = np.kron(Pi_f,np.ones((56,1)))

	# Compute the influence matrix
	M_1 = np.nan_to_num((psi/(1+psi))*eta*(np.eye(168) - alpha)*(np.eye(168) + (np.eye(168) - Pi_f1_kron)*P))
	M_2 = np.nan_to_num((np.eye(168) - eta)*(np.eye(168) + (np.eye(168) - Pi_x)*P))
	Lambda = inv(np.eye(168) - M_1 - M_2)

	# Compute log-deviation in output 
	L_1 = np.nan_to_num(Lambda*eta)
	L_1 = np.nan_to_num(L_1*(np.eye(168) - alpha))

	ln_Y_mean = L_1*Xi_j_mean
	ln_Y_max = L_1*Xi_j_max

	print('Successfully simulated log-deviation in output...')

	# Compute log-deviation in employment 
	L_2 = (np.eye(168) + (psi/(1+psi))*(np.eye(168) + (np.eye(168) - Pi_f1_kron)*P)*L_1)
	ln_L_mean = L_2*Xi_j_mean
	ln_L_max = L_2*Xi_j_max

	print('Successfully simulated log-deviation in employment...')

	# Compute the maximum impact on GDP
	d_max = {'usa_eta_j':list(usa_eta_j),'usa_alpha_j':list(usa_alpha_j),'usa_domar_j':usa_domar,'va_imp_max':[x[0] for x in np.array(ln_L_max[-56:])[0:]]}
	acc_max = pd.DataFrame(d_max)
	acc_max['va_cont_j'] = acc_max['usa_eta_j']*(1-acc_max['usa_alpha_j'])*acc_max['usa_domar_j']*acc_max['va_imp_max']

	gdp_max_impact = 100*acc_max['va_cont_j'].sum()
	

	# Compute the mean impact on GDP
	d_mean = {'usa_eta_j':list(usa_eta_j),'usa_alpha_j':list(usa_alpha_j),'usa_domar_j':usa_domar,'va_imp_max':[x[0] for x in np.array(ln_L_mean[-56:])[0:]]}
	acc_mean = pd.DataFrame(d_mean)
	acc_mean['va_cont_j'] = acc_mean['usa_eta_j']*(1-acc_mean['usa_alpha_j'])*acc_mean['usa_domar_j']*acc_mean['va_imp_max']

	gdp_mean_impact = 100*acc_mean['va_cont_j'].sum()

	print('Simulation completed!')

	return [ln_Y_mean,ln_Y_max,ln_L_mean,ln_L_max, gdp_mean_impact,gdp_max_impact]

#results = run_simulation(2.75,0.5,2)


