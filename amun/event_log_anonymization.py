import gc
import os
import shutil
import time

from amun.guessing_advantage import estimate_epsilon_risk_vectorized_with_normalization, get_noise_case_variant
from amun.input_module import xes_to_DAFSA
from amun.noise_injection import laplace_noise_injection
from amun.trace_anonymization import anonymize_traces_compacted


def event_log_anonymization(data_dir, dataset, delta, precision, tmp_dir):
    print("Processing the dataset: %s" % (dataset))
    start = time.time()
    data, variants_count = xes_to_DAFSA(data_dir, dataset)
    end = time.time()
    print("reading to DAFSA annotation %s" % (end - start))
    """ Clearing tmp folder"""
    curr_dir = os.getcwd()
    if os.path.isdir(os.path.join( tmp_dir)):
        # delete tmp
        # os.remove(os.path.join(curr_dir, 'tmp'))
        shutil.rmtree(os.path.join( tmp_dir))
    # create tmp
    os.mkdir(os.path.join( tmp_dir))

    # move epsilon estimation before the trace anonymization
    data = data[['case:concept:name', 'concept:name', 'time:timestamp', 'relative_time', 'trace_variant', 'prev_state',
                 'state']]
    start = time.time()
    # optimize epsilon estimation (memory issues)
    # tmp directory for concurrent runs
    data = estimate_epsilon_risk_vectorized_with_normalization(data, delta, precision,tmp_dir)
    end = time.time()
    print("estimate epsilon :  %s" % (end - start))
    gc.collect()
    noise, eps = get_noise_case_variant(delta)
    start = time.time()
    data = anonymize_traces_compacted(data, eps)
    end = time.time()
    print("anonymize traces %s" % (end - start))
    # Laplace Noise Injection
    data = laplace_noise_injection(data)
    return data, variants_count