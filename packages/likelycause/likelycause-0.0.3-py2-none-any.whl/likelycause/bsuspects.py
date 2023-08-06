"""My chocobo cooking script."""

import os
import warnings
import scipy
from sklearn.preprocessing import StandardScaler
import scipy.stats
from statsmodels.distributions.empirical_distribution import ECDF

def bayes_suspects (df,y_input,x_input,interval=0.05,min=10):
    import warnings
    warnings.filterwarnings("ignore")
    
    import scipy
    from sklearn.preprocessing import StandardScaler
    import scipy.stats
    from statsmodels.distributions.empirical_distribution import ECDF
    #from likelycause import fvlikelihood    
    
    def fvlikelihood (df,a,value,interval,min,b='NULL'):    
        if b == 'NULL':
            return [len(df),scipy.stats.gaussian_kde(df[a]).integrate_box_1d((1-interval)*df[a].iloc[value],(1+interval)*df[a].iloc[value])]
        else:    
            if len(df[(df[a]<df[a].iloc[value]*(1+interval))&(df[a]>df[a].iloc[value]*(1-interval))])<=min:
                return [0,0]
            else:
                return [len(df[(df[a]<df[a].iloc[value]*(1+interval))&(df[a]>df[a].iloc[value]*(1-interval))]),
                scipy.stats.gaussian_kde(df[(df[a]<df[a].iloc[value]*(1+interval))&(df[a]>df[a].iloc[value]*(1-interval))][b]).integrate_box_1d((1-interval)*df[b].iloc[value],(1+interval)*df[b].iloc[value])]


    
    df['index_col'] = df.index
    namey = 'prob_'+y_input
    df[namey] = df['index_col'].apply(lambda x: fvlikelihood(df,a=y_input,value=x,interval=interval,min=min)[1])
    
    candidates = list()
    for value in x_input:
        namex = 'prob_'+value
        df[namex] = df['index_col'].apply(lambda x: fvlikelihood(df,a=value,value=x,interval=interval,min=min)[1])
        namex2 = 'prob_' + y_input + '_' + value
        df[namex2] = df['index_col'].apply(lambda x: fvlikelihood(df,a=value,value=x,interval=interval,min=min,b=value)[1])
        candidates.append(namex2)
        
    cols = candidates
    cols_index = list()
    for col in cols:    
        cols_index.append(df.columns.get_loc(col))

    bayes_cause = list()
    for i in range(len(df_bayes)):
        if np.isnan(max(df.iloc[i,cols_index]))== True:
            final = 'insufficient data'
            bayes_cause.append(final)
        else:
            final = cols[list(df.iloc[i,cols_index]).index(max(df.iloc[i,cols_index]))]
            bayes_cause.append(final)

    df['bayes_cause']=bayes_cause
    
    del df['index_col']
    
    print ('We have identified your bayesian suspects!')