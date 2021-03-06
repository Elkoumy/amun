import pandas as pd


def row_transform(rows, datasets):
    res = str(rows.delta[0])+"|"
    vals=[]
    for i in datasets:
        vals.append(rows.loc[rows.dataset==i,"smape_time"])

    res+="|".join(vals)
    return res


data=pd.read_csv("../error_metrics/all_error.csv",
             names=["dataset","precision","delta","iteration","smape_time","smape_variant",
                     "oversampling_ratio","eps","eps_trace"])

data=data.groupby(["dataset","precision","delta"]).mean().reset_index()
#TODO: filter the precision in case of multiple precisions
data=data[["dataset","delta","smape_time","oversampling_ratio"]]

t=pd.pivot_table(data, values = 'smape_time', index=['delta'], columns = 'dataset').reset_index()
# res=data.groupby(['delta']).apply(row_transform,datasets=dataset_names)
t.to_csv("results.csv",index=False, header=True)
print("text")

