
from pm4py.objects.log.adapters.pandas import csv_import_adapter
import pandas as pd
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream

log = xes_import_factory.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\TLKC 10-23-20 15-19-47 Sepsis Cases - Event Log set_1_2_0.5_0.1_seconds.xes")
data = get_dataframe_from_event_stream(log)

data.to_csv(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Sepsis_protected_3.csv")

