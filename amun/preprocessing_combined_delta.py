import os
import pandas as pd
result_log_delta=pd.read_csv(os.path.join('../experiment_logs', "combined_result_log_delta.csv"))
import json
from statistics import median
from math import inf
import numpy as np

temp=result_log_delta.epsilon
# t=temp[0].replace("'", "\"").replace("(\"", "\"(").replace("\")", ")\"").replace('", "',',').replace("inf","10000000")
# val=median([x if x !=1000000 else inf for x in list(json.loads(t).values())])


# val=median([x if x !=1000000 else inf for x in list(json.loads(temp[0].replace("'", "\"").replace("(\"", "\"(").replace("\")", ")\"").replace('", "',',').replace("inf","10000000")).values())])

# result_log_delta['median_epsilon']=result_log_delta.epsilon.apply(lambda y : y if y.replace('.','',1).isdigit() else median([x if x !=10000000 else inf for x in list(json.loads(y.replace("'", "\"").replace("(\"", "\"(").replace("\")", ")\"").replace('", "',',').replace("inf","10000000")).values())]))
result=[]
for i in range(0,result_log_delta.shape[0]):
    res=0
    if not result_log_delta.epsilon[i].replace('.','',1).isdigit():
        try:
            res=median([x if x != 10000000 else inf for x in list(
            json.loads(
                result_log_delta.epsilon[i].replace("\\\'",'\"').replace("'", "\"").replace("(\"", "\"(").replace("\")", ")\"").replace('", "', ',').replace("(\'", "\"").replace("\')", "\"(").replace("\', \'", ',').replace("inf","10000000")).values())])
        except:
            res=inf
    else:
        res=float(result_log_delta.epsilon[i])

    result.append(res)

result_log_delta["median_epsilon"]=result
result_log_delta=result_log_delta[["dataset","aggregate_type","delta","median_epsilon","MAPE","SMAPE"]]


result_log_delta=result_log_delta.groupby(["dataset","aggregate_type","delta"],as_index=False).mean()
result_log_delta.to_csv(os.path.join('../experiment_logs', "combined_result_log_delta_subsetted.csv"),index=0)