import pandas as pd



def preprocess_SaCoFa(row):
    """BPIC12_t_0.81_ba_prune_N20_P1309_0.0_0.xes"""
    row['engine'] = 'SaCoFa'
    row['dataset'] = row['file'].split("_")[0]
    row['epsilon']=row['file'].split("_")[2]
    if row['file'].split("_")[2]=='0.81':
        row['delta'] = '0.2'
    elif row['file'].split("_")[2]=='1.238':
        row['delta'] = '0.3'
    elif row['file'].split("_")[2]=='1.7':
        row['delta'] = '0.4'
    row['N']=row['file'].split("_")[5][1:]
    row['P']=row['file'].split("_")[6][1:]
    row['prunning']=row['file'].split("_")[3]+'_'+row['file'].split("_")[4]

    return row

def preprocess_PRIPEL(row):
    """BPIC12_t_epsilon_1.7_k131_N20_delta0.0_anonymizied.xes"""
    row['engine'] = 'pripel'
    row['dataset'] = row['file'].split("_")[0]
    # row['approach'] = "pripel"
    row['epsilon'] = row['file'].split("_")[3]
    if row['file'].split("_")[3] == '0.81':
        row['delta'] = '0.2'
    elif row['file'].split("_")[3] == '1.238':
        row['delta'] = '0.3'
    elif row['file'].split("_")[3] == '1.7':
        row['delta'] = '0.4'

    row['N'] = row['file'].split("_")[5][1:]
    row['P'] = row['file'].split("_")[4][1:]
    return row

def preprocess_jaccard(row):
    if row['file'].find("anonymizied") != -1:
        return preprocess_PRIPEL(row)
    else:
        return preprocess_SaCoFa(row)

def preprocess_emd(row):

    row['engine'] = 'pripel'
    row['dataset'] = row['file'].split("_")[0]
    # row['approach'] = "pripel"
    row['epsilon']=row['file'].split("_")[3]
    row['delta'] =row['file'].split("_")[6][5:]
    row['N'] = row['file'].split("_")[5][1:]
    row['P'] = row['file'].split("_")[4][1:]

    return row

# data=pd.read_csv(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\jaccard.csv")
# data=data.apply(preprocess_jaccard,axis=1)
# data=data.drop('file',axis=1)
# data.to_csv(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\final_result_jaccard_parsed.csv",index=False)

data=pd.read_csv(r"C:\Users\elkoumy\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\emd_all_pripel.csv")
data=data.apply(preprocess_emd,axis=1)
data=data.drop('file',axis=1)
data.to_csv(r"C:\Users\elkoumy\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\emd_all_pripel_parsed.csv",index=False)

print("**")
