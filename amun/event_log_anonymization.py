import gc
import os
import shutil
import time

# from amun.guessing_advantage import estimate_epsilon_risk_vectorized_with_normalization, get_noise_case_variant
# from amun.guessing_advantage_new import estimate_epsilon_risk_vectorized_with_normalization, get_noise_case_variant
from amun.guessing_advantage_partitioned import estimate_epsilon_risk_vectorized_with_normalization, get_noise_case_variant
from amun.input_module import xes_to_DAFSA
from amun.noise_injection import laplace_noise_injection
# from amun.trace_anonymization import anonymize_traces_compacted
from amun.trace_anonymization_over_and_under_sampling import anonymize_traces_compacted
from amun.epsilon_estimation_start_timestamp import estimate_epsilon_risk_for_start_timestamp
from amun.outlier_detection_and_removal import outlier_detection_and_removal
from amun.postprocessing import filtering_postprocessing
from amun.hashing_ids import vectorized_hashing


def event_log_anonymization(data_dir, dataset, delta, precision, tmp_dir):
    print("Processing the dataset: %s" % (dataset))
    print("with Delta: %s , and precision: %s" %(delta,precision))
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
    #TODO: filter out outliers
    # data_filtered=outlier_detection_and_removal(data)
    # data = outlier_detection_and_removal(data)


    data = estimate_epsilon_risk_vectorized_with_normalization(data, delta, precision,tmp_dir)
    data= estimate_epsilon_risk_for_start_timestamp(data, delta)
    end = time.time()
    print("estimate epsilon :  %s" % (end - start))
    gc.collect()
    noise, eps = get_noise_case_variant(delta)
    start = time.time()
    data = anonymize_traces_compacted(data, eps)
    end = time.time()
    print("anonymize traces %s" % (end - start))

    # Mark the start activity of traces ( they start from state s0)

    # Laplace Noise Injection
    data = laplace_noise_injection(data)
    data['eps_trace']=eps

    data=filtering_postprocessing(data)

    # # TODO: estimate epsilon after outlier removal
    # data_filtered = estimate_epsilon_risk_vectorized_with_normalization(data_filtered, delta, precision, tmp_dir)
    # data_filtered = estimate_epsilon_risk_for_start_timestamp(data_filtered, delta)
    # end = time.time()
    # print("estimate epsilon :  %s" % (end - start))
    # gc.collect()
    # noise, eps = get_noise_case_variant(delta)
    # start = time.time()
    # data_filtered = anonymize_traces_compacted(data_filtered, eps)
    # end = time.time()
    # print("anonymize traces %s" % (end - start))
    #
    # # Mark the start activity of traces ( they start from state s0)
    #
    # # Laplace Noise Injection
    # data_filtered = laplace_noise_injection(data_filtered)
    # data_filtered['eps_trace'] = eps

    #Hashing IDs
    data['case:concept:name']=vectorized_hashing(data['case:concept:name'])
    return data, variants_count