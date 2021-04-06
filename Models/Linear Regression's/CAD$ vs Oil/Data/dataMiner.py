#------------------------------------------------------
# Import Modules
#------------------------------------------------------
from fredapi import Fred
import csv
#------------------------------------------------------
# Set FRED api key (free just create an account)
#------------------------------------------------------
fred = Fred(api_key='d3f95f078264238c16bac9b1cd4bffdb')
#------------------------------------------------------
# Define target dataset's
#------------------------------------------------------
CAD = fred.get_series('DEXCAUS')[3913:-4] # Fitting data to fit OIL data
OIL = fred.get_series('DCOILWTICO')
#------------------------------------------------------
# Exporting to csv
#------------------------------------------------------
filename = 'dataset.csv'
columns = ['Date','CAD$ Exchange Rate','Oil Prices']
with open(filename,'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(columns)
	for nth in range(len(CAD.index)):
		row = [CAD.index[nth],CAD.values[nth],OIL.values[nth]]
		csvwriter.writerow(row)
#------------------------------------------------------
