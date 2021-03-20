#--------------------------------------------------------------------------------------------------------
# Importing Python Modules
import csv
import pandas as pd
import pathlib
import numpy as np
from math import sqrt, pi, log, e
from enum import Enum
import scipy.stats as stat
from scipy.stats import norm
from scipy import stats
import sympy
from sympy.stats import Normal, cdf
from sympy import init_printing
init_printing()
#--------------------------------------------------------------------------------------------------------
# Importing Data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("Data").resolve()
dataset = pd.read_csv(DATA_PATH.joinpath("market-data.csv"))
#--------------------------------------------------------------------------------------------------------
# Decimal manipulation function for data cleaning
def mDP(num,d_p):
    for _ in range(abs(d_p)):
        if d_p>0:
            num *= 10;
        else:
            num /= 10.;
    return float(num)
#------------------------------------
# Black 76 Model
def b76(f, k, r, sigma, t, option='call', exact=False):
    d1 = (np.log(f / k) + (sigma ** 2 / 2) * t) / (sigma * sqrt(t))          # Derivative 1
    d2 = d1 - sigma * sqrt(t)                                                # Derivative 2
    if option == 'call':         
        price = e**(-r * t) * (f * norm.cdf(d1) - k * norm.cdf(d2))          # Theoratical Price
        delta = (e**(r*t))*(norm.cdf(d1))                                    # Delta 
        p_density = 1 / sqrt(2 * np.pi) * e**(-d1 ** 2 * 0.5)                # Probabiltiy Density
        gamma = p_density / (f * sigma * sqrt(t))                            # Gamma
        vega = (f*(sqrt(t))*(p_density))                                     # Vega
        theta = -(f*sigma*norm.pdf(d1))/2*sqrt(t)-r*k*e**(-r*t)*norm.cdf(d2) #Theta
    elif option == 'put':
        price = e**(-r * t) * (k * norm.cdf(-d2) - f * norm.cdf(-d1))
        delta = (e**(r*t))*(norm.cdf(d1)-1)
        p_density = 1 / sqrt(2 * np.pi) * e**(-d1 ** 2 * 0.5)
        gamma = p_density / (f * sigma * sqrt(t))
        vega = (f*(sqrt(t))*(p_density))
        theta = -(f*sigma*norm.pdf(d1))/2*sqrt(t)-r*k*e**(-r*t)*norm.cdf(d2)
    return delta,gamma,vega,theta
#------------------------------------
# Black 76 Theoratical Price for backsolving for sigma
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
    while 1:    # While loop
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
    return i_V
    #------------------------------------
#--------------------------------------------------------------------------------------------------------
# Inputs for Model
f = int(dataset['F']) 
k = int(dataset['K1'])
r = float(dataset['R'])
t = float(dataset['T'])
op_c = float(dataset['K1_c_AP'])
op_p = float(dataset['K1_p_AP'])
sigma_c = i_Vol('c',op_c,f,k,r,t/365) 
sigma_p = i_Vol('p',op_p,f,k,r,t/365)
#--------------------------------------------------------------------------------------------------------
# Running Model to get greeks
greeks_c = b76(f,k,r,sigma_c,t/365,option='call')
greeks_p = b76(f,k,r,sigma_p,t/365,option='put')
greeks_c_D = int(mDP(greeks_c[0],2))
greeks_c_G = round(mDP(greeks_c[1],2),3)
greeks_c_V = round(float(mDP(greeks_c[2],-2)),3)
greeks_c_T = round(mDP(greeks_c[3],-2),3)
greeks_p_D = int(mDP(greeks_p[0],2))
greeks_p_G = round(mDP(greeks_p[1],2),3)
greeks_p_V = round(float(mDP(greeks_p[2],-2)),3)
greeks_p_V = "{:.3f}".format(greeks_p_V)
greeks_p_T = round(mDP(greeks_p[3],-2),3)
greeks_c = [greeks_c_D,greeks_c_G,greeks_c_V,greeks_c_T]
greeks_p = [greeks_p_D,greeks_p_G,greeks_p_V,greeks_p_T]
print("Call Option @ Strike {} Greeks: |Delta: {} |Gamma: {}|Vega: {}|Theta: {}".format(k,greeks_c[0],greeks_c[1],greeks_c[2],greeks_c[3]))
print("Put Option @ Strike {} Greeks: |Delta: {} |Gamma: {}|Vega: {}|Theta: {}".format(k,greeks_p[0],greeks_p[1],greeks_p[2],greeks_p[3]))
#--------------------------------------------------------------------------------------------------------