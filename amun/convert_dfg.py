
import numpy as np
import pandas as pd
from math import sqrt
from collections import Counter
from amun.differental_privacy_module import AggregateType

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
    dfg_time_counter=Counter()
    for key in dfg_time.keys():
        res=0
        if aggregation_type==AggregateType.SUM:
            res=sum(dfg_time[key])
        elif aggregation_type==AggregateType.MIN:
            res=min(dfg_time[key])
        elif aggregation_type==AggregateType.MAX:
            res=max(dfg_time[key])
        elif aggregation_type==AggregateType.AVG:
            res=sum(dfg_time[key])/len(dfg_time[key])
        dfg_time_counter[key]=res

    return dfg_time_counter