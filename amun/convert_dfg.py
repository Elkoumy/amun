
import numpy as np
import pandas as pd
from math import sqrt
from collections import Counter
from amun.differental_privacy_module import AggregateType
import concurrent.futures
import multiprocessing as mp
from itertools import repeat
import amun.multiprocessing_helper_functions


def convert_DFG_to_dataframe(out_dir,freq,time):
    event_count =int(sqrt(len(freq)))
    freq=pd.DataFrame( np.array(freq).reshape(event_count, event_count))
    time=pd.DataFrame(  np.array(time).reshape(event_count, event_count))
    freq.to_csv(r"DFG_log/freq.out",index=0,header=0)
    time.to_csv(r"DFG_log/time.out", index=0, header=0)

    return freq,time

def convert_DFG_to_counter(df,col_names):
    dfg ={}
    df.columns=col_names
    for col in df.columns:
        for ix,val in enumerate(df[col]):
            if int(val) !=0:
                # dfg[(str(col),str(df.index.values[ix]))]=float(val)
                dfg[(str(col), str(df.columns[ix]))] = float(val)
                # print("("+str(col) +","+str(df.index.values[ix])+") ="+str(val))

    return Counter(dfg)

def convert_conter_to_list(counter, col_names):
    res=[]
    c = dict(counter)
    for i in col_names:
        for j in col_names:
            if (i,j) in c.keys():
                res.append(c[(i,j)])
            else:
                res.append(0)
    return res
    return res


def calculate_time_dfg(dfg_time, aggregation_type):
    # dfg_time_counter=Counter()
    # # for key in dfg_time.keys():
    # #     key,res=perform_aggregate_parallel(key,aggregation_type, dfg_time)
    # #     dfg_time_counter[key] = res
    # TASKS_AT_ONCE=amun.multiprocessing_helper_functions.TASKS_AT_ONCE
    # tasks_to_do = dfg_time.values()
    # result = {}
    # id = 0
    # keys = list(dfg_time.keys())
    # for task_set in amun.multiprocessing_helper_functions.chunked_iterable(tasks_to_do, TASKS_AT_ONCE):
    #     with concurrent.futures.ProcessPoolExecutor() as executor:
    #         futures = {
    #             executor.submit(perform_aggregate_parallel,task,aggregation_type)
    #             for task in task_set
    #         }
    #
    #         for fut in concurrent.futures.as_completed(futures):
    #             key=keys[id]
    #             dfg_time_counter[key] = fut.result()
    #
    #             id += 1

    p = mp.Pool(mp.cpu_count())
    print("convert dfg before starmap")
    result = p.starmap(perform_aggregate_parallel, zip(dfg_time.values(), repeat(aggregation_type) )  )

    p.close()
    p.join()
    print("convert dfg aftr join")
    dfg_time_counter = Counter(  dict(zip(list(dfg_time.keys()), result))  )


    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     results=[executor.submit(perform_aggregate_parallel,key,aggregation_type,dfg_time[key]) for key in dfg_time.keys()]
    #
    #     for f in concurrent.futures.as_completed(results):
    #         dfg_time_counter[f.result()[0]]=f.result()[1]

    return dfg_time_counter


def perform_aggregate_parallel(dfg_time_inner,aggregation_type ):
    res = 0
    if aggregation_type == AggregateType.SUM:
        res = sum(dfg_time_inner)
    elif aggregation_type == AggregateType.MIN:
        res = min(dfg_time_inner)
    elif aggregation_type == AggregateType.MAX:
        res = max(dfg_time_inner)
    elif aggregation_type == AggregateType.AVG:
        res = sum(dfg_time_inner) / len(dfg_time_inner)
    return  res




