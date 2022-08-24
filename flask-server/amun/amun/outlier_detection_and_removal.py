

def outlier_detection_and_removal(data):
    #calculate Standard Deviation
    data['std'] = data.groupby(['prev_state', 'concept:name', 'state'])['relative_time'].transform('std')
    # data['quantile_9'] = data.groupby(['prev_state', 'concept:name', 'state'])['relative_time'].transform('quantile',q=0.93)
    # data['quantile_1'] = data.groupby(['prev_state', 'concept:name', 'state'])['relative_time'].transform('quantile',
    #                                                                                                       q=0.1)
    #calculate mean
    data['mean'] = data.groupby(['prev_state', 'concept:name', 'state'])['relative_time'].transform('mean')
    #anomaly cutoff at 3*std
    anomally_cutoff= data['std']*2
    data['upper_bound']=data['mean'] + anomally_cutoff
    # data['upper_bound'] = data['quantile_9']
    data['lower_bound']=data['mean'] - anomally_cutoff
    # data['lower_bound'] = data['quantile_1']

    #filter out outliers
    data['remove']=False
    data.loc[data['relative_time'] > data['upper_bound'], 'remove'] = True
    data.loc[data['relative_time'] < data['lower_bound'], 'remove'] = True
    # data = data.loc[data['remove'] == False]
    cases_to_delete = data.loc[data['remove'] == True]['case:concept:name'].unique()
    data=data[~data['case:concept:name'].isin(cases_to_delete)]
    data=data.reset_index(drop=True)
    return data