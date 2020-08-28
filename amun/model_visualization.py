from pm4py.visualization.dfg import factory as dfg_vis_factory

from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.conversion.log.versions.to_dataframe import get_dataframe_from_event_stream
from pm4py.algo.discovery.dfg import factory as dfg_factory

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def view_model(dfg, dir=""):
    #rounding for better plot
    for key in dfg.keys():
        dfg[key]=round(dfg[key])

    parameters = {"format": "svg"}

    gviz = dfg_vis_factory.apply(dfg,  variant="frequency", parameters=parameters)
    # gviz = dfg_vis_factory.apply(dfg, variant="performance", parameters=parameters)# for time
    dfg_vis_factory.save(gviz,dir+".svg")
    drawing = svg2rlg(dir+".svg")
    renderPDF.drawToFile(drawing, dir+".pdf")
    return

# log = xes_import_factory.apply(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Data\Data XES\Sepsis Cases - Event Log.xes")
# data=get_dataframe_from_event_stream(log)
# dfg_freq = dfg_factory.apply(log,variant="frequency")
#
# view_model(dfg_freq,r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures\temp")