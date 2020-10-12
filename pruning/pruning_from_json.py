import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
# pruning_dir="pruning"
files=["Unrineweginfectie_time","Hospital_freq","CreditReq_freq","BPIC20_time","CreditReq_time","BPIC15_freq","BPIC13_time","BPIC13_freq","BPIC17_time","BPIC15_time","BPIC17_freq","BPIC12_freq","BPIC12_time","BPIC18_time","BPIC20_freq","Sepsis_freq","CCC19_freq","BPIC14_time","BPIC14_freq","BPIC19_freq","BPIC19_time","Traffic_freq","Sepsis_time","CCC19_time","Traffic_time","BPIC18_freq","Unrineweginfectie_freq","Hospital_time"]
output=""
for file in files:
    nodes={}
    edges=[]
    # echo the dataset
    parameters=file.split('_')
    output += "elif dataset=='" + parameters[0] + "' and type== '"+parameters[1]+"' :\n"
    with open(os.path.join(dir_path,file+".json")) as json_file:
        data = json.load(json_file)
        for item in data:


            if list(item['data'].keys())[0]=='shape': # this is a node
                nodes[item['data']['id']]= item['data']['oriname']

            elif list(item['data'].keys())[0]=='strength': # this is an edge
                if nodes[item['data']['target']] !='[]' and nodes[item['data']['source']] !='|>':
                    edges.append((nodes[item['data']['source']],nodes[item['data']['target']]))
    output +="\tresult="+str(edges)+"\n"


print(output)
