import pandas as pd
import numpy as np
import scipy

from scipy.stats import laplace

def estimate_precsion(max, min ):
    diff= 1/max

    precision=(diff - min) / (max - min)


    return precision


def match_vals(row, cumsum, precision):
    cdf=float(cumsum[cumsum.index==row['relative_time']])
    #cdf plus
    val_plus= row['relative_time']+precision
    if val_plus>=1:
        cdf_plus=1.0
    else:
        cdf_plus=float(cumsum[cumsum.index <= val_plus].max())

    #cdf minus
    val_minus = row['relative_time'] - precision
    if val_minus < 0:
        cdf_minus = 0.0
    else:
        cdf_minus = float(cumsum[cumsum.index <= val_minus].max())

    return [cdf, cdf_plus, cdf_minus]


def epsilon_vectorized_internal(data, delta):
    if data.p_k+delta >=1:
        #in case p_k+delta>1, set epsilon = 0.5
        return 0.1

    # r =1 because of normalization
    return (- np.log(data.p_k / (1.0 - data.p_k) * (1.0 / (delta + data.p_k) - 1.0)))


def add_noise(data, max, min):
    noise=0
    sens_time=1
    noise = laplace.rvs(loc=0, scale=sens_time / data['eps'], size=1)[0]
    if noise+data['relative_time_original']<0:
        noise=-data['relative_time_original']

    # noise = abs(noise)
    noise=noise *(max-min)+min
    return noise

def estimate_epsilon_risk_for_start_timestamp(vals, delta):
    #normalization
    min=vals.min()
    max=vals.max()
    precision = estimate_precsion(max, min)

    norm_vals=(vals-min)/(max-min)
    norm_vals=norm_vals.round(5)

    norm_cdf = pd.Series(scipy.stats.norm.cdf(vals))
    norm_vals= norm_vals.sort_values()


    x, counts = np.unique(norm_vals, return_counts=True)
    counts = pd.Series(data=counts, index=x)
    cumsum= counts.cumsum()

    cumsum = cumsum / cumsum.iloc[-1]
    # res = pd.DataFrame({'vales': vals, 'cumsum': cumsum})

    df=norm_vals.to_frame()
    df.columns = ['relative_time']

    temp=df.apply( match_vals,cumsum=cumsum, precision=precision ,axis=1)
    temp = temp.to_frame()
    t2 = pd.DataFrame.from_records(temp[0])
    t2.index = temp.index

    df['cdf']=t2[0]
    df['cdf_plus'] = t2[1]
    df['cdf_minus'] = t2[2]
    df['p_k']=df['cdf_plus']- df['cdf_minus']
    df['eps']= df.apply(epsilon_vectorized_internal, delta=delta, axis=1)
    df['relative_time_original']=df['relative_time'] *(max-min)+min
    df['noise']=df.apply(add_noise, max=max, min= min, axis=1)
    df['time_diff']=df['noise'] +df['relative_time_original']
    return df[['eps']]