"""
This module includes the functions to plot the distribution of the delta with different distance values.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


def plot_results(result_log_delta,result_log_alpha,delta_logger_freq, delta_logger_time):
    plot_delta_distributions_time(delta_logger_time)
    plot_delta_distributions_freq(delta_logger_freq)
    plot_input_delta(result_log_delta)
    # plot_input_EMD(result_log_alpha)

def plot_delta_distribution_time(delta_per_distance):

    axis= []
    data=[]

    for distance in delta_per_distance.keys():
        data.append(list(delta_per_distance[distance].values()))
        axis.append(distance)

    # Creating plot
    plt.boxplot(data)
    plt.xticks(list(range(1,len(data)+1)),labels=axis)
    plt.title('Delta Distribution with EMD (time) ')
    plt.xlabel('EMD')
    plt.ylabel('Delta')
    # show plot
    plt.show()



def plot_delta_distribution_freq(delta_per_distance):

    axis= []
    data=[]
    # data=list(delta_per_distance.values())
    for distance in delta_per_distance.keys():
        data.append(list(delta_per_distance[distance].values()))
        axis.append(distance)

    # Creating plot
    plt.boxplot(data)
    plt.xticks(list(range(1,len(data)+1)),labels=axis)
    plt.title('Delta Distribution with EMD (freq) ')
    plt.xlabel('EMD')
    plt.ylabel('Delta')
    # show plot
    plt.show()

def plot_delta_distributions_time(delta_logger):

    g = sns.FacetGrid(delta_logger, row="dataset", col="aggregate_type", margin_titles=True)
    g.map(sns.boxplot, "emd", "\u03B4" )
    plt.show()
    g.savefig(os.path.join('../experiment_figures', 'Input_emd_time_dfg_delta_distribution.pdf'))


def plot_delta_distributions_freq(delta_logger):

    g = sns.FacetGrid(delta_logger, row="dataset", col="aggregate_type", margin_titles=True)
    g.map(sns.boxplot, "emd", "\u03B4" )
    plt.show()
    g.savefig(os.path.join('../experiment_figures', 'Input_emd_freq_dfg_delta_distribution.pdf'))

def plot_input_delta(result_log_delta):

    #epsilon for freq
    g = sns.FacetGrid(result_log_delta, col="aggregate_type", margin_titles=True)
    g.map(sns.lineplot, "delta", "epsilon_freq","dataset")
    plt.subplots_adjust(top=0.2)
    g.fig.suptitle('\u03B5 Distribution with  Frequency DFG (\u03B4 input)')  # can also get the figure from plt.gcf()
    # g.set_titles('Epsilon Distribution with  Frequency DFG')

    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    axes[0].set_ylabel("\u03B5") #epsilon
    for ax in axes:
        ax.set_xlabel("\u03B4") #delta

    plt.legend()
    plt.show()
    g.savefig(os.path.join('../experiment_figures', 'Input_delta_freq_dfg_epsilon_distribution.pdf'))

    # epsilon for time
    g = sns.FacetGrid(result_log_delta, col="aggregate_type", margin_titles=True)
    g.map(sns.lineplot, "delta", "epsilon_time","dataset")
    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    plt.subplots_adjust(top=0.2)
    g.fig.suptitle('\u03B5 Distribution with Time DFG  (\u03B4 input)')
    for ax in axes:
        ax.set_xlabel("\u03B4")  # delta
    axes[0].set_ylabel("\u03B5") #epsilon
    # plt.ylabel('Epsilon')
    plt.legend()
    plt.show()
    g.savefig(os.path.join('../experiment_figures', 'Input_delta_time_dfg_epsilon_distribution.pdf'))

    #emd for freq
    g = sns.FacetGrid(result_log_delta,  col="aggregate_type", margin_titles=True)
    g.map(sns.lineplot, "delta", "emd_freq","dataset")
    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    plt.subplots_adjust(top=0.2)
    g.fig.suptitle('EMD Distribution with Frequency DFG  (\u03B4 input)')
    for ax in axes:
        ax.set_xlabel("\u03B4")  # delta
    axes[0].set_ylabel("Percentage EMD")
    # plt.ylabel('EMD')
    plt.legend()
    plt.show()
    g.savefig(os.path.join('../experiment_figures', 'Input_delta_freq_dfg_EMD_distribution.pdf'))

    # emd for freq
    g = sns.FacetGrid(result_log_delta,  col="aggregate_type", margin_titles=True)
    g.map(sns.lineplot, "delta", "emd_time","dataset")
    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    plt.subplots_adjust(top=0.2)
    g.fig.suptitle('EMD Distribution with Time DFG  (\u03B4 input)')
    for ax in axes:
        ax.set_xlabel("\u03B4")  # delta
    axes[0].set_ylabel("Percentage EMD")
    # plt.ylabel('EMD')
    plt.legend()
    plt.show()
    g.savefig(os.path.join('../experiment_figures', 'Input_delta_time_dfg_EMD_distribution.pdf'))

def plot_input_EMD(result_log_alpha):
    #epsilon for freq
    g = sns.FacetGrid(result_log_alpha, row="dataset", col="aggregate_type", margin_titles=True)
    g.map(sns.barplot, 'alpha', "epsilon_freq")
    plt.subplots_adjust(top=0.2)
    g.fig.suptitle('\u03B5 Distribution with  Frequency DFG  (EMD input)')
    plt.xlabel('\u03B1')#alpha
    plt.ylabel('\u03B5')#epsilon
    plt.show()
    g.savefig(os.path.join('../experiment_figures', 'Input_EMD_freq_dfg_epsilon_distribution.pdf'))

    #epsilon for time
    g = sns.FacetGrid(result_log_alpha, row="dataset", col="aggregate_type", margin_titles=True)
    g.map(sns.barplot, "alpha", "epsilon_time")
    plt.subplots_adjust(top=0.2)
    g.fig.suptitle('\u03B5 Distribution with  Frequency DFG  (EMD input)')
    plt.xlabel('\u03B1')
    plt.ylabel('\u03B5')
    plt.show()
    g.savefig(os.path.join('../experiment_figures', 'Input_EMD_time_dfg_epsilon_distribution.pdf'))

    #Delta for freq
    g = sns.FacetGrid(result_log_alpha, row="dataset", col="aggregate_type", margin_titles=True)
    g.map(sns.barplot, "alpha", "delta_freq")
    plt.subplots_adjust(top=0.2)
    g.fig.suptitle('\u03B5 Distribution with  Frequency DFG  (EMD input)')
    plt.xlabel('\u03B1')
    plt.ylabel('\u03B5')
    plt.show()
    g.savefig(os.path.join('../experiment_figures', 'Input_EMD_freq_dfg_delta_distribution.pdf'))



result_log_alpha=pd.read_csv(os.path.join('../experiment_logs', "result_log_alpha.csv"))
result_log_delta= pd.read_csv(os.path.join('../experiment_logs', "result_log_delta.csv"))
# delta_logger=pd.read_csv("delta_logger.csv")
#
#
plot_input_delta(result_log_delta)
# plot_input_EMD(result_log_alpha)
# plot_delta_distributions_time(delta_logger)