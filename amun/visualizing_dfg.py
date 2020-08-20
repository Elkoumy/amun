"""
The functionality implemented in this modules takes the DFG as input and export the plot as a figure.

"""

import os
from pm4py.visualization.dfg import factory as dfg_vis_factory

"""
The function draw_DFG takes the dfg as a counter object
"""
def draw_DFG(dfg):
    parameters = {"format": "svg"}
    gviz = dfg_vis_factory.apply(dfg,  variant="performance", parameters=parameters)
    # log = xes_importer.import_log(r"")
    # dfg = dfg_factory.apply(log)
    # gviz = dfg_vis_factory.apply(dfg, log=log, variant="performance", parameters=parameters)
    dfg_vis_factory.save(gviz, "dfg.svg")

