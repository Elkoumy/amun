from amun.earth_movers_distance import earth_mover_dist_freq,earth_mover_dist_time
from amun.jaccard_distance.jaccard_distance import soft_jaccard_score
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.traces.log import case_statistics
import pandas as pd
import os

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

    anonymized = xes_importer.apply(anonymized_dir)

    variants_count = case_statistics.get_variant_statistics(original)
    original_variant = [var['variant'].split(',') for var in variants_count]

    variants_count = case_statistics.get_variant_statistics(anonymized)
    anonymized_variant = [var['variant'].split(',') for var in variants_count]

    del original
    del anonymized
    jaccard=soft_jaccard_score(original_variant, anonymized_variant)


    file_name=os.path.split(anonymized_dir)[1]
    dic={"file":file_name, "jaccard": jaccard}
    res=pd.DataFrame.from_dict(dic,orient="index").T
    res.to_csv(os.path.join(comparison_dir,"jaccard",file_name+".comp"),index=False)

if __name__ == "__main__":

    mode = os.sys.argv[1]
    org_path = os.sys.argv[2]
    anonymized_dir = os.sys.argv[3]
    comparison_dir = os.sys.argv[4]

    if mode=="emd":
        compare_emd(org_path,anonymized_dir,comparison_dir)
    else:
        compare_jaccard(org_path,anonymized_dir,comparison_dir)


