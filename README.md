# bea-economic-model
### Updated: 09/16/2020

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

The code for computing household expenditure shares is called [get_hh_shares.py](get_hh_shares.py). The code (generally) proceeds as follows:

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

The code for constructing the intermediate input shares matrix is given in [get_int_shares.py](get_hh_shares.py). In general, the code does the following:

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

The code for computing the factor shares is in [get_fac_shares.py](get_fac_shares.py). The code proceeds as follows:

1. Download the SEA and exchange rate data from the WIOD website
  - Exchange rates are used to convert local currency into a common currency to aggregate regions into the ROW component
2. Compute ![\alpha ](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Calpha+) and ![\eta ](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Ceta+) for each country-sector

If the code runs successfully, you should see a few printed statements:

1. ```Successfully downloaded SEA data for WIOD!``` --> The SEA data download was successful
2. ```Successfully downloaded exchange rate data for WIOD!``` --> The exhange rate data download was successful
3. ```Successfully calibrated factor shares!``` --> Factor shares were calibrated appropriately. 

and the factor shares vectors will be return for each region, i.e. ![\mathbf{\alpha}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5Calpha%7D) and ![\mathbf{\eta}](https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathbf%7B%5Ceta%7D) will be returned for China, ROW, and the USA. The vectors are given by ```chn_alpha_j```, ```row_alpha_j```, ```usa_alpha_j```, ```chn_eta_j```, ```row_eta_j```, and ```usa_eta_j```. It should be noted that we do not average these directly within the code. 


