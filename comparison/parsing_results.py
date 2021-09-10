import pandas as pd


def preprocess_jaccard(row):
    if row['file'].find("e_anonymized")!=-1:
        row['engine']='amun'
        row['dataset']=row['file'].split("_")[2]
        row['approach']=row['file'].split("_")[4]
        row['delta'] = row['file'].split("_")[6][1:]

    else:
        row['engine'] = 'pripel'
        row['dataset'] = row['file'].split("_")[0]
        row['approach'] = "pripel"
        if row['file'].split("_")[3]=='0.81':
            row['delta'] = '0.2'
        elif row['file'].split("_")[3]=='1.238':
            row['delta'] = '0.3'
        elif row['file'].split("_")[3]=='1.7':
            row['delta'] = '0.4'

    return row

def preprocess_emd(row):
    if row['file'].find("e_anonymized")!=-1:
        row['engine']='amun'
        row['dataset']=row['file'].split("_")[2]
        row['approach']=row['file'].split("_")[4]
        row['epsilon']=''
        row['delta'] = row['file'].split("_")[6][1:]

    else:
        row['engine'] = 'pripel'
        row['dataset'] = row['file'].split("_")[0]
        row['approach'] = "pripel"
        row['epsilon']=row['file'].split("_")[3]
        row['delta'] =row['file'].split("_")[6][5:]

    return row

data=pd.read_csv(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\combined_jaccard.txt")

data=data.apply(preprocess_jaccard,axis=1)
data.to_csv(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\parsed_jaccard.csv", index=False)


data=pd.read_csv(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\combined_emd.txt")

data=data.apply(preprocess_emd,axis=1)
data['emd_time']=data['emd_time']/24.0/30.0# in month
data.to_csv(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\comparison\parsed_emd.csv", index=False)

print("**")