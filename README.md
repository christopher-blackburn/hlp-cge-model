# bea-economic-model
### Updated: 09/17/2020

## Current Tasks

- [x] Calibrate the Model to WIOD for 3 regions and 56 sectors
  - [x] Calibrate ![\mathbf{\Pi}^{f}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPi%7D%5E%7Bf%7D) (household expenditure shares) 
  - [x] Calibrate ![\mathbf{\Pi}^{x}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPi%7D%5E%7Bx%7D) (intermediate input expenditure shares)
  - [x] Calibrate ![\mathbf{\alpha}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5Calpha%7D) and ![\mathbf{\eta}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5Ceta%7D) (factor cost shares) 
  - [x] Calibrate ![\mathbf{\Upsilon}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CUpsilon%7D) (value added shares)
  - [x] Calibrate ![\mathbf{\Psi}^{x}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPsi%7D%5E%7Bx%7D) (Revenue share of intermediate inputs)
  - [x] Calibrate ![\mathbf{\Psi}^{f}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPsi%7D%5E%7Bf%7D) (Revenue share of final demand)
- [ ] Run and anlayze prototype simulations
  - [x] Solve the model for heterogeneous factor shares
  - [x] Solve the model for industry-specific labor supply shocks (as opposed to occupation specific)
  - [x] Calibrate labor supply shocks 
  - [] Simulate model to obtain preliminary results
- [ ] Model improvements and extensions

## Running the Model

To execute the model, you will need to have access to ```Python 3``` and the following packages:

1. ``numpy``
2. ``pandas``

### Calibration 

In order to calibrate the model, you will need to download and execute the file ```calibrate.py``` ([found here](Calibration/calibrate.py). The script creates an instance of a function that can then be used to calibrate the model and collect the matrices required for the simulation. Here is an example of how to execute the calibration file. Note this is not the only way to execute the file. In Python 3, execute the following code

``` import os 

# Change to the directory with the calibration.py file
os.chdir(path_to_file)

# Import the calibration script
from calibrate import calibrate

# Execute the model
M = calibrate()
```
You should see a myriad of statements highlighting different successful calibrations. If the model calibrates without error, you should see a statement ```***MODEL CALIBRATED***``` After the model has been successfully calibrated, the object ```M``` is a list containing the calibrated matrices in the model. This object will be referenced later. 



## About

This project contains the code for constructing and using the BEA economic model. The model is based on the paper by Huo, Levchenko, and Pandalai-Nayar (2020) and adapted to leverage the internal data source of the Bureau of Economic Analysis. 


## Introduction 

This is a technical document that describes the data and method for estimating the BEA economic model. The model is based off of Huo, Levchenko, and Pandalai-Nayar's (2020) "International Comovement in the Global Production Network." For the rest of the document, we will refer to this paper as HLP. As we proceed with the document, we highlight the components of the model and the data that goes along with these various components. We note that all equations were generated using this [website](https://tex-image-link-generator.herokuapp.com/). 

The technical document proceeds as follows. The first section highlights the consumption side of the economy. We present the economic environment as given in HLP and the corresponding data requirements. For the initial version of this document, in which there will more than likely be several iterations, we start by presenting the data used as given in HLP.

The next section goes into the production side of the economy. 

## Households

In the model, each country ![n](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+n) is populated with a representative household. The represenative household consumes final goods and supplies labor and capital to industries. The household's problem is given by

![\max_{\mathcal{F}_n,\lbrace H_{nj} \rbrace} \mathcal{F}_{n} - \sum_{j}H_{nj}^{1+ \frac{1}{\psi}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmax_%7B%5Cmathcal%7BF%7D_n%2C%5Clbrace+H_%7Bnj%7D+%5Crbrace%7D+%5Cmathcal%7BF%7D_%7Bn%7D+-+%5Csum_%7Bj%7DH_%7Bnj%7D%5E%7B1%2B+%5Cfrac%7B1%7D%7B%5Cpsi%7D%7D)

subject to 


![P_{n}\mathcal{F}_n = \sum_{j}W_{nj}H_{nj} + R_{nj}K_{nj}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+P_%7Bn%7D%5Cmathcal%7BF%7D_n+%3D+%5Csum_%7Bj%7DW_%7Bnj%7DH_%7Bnj%7D+%2B+R_%7Bnj%7DK_%7Bnj%7D)

The consumption index ![\mathcal{F}_{n}](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cmathcal%7BF%7D_%7Bn%7D) is assumed to be constant elasticity of substition given by

![\mathcal{F}_{n}= \left[\sum_j \sum_m \vartheta^{\frac{1}{\rho}}_{mj,n} \mathcal{F}_{mj,n}^{\frac{\rho-1}{\rho}} \right]^{\frac{\rho}{\rho-1}}](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cmathcal%7BF%7D_%7Bn%7D%3D+%5Cleft%5B%5Csum_j+%5Csum_m+%5Cvartheta%5E%7B%5Cfrac%7B1%7D%7B%5Crho%7D%7D_%7Bmj%2Cn%7D+%5Cmathcal%7BF%7D_%7Bmj%2Cn%7D%5E%7B%5Cfrac%7B%5Crho-1%7D%7B%5Crho%7D%7D+%5Cright%5D%5E%7B%5Cfrac%7B%5Crho%7D%7B%5Crho-1%7D%7D)

It should be noted that we deviate from the notation in HLP, and adopt a certain convention throughout the rest of the paper. That is, we will tend to reserve the first index for the <i>source</i> country(-sector) and the second index for the <i>destination</i> country(-sector). When we turn to the matrix notation, we will be explicit about the entries of each matrix. 

We now turn to the first major result of the paper that requires calibration. That is, the representative household in ![n](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+n)'s expenditure share on final goods ![j](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+j) sourced from country ![m](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+m) is given by

![\pi_{mj,n} = \frac{\vartheta_{mj,n}P_{mj,n}^{1-\rho}}{\sum_{k,l}\vartheta_{kl,n}P_{kl,n}^{1-\rho}}](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cpi_%7Bmj%2Cn%7D+%3D+%5Cfrac%7B%5Cvartheta_%7Bmj%2Cn%7DP_%7Bmj%2Cn%7D%5E%7B1-%5Crho%7D%7D%7B%5Csum_%7Bk%2Cl%7D%5Cvartheta_%7Bkl%2Cn%7DP_%7Bkl%2Cn%7D%5E%7B1-%5Crho%7D%7D)

### Calibrating Household Expenditure Shares

The first major component of the model that requires calibration is the expenditure share of the representative households. According to HLP, the dataset used to calibrate the final use parameters is the WIOD. The following code segment calibrates these parameters using the WIOD. According to the download portion of the website, the input-ouput tables are in current prices, denoted in millions of dollars. The database covers 28 EU countries and 15 other major countries in the world for the period 2000-2014. However, for the purpose of this exercise we only need to recover the 2014 input-output table. As a check on our code, there are 43 countries (and ROW component) in the data and each country has 56 sectors. This implies the country-sector vector length is ![NJ = 44 \times 56 = 2,464](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+NJ+%3D+44+%5Ctimes+56+%3D+2%2C464). 

In essence, the following code performs these operations. In the WIOD data, the expenditure by the representative household ![n](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+n) on country-sector ![mj](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+mj) is given by the ![NJ \times N](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+NJ+%5Ctimes+N) vector ![\mathbf{F}](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cmathbf%7BF%7D). To compute expenditure shares, we first compute total household expenditure in ![N](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+N) to compute this we use 

![\mathbf{F}_{total} = \mathbf{\iota}\mathbf{F}](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cmathbf%7BF%7D_%7Btotal%7D+%3D+%5Cmathbf%7B%5Ciota%7D%5Cmathbf%7BF%7D)

where ![\mathbf{\iota}](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cmathbf%7B%5Ciota%7D) is a ![1 \times NJ](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+1+%5Ctimes+NJ) vector of 1s. Hence, the matrix ![\mathbf{F}_{total}](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cmathbf%7BF%7D_%7Btotal%7D) is a ![1 \times N](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+1+%5Ctimes+N) matrix where each entry corresponds to each country's household expenditures on final goods. The next step is to compute the final use expenditure shares using the following expression

![\mathbf{\Pi}^{f} = \left[\mathbf{F}diag(\mathbf{F}_{total})^{-1}\right]^{'}](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cmathbf%7B%5CPi%7D%5E%7Bf%7D+%3D+%5Cleft%5B%5Cmathbf%7BF%7Ddiag%28%5Cmathbf%7BF%7D_%7Btotal%7D%29%5E%7B-1%7D%5Cright%5D%5E%7B%27%7D)

We note that this procedure is general for the ![N](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+N) country case. However, we make some adjustments because we role up these expenditures into a rest of the world component. 

The code for computing household expenditure shares is called [get_hh_shares.py](Calibration/get_hh_shares.py). The code (generally) proceeds as follows:

1. Download the 2014 WIOT from the WIOD website
2. Extract household spending components by each region
3. Roll up expenditures for ROW (sum the columns)
4. Sum the row elements to make sure the matrix is NJ x N, where N=3 and J=56
5. Extract the matrix elements and compute the final expenditure share matrix

If run successfully, the code should should generate the statement ```Successfully computed the expenditure share matrix!``` and return the matrix ```Pi_f``` that corresponds to the ![\mathbf{\Pi}^{f}](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cmathbf%7B%5CPi%7D%5E%7Bf%7D) matrix from HLP (2020). 

## Firms

With the household side of the economy calibrated, we turn our attention to the production side of the economy. Each industry ![nj](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+nj) is populated by a representative firm with access to CRS production function given by

![Y_{nj} = \left(K_{nj}^{\alpha_j}H_{nj}^{1-\alpha_j}\right)^{\eta_j}X_{nj}^{1-\eta_j}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+Y_%7Bnj%7D+%3D+%5Cleft%28K_%7Bnj%7D%5E%7B%5Calpha_j%7DH_%7Bnj%7D%5E%7B1-%5Calpha_j%7D%5Cright%29%5E%7B%5Ceta_j%7DX_%7Bnj%7D%5E%7B1-%5Ceta_j%7D)

where intermediate input usage is a composite of intermediates inputs sourced from other industries. The composite intermediate is given by

![X_{nj} = \left(\sum_{i} \sum_{m}\mu_{mi,nj}^{\frac{1}{\epsilon}}X_{mi,nj}^{\frac{\epsilon-1}{\epsilon}}\right)^{\frac{\epsilon}{\epsilon-1}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+X_%7Bnj%7D+%3D+%5Cleft%28%5Csum_%7Bi%7D+%5Csum_%7Bm%7D%5Cmu_%7Bmi%2Cnj%7D%5E%7B%5Cfrac%7B1%7D%7B%5Cepsilon%7D%7DX_%7Bmi%2Cnj%7D%5E%7B%5Cfrac%7B%5Cepsilon-1%7D%7B%5Cepsilon%7D%7D%5Cright%29%5E%7B%5Cfrac%7B%5Cepsilon%7D%7B%5Cepsilon-1%7D%7D)

One important assumption that might be relevant for future interations is that an input's price is given by

![P_{mi,nj} = \tau_{mi,n}P_{mi}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+P_%7Bmi%2Cnj%7D+%3D+%5Ctau_%7Bmi%2Cn%7DP_%7Bmi%7D)

where ![\tau_{mi,n}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ctau_%7Bmi%2Cn%7D) is an iceberg trade cost that is constant and exogenous. The constant and exogenous assumption might be something we want to consider adapting in future iterations of the model. 

Under cost minimization, we have the share of intermediates sourced from $mi$ in total intermediate spending in $nj$ is given by 

![\pi_{mi,nj}^{x} = \frac{\mu_{mi,nj} P_{mi,nj}^{1-\epsilon}}{\sum_{k,l}\mu_{kl,nj} P_{kl,nj}^{1-\epsilon}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cpi_%7Bmi%2Cnj%7D%5E%7Bx%7D+%3D+%5Cfrac%7B%5Cmu_%7Bmi%2Cnj%7D+P_%7Bmi%2Cnj%7D%5E%7B1-%5Cepsilon%7D%7D%7B%5Csum_%7Bk%2Cl%7D%5Cmu_%7Bkl%2Cnj%7D+P_%7Bkl%2Cnj%7D%5E%7B1-%5Cepsilon%7D%7D)

With this result, we are now ready to turn to the next calibrated parameter of the model. 

### Calibrating Intermediate Input Shares

Intermediate input shares are calibrated using the 2014 WIOT. To compute a country-sector ![mi](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+mi)'s share of intermediate spending in ![nj](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+nj), we start by defining the ![NJ \times NJ](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+NJ+%5Ctimes+NJ) matrix of intermediate transactions as ![\mathbf{X}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7BX%7D). We first need to compute total intermediate spending for each country-industry pair. Total intermediate spending is computed as 

![\mathbf{X}_{total} = \mathbf{\iota}\mathbf{X}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7BX%7D_%7Btotal%7D+%3D+%5Cmathbf%7B%5Ciota%7D%5Cmathbf%7BX%7D)

With this, we perform a similar operation as before and calibrate the intermediate shares matrix to the 2014 WIOT as follows

![\mathbf{\Pi}^{x} = \left[\mathbf{X}diag\left(\mathbf{X}_{total}\right)\right]^{'}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPi%7D%5E%7Bx%7D+%3D+%5Cleft%5B%5Cmathbf%7BX%7Ddiag%5Cleft%28%5Cmathbf%7BX%7D_%7Btotal%7D%5Cright%29%5Cright%5D%5E%7B%27%7D)

We note the transpose here is actually important. The entries in ![\mathbf{X}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7BX%7D) correspond to intermediate payments from the column country-sector to the row country-sector. In contrast, the intermediate shares matrix in HLP uses the opposite convention.  Hence, after computing the shares matrix, we need to transpose the matrix to make them consistent.

The code for constructing the intermediate input shares matrix is given in [get_int_shares.py](Calibration/get_hh_shares.py). In general, the code does the following:

1. Extracts intermediate input transaction matrix for each region, i.e. China, USA, and ROW
2. Collapse spending from other regions and ROW into a single region titled ROW.
3. Compute the intermediate input shares matrix

If the code runs successfully, you should see a statement print ```Successfully computed the expenditure share matrix!``` and the matrix ```Pi_x``` returned. 

### Calibrating Factor Shares

With the intermediate shares matrix calibrated, we next calibrate the factor shares in the Cobb-Douglas top-level production function. For this calibration, HLP use the KLEMS dataset. One might wonder why HLP decide to use KLEMS rather than WIOD. For the BEA model, we instead use the WIOD socioeconomic accounts (SEA) to calibrate the factor shares. First, the SEA's industry definitions match those in the WIOD. Generally, the KLEMS datasets do not match on a one-to-one basis. Second, the regional coverage of the SEA's are complete, whereas the KLEMS database does not cover all the regions included in the WIOD. 

Before discussing the calibration, we first introduce the theory that motivates the calibration. If you are familiar with the Cobb-Douglas production function and its parameters, you can move on. Otherwise, the following derivations may prove to be insightful. The top-level production function for a firm is Cobb-Douglas and given by

![Y_{nj} = \left(K_{nj}^{\alpha_j}H_{nj}^{1-\alpha_j}\right)^{\eta_j}X_{nj}^{1-\eta_j}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+Y_%7Bnj%7D+%3D+%5Cleft%28K_%7Bnj%7D%5E%7B%5Calpha_j%7DH_%7Bnj%7D%5E%7B1-%5Calpha_j%7D%5Cright%29%5E%7B%5Ceta_j%7DX_%7Bnj%7D%5E%7B1-%5Ceta_j%7D)

We should note this equation is taken directly from HLP. One important detail about this equation is that the the parameters on the production function are only indexed by industry ![j](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+j) and not by the country-industry pair ![nj](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+nj). After speaking with Zhen Huo, the authors deployed this assumption to reduce noise in the data. However, he claimed the model can be solved with the heterogeneity across countries. To understand each parameter, let's compute the first order conditions:

1. The first-order condition with respect to capital implies

![\eta_j \alpha_j = \frac{r K_{nj}}{P_{nj}Y_{nj}} = \frac{KC_{nj}}{GO_{nj}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ceta_j+%5Calpha_j+%3D+%5Cfrac%7Br+K_%7Bnj%7D%7D%7BP_%7Bnj%7DY_%7Bnj%7D%7D+%3D+%5Cfrac%7BKC_%7Bnj%7D%7D%7BGO_%7Bnj%7D%7D)

2. The first-order condition with respect to labor implies 

![\eta_j \left(1-\alpha_j\right) = \frac{w H_{nj}}{P_{nj}Y_{nj}} = \frac{LC_{nj}}{GO_{nj}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ceta_j+%5Cleft%281-%5Calpha_j%5Cright%29+%3D+%5Cfrac%7Bw+H_%7Bnj%7D%7D%7BP_%7Bnj%7DY_%7Bnj%7D%7D+%3D+%5Cfrac%7BLC_%7Bnj%7D%7D%7BGO_%7Bnj%7D%7D)

3. Combining (1) and (2) implies 

![\eta_j = \frac{r K_{nj} + w H_{nj}}{P_{nj}Y_{nj}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ceta_j+%3D+%5Cfrac%7Br+K_%7Bnj%7D+%2B+w+H_%7Bnj%7D%7D%7BP_%7Bnj%7DY_%7Bnj%7D%7D)

4. Combining (3) with (1) implies 

![\alpha_j = \frac{r K_{nj}}{r K_{nj} + w H_{nj}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Calpha_j+%3D+%5Cfrac%7Br+K_%7Bnj%7D%7D%7Br+K_%7Bnj%7D+%2B+w+H_%7Bnj%7D%7D)

and 

![1-\alpha_j = \frac{w L_{nj}}{r K_{nj} + w H_{nj}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+1-%5Calpha_j+%3D+%5Cfrac%7Bw+L_%7Bnj%7D%7D%7Br+K_%7Bnj%7D+%2B+w+H_%7Bnj%7D%7D)

The code for computing the factor shares is in [get_fac_shares.py](Calibration/get_fac_shares.py). The code proceeds as follows:

1. Download the SEA and exchange rate data from the WIOD website
  - Exchange rates are used to convert local currency into a common currency to aggregate regions into the ROW component
2. Compute ![\alpha ](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Calpha+) and ![\eta ](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ceta+) for each country-sector

If the code runs successfully, you should see a few printed statements:

1. ```Successfully downloaded SEA data for WIOD!``` --> The SEA data download was successful
2. ```Successfully downloaded exchange rate data for WIOD!``` --> The exhange rate data download was successful
3. ```Successfully calibrated factor shares!``` --> Factor shares were calibrated appropriately. 

and the factor shares vectors will be return for each region, i.e. ![\mathbf{\alpha}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5Calpha%7D) and ![\mathbf{\eta}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5Ceta%7D) will be returned for China, ROW, and the USA. The vectors are given by ```chn_alpha_j```, ```row_alpha_j```, ```usa_alpha_j```, ```chn_eta_j```, ```row_eta_j```, and ```usa_eta_j```. It should be noted that we do not average these directly within the code. 

## Market Clearing Condition

HLP use a first-order approximation to the market clearing condition to solve the model in closed-form. In matrix notation, the market clearing condition based on the first-order approximation is given by 

![\begin{align*}
\ln \mathbf{P}_t + \ln \mathbf{Y}_t =& \left(\mathbf{\Psi}^{f}\mathbf{\Upsilon}+ \mathbf{\Psi}^{x}\right)\left( \ln \mathbf{P}_t + \ln \mathbf{Y}_t \right) + \left(1-\rho\right)\left( \diag(\mathbf{\Psi}^{f}\mathbf{1}) - \mathbf{\Psi}^{f}\mathbf{\Pi}^{f}\right)\ln \mathbf{P}_{t}\\
&+\left(1-\epsilon\right)\left(\diag(\mathbf{\Psi}^{x}\mathbf{1} )- \mathbf{\Psi}^{x} \mathbf{\Pi}^{x}\right)\ln \mathbf{P}_t
\end{align*}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cbegin%7Balign%2A%7D%0A%5Cln+%5Cmathbf%7BP%7D_t+%2B+%5Cln+%5Cmathbf%7BY%7D_t+%3D%26+%5Cleft%28%5Cmathbf%7B%5CPsi%7D%5E%7Bf%7D%5Cmathbf%7B%5CUpsilon%7D%2B+%5Cmathbf%7B%5CPsi%7D%5E%7Bx%7D%5Cright%29%5Cleft%28+%5Cln+%5Cmathbf%7BP%7D_t+%2B+%5Cln+%5Cmathbf%7BY%7D_t+%5Cright%29+%2B+%5Cleft%281-%5Crho%5Cright%29%5Cleft%28+%5Cdiag%28%5Cmathbf%7B%5CPsi%7D%5E%7Bf%7D%5Cmathbf%7B1%7D%29+-+%5Cmathbf%7B%5CPsi%7D%5E%7Bf%7D%5Cmathbf%7B%5CPi%7D%5E%7Bf%7D%5Cright%29%5Cln+%5Cmathbf%7BP%7D_%7Bt%7D%5C%5C%0A%26%2B%5Cleft%281-%5Cepsilon%5Cright%29%5Cleft%28%5Cdiag%28%5Cmathbf%7B%5CPsi%7D%5E%7Bx%7D%5Cmathbf%7B1%7D+%29-+%5Cmathbf%7B%5CPsi%7D%5E%7Bx%7D+%5Cmathbf%7B%5CPi%7D%5E%7Bx%7D%5Cright%29%5Cln+%5Cmathbf%7BP%7D_t%0A%5Cend%7Balign%2A%7D%0A)

Hence, we need to calibrate ![\mathbf{\Upsilon}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CUpsilon%7D%0A), ![\mathbf{\Psi}^{x}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPsi%7D%5E%7Bx%7D%0A), and ![\mathbf{\Psi}^{f}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPsi%7D%5E%7Bf%7D%0A) to solve the model. The following sections detail the approach to calibrating these matrices. 

### Calibrating Value Added Shares

In the market clearing condition, the matrix ![\mathbf{\Upsilon}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CUpsilon%7D%0A) stores the value added shares of each country-sector to a country's total GDP. In the HLP model, the value added of an industry can be computed as 

![\eta_{i}P_{mi}Y_{mi}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ceta_%7Bi%7DP_%7Bmi%7DY_%7Bmi%7D)

Calibrating these parameters is relatively straightforward. First, we compute value added from each industry. Here we deviate slightly from HLP in order to match the data. We compute value added of industry ![(m,i)](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%28m%2Ci%29) as 

![\eta_{mi}P_{mi}Y_{mi}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ceta_%7Bmi%7DP_%7Bmi%7DY_%7Bmi%7D)

Second, we compute GDP for each country. For country ![m](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+m), we sum up the value added of all industries in the country. That is, we compute 

![GDP_{m} = P_{n}\mathcal{F}_{n} =  \sum_{i} \eta_{mi}P_{mi}Y_{mi}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+GDP_%7Bm%7D+%3D+P_%7Bn%7D%5Cmathcal%7BF%7D_%7Bn%7D+%3D++%5Csum_%7Bi%7D+%5Ceta_%7Bmi%7DP_%7Bmi%7DY_%7Bmi%7D)

Third, we compute entries in ![\mathbf{\Upsilon}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CUpsilon%7D%0A) as follows

![\mathbf{\Upsilon}_{n,mi} = \frac{\eta_{mi}P_{mi}Y_{mi}}{P_{n}\mathcal{F}_{n}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CUpsilon%7D_%7Bn%2Cmi%7D+%3D+%5Cfrac%7B%5Ceta_%7Bmi%7DP_%7Bmi%7DY_%7Bmi%7D%7D%7BP_%7Bn%7D%5Cmathcal%7BF%7D_%7Bn%7D%7D)

for when ![n=m](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+n%3Dm) and 0 otherwise. 

The code for calibrating the value added share matrix is in [get_va_shares.py](Calibration/get_va_shares.py). If the code is run successfully, you should observe a printed statement that proclaims ```Successfully calibrated the value added shares matrix!```. 

### Calibrating Revenue Share of Intermediates

The next matrix to calibrate is ![\mathbf{\Psi}^{x}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPsi%7D%5E%7Bx%7D%0A) which contains the share of total revenue from intermediate spending on different inputs. The method for computing this matrix is similar to the procedure for computing intermediate input shares. As before, let ![\mathbf{X}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7BX%7D) be the intermediate transactions matrix. Furthermore, let ![\mathbf{PY}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7BPY%7D) be the vector of gross output for each country-sector. To compute each intermediate's contribution to total revenue in the row country-sector, we compute the following matrix

![\mathbf{\Psi}^{x} = \left[\mathbf{X}^{'}\diag(\mathbf{PY})^{-1}\right]^{'}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPsi%7D%5E%7Bx%7D+%3D+%5Cleft%5B%5Cmathbf%7BX%7D%5E%7B%27%7D%5Cdiag%28%5Cmathbf%7BPY%7D%29%5E%7B-1%7D%5Cright%5D%5E%7B%27%7D)

The code that performs these operations is in [get_psix_shares.py](Calibration/get_psix_shares.py). If successfully computed, you should see the statement ```Successfully calibrated intermediate spending revenue shares!``` print on your screen. 



### Calibrating Revenue Share of Final Demand

The final matrix to calibrate is ![\mathbf{\Psi}^{f}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPsi%7D%5E%7Bf%7D%0A) which contains the share of total revenue from household spending. The method for computing entries in this matrix is straightforward. First, compute gross output for a country-sector as ![P_{nj}Y_{nj}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+P_%7Bmi%7DY_%7Bmi%7D%0A). Second, compute household spending from a country on this industry as ![\pi_{m,nj}^{f}P_{m}\mathcal{F}_{m}
](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cpi_%7Bm%2Cnj%7D%5E%7Bf%7DP_%7Bm%7D%5Cmathcal%7BF%7D_%7Bm%7D%0A). 

Hence, the entries in ![\mathbf{\Psi}^{f}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPsi%7D%5E%7Bf%7D%0A) are given by

![\mathbf{\Psi}_{nj,m}^{f} = \frac{\pi_{m,nj}^{f}P_{m}\mathcal{F}_{m}}{P_{nj}Y_{nj}}
](https://render.githubusercontent.com/render/math?math=%5Ctextstyle+%5Cmathbf%7B%5CPsi%7D_%7Bnj%2Cm%7D%5E%7Bf%7D+%3D+%5Cfrac%7B%5Cpi_%7Bm%2Cnj%7D%5E%7Bf%7DP_%7Bm%7D%5Cmathcal%7BF%7D_%7Bm%7D%7D%7BP_%7Bnj%7DY_%7Bnj%7D%7D%0A)

The code for computing this matrix is in [get_psif_shares.py](Calibration/get_psif_shares.py). If successfully calibrated, you should see a statement ```Successfully calibrated final spending revenue shares!```. 


## Calibrating Labor Supply Shocks

Bonadio et al. (2020) applies the HLP model to study the propagation of COVID-19 shocks across international and domestic input-output linkages. To model the labor supply shock, the authors assume households allocate their time across occupations. That is, household preferences are formulated as 

![\max_{\mathcal{F}_{n},\lbrace L_{nl} \rbrace} \mathcal{F}_{n} - \sum_{l=1}^{\mathcal{O}} \frac{1}{1+\frac{1}{\psi}}\left( \frac{L_{nl}}{\xi_{nl}}\right)^{1 + \frac{1}{\psi}}
](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmax_%7B%5Cmathcal%7BF%7D_%7Bn%7D%2C%5Clbrace+L_%7Bnl%7D+%5Crbrace%7D+%5Cmathcal%7BF%7D_%7Bn%7D+-+%5Csum_%7Bl%3D1%7D%5E%7B%5Cmathcal%7BO%7D%7D+%5Cfrac%7B1%7D%7B1%2B%5Cfrac%7B1%7D%7B%5Cpsi%7D%7D%5Cleft%28+%5Cfrac%7BL_%7Bnl%7D%7D%7B%5Cxi_%7Bnl%7D%7D%5Cright%29%5E%7B1+%2B+%5Cfrac%7B1%7D%7B%5Cpsi%7D%7D%0A)

Note the labor supply shifter ![\xi_{nl}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cxi_%7Bnl%7D) is indexed by occupation and region. Hence, the authors calibrate the labor supply shifter as follows 

![\Delta \ln \xi_{nl}  = - \left(1-\omega_{l}\right) \times f\left(GRT_{n}\right)](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5CDelta+%5Cln+%5Cxi_%7Bnl%7D++%3D+-+%5Cleft%281-%5Comega_%7Bl%7D%5Cright%29+%5Ctimes+f%5Cleft%28GRT_%7Bn%7D%5Cright%29)

where ![\omega_{l}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Comega_%7Bl%7D) is an occupation's telework capacity from [Dingel and Neiman (2020)](https://www.nber.org/papers/w26948.pdf). The GRT refers to the Government Response Tracker (see [Hale et al. (2020)](https://covidtracker.bsg.ox.ac.uk/about-api) for more details). 

In Footnote 12 of their [working paper](https://www.nber.org/papers/w27224.pdf), they note that the elasticity of substitution ![\kappa](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ckappa) is set equal to 1 in the simulations. This implies the sectoral occupational shares are unaffected by the labor supply shock and the occupational share matrix ![\mathbf{\Pi}^{\mathcal{O}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5CPi%7D%5E%7B%5Cmathcal%7BO%7D%7D) drops out of the first-order approximation. 

Because of this, we elect to follow the approach of HLP and assume the representative household allocates labor across sectors rather than occupations. For the purpose of comparison, we formulate the representative household's preferences as 

![\max_{\mathcal{F}_{n},\lbrace L_{nj} \rbrace} \mathcal{F}_{n} - \sum_{j=1} \frac{1}{1+\frac{1}{\psi}}\left( \frac{L_{nj}}{\xi_{nj}}\right)^{1 + \frac{1}{\psi}}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmax_%7B%5Cmathcal%7BF%7D_%7Bn%7D%2C%5Clbrace+L_%7Bnj%7D+%5Crbrace%7D+%5Cmathcal%7BF%7D_%7Bn%7D+-+%5Csum_%7Bj%3D1%7D+%5Cfrac%7B1%7D%7B1%2B%5Cfrac%7B1%7D%7B%5Cpsi%7D%7D%5Cleft%28+%5Cfrac%7BL_%7Bnj%7D%7D%7B%5Cxi_%7Bnj%7D%7D%5Cright%29%5E%7B1+%2B+%5Cfrac%7B1%7D%7B%5Cpsi%7D%7D)

In this formulation, the labor supply shifter ![\xi_{nj}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cxi_%7Bnj%7D) is instead indexed by sector rather than occupation. Therefore, we calibrate the labor supply shifter as follows

![\Delta \ln \xi_{nj} = -f\left(GRT_{n}\right)\sum_{l=1}^{\mathcal{O}} \pi_{lj}^{\mathcal{O}} \left(1-\omega_{l}\right) ](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5CDelta+%5Cln+%5Cxi_%7Bnj%7D+%3D+-f%5Cleft%28GRT_%7Bn%7D%5Cright%29%5Csum_%7Bl%3D1%7D%5E%7B%5Cmathcal%7BO%7D%7D+%5Cpi_%7Blj%7D%5E%7B%5Cmathcal%7BO%7D%7D+%5Cleft%281-%5Comega_%7Bl%7D%5Cright%29+)

The term in the summation captures an industry's capacity to maintain normal operations during a lockdown as in [Blackburn and Moreno-Cruz (2020)](https://www.dropbox.com/s/gtja41hnhgfzssf/Physical_Contact_Index_COVID19%20%289%29.pdf?dl=0). 

To calibrate the labor supply shocks, we need to acquire several data sources. The first data source is the government response tracker (GRT) dataset. The dataset is available via direct download from a Github repository. The second dataset is the Occupational Employment Statistics (OES) dataset. We use the 2019 OES data to get a more accurate read on the composition of occupational employment across industries. The third dataset is the telework dataset from Dingel and Neiman (2020). We use the crosswalk file between ONET and BLS codes available on their Github replication page. The fourth dataset is the 2017 Penn World Table. We use the Penn World Table to aggregate the GRT stringency index into a ROW component. 

The code for downloading these datasets is found in [get_grt_data.py](Calibration/get_grt_data.py). With this data, we calibrate the labor supply shocks given by the relevant formula above. The labor supply shocks are calibrated in the the code [get_labor_shocks.py](Calibration/get_labor_shocks.py). It is important to note that since we are primarily interested in the effects in the first quarter of 2020, we set labor supply shocks in the United States and ROW to zero. We plan to explore variations where these shocks are non-zero in future iterations. In the initial iteration, we compute two version of the stringency index for China: (i) the average stringency index for 2020Q1, and (ii) the maximum stringency index for 2020Q1. 

### Government Response Tracker

One area where we need to think about in more detail is how we use the GRT stringency index. In the Bonadio et al. (2020) paper, they use the GRT index along with a curve fitting procedure to create a cardinal measure from the stringency index. They note the curve fitting adjusts the dispersion of the index, but the average stringecy is relatively unchanged. They provide the mean and standard deviation from the fitted lognormal distribution to the Industrial Production data.

### Model Solution with Industry Labor Supply Shocks

In this subsection, we solve the model using our specification of labor supply shocks. For a full proof, please see the companion paper as we omit certain details. We begin with the log-linearized intertermporal labor supply function given by 

![    \ln \mathbf{L}_t^{s} = \psi\left(\ln \mathbf{W}_t - \left(\mathbf{\Pi}^{f} \otimes \mathbf{1}\right)\ln \mathbf{P}_t\right) + \left(1+\psi\right)\ln \mathbf{\xi}_t](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+++++%5Cln+%5Cmathbf%7BL%7D_t%5E%7Bs%7D+%3D+%5Cpsi%5Cleft%28%5Cln+%5Cmathbf%7BW%7D_t+-+%5Cleft%28%5Cmathbf%7B%5CPi%7D%5E%7Bf%7D+%5Cotimes+%5Cmathbf%7B1%7D%5Cright%29%5Cln+%5Cmathbf%7BP%7D_t%5Cright%29+%2B+%5Cleft%281%2B%5Cpsi%5Cright%29%5Cln+%5Cmathbf%7B%5Cxi%7D_t)

We next solve for the log-linearized labor demand function in matrix notation which is given by

![    \ln \mathbf{L}_{t}^{d} = \ln \mathbf{Y}_t + \ln \mathbf{P}_t - \ln \mathbf{W}_t](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+++++%5Cln+%5Cmathbf%7BL%7D_%7Bt%7D%5E%7Bd%7D+%3D+%5Cln+%5Cmathbf%7BY%7D_t+%2B+%5Cln+%5Cmathbf%7BP%7D_t+-+%5Cln+%5Cmathbf%7BW%7D_t)

The labor market clearing condition implies that equilibrium employment is given by 

![   \ln \mathbf{L}_t = \ln \mathbf{\xi}_t + \frac{\psi}{1+\psi}\ln \mathbf{Y}_t + \frac{\psi}{1+\psi}\left(\mathbf{I} - \mathbf{\Pi}^{f}\otimes\mathbf{1}\right)\ln\mathbf{P}_t](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle++++%5Cln+%5Cmathbf%7BL%7D_t+%3D+%5Cln+%5Cmathbf%7B%5Cxi%7D_t+%2B+%5Cfrac%7B%5Cpsi%7D%7B1%2B%5Cpsi%7D%5Cln+%5Cmathbf%7BY%7D_t+%2B+%5Cfrac%7B%5Cpsi%7D%7B1%2B%5Cpsi%7D%5Cleft%28%5Cmathbf%7BI%7D+-+%5Cmathbf%7B%5CPi%7D%5E%7Bf%7D%5Cotimes%5Cmathbf%7B1%7D%5Cright%29%5Cln%5Cmathbf%7BP%7D_t)

In a similar fashion, the first-order condition for intermediate inputs is given by

![    \ln \mathbf{X}_t = \ln \mathbf{Y}_t + \left(\mathbf{I} - \mathbf{\Pi}^{x}\right)\ln \mathbf{P}_t](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+++++%5Cln+%5Cmathbf%7BX%7D_t+%3D+%5Cln+%5Cmathbf%7BY%7D_t+%2B+%5Cleft%28%5Cmathbf%7BI%7D+-+%5Cmathbf%7B%5CPi%7D%5E%7Bx%7D%5Cright%29%5Cln+%5Cmathbf%7BP%7D_t)

and the log-linearized production function is 

![    \ln \mathbf{Y}_t = \mathbf{\eta}\left(\mathbf{I} - \mathbf{\alpha}\right)  \ln \mathbf{L}_t + \left(\mathbf{I}-\mathbf{\eta}\right)\ln \mathbf{X}_t](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+++++%5Cln+%5Cmathbf%7BY%7D_t+%3D+%5Cmathbf%7B%5Ceta%7D%5Cleft%28%5Cmathbf%7BI%7D+-+%5Cmathbf%7B%5Calpha%7D%5Cright%29++%5Cln+%5Cmathbf%7BL%7D_t+%2B+%5Cleft%28%5Cmathbf%7BI%7D-%5Cmathbf%7B%5Ceta%7D%5Cright%29%5Cln+%5Cmathbf%7BX%7D_t)

Substituting the expressions for intermediate inputs and equilibrium employment into the log-linearized production, we can solve for the log-deviation in output as 

![    \ln \mathbf{Y}_t = \left[\mathbf{I} - \frac{\psi}{1+\psi}\mathbf{\eta}\left(\mathbf{I}-\mathbf{\alpha}\right)\left(\mathbf{I} + \left(\mathbf{I} - \mathbf{\Pi}^{f}\otimes \mathbf{1}\right)\mathcal{P}\right) - \left(\mathbf{I} - \mathbf{\eta}\right)\left(\mathbf{I} + \left(\mathbf{I} - \mathbf{\Pi}^{x}\right)\mathcal{P}\right)\right]^{-1}\mathbf{\eta}\left(\mathbf{I}-\mathbf{\alpha}\right) \ln \mathbf{\xi}_t](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+++++%5Cln+%5Cmathbf%7BY%7D_t+%3D+%5Cleft%5B%5Cmathbf%7BI%7D+-+%5Cfrac%7B%5Cpsi%7D%7B1%2B%5Cpsi%7D%5Cmathbf%7B%5Ceta%7D%5Cleft%28%5Cmathbf%7BI%7D-%5Cmathbf%7B%5Calpha%7D%5Cright%29%5Cleft%28%5Cmathbf%7BI%7D+%2B+%5Cleft%28%5Cmathbf%7BI%7D+-+%5Cmathbf%7B%5CPi%7D%5E%7Bf%7D%5Cotimes+%5Cmathbf%7B1%7D%5Cright%29%5Cmathcal%7BP%7D%5Cright%29+-+%5Cleft%28%5Cmathbf%7BI%7D+-+%5Cmathbf%7B%5Ceta%7D%5Cright%29%5Cleft%28%5Cmathbf%7BI%7D+%2B+%5Cleft%28%5Cmathbf%7BI%7D+-+%5Cmathbf%7B%5CPi%7D%5E%7Bx%7D%5Cright%29%5Cmathcal%7BP%7D%5Cright%29%5Cright%5D%5E%7B-1%7D%5Cmathbf%7B%5Ceta%7D%5Cleft%28%5Cmathbf%7BI%7D-%5Cmathbf%7B%5Calpha%7D%5Cright%29+%5Cln+%5Cmathbf%7B%5Cxi%7D_t)


### Model Solution with Heterogeneous Factor Shares

HLP average the factor share parameters. However, the equilibrium solution and characterization of the matrices is general and does not require averaging. Instead, we can simply replace the elements of the facto share matrix with country-specific factor shares without re-solving the model. 



