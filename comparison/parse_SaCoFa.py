import pandas as pd



def preprocess_jaccard(row):

    row['engine'] = 'SaCoFa'
    row['dataset'] = row['file'].split("_")[0]
    row['epsilon']=row['file'].split("_")[2]
    row['delta'] =  row['file'].split("_")[7]
    # if row['file'].split("_")[2]=='0.81':
    #     row['delta'] = '0.2'
    # elif row['file'].split("_")[2]=='1.238':
    #     row['delta'] = '0.3'
    # elif row['file'].split("_")[2]=='1.7':
    #     row['delta'] = '0.4'
    row['N']=row['file'].split("_")[5][1:]
    row['P']=row['file'].split("_")[6][1:]
    row['prunning']=row['file'].split("_")[3]+'_'+row['file'].split("_")[4]

    return row


data=pd.read_csv(r"C:\Users\elkoumy\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\emd_all_sacofa.txt")
data=data.apply(preprocess_jaccard,axis=1)
data=data.drop('file',axis=1)
data.to_csv(r"C:\Users\elkoumy\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\emd_all_sacofa_parsed.csv",index=False)
print("**")
