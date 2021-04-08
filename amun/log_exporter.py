from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import pandas as pd
import os

def relative_time_to_XES(data,out_dir,file_name):
    """
    This method takes the dataframe as an input and transforms the relative time back to timestamps
    :param data: the anonymized event log (case:concept:name, concept:name, relative_time_anonymized)
    :return: It exports the event log as XES to the specified directory.
    """

    # get the timestamp of the first event
    #(minimum timestamp per case)
    # # WRONG WAY :or (maximum double representation, and convert it back to timestamp)

    # data[['case_start_time','case_start_time_anmzd','original_start']] = data.groupby(['case:concept:name'])['relative_time_original','relative_time_anonymized','time:timestamp'].transform('max')
    min_timestamp=data['time:timestamp'].min()
    data['original_start'] = data.groupby(['case:concept:name'])[ 'time:timestamp'].transform('min')
    data['case_start_time']=0.0
    data['case_start_time_anmzd'] = 0.0


    data.loc[data.original_start == data['time:timestamp'],  'case_start_time_anmzd']=data.loc[data.original_start==data['time:timestamp'],'relative_time_anonymized']
    data.loc[data.original_start == data['time:timestamp'], 'case_start_time'] = data.loc[
        data.original_start == data['time:timestamp'], 'relative_time_original']

    # case start time to the entire case

    data['case_start_time' ] = data.groupby(['case:concept:name'])[
        'case_start_time'].transform('max')

    data[ 'case_start_time_anmzd' ] = data.groupby(['case:concept:name'])[
         'case_start_time_anmzd'].transform('max')


    #  make first relative zero per group
    data.loc[data.original_start==data['time:timestamp'], 'relative_time_original'] = 0
    data.loc[data.original_start==data['time:timestamp'],'relative_time_anonymized']=0

    # return back to timestamp
    data['case_start_time']=data['case_start_time']*pd.Timedelta('1d') +min_timestamp
    #data['case_start_time_anmzd1']=data['case_start_time_anmzd']
    data['case_start_time_anmzd'] = data['case_start_time_anmzd'] * pd.Timedelta('1d') + min_timestamp

    # data['case_start_time']=data['case_start_time']*pd.Timedelta('1d') + pd.Timestamp(
    #     "1970-01-01T00:00:00Z")
    # #data['case_start_time_anmzd1']=data['case_start_time_anmzd']
    # data['case_start_time_anmzd'] = data['case_start_time_anmzd'] * pd.Timedelta('1d') + pd.Timestamp(
    #     "1970-01-01T00:00:00Z")


    #CUMSUM relative time per group

    data[['cumm_relative_time','cumm_relative_time_anymzd']] = data.groupby(['case:concept:name'])['relative_time_original','relative_time_anonymized'].cumsum()
    # stats_df = stats_df.reset_index()

    # relative +time per group
    # we use m seconds as in the input module (should be selected by the user)

    # data['time:timestamp_original'] = data['case_start_time'] + data['cumm_relative_time'].astype(
    #     'timedelta64[ms]')   # in m seconds
    #
    # data['cumm_relative_time_anymzd'] = (data['cumm_relative_time_anymzd'] / 1000.0 / 60.0 / 60.0).astype(
    #     'timedelta64[h]')

    data['time:timestamp_original'] = data['case_start_time'] + data['cumm_relative_time'].astype(
        'timedelta64[s]')  # in seconds
    try:

        # data['cumm_relative_time_anymzd'] = data['cumm_relative_time_anymzd'].astype('timedelta64[s]')
        # data['time:timestamp']=data.apply(lambda e:(e['case_start_time_anmzd']+ e['cumm_relative_time_anymzd'] ) ,axis=1)

        data['time:timestamp'] = data['case_start_time_anmzd'] + data['cumm_relative_time_anymzd']  # in m seconds
    except:

        data['cumm_relative_time_anymzd'] = (data['cumm_relative_time_anymzd'] /24).astype('timedelta64[D]')
        # data['cumm_relative_time_anymzd'] = data['cumm_relative_time_anymzd'].astype('timedelta64[s]')
        # data['time:timestamp']=data.apply(lambda e:(e['case_start_time_anmzd']+ e['cumm_relative_time_anymzd'] ) ,axis=1)
        try:
            data['time:timestamp'] = data['case_start_time_anmzd'] + data['cumm_relative_time_anymzd'].astype('timedelta64[D]')  # in m seconds

        except:
            #BPI19 raises an error here
            data['cumm_relative_time_anymzd'] = (data['cumm_relative_time_anymzd'] //365).astype('timedelta64[Y]')
            data.loc[data['case_start_time_anmzd'].isnull(), 'case_start_time_anmzd'] = pd.Timestamp.max
            data['case_start_time_anmzd']=pd.to_datetime(data['case_start_time_anmzd'])
            # print("data dtypes are: %s"%(data.dtypes))
            # data['time:timestamp'] = data['case_start_time_anmzd'] + data['cumm_relative_time_anymzd']
            data['time:timestamp'] = data['case_start_time_anmzd'] + data['cumm_relative_time_anymzd'].astype(
                'timedelta64[Y]')



    data['case:concept:name']= data['case:concept:name'].astype('str')

    #Fixing the overflow of time
    data.loc[data['time:timestamp'].isnull(),'time:timestamp']=pd.Timestamp.max

    #renaming epsilon columns
    data.rename(columns={'eps': 'epsilon_per_event', 'eps_trace': 'case:epsilon_per_trace'}, inplace=True)
    data=data[['case:concept:name','case:epsilon_per_trace','concept:name','time:timestamp','epsilon_per_event']]
    data['lifecycle:transition']="complete"



    log = conversion_factory.apply(data)
    xes_exporter.export_log(log, os.path.join(out_dir,file_name+".xes"))


    return data





def relative_time_to_XES2(data,out_dir,file_name):

    data['noise_timedelta']=data.apply(noise_unit_converter, axis=1)

    data['case:concept:name'] = data['case:concept:name'].astype('str')

    # cummulative sum per case.
    data['cumm_noise_timedelta'] = data.groupby(['case:concept:name'])['noise_timedelta'].cumsum()

    # convert the float to timedelta
    data['cumm_noise_timedelta'] =pd.to_timedelta(data['cumm_noise_timedelta'], unit='s')
    #debugging the data
    # data.to_csv("data.csv", index=False)
    # data['cumm_noise_timedelta'] = pd.to_timedelta(data['cumm_noise_timedelta'], unit='D')

    data['time:timestamp']= data['time:timestamp']+ data['cumm_noise_timedelta']
    # data.to_csv("data_after_addition.csv", index=False)


    # Fixing the overflow of time
    data.loc[data['time:timestamp'].isnull(), 'time:timestamp'] = pd.Timestamp.max

    # renaming epsilon columns
    data.rename(columns={'eps': 'epsilon_per_event', 'eps_trace': 'case:epsilon_per_trace'}, inplace=True)
    data = data[['case:concept:name', 'case:epsilon_per_trace', 'concept:name', 'time:timestamp', 'epsilon_per_event']]

    data['lifecycle:transition'] = "complete"

    log = conversion_factory.apply(data)
    xes_exporter.export_log(log, os.path.join(out_dir, file_name + ".xes"))


    return data


def noise_unit_converter(row):
    res=0
    if row.prev_state==0: #timestamp noise (in days)
        # convert das to hours
        res=row.noise*24*60*60
        # res=0

    else:
        res=row.noise*1.0
    #
        # res = pd.to_timedelta(row.noise ,unit='s')

    return res