from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
import pandas as pd
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter

log = xes_import_factory.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data\BPIC13.xes")
data = get_dataframe_from_event_stream(log)
data['time:timestamp']=pd.to_datetime(data['time:timestamp'],utc=True)
res=data.groupby(['case:concept:name','concept:name'])['time:timestamp'].max()
res=res.reset_index()

log = conversion_factory.apply(res)
xes_exporter.export_log(log, r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\data\BPIC13_t.xes")
