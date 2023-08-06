"""My chocobo cooking script."""
import os
import warnings
import scipy
from sklearn.preprocessing import StandardScaler
import scipy.stats
from statsmodels.distributions.empirical_distribution import ECDF
from datetime import datetime, timedelta

def last_period (df,unique_id,interval,periods,date_column,to_past):
    warnings.filterwarnings("ignore")
    
    df['num'] = df.index
    
    prefix = 'l'+str(periods)+interval[0]
    
    if interval == 'weeks':
         df[prefix] = df[date_column].apply(lambda x: x- timedelta(weeks=periods))
    if interval == 'days':
         df[prefix] = df[date_column].apply(lambda x: x- timedelta(days=periods))
    if interval == 'hours':
         df[prefix] = df[date_column].apply(lambda x: x- timedelta(days=periods))
            
    for col in to_past:
        col_name = 'v'+col
        df[col_name] = df['num'].apply(lambda x: df[col][x]/    
                            (df[(df[unique_id]==df[unique_id][x]) & (df[date_column]==df[prefix][x])][col].sum()+1))