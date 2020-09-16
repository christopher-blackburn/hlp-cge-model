# bea-economic-model
### Updated: 09/16/2020

This project contains the code for constructing and using the BEA economic model. The model is based on the paper by Huo, Levchenko, and Pandalai-Nayar (2020) and adapted to leverage the internal data source of the Bureau of Economic Analysis. 


## Introduction 

This is a technical document that describes the data and method for estimating the BEA economic model. The model is based off of Huo, Levchenko, and Pandalai-Nayar's (2020) "International Comovement in the Global Production Network." For the rest of the document, we will refer to this paper as HLP. As we proceed with the document, we highlight the components of the model and the data that goes along with these various components. 

The technical document proceeds as follows. The first section highlights the consumption side of the economy. We present the economic environment as given in HLP and the corresponding data requirements. For the initial version of this document, in which there will more than likely be several iterations, we start by presenting the data used as given in HLP.

The next section goes into the production side of the economy. 

## Households

In the model, each country $n$ is populated with a representative household. The represenative household consumes final goods and supplies labor and capital to industries. The household's problem is given by

<img src=
"https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmax_%7B%5Cmathcal%7BF%7D_n%2C%5Clbrace+H_%7Bnj%7D+%5Crbrace%7D+%5Cmathcal%7BF%7D_%7Bn%7D+-+%5Csum_%7Bj%7DH_%7Bnj%7D%5E%7B1%2B+%5Cfrac%7B1%7D%7B%5Cpsi%7D%7D" 
alt="\max_{\mathcal{F}_n,\lbrace H_{nj} \rbrace} \mathcal{F}_{n} - \sum_{j}H_{nj}^{1+ \frac{1}{\psi}}">

subject to 


"https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+P_%7Bn%7D%5Cmathcal%7BF%7D_n+%3D+%5Csum_%7Bj%7DW_%7Bnj%7DH_%7Bnj%7D+%2B+R_%7Bnj%7DK_%7Bnj%7D" 
alt="P_{n}\mathcal{F}_n = \sum_{j}W_{nj}H_{nj} + R_{nj}K_{nj}">

The consumption index "https://render.githubusercontent.com/render/math?math=%5Cdisplaystyle+%5Cmathcal%7BF%7D_%7Bn%7D" 
alt="\mathcal{F}_{n}"> is defined  assumed to be constant elasticity of substition given by

$$\mathcal{F}_{n}= \left[\sum_j \sum_m \vartheta^{\frac{1}{\rho}}_{mj,n} \mathcal{F}_{mj,n}^{\frac{\rho-1}{\rho}} \right]^{\frac{\rho}{\rho-1}}$$

It should be noted that we deviate from the notation in HLP, and adopt a certain convention throughout the rest of the paper. That is, we will tend to reserve the first index for the <i>source</i> country(-sector) and the second index for the <i>destination</i> country(-sector). When we turn to the matrix notation, we will be explicit about the entries of each matrix. 

We now turn to the first major result of the paper that requires calibration. That is, the representative household in $n$'s expenditure share on final goods $j$ sourced from country $m$ is given by

$$\pi_{mj,n} = \frac{\vartheta_{mj,n}P_{mj,n}^{1-\rho}}{\sum_{k,l}\vartheta_{kl,n}P_{kl,n}^{1-\rho}}$$

### Calibrating Household Expenditure Shares

The first major component of the model that requires calibration is the expenditure share of the representative households. According to HLP, the dataset used to calibrate the final use parameters is the WIOD. The following code segment calibrates these parameters using the WIOD. According to the download portion of the website, the input-ouput tables are in current prices, denoted in millions of dollars. The database covers 28 EU countries and 15 other major countries in the world for the period 2000-2014. However, for the purpose of this exercise we only need to recover the 2014 input-output table. As a check on our code, there are 43 countries (and ROW component) in the data and each country has 56 sectors. This implies the country-sector vector length is $NJ = 44 \times 56 = 2,464$. 

In essence, the following code performs these operations. In the WIOD data, the expenditure by the representative household $n$ on country-sector $mj$ is given by the $NJ \times N$ vector $\mathbf{F}$. To compute expenditure shares, we first compute total household expenditure in $N$ to compute this we use 

$$\mathbf{F}_{total} = \mathbf{\iota}\mathbf{F}$$

where $\mathbf{\iota}$ is a $1 \times NJ$ vector of 1s. Hence, the matrix $\mathbf{F}_{total}$ is a $1 \times N$ matrix where each entry corresponds to each country's household expenditures on final goods. The next step is to compute the final use expenditure shares using the following expression

$$\mathbf{\Pi}^{f} = \left[\mathbf{F}diag(\mathbf{F}_{total})^{-1}\right]^{'}$$

We note that this procedure is general for the $N$ country case. However, we make some adjustments because we role up these expenditures into a rest of the world component. 
