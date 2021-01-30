"""
In this file, we implement the functionality that anonymizes the trace variant based on
the DAFSA automata and using differential privacy
"""
import pandas as pd
import numpy as np
import random as r
import time
import swifter

def build_DAFSA_bit_vector(data):
    #calculate the bit vector dataframe from the trace and state anotated event log

    #getting unique dafsa edges and trace variant
    # data=data.groupby(['prev_state', 'concept:name','state','trace_variant']).size().reset_index().rename(columns={0: 'count'})
    # data.drop('count',axis=1, inplace=True)
    bit_vector_df= pd.pivot_table(data=data, values= 'case:concept:name',  index=['prev_state', 'concept:name','state'],columns=['trace_variant'], aggfunc='count', fill_value=0).reset_index()
    bit_vector_df['added_noise']= [0]* bit_vector_df.shape[0]

    return bit_vector_df

def reversed_normalization(a):
    # where 0 has the largest weight.
    m = max(a)
    a = m - a
    if sum(a)==0:
        #if all the items are zeros
        a=a+1
    else:
        a=a/sum(a)

    return a

def pick_random_edge_trace(bit_vector_df,noise):
    #picks a random edge, then picks a random trace variant of that edge. It adds the noise
    #to the column added noise


    need_noise = bit_vector_df.loc[bit_vector_df.added_noise < noise,:].dropna()


    #performing weighted random sampling

    # perform reverse weight
    edge_sampling_weights=reversed_normalization(need_noise.added_noise)


    picked_edge =need_noise.sample(weights=edge_sampling_weights)

    # pick random trace variant
    traces=picked_edge.drop(['prev_state','concept:name','state','added_noise'],axis=1)
    traces=traces.T.reset_index() #transpose the traces
    traces.columns=['trace_variant','trace_count']
    # traces.trace_count=traces.trace_count.astype(int)
    trace_sampling_weights=traces.trace_count/traces.trace_count.sum()
    picked_trace= traces.sample(weights=trace_sampling_weights)
    picked_trace=picked_trace.trace_variant.iloc[0]

    # update the noise of all edges of that trace
    bit_vector_df.added_noise[bit_vector_df[picked_trace]>0]=bit_vector_df.added_noise[bit_vector_df[picked_trace]>0]+1

    return bit_vector_df, picked_trace


def sampling(row,duplicated_traces):

    row=row.sample(n=duplicated_traces[row.trace_variant])

    return row
def execute_oversampling(data,duplicated_traces):
    #count per trace variant
    duplicated_traces=pd.Series(duplicated_traces).value_counts()
    all_traces=pd.Series(data.trace_variant.unique())
    non_duplicated=(set(list(data.trace_variant.unique())) - set(list(duplicated_traces.index)))
    # non_duplicated=all_traces[~all_traces.isin(list(duplicated_traces.index))]
    # non_duplicated[:]=0
    non_duplicated= pd.Series([0]*len(non_duplicated),index=non_duplicated)

    duplicated_traces=duplicated_traces.append(non_duplicated) #all the sampling ratios should exist



    #sampling from event log based on the count of each trace variant
    duplicated_cases=data[['trace_variant','case:concept:name']].reset_index(drop=True)
    duplicated_cases=duplicated_cases.groupby(['case:concept:name','trace_variant']).size().reset_index()

    # duplicated_cases=duplicated_cases.apply(lambda x:x.sample(n=duplicated_traces[x.trace_variant]), axis=1)#.reset_index(drop=True)
    duplicated_cases = duplicated_cases.swifter.apply(sampling,duplicated_traces=duplicated_traces, axis=1)  # .reset_index(drop=True)
    duplicated_cases=duplicated_cases.drop(['trace_variant'],axis=1)

    #  fix the problem when same case duplicated
    # take out the duplicated case id
    cases_more_than_once = duplicated_cases.groupby(['case:concept:name'])['case:concept:name'].count()

    # all the cases only once
    duplicated_cases=duplicated_cases['case:concept:name'].unique()
    duplicated_cases=pd.DataFrame(duplicated_cases,columns=['case:concept:name'])
    data = duplicate_cases(data, duplicated_cases)

    cases_more_than_once = cases_more_than_once-1 # already duplicated once
    cases_more_than_once=cases_more_than_once[cases_more_than_once>0]

    # loop for the duplicated case ids and every time add only one duplication
    while len(cases_more_than_once>0):
        duplicated_cases=cases_more_than_once.to_frame()
        duplicated_cases.columns = ['cnt']
        duplicated_cases=duplicated_cases.reset_index()
        duplicated_cases.drop(['cnt'],axis=1, inplace=True)
        data = duplicate_cases(data, duplicated_cases)

        cases_more_than_once = cases_more_than_once-1  #  duplicated once
        cases_more_than_once = cases_more_than_once[cases_more_than_once > 0]


    return data


def duplicate_cases(data, duplicated_cases):
    #this function duplicate the cases only once and append them to the event log

    duplicated_cases = duplicated_cases.rename(columns={'case:concept:name': 'duplicated_case_ids'})
    duplicated_cases = duplicated_cases.merge(data, how='left', left_on='duplicated_case_ids',
                                              right_on='case:concept:name').drop('duplicated_case_ids', axis=1)
    #  replace the case id in the sample
    case_ids = duplicated_cases['case:concept:name'].unique()
    randomlist = r.sample(range(data.shape[0]+1, data.shape[0]+1+len(case_ids) * 2), len(case_ids))
    mapping = pd.Series(randomlist, index=case_ids).to_dict()
    duplicated_cases['case:concept:name'].replace(mapping, inplace=True)
    # you can use the duplicated case id to filter them and treat them separately
    # append data + duplicated_cases
    data = data.append(duplicated_cases, ignore_index=True)
    return data


def anonymize_traces(data, noise):
    start=time.time()
    bit_vector_df= build_DAFSA_bit_vector(data)
    end = time.time()
    print("build bit vector: %s" % (end - start))

    duplicated_traces=[] # to keep track of the duplicated trace ids


    start = time.time()
    #  check if there is an edge that needs anonymization
    cnt=bit_vector_df.loc[bit_vector_df.added_noise<noise,"added_noise"].count()

    while cnt>0:
        #  pick a random edge and a random trace
        bit_vector_df, duplicated_trace= pick_random_edge_trace(bit_vector_df,noise)
        duplicated_traces.append(duplicated_trace)

        #TODO: compare with performance of shape
        cnt = bit_vector_df.loc[bit_vector_df.added_noise < noise,"added_noise"].count()



    end = time.time()
    print("finding duplicated traces: %s"%(end-start))

    # execute the oversampling
    start=time.time()
    data=execute_oversampling(data,duplicated_traces)
    end=time.time()
    print("execute oversampoling %s:"%(end-start))
    return data