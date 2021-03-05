from scipy.stats import laplace

def laplace_noise_injection(data):
    #in this method, we inject the noise to the timestamp attribute.
    # First, we need to count the duplication per event.
    # Then, we divide the epsilon by the count of duplication

    data['counts']= data.groupby(['original_case:concept:name','prev_state','concept:name','state'])['concept:name'].transform('count')

    # data['eps']=data['eps']/data['counts']
    #TODO: divide per counts only for relative time
    data['eps']=data.apply(divid_counts,axis=1)

    #noise according to the original value
    data['noise']= data.apply(add_noise, axis=1)

    #anonymize relative time
    data['relative_time_anonymized']=data['relative_time_original']+data['noise']

    # data.drop(['original_case:concept:name','relative_time_max', 'relative_time_min','p_k','eps','counts','noise'], inplace=True, axis=1)
    data=data[['case:concept:name','time:timestamp','concept:name','relative_time_original','relative_time_anonymized','trace_variant','eps','prev_state','noise']]#,'eps','noise','p_k']]
    return data

def add_noise(data):
    #stop noise for starttime
    if data.prev_state == 0:
        noise=0
    else:
        noise=0
        sens_time=1
        noise = laplace.rvs(loc=0, scale=sens_time / data['eps'], size=1)[0]
        noise=abs(noise)

        noise=noise *(data['relative_time_max']-data['relative_time_min'])+data['relative_time_min']
    return noise

def divid_counts(row):
    if row.prev_state!=0:
        res=row.eps/row.counts
    else:
        res=row.eps
    return res