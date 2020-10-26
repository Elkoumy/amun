
from pm4py.objects.log.adapters.pandas import csv_import_adapter
import pandas as pd
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import pandas as pd
import hashlib
import random
import string
import datetime as dt

def hash_column(column):
    # Get a unique list of the clear text, as a List
    tmplist = list(set(column))
    # Add some random characters before and after the team name.
    # Structured them in a Dictionary
    # Example -- Liverpool -> aaaaaaaLiverpoolbbbbbbbb
    mapping1 = {i : (''.join(random.choice(string.hexdigits) for i in range(12)))+i+(''.join(random.choice(string.hexdigits) for i in range(12)))  for i in tmplist}

    # Create a new column containing clear_text_Nonce
    column_padded = [mapping1[i] for i in column]
    # display(data.head())
    # Hash the clear_text+Nonce string
    column_hashed = [hashlib.sha1(str.encode(str(i))).hexdigest() for i in column_padded]

    return column_hashed


log = xes_import_factory.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\predictive pm\PRT2.xes\Commercial-Original.xes")
# log = xes_import_factory.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\TLKC 10-25-20 11-28-28 Commercial-Original set_2_10_0.5_0.5_seconds.xes")
# log = xes_import_factory.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\predictive pm\poc_processmining.xes\poc_processmining.xes")

data = get_dataframe_from_event_stream(log)
data = data[['lifecycle:transition', 'time:timestamp','ASSIGNEDTEAMNAME','concept:name',  'org:resource', 'case:concept:name','CREATEDT','incAmt']]
# data = data[['lifecycle:transition', 'time:timestamp','concept:name',  'org:resource', 'case:concept:name']]
# data = data[['lifecycle:transition', 'time:timestamp','concept:name',  'org:resource', 'case:concept:name']]
data['concept:name']=hash_column(data['concept:name'])
data['org:resource']=hash_column(data['org:resource'])
data['ASSIGNEDTEAMNAME']=hash_column(data['ASSIGNEDTEAMNAME'])
data['case:concept:name']=hash_column(data['case:concept:name'])

data['time:timestamp']=data['time:timestamp'].dt.tz_localize(None)
data.CREATEDT=pd.to_datetime( data.CREATEDT.astype(str)+'+10:00')
data['CREATEDT']=data['CREATEDT'].dt.tz_localize(None)
data['time:timestamp']=(data['time:timestamp'] - data.loc[0,'CREATEDT'])+dt.datetime(1971, 1, 1, 0, 0)
data['CREATEDT']=(data['CREATEDT'] - data.loc[0,'CREATEDT'])+dt.datetime(1971, 1, 1, 0, 0)

log = conversion_factory.apply(data)
xes_exporter.export_log(log, r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Commercial-Original.xes")

