"""
This module implements the functionality of comparing two event logs based on Jaccard Distance between case variants.

"""
import pandas as pd
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


def similarity_apply(row):
    res=similarity(row[0],row[1])
    return res

import swifter

def soft_intersection_list(tokens1, tokens2):
    # start = time.time()
    # intersected_list = [((token1, token2), similarity(token1, token2)) for token1, token2 in product(tokens1, tokens2)]
    #
    # intersected_list = sorted(intersected_list, key=lambda item: item[1], reverse=True)
    #
    # included_list = set()
    # used_tokens1 = set()
    # used_tokens2 = set()
    # for (token1, token2), sim in intersected_list:
    #     if (not (token1 in used_tokens1)) and (not (token2 in used_tokens2)):
    #         included_list.add(((token1, token2), sim))
    #         used_tokens1.add(token1)
    #         used_tokens2.add(token2)
    #
    # end = time.time()
    # diff = end - start
    # print("intersected_list (list): %s (minutes)" % (diff / 60.0))



    start = time.time()
    tokens = pd.DataFrame(product(tokens1, tokens2))

    tokens['similarity'] = tokens.swifter.apply(similarity_apply, axis=1)
    tokens = tokens.groupby([0, 1]).max() #unique values

    tokens.sort_values('similarity', ascending=False, inplace=True)

    included_list = set()
    used_tokens1 = set()
    used_tokens2 = set()
    end1 = time.time()
    diff = end1 - start
    print("intersected_list Dataframe before loop: %s (minutes)" % (diff / 60.0))
    for item in tokens.itertuples():
        token1=item[0][0]
        token2=item[0][1]
        sim=item[1]
        if (not (token1 in used_tokens1)) and (not (token2 in used_tokens2)):
            included_list.add(((token1, token2), sim))
            used_tokens1.add(token1)
            used_tokens2.add(token2)

    end = time.time()
    diff = end - start
    print("intersected_list Dataframe: %s (minutes)" % (diff / 60.0))


    return included_list

import time

def false_positives_and_negatives(original_tokens, anonymized_tokens):
    false_positives=0
    false_negatives=0

    for token in original_tokens:
        if token not in anonymized_tokens:
            false_negatives+=1

    for token in anonymized_tokens:
        if token not in original_tokens:
            false_positives+=1

    return false_positives, false_negatives

def soft_jaccard_score(original_tokens, anonymized_tokens):
    start=time.time()
    original_tokens=convert_log_traces_to_paths(original_tokens)
    end=time.time()
    diff=end-start
    print("first token : %s (minutes)" %(diff/60.0))

    start = time.time()
    anonymized_tokens = convert_log_traces_to_paths(anonymized_tokens)
    end = time.time()
    diff = end - start
    print("second token : %s (minutes)" % (diff / 60.0))

    start = time.time()
    """The longest part is in soft_intersection_list"""
    intersection_list = soft_intersection_list(original_tokens, anonymized_tokens)
    end = time.time()
    diff = end - start
    print("soft_intersection_list : %s (minutes)" % (diff / 60.0))

    false_positives,false_negatives=false_positives_and_negatives(original_tokens, anonymized_tokens)

    start = time.time()
    num_intersections = sum([item[1] for item in intersection_list])
    end = time.time()
    diff = end - start
    print("num_intersections : %s (minutes)" % (diff / 60.0))


    start = time.time()
    length_of_original_tokens= sum([len(trace.split(os.sep)) for trace in original_tokens ])
    length_of_anonymized_tokens = sum([len(trace.split(os.sep)) for trace in anonymized_tokens])
    end = time.time()
    diff = end - start
    print("length of tokens : %s (minutes)" % (diff / 60.0))


    # num_unions = len(original_tokens) + len(anonymized_tokens) - num_intersections
    num_unions = length_of_original_tokens + length_of_anonymized_tokens - num_intersections
    jaccard_similarity=float(num_intersections)/float(num_unions)
    jaccard_distance=1-jaccard_similarity
    return jaccard_distance, false_positives,false_negatives




