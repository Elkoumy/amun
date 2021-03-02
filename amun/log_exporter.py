from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter

def relative_time_to_XES(data,out_dir):
    """
    This method takes the dataframe as an input and transforms the relative time back to timestamps
    :param data: the anonymized event log (case:concept:name, concept:name, relative_time_anonymized)
    :return: It exports the event log as XES to the specified directory.
    """

    #TODO: get the timestamp of the first event

    #TODO: event_timestamp= prev+relative ===> accumulation per case

    # log = conversion_factory.apply(data[['case:concept:name','concept:name','time:timestamp']])
    # xes_exporter.export_log(log, os.path.join(data_dir,dataset+"_anonymized.xes"))

    return