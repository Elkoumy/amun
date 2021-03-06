import pandas as pd




data=pd.read_csv("../error_metrics/all_error.csv",
             names=["dataset","precision","delta","iteration","smape_time","smape_variant",
                     "oversampling_ratio","eps","eps_trace"])

data=data.groupby(["dataset","precision","delta"]).mean().reset_index()

#TODO: filter the precision in case of multiple precisions
data=data[["dataset","delta","smape_time","oversampling_ratio"]]

t=pd.pivot_table(data, values = 'smape_time', index=['delta'], columns = 'dataset').reset_index()

t.to_csv("results.csv",index=False, header=True)


print("text")

