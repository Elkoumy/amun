import pandas as pd




data=pd.read_csv("../error_metrics/all_error.csv",
             names=["dataset","precision","delta","iteration","smape_time","smape_variant",
                     "oversampling_ratio","eps","eps_trace"])

data=data.groupby(["dataset","precision","delta"]).mean().reset_index()

#filter the precision in case of multiple precisions
data=data[["dataset","delta","smape_time","oversampling_ratio"]]

t=pd.pivot_table(data, values = 'smape_time', index=['delta'], columns = 'dataset').reset_index()

t.to_csv("results_time.csv",index=False, header=True)

t=pd.pivot_table(data, values = 'oversampling_ratio', index=['delta'], columns = 'dataset').reset_index()

t.to_csv("results_oversampling.csv",index=False, header=True)

#wall-to-wall
data=pd.read_csv("../execution time/all_time.csv",
             names=["dataset","precision","delta","iteration","time"])

data=data.groupby(["dataset","precision","delta"]).mean().reset_index()

t=pd.pivot_table(data, values = 'time', index=['delta'], columns = 'dataset').reset_index()

t.to_csv("results_wall_to_wall.csv",index=False, header=True)
print("text")

