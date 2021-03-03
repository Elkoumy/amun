"""
In this file, we implement the functionality that anonymizes the trace variant based on
the DAFSA automata and using differential privacy
"""
import pandas as pd
import numpy as np
import random as r
import time
#import swifter

def build_DAFSA_bit_vector(data):
    #calculate the bit vector dataframe from the trace and state anotated event log

    #getting unique dafsa edges and trace variant
    # data=data.groupby(['prev_state', 'concept:name','state','trace_variant']).size().reset_index().rename(columns={0: 'count'})
    # data.drop('count',axis=1, inplace=True)


    bit_vector_df=data.groupby(['prev_state', 'concept:name','state','trace_variant'])['case:concept:name'].count().unstack().reset_index()
    # bit_vector_noise = data.groupby(['prev_state', 'concept:name', 'state'])[
    #     'case:concept:name'].count()  # .unstack().reset_index()

    #indexed by transition
    # bit_vector_df=data.groupby(['prev_state', 'concept:name','state'])['trace_variant'].unique().apply(list)

    #indexed by trace_variant
    # bit_vector_trace_variant = data.groupby(['trace_variant'])[['prev_state', 'concept:name', 'state']].apply(list)

    # del(data)
    # bit_vector_df[:]=True
    # bit_vector_df=bit_vector_df.reset_index()
    # bit_vector_df = bit_vector_df.to_frame()
    #  fix memory error

    # bit_vector_df=bit_vector_df.unstack()
    # print('1')
    # bit_vector_df=bit_vector_df.reset_index()
    # print('2')
    # bit_vector_df.fillna(False,inplace=True)
    # print('3')
    # res=data.groupby(['prev_state', 'concept:name','state','trace_variant'])['case:concept:name'].transform('any')#.unstack().reset_index()
    # bit_vector_df= pd.pivot_table(data=data, values= 'case:concept:name',  index=['prev_state', 'concept:name','state'],columns=['trace_variant'], aggfunc='count', fill_value=0).reset_index()
    bit_vector_df['added_noise']= [0]* bit_vector_df.shape[0]

    # bit_vector_df.drop('case:concept:name', axis=1, inplace=True)

    return bit_vector_df



def build_DAFSA_bit_vector_compacted(data):
    #calculate the bit vector dataframe from the trace and state anotated event log


    #indexed by transition
    #not unique as we perform weighted sampling
    bit_vector_df=data.groupby(['prev_state', 'concept:name','state'])['trace_variant'].apply(list)

    #indexed by trace_variant
    bit_vector_trace_variant = data.groupby(['trace_variant'])[['prev_state', 'concept:name', 'state']].apply(lambda x: x.values.tolist())

    # del(data)
    # bit_vector_df[:]=True
    # bit_vector_df=bit_vector_df.reset_index()
    bit_vector_df = bit_vector_df.to_frame()
    # fix memory error


    bit_vector_df['added_noise']= [0]* bit_vector_df.shape[0]

    # bit_vector_df.drop('case:concept:name', axis=1, inplace=True)
    # print("*********** yay ***************&&")
    return bit_vector_df ,bit_vector_trace_variant


def reversed_normalization(a):
    # where 0 has the largest weight.
    m = max(a)
    a = a
    a = m - a

    #if all edges need the same noise
    # if need_noise.added_noise.max()==need_noise.added_noise.min():
    #     #make the weight for the one that is common between most traces
    #     s=need_noise.iloc[:,3:-1].sum(axis=1)
    #     a=s/s.sum()

    if sum(a)==0:
        #if all the items are zeros
        a=(a+1)/a.shape[0]
    else:

        a=a/sum(a)

    return a

def pick_random_edge_trace(bit_vector_df,noise):
    #picks a random edge, then picks a random trace variant of that edge. It adds the noise
    #to the column added noise


    # need_noise = bit_vector_df.loc[bit_vector_df.added_noise < noise, :].dropna()
    added_noise=bit_vector_df.added_noise
    need_noise=added_noise[added_noise<noise]


    #performing weighted random sampling

    # perform reverse weight
    # make the weight of the edge that is part of a lot of trace variants to be larger

    edge_sampling_weights=reversed_normalization(need_noise)


    picked_edge_index =need_noise.sample(weights=edge_sampling_weights).index[0]
    # pick random trace variant
    # traces=picked_edge.drop(['prev_state','concept:name','state','added_noise'],axis=1)
    traces=bit_vector_df.iloc[picked_edge_index,3:-1]
    traces=traces.T.reset_index() #transpose the traces
    traces.columns=['trace_variant','trace_count']
    # traces.trace_count=traces.trace_count.astype(int)

    """*** Compare here"""
    trace_sampling_weights=traces.trace_count/traces.trace_count.sum()
    #picking traces as the noise size
    # picked_trace= traces.sample(n=noise, weights=trace_sampling_weights, replace=True)


    picked_trace = traces.sample(n=noise, weights=trace_sampling_weights, replace=True)


    # picked_trace=picked_trace.trace_variant.iloc[0]
    # picked_trace = picked_trace.trace_variant

    # update the noise of all edges of that trace
    # bit_vector_df.added_noise[bit_vector_df[picked_trace]>0]=bit_vector_df.added_noise[bit_vector_df[picked_trace]>0]+1

    for trace_index in range(0,noise):
        trace= picked_trace.trace_variant.iloc[trace_index]
        bit_vector_df.added_noise[bit_vector_df[trace] > 0] = bit_vector_df.added_noise[
                                                                         bit_vector_df[trace] > 0] + 1

    return bit_vector_df, picked_trace



def pick_random_edge_trace_compacted(bit_vector_df, bit_vector_trace_variant,noise):
    #picks a random edge, then picks a random trace variant of that edge. It adds the noise
    #to the column added noise

    func_start=time.time()

    # need_noise = bit_vector_df.loc[bit_vector_df.added_noise < noise, :].dropna()
    added_noise=bit_vector_df.added_noise
    need_noise=added_noise[added_noise<noise]


    #performing weighted random sampling

    # perform reverse weight
    # make the weight of the edge that is part of a lot of trace variants to be larger
    start=time.time()
    edge_sampling_weights=reversed_normalization(need_noise)
    end=time.time()
    # print("reversed_normalization : %s" %(end-start))

    picked_edge_index =need_noise.sample(weights=edge_sampling_weights).index[0]
    # pick random trace variant
    # traces=picked_edge.drop(['prev_state','concept:name','state','added_noise'],axis=1)
    start=time.time()
    traces=pd.Series(bit_vector_df.loc[picked_edge_index,'trace_variant'])
    traces=traces.value_counts().to_frame().reset_index()

    traces.columns=['trace_variant','trace_count']
    end = time.time()
    # print("counting : %s" % (end - start))

    # traces.trace_count=traces.trace_count.astype(int)

    """*** Compare here"""
    trace_sampling_weights=traces.trace_count/traces.trace_count.sum()
    # trace_sampling_weights = traces/ traces.sum()
    #picking traces as the noise size
    # picked_trace= traces.sample(n=noise, weights=trace_sampling_weights, replace=True)


    picked_trace = traces.sample(n=noise, weights=trace_sampling_weights, replace=True)


    # picked_trace=picked_trace.trace_variant.iloc[0]
    # picked_trace = picked_trace.trace_variant

    # update the noise of all edges of that trace
    # bit_vector_df.added_noise[bit_vector_df[picked_trace]>0]=bit_vector_df.added_noise[bit_vector_df[picked_trace]>0]+1

    # for trace_index in range(0,noise):
    #     trace= picked_trace.trace_variant.iloc[trace_index]
    #     bit_vector_df.added_noise[bit_vector_df[trace] > 0] = bit_vector_df.added_noise[
    #                                                                      bit_vector_df[trace] > 0] + 1
    start=time.time()
    for trace_index in picked_trace.trace_variant:
        trace_edges= bit_vector_trace_variant.iloc[trace_index]
        bit_vector_df.added_noise.loc[trace_edges] = bit_vector_df.added_noise.loc[trace_edges] + 1
    end = time.time()
    # print("trace index loop : %s" % (end - start))

    func_end=time.time()
    # print("pick_random_edge_trace_compacted time : %s"%(func_end-func_start))
    return bit_vector_df, picked_trace

def sampling(row,duplicated_traces):
    trace_variant= row.trace_variant.iloc[0]
    sample_size=duplicated_traces[trace_variant]
    row=row.sample(n=sample_size, replace=True)

    return row
def execute_oversampling(data,duplicated_traces):
    #duplicating the original case id to know which case is original and which is a copy.
    # that is needed to estimate to scale the epsilon of the duplicated cases.
    data['original_case:concept:name']=data['case:concept:name']

    #count per trace variant
    duplicated_traces=pd.Series(duplicated_traces).value_counts()
    all_traces=pd.Series(data.trace_variant.unique())
    non_duplicated=(set(list(data.trace_variant.unique())) - set(list(duplicated_traces.index)))
    # non_duplicated=all_traces[~all_traces.isin(list(duplicated_traces.index))]
    # non_duplicated[:]=0
    non_duplicated= pd.Series([0]*len(non_duplicated),index=non_duplicated)

    duplicated_traces=duplicated_traces.append(non_duplicated) #all the sampling ratios should exist

    #  duplicated traces

    #sampling from event log based on the count of each trace variant
    duplicated_cases=data[['trace_variant','case:concept:name']].reset_index(drop=True)
    duplicated_cases=duplicated_cases.groupby(['case:concept:name','trace_variant']).size().reset_index()
    start=time.time()
    # duplicated_cases=duplicated_cases.apply(lambda x:x.sample(n=duplicated_traces[x.trace_variant]), axis=1)#.reset_index(drop=True)
    # duplicated_cases = duplicated_cases.swifter.apply(sampling,duplicated_traces=duplicated_traces, axis=1)  # .reset_index(drop=True)
    duplicated_cases = duplicated_cases.groupby(['trace_variant']).apply(sampling, duplicated_traces=duplicated_traces)  # .reset_index(drop=True)
    duplicated_cases=duplicated_cases.drop(['trace_variant'],axis=1)

    #  fix the problem when same case duplicated
    # take out the duplicated case id
    cases_more_than_once = duplicated_cases.groupby(['case:concept:name'])['case:concept:name'].count()
    end=time.time()
    print("sampling time: %s" %(end-start))

    # all the cases only once
    duplicated_cases=duplicated_cases['case:concept:name'].unique()
    duplicated_cases=pd.DataFrame(duplicated_cases,columns=['case:concept:name'])
    data = duplicate_cases(data, duplicated_cases)

    cases_more_than_once = cases_more_than_once-1 # already duplicated once
    cases_more_than_once=cases_more_than_once[cases_more_than_once>0]

    # loop for the duplicated case ids and every time add only one duplication
    start=time.time()
    while len(cases_more_than_once>0):
        duplicated_cases=cases_more_than_once.to_frame()
        duplicated_cases.columns = ['cnt']
        duplicated_cases=duplicated_cases.reset_index()
        duplicated_cases.drop(['cnt'],axis=1, inplace=True)
        data = duplicate_cases(data, duplicated_cases)

        cases_more_than_once = cases_more_than_once-1  #  duplicated once
        cases_more_than_once = cases_more_than_once[cases_more_than_once > 0]

    end = time.time()
    print("loop of duplication: %s" % (end - start))
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
    # start=time.time()
    bit_vector_df= build_DAFSA_bit_vector(data)
    # end = time.time()
    # print("build bit vector: %s" % (end - start))

    duplicated_traces=[] # to keep track of the duplicated trace ids


    # start = time.time()
    #  check if there is an edge that needs anonymization
    cnt=bit_vector_df.loc[bit_vector_df.added_noise<noise,"added_noise"].shape[0]
    iter=0
    while cnt>0:

        #  pick a random edge and a random trace

        bit_vector_df, duplicated_trace= pick_random_edge_trace(bit_vector_df,noise)
        # duplicated_traces.append(duplicated_trace)
        duplicated_traces.extend(duplicated_trace)

        cnt = bit_vector_df.loc[bit_vector_df.added_noise < noise,"added_noise"].shape[0]
        iter+=1





    # print("******** end of loop ****")
    # print("iter=:%s"%(iter))

    print("no of iteration = %s"%(iter))
    # execute the oversampling
    # start=time.time()
    data=execute_oversampling(data,duplicated_traces)
    # end=time.time()
    # print("execute oversampoling %s:"%(end-start))
    return data


def anonymize_traces_compacted(data, noise):
    # start=time.time()
    bit_vector_df,bit_vector_trace_variant= build_DAFSA_bit_vector_compacted(data)
    # end = time.time()
    # print("build bit vector: %s" % (end - start))

    duplicated_traces=[] # to keep track of the duplicated trace ids


    # start = time.time()
    #  check if there is an edge that needs anonymization
    cnt=bit_vector_df.loc[bit_vector_df.added_noise<noise,"added_noise"].shape[0]

    iter=0
    while cnt>0:
        loop_start=time.time()
        #  pick a random edge and a random trace
        start=time.time()
        bit_vector_df, duplicated_trace= pick_random_edge_trace_compacted(bit_vector_df,bit_vector_trace_variant,noise)
        end=time.time()
        # print("pick_random_edge_trace_compacted: %s"%(end-start))
        # duplicated_traces.append(duplicated_trace)
        duplicated_traces.extend(duplicated_trace.trace_variant)

        start = time.time()
        cnt = bit_vector_df.loc[bit_vector_df.added_noise < noise,"added_noise"].shape[0]
        end = time.time()
        # print("counting time: %s" % (end - start))
        iter+=1
        loop_end=time.time()
        # print("loop time: %s" %(loop_end-loop_start))




    print("******** end of loop ****")
    print("iter=:%s"%(iter))


    # print("no of iteration = %s"%(iter))
    # execute the oversampling
    # start=time.time()
    data=execute_oversampling(data,duplicated_traces)
    # end=time.time()
    # print("execute oversampoling %s:"%(end-start))
    return data