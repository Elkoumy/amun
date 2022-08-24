"""
Plotting the laplace distribution for the paper
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp
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
plt.text(x=3, y=-0.05,s="\u03B1", color='r',fontsize=12)
plt.text(x=-3, y=-0.05,s="-\u03B1", color='r',fontsize=12)

#beta
# plt.axhline(y=0.06,xmin=0.666,xmax=0.95, color="k", linestyle="-.")
# plt.text(x=5.7, y=0.07,s="\u03B2", color='k',fontsize=8)
#
# plt.axhline(y=0.06,xmin=0.05,xmax=0.33, color="k", linestyle="-.")
# plt.text(x=-5.7, y=0.07,s="\u03B2", color='k',fontsize=8)

plt.axhline(y=0.06,xmin=0.33,xmax=0.666, color="k", linestyle="--")
plt.text(x=-1.2, y=0.07,s="1 - \u03B2", color='k',fontsize=12)

#fill intersection
x_intersection=x[ np.logical_and(x<3.0, x>-3.0)]
y_intersection=pdf[np.logical_and(x<3.0, x>-3.0)]
plt.fill(x_intersection,y_intersection, facecolor='blue', alpha=0.5)

#hide ticks
plt.xticks([])
plt.yticks([])

plt.xlabel("x",size=12)
plt.ylabel("y",size=12)
plt.savefig(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\paper\amun-workshop-paper\figures\laplace.pdf")
plt.show()


"""Plot guessing advantage"""
#normal distribution
loc, scale = 0., 2.4
g = (1/(scale * np.sqrt(2 * np.pi)) *
     np.exp(-(x - loc)**2 / (2 * scale**2)))
plt.plot(x,g)
plt.axvline(x=0.,color='k')

#R_ij
plt.axvline(x=8,ymax=0.05,color='r', linestyle='--')
plt.text(x=7.7, y=-0.02,s="$r_{ij}$", color='k',rotation=-45,fontsize=12)

#t_k
plt.axvline(x=4,ymax=0.25,color='k', linestyle='--')
plt.text(x=3.7, y=-0.03,s="$t^k_{ij}-p.r_{ij}$", color='k',rotation=-45,fontsize=12)

plt.axvline(x=5,ymax=0.15,color='k', linestyle='--')
plt.text(x=4.7, y=-0.01,s="$t^k_{ij}$", color='k',rotation=-45,fontsize=12)

plt.axvline(x=6,ymax=0.085,color='k', linestyle='--')
plt.text(x=5.7, y=-0.03,s="$t^k_{ij}+p.r_{ij}$", color='k',rotation=-45,fontsize=12)


#fill intersection
x_intersection=x[ np.logical_and(x<8.0, x>-8.0)]
y_intersection=g[np.logical_and(x<8.0, x>-8.0)]
plt.fill(x_intersection,y_intersection, facecolor='orange', alpha=0.5)

x_intersection=x[ np.logical_and(x<6.0, x>4.0)]
y_intersection=g[np.logical_and(x<6.0, x>4.0)]
plt.fill_between(x_intersection,(0-y_intersection)*-1, facecolor="blue", alpha=2)
#hide ticks
plt.xticks([])
plt.yticks([])

plt.xlabel("x",size=12)
plt.ylabel("PDF",size=12)
plt.savefig(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\paper\amun-workshop-paper\figures\guessing_advantage.pdf")
plt.show()



import scipy.stats as ss

x = np.linspace(-5, 5, 5000)
mu = 0
sigma = 2

# y_pdf = ss.norm.pdf(x, mu, sigma) # the normal pdf
y_cdf = ss.norm.cdf(x, mu, sigma) # the normal cdf

# plt.plot(x, y_pdf, label='pdf')
plt.plot(x, y_cdf, label='cdf')
plt.xticks([])
plt.yticks([])



#t_k
plt.axvline(x=2,ymax=0.8,color='k', linestyle='--')
plt.text(x=1.8, y=-0.2,s="$t^k_{ij}-p.r_{ij}$  ", color='k',rotation=-45,fontsize=12)

plt.axhline(y=0.83,xmax=0.68,color='k', linestyle='--')

plt.axvline(x=3,ymax=0.9,color='k', linestyle='--')
plt.text(x=2.8, y=-0.1,s="$t^k_{ij}$  ", color='k',rotation=-45,fontsize=12)

# plt.axhline(y=0.93,xmax=0.77,color='k', linestyle='--')

plt.axvline(x=4,ymax=0.93,color='k', linestyle='--')
plt.text(x=3.8, y=-0.2,s="$t^k_{ij}+p. r_{ij}$  ", color='k',rotation=-45,fontsize=12)

plt.axhline(y=0.977,xmax=0.87,color='k', linestyle='--')

plt.axvline(x=-5,ymin=0.8,ymax=0.93,color='k', linestyle='--')
plt.text(x=-4.9, y=0.9,s="$P^k_{ij}$", color='k',rotation=-90,fontsize=12)
plt.xlabel("x",size=12)
plt.ylabel("CDF",size=12)

plt.savefig(r"C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\paper\amun-workshop-paper\figures\CDF.pdf")
plt.show()



