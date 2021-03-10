import pandas as pd




data=pd.read_csv("../error_metrics/all_error_precision.csv",
             names=["dataset","precision","delta","iteration","smape_time","smape_variant",
                     "oversampling_ratio","eps","eps_trace"])




#filter the precision in case of multiple precisions
delta_experiment= data.loc[data.precision==0.1]
delta_experiment=delta_experiment.groupby(["dataset","delta"]).mean().reset_index()

delta_experiment=delta_experiment[["dataset","delta","smape_time","oversampling_ratio"]]
delta_experiment.smape_time= delta_experiment.smape_time.round(1)
delta_experiment.oversampling_ratio= delta_experiment.oversampling_ratio.round(1)

t=pd.pivot_table(delta_experiment, values = 'smape_time', index=['delta'], columns = 'dataset').reset_index()

t.to_csv("results_smape_time_delta.csv",index=False, header=True , sep="&")

t=pd.pivot_table(delta_experiment, values = 'oversampling_ratio', index=['delta'], columns = 'dataset').reset_index()

t.to_csv("results_oversampling_delta.csv",index=False, header=True, sep="&")



#filter the delta to be 0.1
precision_experiment= data.loc[data.delta==0.1]
precision_experiment=precision_experiment.groupby(["dataset","precision"]).mean().reset_index()

precision_experiment=precision_experiment[["dataset","precision","smape_time","oversampling_ratio"]]
precision_experiment.smape_time= precision_experiment.smape_time.round(1)
precision_experiment.oversampling_ratio= precision_experiment.oversampling_ratio.round(1)


t=pd.pivot_table(precision_experiment, values = 'smape_time', index=['precision'], columns = 'dataset').reset_index()

t.to_csv("results_smape_time_precision.csv",index=False, header=True, sep="&")

t=pd.pivot_table(precision_experiment, values = 'oversampling_ratio', index=['precision'], columns = 'dataset').reset_index()

t.to_csv("results_oversampling_precision.csv",index=False, header=True, sep="&")






#wall-to-wall
data=pd.read_csv("../execution time/all_time_wall_to_wall.csv",
             names=["dataset","precision","delta","iteration","time"])

data=data.loc[(data.precision==0.1) & (data.delta==0.2),:]
data=data.groupby(["dataset","precision","delta"]).mean().reset_index()
data.time=data.time/60.0 # in minutes
data.time=data.time.round(1)

t=pd.pivot_table(data, values = 'time', index=['delta'], columns = 'dataset').reset_index()

t.to_csv("results_wall_to_wall.csv",index=False, header=True, sep="&")


print("text")