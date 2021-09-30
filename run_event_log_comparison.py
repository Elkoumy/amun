from amun.earth_movers_distance import earth_mover_dist_freq,earth_mover_dist_time
from amun.jaccard_distance.jaccard_distance import soft_jaccard_score
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.traces.log import case_statistics
import pandas as pd
import os
from datetime import datetime

def compare_emd(original_dir,anonymized_dir,comparison_dir):
    original = xes_importer.apply(original_dir)

    anonymized = xes_importer.apply(anonymized_dir)

    res_freq = earth_mover_dist_freq(original, anonymized)
    res_time = earth_mover_dist_time(original, anonymized)

    file_name=os.path.split(anonymized_dir)[1]
    dic={"file":file_name, "emd_freq": res_freq, "emd_time":res_time}
    res=pd.DataFrame.from_dict(dic,orient="index").T
    res.to_csv(os.path.join(comparison_dir,"emd",file_name+".comp"),index=False)


def compare_jaccard(original_dir,anonymized_dir,comparison_dir):
    original = xes_importer.apply(original_dir)



    variants_count = case_statistics.get_variant_statistics(original)
    original_variant = [var['variant'].split(',') for var in variants_count]
    del original
    del variants_count

    anonymized = xes_importer.apply(anonymized_dir)
    variants_count = case_statistics.get_variant_statistics(anonymized)
    anonymized_variant = [var['variant'].split(',') for var in variants_count]
    del anonymized
    del variants_count


    jaccard,false_positives,false_negatives=soft_jaccard_score(original_variant, anonymized_variant)


    file_name=os.path.split(anonymized_dir)[1]
    dic={"file":file_name, "jaccard": jaccard, "false_positives":false_positives, "false_negatives":false_negatives}
    res=pd.DataFrame.from_dict(dic,orient="index").T
    res.to_csv(os.path.join(comparison_dir,"jaccard",file_name+".comp"),index=False)

if __name__ == "__main__":
    datasets = [ "Sepsis_t", "Unrineweginfectie_t", "BPIC14_t", "Traffic_t", "Hospital_t", "CreditReq_t",
                "BPIC20_t",
                "BPIC12_t", "BPIC13_t", "BPIC15_t", "BPIC17_t", "BPIC18_t", "BPIC19_t"]
    # datasets=["Unrineweginfectie_t"]
    dir_path = os.path.dirname(os.path.realpath(__file__))
    comparison_dir = os.path.join(dir_path, "comparison")
    amun_dir=os.path.join(dir_path,"anonymized_logs","amun")
    pripel_trace_dir = os.path.join(dir_path, "anonymized_logs", "pripel","trace_variant")
    pripel_time_dir = os.path.join(dir_path, "anonymized_logs", "pripel","time")
    SaCoFa_trace_dir = os.path.join(dir_path, "anonymized_logs", "SaCoFa")


    for dataset in datasets:
        org_path=os.path.join(dir_path,"data",dataset+".xes")
        print("Dataset: %s"%(dataset))
        files=list(os.walk(amun_dir))[0][2]
        # for log in files:
        #     print("Current file : %s"%(log))
        #     print(datetime.now())
        #     if log.find(dataset)!=-1:
        #         anonymized_dir=os.path.join(amun_dir,log)
        #         compare_emd(org_path,anonymized_dir,comparison_dir)
        #         compare_jaccard(org_path, anonymized_dir, comparison_dir)

        # files = list(os.walk(pripel_trace_dir))[0][2]
        # for log in files:
        #     if log.find(dataset)!=-1:
        #         anonymized_dir = os.path.join(pripel_trace_dir, log)
        #         compare_jaccard(org_path, anonymized_dir, comparison_dir)
        #
        # files = list(os.walk(pripel_time_dir))[0][2]
        # for log in files:
        #     if log.find(dataset)!=-1:
        #         anonymized_dir = os.path.join(pripel_time_dir, log)
        #         compare_emd(org_path, anonymized_dir, comparison_dir)

        files = list(os.walk(SaCoFa_trace_dir))[0][2]
        for log in files:
            if log.find(dataset) != -1:
                anonymized_dir = os.path.join(SaCoFa_trace_dir, log)
                compare_jaccard(org_path, anonymized_dir, comparison_dir)
                compare_emd(org_path, anonymized_dir, comparison_dir)

