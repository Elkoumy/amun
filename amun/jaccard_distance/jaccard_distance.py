"""
This module implements the functionality of comparing two event logs based on Jaccard Distance between case variants.

"""

from itertools import product
import os

def similarity(trace1, trace2):
    lcp=os.path.commonpath([trace1, trace2])
    lcp=len(lcp.split(os.sep))

    return lcp

def convert_log_traces_to_paths(l):
    res=[]

    for trace in l:
        res.append(os.path.join(*trace))

    return res


def soft_intersection_list(tokens1, tokens2):
    intersected_list = [((token1, token2), similarity(token1, token2)) for token1, token2 in product(tokens1, tokens2)]
    intersected_list = sorted(intersected_list, key=lambda item: item[1], reverse=True)

    included_list = set()
    used_tokens1 = set()
    used_tokens2 = set()
    for (token1, token2), sim in intersected_list:
        if (not (token1 in used_tokens1)) and (not (token2 in used_tokens2)):
            included_list.add(((token1, token2), sim))
            used_tokens1.add(token1)
            used_tokens2.add(token2)

    return included_list


def soft_jaccard_score(tokens1, tokens2):
    tokens1=convert_log_traces_to_paths(tokens1)
    tokens2 = convert_log_traces_to_paths(tokens2)

    intersection_list = soft_intersection_list(tokens1, tokens2)
    num_intersections = sum([item[1] for item in intersection_list])
    length_of_tokens1= sum([len(trace.split(os.sep)) for trace in tokens1 ])
    length_of_tokens2 = sum([len(trace.split(os.sep)) for trace in tokens2])
    # num_unions = len(tokens1) + len(tokens2) - num_intersections
    num_unions = length_of_tokens1 + length_of_tokens2 - num_intersections
    jaccard_similarity=float(num_intersections)/float(num_unions)
    jaccard_distance=1-jaccard_similarity
    return jaccard_distance




