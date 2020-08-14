"""
This module includes the functions to plot the distribution of the delta with different distance values.
"""

import matplotlib.pyplot as plt
import seaborn as sns

def plot_delta_distribution(delta_per_distance):

    axis= []
    data=[]

    for distance in delta_per_distance.keys():
        data.append(list(delta_per_distance[distance].values()))
        axis.append(distance)

    # Creating plot
    plt.boxplot(data)
    plt.xticks(list(range(1,len(data)+1)),labels=axis)
    plt.title('Delta Distribution with EMD ')
    plt.xlabel('EMD')
    plt.ylabel('Delta')
    # show plot
    plt.show()


def plot_delta_distributions(delta_logger):

    g = sns.FacetGrid(delta_logger, row="dataset", col="aggregate_type", margin_titles=True)
    g.map(sns.boxplot, "emd", "delta" )
    plt.show()
