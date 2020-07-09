"""
This module implements the functionality of reading the input from the user. The following formats are supported:
    * DFG
    * XES
"""
import sys
import os
import pandas as pd
import time
from datetime import datetime
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
from pm4py.objects.log.exporter.csv import factory as csv_exporter
from pm4py.algo.discovery.dfg import factory as dfg_factory

def read_xes(xes_file):
    #read the xes file
    log = xes_import_factory.apply(xes_file)
    data=get_dataframe_from_event_stream(log)
    dfg = dfg_factory.apply(log)

    return dfg
