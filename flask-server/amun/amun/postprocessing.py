"""
In this module, we implement the required post anonymization processing tasks
"""

def filtering_postprocessing(data):
    anonymized_case_duration = data.groupby('case:concept:name').relative_time_anonymized.sum()

    upper_limit = anonymized_case_duration.mean() + anonymized_case_duration.std() * 2
    lower_limit = anonymized_case_duration.mean() - anonymized_case_duration.std() * 2

    upper_cases = anonymized_case_duration[anonymized_case_duration > upper_limit].index
    lower_cases = anonymized_case_duration[anonymized_case_duration < lower_limit].index

    data = data.loc[~ data['case:concept:name'].isin(upper_cases)]
    data = data.loc[~ data['case:concept:name'].isin(lower_cases)]

    data=data.reset_index()
    return data