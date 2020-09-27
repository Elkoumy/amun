"""
This module includes the functions to plot the distribution of the delta with different distance values.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

from amun.guessing_advantage import AggregateType


def plot_results(result_log_delta,result_log_alpha,delta_logger_freq, delta_logger_time, dir=r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'):
    # editing the name of datasets
    #datasets = ["Sepsis Cases - Event Log", "CreditRequirement", "Road_Traffic_Fine_Management_Process"]
    result_log_delta.dataset.replace("Sepsis Cases - Event Log","Sepsis" ,inplace=True)
    result_log_delta.dataset.replace("CreditRequirement", "Credit Req.", inplace=True)
    result_log_delta.dataset.replace("Road_Traffic_Fine_Management_Process", "Road Traffic", inplace=True)

    result_log_alpha.dataset.replace("Sepsis Cases - Event Log", "Sepsis", inplace=True)
    result_log_alpha.dataset.replace("CreditRequirement", "Credit Req.", inplace=True)
    result_log_alpha.dataset.replace("Road_Traffic_Fine_Management_Process", "Road Traffic", inplace=True)

    delta_logger_freq.dataset.replace("Sepsis Cases - Event Log", "Sepsis", inplace=True)
    delta_logger_freq.dataset.replace("CreditRequirement", "Credit Req.", inplace=True)
    delta_logger_freq.dataset.replace("Road_Traffic_Fine_Management_Process", "Road Traffic", inplace=True)

    delta_logger_time.dataset.replace("Sepsis Cases - Event Log", "Sepsis", inplace=True)
    delta_logger_time.dataset.replace("CreditRequirement", "Credit Req.", inplace=True)
    delta_logger_time.dataset.replace("Road_Traffic_Fine_Management_Process", "Road Traffic", inplace=True)

    plot_delta_distributions_time(delta_logger_time,dir)
    plot_delta_distributions_freq(delta_logger_freq,dir)
    plot_input_delta(result_log_delta,dir)
    plot_input_EMD(result_log_alpha,dir)


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

def plot_delta_distributions_time(delta_logger,dir):

    g = sns.FacetGrid(delta_logger, row="dataset", col="aggregate_type", margin_titles=True)
    g.map(sns.boxplot, "emd", "delta" )
    # g.fig.suptitle(' \u03B5  Distribution for  Time DFG  (EMD input)')
    plt.subplots_adjust(top=0.7)
    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    axes[2].set_title("Aggregate: Min")
    axes[3].set_title("Aggregate: Max")
    # axes[0].set_ylabel("Max \u03B4")  # delta
    for ax in axes:
        ax.set_xlabel("MAPE")  # alpha
        ax.set_ylabel("\u03B4")
    plt.show()
    g.savefig(os.path.join(dir, 'Input_emd_time_dfg_delta_distribution.pdf'))


    for data in delta_logger.dataset.unique():
        subset= delta_logger[delta_logger.dataset == data]
        g = sns.FacetGrid(subset,  col="aggregate_type", margin_titles=True)
        g.map(sns.boxplot, "emd", "delta")
        # g.fig.suptitle(' \u03B5  Distribution for  Time DFG  (EMD input)')
        plt.subplots_adjust(top=0.7)
        axes = g.axes.flatten()
        axes[0].set_title("Aggregate: Average")
        axes[1].set_title("Aggregate: Sum")
        axes[2].set_title("Aggregate: Min")
        axes[3].set_title("Aggregate: Max")
        # axes[0].set_ylabel("Max \u03B4")  # delta
        for ax in axes:
            ax.set_xlabel("MAPE")  # alpha
            ax.set_ylabel("\u03B4")
        plt.show()
        g.savefig(os.path.join(dir, 'Input_emd_time_dfg_delta_distribution_'+data+'.pdf'))

def plot_delta_distributions_freq(delta_logger,dir):

    g = sns.FacetGrid(delta_logger, row="dataset", margin_titles=True)
    g.map(sns.boxplot, "emd", "delta" )
    # g.fig.suptitle(' \u03B5  Distribution for  Freq DFG  (EMD input)')
    plt.subplots_adjust(top=0.7)
    axes = g.axes.flatten()
    # axes[0].set_title("Aggregate: Average")
    # axes[1].set_title("Aggregate: Sum")
    axes[0].set_ylabel(" \u03B4")  # delta
    for ax in axes:
        ax.set_xlabel("MAPE")  # alpha
        ax.set_ylabel("\u03B4") #delta
    plt.show()
    g.savefig(os.path.join(dir, 'Input_emd_freq_dfg_delta_distribution.pdf'))


    for data in delta_logger.dataset.unique():
        subset= delta_logger[delta_logger.dataset == data]
        g = sns.FacetGrid(subset, row="dataset", margin_titles=True)
        g.map(sns.boxplot, "emd", "delta")
        # g.fig.suptitle(' \u03B5  Distribution for  Freq DFG  (EMD input)')
        plt.subplots_adjust(top=0.7)
        axes = g.axes.flatten()
        # axes[0].set_title("Aggregate: Average")
        # axes[1].set_title("Aggregate: Sum")
        axes[0].set_ylabel(" \u03B4")  # delta
        for ax in axes:
            ax.set_xlabel("MAPE")  # alpha
            ax.set_ylabel("\u03B4")  # delta
        plt.show()
        g.savefig(os.path.join(dir, 'Input_emd_freq_dfg_delta_distribution_'+data+'.pdf'))

def plot_input_delta(result_log_delta,dir):

    #epsilon for freq
    # g = sns.FacetGrid(result_log_delta, col="aggregate_type", margin_titles=True)
    # g.map(sns.lineplot, "delta", "epsilon_freq","dataset")
    g=sns.lineplot("delta", "epsilon_freq","dataset", data=result_log_delta)
    # g.set_title('\u03B5 Distribution with  Frequency DFG (\u03B4 input)')  # can also get the figure from plt.gcf())
    # plt.subplots_adjust(top=0.2)

    # g.fig.suptitle('\u03B5 Distribution with  Frequency DFG (\u03B4 input)')  # can also get the figure from plt.gcf()
    # g.set_titles('Epsilon Distribution with  Frequency DFG')
    g.set_ylabel("\u03B5") #epsilon
    g.set_xlabel("\u03B4") #delta

    # axes = g.axes.flatten()
    # axes[0].set_title("Aggregate: Average")
    # axes[1].set_title("Aggregate: Sum")
    # axes[0].set_ylabel("\u03B5") #epsilon
    # for ax in axes:
    #     ax.set_xlabel("\u03B4") #delta

    plt.legend()
    plt.savefig(os.path.join(dir, 'Input_delta_freq_dfg_epsilon_distribution.pdf'))
    plt.show()


    # epsilon for time
    g = sns.FacetGrid(result_log_delta, col="aggregate_type", margin_titles=True)
    g.map(sns.lineplot, "delta", "epsilon_time","dataset")
    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    axes[2].set_title("Aggregate: Min")
    axes[3].set_title("Aggregate: Max")
    plt.subplots_adjust(top=0.2)
    # g.fig.suptitle('\u03B5 Distribution with Time DFG  (\u03B4 input)')
    for ax in axes:
        ax.set_xlabel("\u03B4")  # delta
    axes[0].set_ylabel("\u03B5") #epsilon
    # plt.ylabel('Epsilon')
    plt.legend()
    plt.show()
    g.savefig(os.path.join(dir, 'Input_delta_time_dfg_epsilon_distribution.pdf'))

    #emd for freq
    # temp=result_log_delta[result_log_delta.aggregate_type=='AggregateType.SUM']
    g=sns.lineplot("delta", "MAPE_freq","dataset",data=result_log_delta)
    # g = sns.lineplot("delta", "emd_freq", "dataset", data=result_log_delta)
    # g.set_title('EMD Distribution with Frequency DFG  (\u03B4 input)')
    g.set_xlabel("\u03B4")  # delta
    g.set_ylabel("MAPE")
    plt.legend()
    plt.savefig(os.path.join(dir, 'Input_delta_freq_dfg_EMD_distribution.pdf'))
    plt.show()


    # emd for time
    g = sns.FacetGrid(result_log_delta,  col="aggregate_type", margin_titles=True)
    g.map(sns.lineplot, "delta", "SMAPE_time","dataset")
    # temp = result_log_delta[result_log_delta.aggregate_type == 'AggregateType.SUM']
    # g = sns.lineplot("delta", "emd_time", "dataset", data=temp)
    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    axes[2].set_title("Aggregate: Min")
    axes[3].set_title("Aggregate: Max")
    plt.subplots_adjust(top=0.2)
    # g.fig.suptitle('EMD Distribution with Time DFG  (\u03B4 input)')
    for ax in axes:
        ax.set_xlabel("\u03B4")  # delta
    axes[0].set_ylabel("SMAPE")
    # plt.ylabel('EMD')
    plt.legend()
    plt.show()
    g.savefig(os.path.join(dir, 'Input_delta_time_dfg_EMD_distribution.pdf'))

def plot_input_EMD(result_log_alpha,dir):
    #epsilon for freq

    g=sns.lineplot( 'alpha', "epsilon_freq","dataset", data=result_log_alpha)
    plt.subplots_adjust(top=1.0)

    # g.set_title('Min \u03B5 for   Frequency DFG  (EMD input)')
    g.set_ylabel("Min \u03B5")#epsilon
    g.set_xlabel("MAPE")  # alpha


    plt.legend()
    plt.savefig(os.path.join(dir, 'Input_EMD_freq_dfg_epsilon_distribution.pdf'))
    plt.show()

    # g.savefig(os.path.join(dir, 'Input_EMD_freq_dfg_epsilon_distribution.pdf'))

    #epsilon for time
    g = sns.FacetGrid(result_log_alpha,  col="aggregate_type", margin_titles=True)
    g.map(sns.lineplot, "alpha", "epsilon_time","dataset")
    plt.subplots_adjust(top=0.2)
    # g.fig.suptitle('Min \u03B5  for  Time DFG  (EMD input)')
    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    axes[2].set_title("Aggregate: Min")
    axes[3].set_title("Aggregate: Max")
    axes[0].set_ylabel("Min \u03B5")#epsilon
    for ax in axes:
        ax.set_xlabel("MAPE")  # alpha
    plt.legend()
    plt.show()
    g.savefig(os.path.join(dir, 'Input_EMD_time_dfg_epsilon_distribution.pdf'))

    #Delta for freq
    # g = sns.FacetGrid(result_log_alpha, col="aggregate_type", margin_titles=True)
    # g.map(sns.lineplot, "alpha", "delta_freq_median","dataset")
    g=sns.lineplot("alpha", "delta_freq_median","dataset", data=result_log_alpha)
    # plt.subplots_adjust(top=0.2)
    # g.fig.suptitle('Median \u03B5 for  Frequency DFG  (EMD input)')
    # g.set_title('Median \u03B5 for  Frequency DFG  (EMD input)')
    g.set_ylabel("Median \u03B4")#delta
    g.set_xlabel("MAPE")  # alpha
    # axes = g.axes.flatten()
    # axes[0].set_title("Aggregate: Average")
    # axes[1].set_title("Aggregate: Sum")
    # axes[0].set_ylabel("Median \u03B4")#delta
    # for ax in axes:
    #     ax.set_xlabel("Percenage EMD")  # alpha
    plt.legend()
    plt.savefig(os.path.join(dir, 'Input_EMD_freq_dfg_delta_median_distribution.pdf'))
    plt.show()


    #Delta for time
    g = sns.FacetGrid(result_log_alpha, col="aggregate_type", margin_titles=True)
    g.map(sns.lineplot, "alpha", "delta_time_median","dataset")
    plt.subplots_adjust(top=0.2)
    # g.fig.suptitle('Median \u03B5 for Time DFG  (EMD input)')
    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    axes[2].set_title("Aggregate: Min")
    axes[3].set_title("Aggregate: Max")
    axes[0].set_ylabel("Median \u03B4")  # delta
    for ax in axes:
        ax.set_xlabel("MAPE")  # alpha
    plt.legend()
    plt.show()
    g.savefig(os.path.join(dir, 'Input_EMD_time_dfg_delta_median_distribution.pdf'))

    #Delta for freq

    g=sns.lineplot( "alpha", "delta_freq_max","dataset", data=result_log_alpha)
    # plt.subplots_adjust(top=0.2)

    g.set_ylabel("Max \u03B4")  # delta
    g.set_xlabel("MAPE")  # alpha

    plt.legend()
    plt.savefig(os.path.join(dir, 'Input_EMD_freq_dfg_delta_max_distribution.pdf'))
    plt.show()


    #Delta for time
    g = sns.FacetGrid(result_log_alpha, col="aggregate_type", margin_titles=True)
    g.map(sns.lineplot, "alpha", "delta_time_max","dataset")
    plt.subplots_adjust(top=0.7)
    # g.fig.suptitle('Max \u03B5 for Time DFG  (EMD input)')
    axes = g.axes.flatten()
    axes[0].set_title("Aggregate: Average")
    axes[1].set_title("Aggregate: Sum")
    axes[2].set_title("Aggregate: Min")
    axes[3].set_title("Aggregate: Max")

    axes[0].set_ylabel("Max \u03B4")  # delta
    for ax in axes:
        ax.set_xlabel("MAPE")  # alpha
    plt.legend()
    plt.show()
    g.savefig(os.path.join(dir, 'Input_EMD_time_dfg_delta_max_distribution.pdf'))

result_log_alpha=pd.read_csv(os.path.join('../experiment_logs', "result_log_alpha.csv"))
result_log_delta= pd.read_csv(os.path.join('../experiment_logs', "result_log_delta.csv"))
delta_logger_time=pd.read_csv(os.path.join('../experiment_logs', "delta_logger_time.csv"))
delta_logger_freq=pd.read_csv(os.path.join('../experiment_logs', "delta_logger_freq.csv"))
plot_results(result_log_delta,result_log_alpha,delta_logger_freq,delta_logger_time)

