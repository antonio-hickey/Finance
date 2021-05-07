"""
Antonio Hickey (https://github.com/antonio-hickey)

Volatility Surface for /ES (S&P500) Future Options
 Using the black-76 model to solve for Implied Volatility
 Then rendering a datset shaped for a 3d surface plot

Target Output Dimenions:
   1(X). Strike
   2(Y). Time Until Expiration
   3(Z). Implied Volatility
"""

#--------------------------
# Importing Modules
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import pathlib
import pandas as pd
import csv
import numpy as np
from math import sqrt, pi, log, e
from scipy.stats import norm
from sympy.stats import Normal, cdf
#--------------------------

#------------------------------------
# Importing Dataset
#------------------------------------
PATH = pathlib.Path(__file__).parent
df = pd.read_csv(PATH.joinpath("dataset.csv"))
#------------------------------------

#------------------------------------
# Black 76 Model
def bs76_P(o_type, sigma, f, k, r, t):
    sigma = float(sigma)
    d1 = (log(f / k) + (sigma ** 2 / 2) * t) / (sigma * sqrt(t))
    d2 = d1 - sigma * sqrt(t)
    if o_type == 'c':
        price = e**(-r * t) * (f * norm.cdf(d1) - k * norm.cdf(d2))
        return price
    elif o_type == 'p':
        price = e**(-r * t) * (k * norm.cdf(-d2) - f * norm.cdf(-d1))
        return price
#------------------------------------   
# IV Calculation
def i_Vol(o_type, o_price, f, k, r, t):
    Accuracy = 0.00001
    higher_vol = 500.0
    max_vol = 500.0
    min_vol = 0.0001
    lower_vol = 0.0001
    i_ = 0
    while 1:
        #------------------------------------
        # Solving for sigma
        i_ +=1
        i_V = (higher_vol + lower_vol)/2.0
        price = bs76_P(o_type, i_V, f, k, r, t)
        #------------------------------------
        # Call
        if o_type == 'c':
            lower_price = bs76_P(o_type, lower_vol, f, k, r, t)
            if (lower_price - o_price) * (price - o_price) > 0:
                lower_vol = i_V
            else:
                higher_vol = i_V
            if abs(price - o_price) < Accuracy:
                break 
                if i_V > max_vol - 5 :
                    i_V = 0.000001
                    break
        #------------------------------------
        # Put
        elif o_type == 'p':
            higher_price = bs76_P(o_type, higher_vol, f, k, r, t)
            if (higher_price - o_price) * (price - o_price) > 0:
                higher_vol = i_V
            else:
                lower_vol = i_V
            if abs(price - o_price) < Accuracy: 
                break 
                if i_ > 50: 
                    break
        #------------------------------------
    #------------------------------------
    # Output IV 
    return i_V
    #------------------------------------
#------------------------------------

# Inputs for model
sigmaC = []
sigmaP = []
dte = []
strike = []

# Loop for each row in dataset
for x in range(len(df)):
    F = df["F"].iloc[x] # Underlying Forward Price
    R = df["R"].iloc[x] # Risk Free Rate
    T = df["TTE"].iloc[x] # Time Until Expiration
    K1 = df["K1"].iloc[x] # Strikes
    K2 = df["K2"].iloc[x]
    K3 = df["K3"].iloc[x]
    K4 = df["K4"].iloc[x]
    K5 = df["K5"].iloc[x]
    K6 = df["K6"].iloc[x]
    K7 = df["K7"].iloc[x]
    K8 = df["K8"].iloc[x]
    K9 = df["K9"].iloc[x]
    K10 = df["K10"].iloc[x]
    CPK1 = df["CAK1"].iloc[x] # Call Prices
    CPK2 = df["CAK2"].iloc[x]
    CPK3 = df["CAK3"].iloc[x]
    CPK4 = df["CAK4"].iloc[x]
    CPK5 = df["CAK5"].iloc[x]
    CPK6 =df["CAK6"].iloc[x]
    CPK7 = df["CAK7"].iloc[x]
    CPK8 = df["CAK8"].iloc[x]
    CPK9 = df["CAK9"].iloc[x]
    CPK10 = df["CAK10"].iloc[x]
    PPK1 = df["PAK1"].iloc[x] # Put Prices
    PPK2 = df["PAK2"].iloc[x]
    PPK3 = df["PAK3"].iloc[x]
    PPK4 = df["PAK4"].iloc[x]
    PPK5 = df["PAK5"].iloc[x]
    PPK6 = df["PAK6"].iloc[x]
    PPK7 = df["PAK7"].iloc[x]
    PPK8 = df["PAK8"].iloc[x]
    PPK9 = df["PAK9"].iloc[x]
    PPK10 = df["PAK10"].iloc[x]
    
    # Call IV
    sigmaC.append(i_Vol('c',CPK1,F,K1,R,T/365))
    sigmaC.append(i_Vol('c',CPK2,F,K2,R,T/365))
    sigmaC.append(i_Vol('c',CPK3,F,K3,R,T/365)) 
    sigmaC.append(i_Vol('c',CPK4,F,K4,R,T/365))
    sigmaC.append(i_Vol('c',CPK5,F,K5,R,T/365))
    sigmaC.append(i_Vol('c',CPK6,F,K6,R,T/365))
    sigmaC.append(i_Vol('c',CPK7,F,K7,R,T/365))
    sigmaC.append(i_Vol('c',CPK8,F,K8,R,T/365))
    sigmaC.append(i_Vol('c',CPK9,F,K9,R,T/365))
    sigmaC.append(i_Vol('c',CPK10,F,K10,R,T/365))
    
    # Put IV
    sigmaP.append(i_Vol('p',PPK2,F,K2,R,T/365))
    sigmaP.append(i_Vol('p',PPK2,F,K2,R,T/365))
    sigmaP.append(i_Vol('p',PPK3,F,K3,R,T/365))
    sigmaP.append(i_Vol('p',PPK4,F,K4,R,T/365))
    sigmaP.append(i_Vol('p',PPK5,F,K5,R,T/365))
    sigmaP.append(i_Vol('p',PPK6,F,K6,R,T/365))
    sigmaP.append(i_Vol('p',PPK7,F,K7,R,T/365))
    sigmaP.append(i_Vol('p',PPK8,F,K8,R,T/365))
    sigmaP.append(i_Vol('p',PPK9,F,K9,R,T/365))
    sigmaP.append(i_Vol('p',PPK10,F,K10,R,T/365))
    
    # Days Until Expiration
    dte.append(df["TTE"].iloc[x])

# List of strikes
strikes = [
    df["K1"].iloc[0],
    df["K2"].iloc[0],
    df["K3"].iloc[0],
    df["K4"].iloc[0],
    df["K5"].iloc[0],
    df["K6"].iloc[0],
    df["K7"].iloc[0],
    df["K8"].iloc[0],
    df["K9"].iloc[0],
    df["K10"].iloc[0] 
]

# Render DataFrame
df_ = {
     # Days Until Expiration
    'DTE': dte,
     # Strikes
    'K1': strikes[0],
    'K2':strikes[1],
    'K3':strikes[2],
    'K4':strikes[3],
    'K5':strikes[4],
    'K6':strikes[5],
    'K7':strikes[6],
    'K8':strikes[7],
    'K9':strikes[8],
    'K10':strikes[9],
     # Calls
    'CIV1':[sigmaC[0],sigmaC[10],sigmaC[20],sigmaC[30],sigmaC[40],sigmaC[50]],
    'CIV2':[sigmaC[1],sigmaC[11],sigmaC[21],sigmaC[31],sigmaC[41],sigmaC[51]],
    'CIV3':[sigmaC[2],sigmaC[12],sigmaC[22],sigmaC[32],sigmaC[42],sigmaC[52]],
    'CIV4':[sigmaC[3],sigmaC[13],sigmaC[23],sigmaC[33],sigmaC[43],sigmaC[53]],
    'CIV5':[sigmaC[4],sigmaC[14],sigmaC[24],sigmaC[34],sigmaC[44],sigmaC[54]],
    'CIV6':[sigmaC[5],sigmaC[15],sigmaC[25],sigmaC[35],sigmaC[45],sigmaC[55]], 
    'CIV7':[sigmaC[6],sigmaC[16],sigmaC[26],sigmaC[36],sigmaC[46],sigmaC[56]],
    'CIV8':[sigmaC[7],sigmaC[17],sigmaC[27],sigmaC[37],sigmaC[47],sigmaC[57]],
    'CIV9':[sigmaC[8],sigmaC[18],sigmaC[28],sigmaC[38],sigmaC[48],sigmaC[58]],  
    'CIV10':[sigmaC[9],sigmaC[19],sigmaC[29],sigmaC[39],sigmaC[49],sigmaC[59]],
     # Puts
    'PIV1':[sigmaP[0],sigmaP[10],sigmaP[20],sigmaP[30],sigmaP[40],sigmaP[50]],
    'PIV2':[sigmaP[1],sigmaP[11],sigmaP[21],sigmaP[31],sigmaP[41],sigmaP[51]], 
    'PIV3':[sigmaP[2],sigmaP[12],sigmaP[22],sigmaP[32],sigmaP[42],sigmaP[52]], 
    'PIV4':[sigmaP[3],sigmaP[13],sigmaP[23],sigmaP[33],sigmaP[43],sigmaP[53]], 
    'PIV5':[sigmaP[4],sigmaP[14],sigmaP[24],sigmaP[34],sigmaP[44],sigmaP[54]], 
    'PIV6':[sigmaP[5],sigmaP[15],sigmaP[25],sigmaP[35],sigmaP[45],sigmaP[55]],
    'PIV7':[sigmaP[6],sigmaP[16],sigmaP[26],sigmaP[36],sigmaP[46],sigmaP[56]], 
    'PIV8':[sigmaP[7],sigmaP[17],sigmaP[27],sigmaP[37],sigmaP[47],sigmaP[57]], 
    'PIV9':[sigmaP[8],sigmaP[18],sigmaP[28],sigmaP[38],sigmaP[48],sigmaP[58]], 
    'PIV10':[sigmaP[9],sigmaP[19],sigmaP[29],sigmaP[39],sigmaP[49],sigmaP[59]],
}
_df = pd.DataFrame(data=df_)

# Structering X 
x_ = [list(_df["K1"].values),list(_df["K2"].values),list(_df["K3"].values),list(_df["K4"].values),list(_df["K5"].values),list(_df["K6"].values),list(_df["K7"].values),list(_df["K8"].values),list(_df["K9"].values),list(_df["K10"].values)]
flast_list = [item for sublist in x_ for item in sublist]
x_ = [_df["K1"].iloc[0],_df["K2"].iloc[0],_df["K3"].iloc[0],_df["K4"].iloc[0],_df["K5"].iloc[0],_df["K6"].iloc[0],_df["K7"].iloc[0],_df["K8"].iloc[0],_df["K9"].iloc[0],_df["K10"].iloc[0],
      _df["K1"].iloc[0],_df["K2"].iloc[0],_df["K3"].iloc[0],_df["K4"].iloc[0],_df["K5"].iloc[0],_df["K6"].iloc[0],_df["K7"].iloc[0],_df["K8"].iloc[0],_df["K9"].iloc[0],_df["K10"].iloc[0],
      _df["K1"].iloc[0],_df["K2"].iloc[0],_df["K3"].iloc[0],_df["K4"].iloc[0],_df["K5"].iloc[0],_df["K6"].iloc[0],_df["K7"].iloc[0],_df["K8"].iloc[0],_df["K9"].iloc[0],_df["K10"].iloc[0],
      _df["K1"].iloc[0],_df["K2"].iloc[0],_df["K3"].iloc[0],_df["K4"].iloc[0],_df["K5"].iloc[0],_df["K6"].iloc[0],_df["K7"].iloc[0],_df["K8"].iloc[0],_df["K9"].iloc[0],_df["K10"].iloc[0],
      _df["K1"].iloc[0],_df["K2"].iloc[0],_df["K3"].iloc[0],_df["K4"].iloc[0],_df["K5"].iloc[0],_df["K6"].iloc[0],_df["K7"].iloc[0],_df["K8"].iloc[0],_df["K9"].iloc[0],_df["K10"].iloc[0],
      _df["K1"].iloc[0],_df["K2"].iloc[0],_df["K3"].iloc[0],_df["K4"].iloc[0],_df["K5"].iloc[0],_df["K6"].iloc[0],_df["K7"].iloc[0],_df["K8"].iloc[0],_df["K9"].iloc[0],_df["K10"].iloc[0],]
# Structering Y
y_ = [_df["DTE"].iloc[0],_df["DTE"].iloc[0],_df["DTE"].iloc[0],_df["DTE"].iloc[0],_df["DTE"].iloc[0],_df["DTE"].iloc[0],_df["DTE"].iloc[0],_df["DTE"].iloc[0],_df["DTE"].iloc[0],_df["DTE"].iloc[0],
      _df["DTE"].iloc[1],_df["DTE"].iloc[1],_df["DTE"].iloc[1],_df["DTE"].iloc[1],_df["DTE"].iloc[1],_df["DTE"].iloc[1],_df["DTE"].iloc[1],_df["DTE"].iloc[1],_df["DTE"].iloc[1],_df["DTE"].iloc[1],
      _df["DTE"].iloc[2],_df["DTE"].iloc[2],_df["DTE"].iloc[2],_df["DTE"].iloc[2],_df["DTE"].iloc[2],_df["DTE"].iloc[2],_df["DTE"].iloc[2],_df["DTE"].iloc[2],_df["DTE"].iloc[2],_df["DTE"].iloc[2],
      _df["DTE"].iloc[3],_df["DTE"].iloc[3],_df["DTE"].iloc[3],_df["DTE"].iloc[3],_df["DTE"].iloc[3],_df["DTE"].iloc[3],_df["DTE"].iloc[3],_df["DTE"].iloc[3],_df["DTE"].iloc[3],_df["DTE"].iloc[3],
      _df["DTE"].iloc[4],_df["DTE"].iloc[4],_df["DTE"].iloc[4],_df["DTE"].iloc[4],_df["DTE"].iloc[4],_df["DTE"].iloc[4],_df["DTE"].iloc[4],_df["DTE"].iloc[4],_df["DTE"].iloc[4],_df["DTE"].iloc[4],
      _df["DTE"].iloc[5],_df["DTE"].iloc[5],_df["DTE"].iloc[5],_df["DTE"].iloc[5],_df["DTE"].iloc[5],_df["DTE"].iloc[5],_df["DTE"].iloc[5],_df["DTE"].iloc[5],_df["DTE"].iloc[5],_df["DTE"].iloc[5]]
# Structering Z Calls
z_ = [list(_df["CIV1"].values),list(_df["CIV2"].values),list(_df["CIV3"].values),list(_df["CIV4"].values),list(_df["CIV5"].values),list(_df["CIV6"].values),list(_df["CIV7"].values),list(_df["CIV8"].values),list(_df["CIV9"].values),list(_df["CIV10"].values)]
flat_list_z = [item for sublist in z_ for item in sublist]
z_ = [_df["CIV1"].iloc[0],_df["CIV2"].iloc[0],_df["CIV3"].iloc[0],_df["CIV4"].iloc[0],_df["CIV5"].iloc[0],_df["CIV6"].iloc[0],_df["CIV7"].iloc[0],_df["CIV8"].iloc[0],_df["CIV9"].iloc[0],_df["CIV10"].iloc[0],
      _df["CIV1"].iloc[1],_df["CIV2"].iloc[1],_df["CIV3"].iloc[1],_df["CIV4"].iloc[1],_df["CIV5"].iloc[1],_df["CIV6"].iloc[1],_df["CIV7"].iloc[1],_df["CIV8"].iloc[1],_df["CIV9"].iloc[1],_df["CIV10"].iloc[1],
      _df["CIV1"].iloc[2],_df["CIV2"].iloc[2],_df["CIV3"].iloc[2],_df["CIV4"].iloc[2],_df["CIV5"].iloc[2],_df["CIV6"].iloc[2],_df["CIV7"].iloc[2],_df["CIV8"].iloc[2],_df["CIV9"].iloc[2],_df["CIV10"].iloc[2],
      _df["CIV1"].iloc[3],_df["CIV2"].iloc[3],_df["CIV3"].iloc[3],_df["CIV4"].iloc[3],_df["CIV5"].iloc[3],_df["CIV6"].iloc[3],_df["CIV7"].iloc[3],_df["CIV8"].iloc[3],_df["CIV9"].iloc[3],_df["CIV10"].iloc[3],
      _df["CIV1"].iloc[4],_df["CIV2"].iloc[4],_df["CIV3"].iloc[4],_df["CIV4"].iloc[4],_df["CIV5"].iloc[4],_df["CIV6"].iloc[4],_df["CIV7"].iloc[4],_df["CIV8"].iloc[4],_df["CIV9"].iloc[4],_df["CIV10"].iloc[4],
      _df["CIV1"].iloc[5],_df["CIV2"].iloc[5],_df["CIV3"].iloc[5],_df["CIV4"].iloc[5],_df["CIV5"].iloc[5],_df["CIV6"].iloc[5],_df["CIV7"].iloc[5],_df["CIV8"].iloc[5],_df["CIV9"].iloc[5],_df["CIV10"].iloc[5],]
# Structering Z Puts
z2_ = [_df["PIV1"].iloc[0],_df["PIV2"].iloc[0],_df["PIV3"].iloc[0],_df["PIV4"].iloc[0],_df["PIV5"].iloc[0],_df["PIV6"].iloc[0],_df["PIV7"].iloc[0],_df["PIV8"].iloc[0],_df["PIV9"].iloc[0],_df["PIV10"].iloc[0],
      _df["PIV1"].iloc[1],_df["PIV2"].iloc[1],_df["PIV3"].iloc[1],_df["PIV4"].iloc[1],_df["PIV5"].iloc[1],_df["PIV6"].iloc[1],_df["PIV7"].iloc[1],_df["PIV8"].iloc[1],_df["PIV9"].iloc[1],_df["PIV10"].iloc[1],
      _df["PIV1"].iloc[2],_df["PIV2"].iloc[2],_df["PIV3"].iloc[2],_df["PIV4"].iloc[2],_df["PIV5"].iloc[2],_df["PIV6"].iloc[2],_df["PIV7"].iloc[2],_df["PIV8"].iloc[2],_df["PIV9"].iloc[2],_df["PIV10"].iloc[2],
      _df["PIV1"].iloc[3],_df["PIV2"].iloc[3],_df["PIV3"].iloc[3],_df["PIV4"].iloc[3],_df["PIV5"].iloc[3],_df["PIV6"].iloc[3],_df["PIV7"].iloc[3],_df["PIV8"].iloc[3],_df["PIV9"].iloc[3],_df["PIV10"].iloc[3],
      _df["PIV1"].iloc[4],_df["PIV2"].iloc[4],_df["PIV3"].iloc[4],_df["PIV4"].iloc[4],_df["PIV5"].iloc[4],_df["PIV6"].iloc[4],_df["PIV7"].iloc[4],_df["PIV8"].iloc[4],_df["PIV9"].iloc[4],_df["PIV10"].iloc[4],
      _df["PIV1"].iloc[5],_df["PIV2"].iloc[5],_df["PIV3"].iloc[5],_df["PIV4"].iloc[5],_df["PIV5"].iloc[5],_df["PIV6"].iloc[5],_df["PIV7"].iloc[5],_df["PIV8"].iloc[5],_df["PIV9"].iloc[5],_df["PIV10"].iloc[5],]
# Redefining
x = x_
y = y_
z = z_
z2 = z2_

# Render Output Dataset
final = {
    'x': x, 'y': y, 'zCall': z, 'zPut': z2
}
print(len(final))
final_set = pd.DataFrame(data=final)
final_set.to_csv("xyz.csv") # Export as xyz.csv
#-----------------------------------------
