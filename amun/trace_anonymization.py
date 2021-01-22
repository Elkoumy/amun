"""
In this file, we implement the functionality that anonymizes the trace variant based on
the DAFSA automata and using differential privacy
"""
import pandas as pd
import numpy as np
def build_DAFSA_bit_vector(data):
    #calculate the bit vector dataframe from the trace and state anotated event log

    #getting unique dafsa edges and trace variant
    # data=data.groupby(['prev_state', 'concept:name','state','trace_variant']).size().reset_index().rename(columns={0: 'count'})
    # data.drop('count',axis=1, inplace=True)
    bit_vector_df= pd.pivot_table(data=data, values= 'case:concept:name',  index=['prev_state', 'concept:name','state'],columns=['trace_variant'], aggfunc=np.sum, fill_value=0).reset_index()


    return bit_vector_df

