from amun.earth_movers_distance import earth_mover_dist_freq,earth_mover_dist_time
from amun.jaccard_distance.jaccard_distance import soft_jaccard_score
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.statistics.traces.log import case_statistics


original = xes_importer.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data\Sepsis_t.xes")

amun = xes_importer.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\anonymized_logs\delta_0.2\precision_0.2\e_anonymized_Sepsis_t_0.2_0.2_0.xes")
pripel = xes_importer.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\External Source Code\PPPM Tools\PRIPEL\data\Sepsis_t_epsilon_1.0_k3_N30_anonymizied.xes")
#
#

"""Earth Movers' Distance"""
"DFG frequencies"
res=earth_mover_dist_freq(original,amun)
print("DFG frequency EMD of Amun= %s"%(res))

res=earth_mover_dist_freq(original,pripel)
print("DFG frequency EMD of Pripel= %s"%(res))


"DFG Time"

res=earth_mover_dist_time(original,amun)
print("DFG time EMD of Amun= %s"%(res))

res=earth_mover_dist_time(original,pripel)
print("DFG time EMD of pripel= %s"%(res))



"""Jaccard Distance"""


variants_count = case_statistics.get_variant_statistics(original)
original_variant=[var['variant'] for var in variants_count]

variants_count = case_statistics.get_variant_statistics(original)
original_variant=[var['variant'].split(',') for var in variants_count]

variants_count = case_statistics.get_variant_statistics(amun)
amun_variant=[var['variant'].split(',') for var in variants_count]

variants_count = case_statistics.get_variant_statistics(pripel)
pripel_variant=[var['variant'].split(',') for var in variants_count]


print("Jaccard distance of Amun %s"%(soft_jaccard_score(original_variant,amun_variant)))

print("Jaccard distance of PRIPEL %s"%(soft_jaccard_score(original_variant,pripel_variant)))