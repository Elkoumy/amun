"""
Plotting the laplace distribution for the paper
"""

import numpy as np
import matplotlib.pyplot as plt

loc, scale = 0., 1.
s = np.random.laplace(loc, scale, 1000)



"""#lot laplace"""
x = np.arange(-8., 8., .01)
pdf = np.exp(-abs(x-loc)/scale)/(2.*scale)
plt.plot(x, pdf)
plt.axvline(x=0.,color='k')

#alpha
plt.axvline(x=3,ymax=0.09,color='r', linestyle='--')
plt.axvline(x=-3,ymax=0.09,color='r', linestyle='--')
plt.text(x=3, y=-0.05,s="\u03B1", color='r')
plt.text(x=-3, y=-0.05,s="-\u03B1", color='r')

#beta
plt.axhline(y=0.06,xmin=0.666,xmax=0.95, color="k", linestyle="-.")
plt.text(x=5.7, y=0.07,s="\u03B2", color='k',fontsize=8)

plt.axhline(y=0.06,xmin=0.05,xmax=0.33, color="k", linestyle="-.")
plt.text(x=-5.7, y=0.07,s="\u03B2", color='k',fontsize=8)

#fill intersection
x_intersection=x[ np.logical_and(x<3.0, x>-3.0)]
y_intersection=pdf[np.logical_and(x<3.0, x>-3.0)]
plt.fill(x_intersection,y_intersection, facecolor='blue', alpha=0.5)

plt.savefig(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\paper\amun-workshop-paper\figures\laplace.pdf")
plt.show()

g = (1/(scale * np.sqrt(2 * np.pi)) *
     np.exp(-(x - loc)**2 / (2 * scale**2)))
# plt.plot(x,g)

