"""
In this file, we implement the GUI functionality required from the project. The project performs the following functionalities:
    * Reading the event logs as XES or reading DFGs.
    * Take either delta as input or accuracy as input.
    * Report the epsilon, delta and accuracy.
    * Plot the DFG for both cases.
    * export the DFG after applying the differential privacy.
"""

import tkinter as tk
from tkinter import filedialog, Text
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk

from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.visualization.dfg import factory as dfg_vis_factory
from pm4py.algo.discovery.dfg import factory as dfg_factory

root = tk.Tk( ) # the object that contains everything
# we add a canvas to put components on it and control the size
# canvas = tk.Canvas(root, height= 700, width= 700, bg="#263D42")
root.config( bg="white")
root.title("Amun")
ico = tk.PhotoImage(file=r"GUI_images/amun_logo.png")
root.tk.call('wm', 'iconphoto', root._w, ico)

file=[]



def add_xes():
    #opening a browse file dialog
    filename= filedialog.askopenfilename(initialdir=r"DFG_log", title="Select File",
                                         filetypes=(("XES","*.xes"), ("all files", "*.*")))
    file.append(filename)

    if list_box.get(0)=="No Files Selected. Please add a file to be processed!":
        list_box.delete(0)
    list_box.insert(len(file), filename)



def run_dfg():
    #call the functions here

    ''' apply differential privacy here  '''

    """ view the dfg diagram on the canvas"""
    # drawing = svg2rlg("dfg.svg")
    drawing = svg2rlg("dfg_out.svg")
    renderPM.drawToFile(drawing, "dfg.png", fmt="PNG")
    img = Image.open('dfg.png')

    # win = tk.Toplevel()
    # win.wm_title("Window")
    # win.tk.call('wm', 'iconphoto', root._w, ico)
    # l = tk.Label(win, text="")
    # img = tk.PhotoImage(file="dfg.png")
    # l.config(image=img)
    # l.image = img
    # l.grid(row=0, column=0)

    return

def view_model():
    # file=list_box.get(list_box.curselection())
    #
    # log = xes_import_factory.apply(file)
    # parameters = {"format": "svg"}
    # dfg = dfg_factory.apply(log)
    # gviz = dfg_vis_factory.apply(dfg,log,  variant="performance", parameters=parameters)
    # dfg_vis_factory.save(gviz, "party_model.svg")
    #
    # drawing = svg2rlg("party_model.svg")
    # renderPM.drawToFile(drawing, "party_model.png", fmt="PNG")
    #
    # win = tk.Toplevel()
    # win.wm_title("Viewing Model of this Party Only")
    # win.tk.call('wm', 'iconphoto', root._w, ico)
    # l = tk.Label(win, text="")
    # img = tk.PhotoImage(file="party_model.png")
    # l.config(image=img)
    # l.image = img
    # l.grid(row=0, column=0)
    return



#to add a frame inside the canvas
#frame= tk.Frame(root, bg="white")
#frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)


#the Amun title
title= tk.Label(root, text="Amun", font='Helvetica 14 bold', bg="white")
title.pack()

'''open file Button'''
openFile = tk.Button(root, text = 'Click Me !',    command=add_xes,  bg="white")
img = tk.PhotoImage(file=r"GUI_images/add_file.png",height = 40, width = 150)
openFile.config(image=img)
openFile.pack(padx=5, pady=10, side=tk.TOP)
# openFile.image=img

'''View Model Button'''
viewModel = tk.Button(root, text = 'Click Me !',    command=view_model,  bg="white",height = 40, width = 170)
img = tk.PhotoImage(file=r"GUI_images/view_model.png")
viewModel.config(image=img)
viewModel.pack()
viewModel.image=img



### list view for listing the files
list_label = tk.Label(root, text="Imported Files", font='Helvetica 10 bold', bg="white")
list_box = tk.Listbox(root,width=40, height=10 )
list_box.insert(1,"No Files Selected. Please add a file to be processed!")
list_label.pack()
list_box.pack()




#### build dfg button
# build_dfg = tk.Button(root, text="Build DFG", command = run_dfg)
# img = tk.PhotoImage(file=r"GUI_images/calculate_dfg.png")
# # build_dfg.grid(row=0)
# build_dfg.config(image=img)
# build_dfg.pack()
# build_dfg.image=img



### University of Tartu Logo
tartu = tk.Label(root, text="", bg="white")
img = tk.PhotoImage(file=r"GUI_images/tartu.png")
img = img.subsample(2)
tartu.config(image=img)
tartu.image = img
tartu.pack(padx=5, pady=10, side=tk.LEFT)


### Cyber Logo
cyber = tk.Label(root, text="", bg="white")
img = tk.PhotoImage(file=r"GUI_images/cybernetica.png")
img = img.subsample(2)
cyber.config(image=img)
cyber.image = img
cyber.pack(padx=5, pady=30, side=tk.LEFT)
#start the application GUI
root.mainloop()