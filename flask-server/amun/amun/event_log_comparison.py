from amun.amun.earth_movers_distance import earth_mover_dist_freq,earth_mover_dist_time
from amun.amun.jaccard_distance.jaccard_distance import soft_jaccard_score
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.traces.log import case_statistics


original = xes_importer.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data\Sepsis_t.xes")

amun_sampling = xes_importer.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\anonymized_logs\delta_0.3\precision_0.2\e_anonymized_Sepsis_t_sampling_p0.2_d0.3_i0.xes")
amun_filtering = xes_importer.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\anonymized_logs\delta_0.3\precision_0.2\e_anonymized_Sepsis_t_filtering_p0.2_d0.3_i0.xes")
amun_oversampling = xes_importer.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\anonymized_logs\delta_0.3\precision_0.2\e_anonymized_Sepsis_t_oversampling_p0.2_d0.3_i0.xes")
pripel = xes_importer.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\External Source Code\PPPM Tools\PRIPEL\comparison\Sepsis_t_epsilon_1.9675273440249_k7_N380_anonymizied.xes")
#
#

"""Earth Movers' Distance"""
"DFG frequencies"
res=earth_mover_dist_freq(original,amun_sampling)
print("DFG frequency EMD of Amun sampling= %s"%(res))

res=earth_mover_dist_freq(original,amun_filtering)
print("DFG frequency EMD of Amun filtering= %s"%(res))

res=earth_mover_dist_freq(original,amun_oversampling)
print("DFG frequency EMD of Amun oversampling= %s"%(res))

res=earth_mover_dist_freq(original,pripel)
print("DFG frequency EMD of Pripel= %s"%(res))


"DFG Time"

res=earth_mover_dist_time(original,amun_sampling)
print("DFG time EMD of Amun sampling= %s"%(res))

res=earth_mover_dist_time(original,amun_filtering)
print("DFG time EMD of Amun filtering= %s"%(res))

res=earth_mover_dist_time(original,amun_oversampling)
print("DFG time EMD of Amun oversampling= %s"%(res))


res=earth_mover_dist_time(original,pripel)
print("DFG time EMD of pripel= %s"%(res))



"""Jaccard Distance"""


variants_count = case_statistics.get_variant_statistics(original)
original_variant=[var['variant'] for var in variants_count]

variants_count = case_statistics.get_variant_statistics(original)
original_variant=[var['variant'].split(',') for var in variants_count]

variants_count = case_statistics.get_variant_statistics(amun_sampling)
amun_sampling_variant=[var['variant'].split(',') for var in variants_count]

variants_count = case_statistics.get_variant_statistics(amun_filtering)
amun_filtering_variant=[var['variant'].split(',') for var in variants_count]

variants_count = case_statistics.get_variant_statistics(amun_oversampling)
amun_oversampling_variant=[var['variant'].split(',') for var in variants_count]

variants_count = case_statistics.get_variant_statistics(pripel)
pripel_variant=[var['variant'].split(',') for var in variants_count]


print("Jaccard distance of Amun sampling =%s"%(soft_jaccard_score(original_variant,amun_sampling_variant)))
print("Jaccard distance of Amun filtering =%s"%(soft_jaccard_score(original_variant,amun_filtering_variant)))
print("Jaccard distance of Amun oversampling =%s"%(soft_jaccard_score(original_variant,amun_oversampling_variant)))

print("Jaccard distance of PRIPEL %s"%(soft_jaccard_score(original_variant,pripel_variant)))