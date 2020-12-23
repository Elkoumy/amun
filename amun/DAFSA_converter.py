from dafsa import DAFSA
import networkx as nx
import matplotlib.pyplot as plt


d= DAFSA(["tap", "taps", "top", "tops", "dibs"])

d= DAFSA(["BDE", "CBDE", "BDE", "CBDF", "BDF"])

# print(d)
# d=DAFSA()
# print(d.lookup("tapppp"))
d.write_figure("example.png",working_dir=r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\amun\amun")

# g=d.to_graph()
# nx.draw(g, with_labels=True, font_weight='bold')
# # plt.show()
