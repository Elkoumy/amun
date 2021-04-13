

def outlier_detection_and_removal(data):
    #calculate Standard Deviation
    data['std'] = data.groupby(['prev_state', 'concept:name', 'state'])['relative_time'].transform('std')
    #calculate mean
    data['mean'] = data.groupby(['prev_state', 'concept:name', 'state'])['relative_time'].transform('mean')
    #anomaly cutoff at 3*std
    anomally_cutoff= data['std']*2
    data['upper_bound']=data['mean'] + anomally_cutoff
    data['lower_bound']=data['mean'] - anomally_cutoff

    #filter out outliers
    data['remove']=False
    data.loc[data['relative_time'] > data['upper_bound'], 'remove'] = True
    data.loc[data['relative_time'] < data['lower_bound'], 'remove'] = True
    data = data.loc[data['remove'] == False]
    return data