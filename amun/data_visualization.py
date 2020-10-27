"""
This module includes the functions to plot the distribution of the delta with different distance values.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

from amun.guessing_advantage import AggregateType


def plot_results(result_log_delta,result_log_alpha,delta_logger_freq, delta_logger_time,execution_time_log, dir=r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'):
    # editing the name of datasets
    #datasets = ["Sepsis Cases - Event Log", "CreditRequirement", "Road_Traffic_Fine_Management_Process"]
    # result_log_delta.dataset.replace("Sepsis Cases - Event Log","Sepsis" ,inplace=True)

    plot_delta_distributions_time(delta_logger_time,dir)
    plot_delta_distributions_freq(delta_logger_freq,dir)
    plot_input_delta(result_log_delta,dir)
    plot_input_alpha(result_log_alpha,dir)
    bubble_heatmap(result_log_delta, result_log_alpha)
    plot_execution_time(execution_time_log, dir)


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
    # axes[0].set_title("Aggregate: Average")
    # axes[1].set_title("Aggregate: Sum")
    # axes[2].set_title("Aggregate: Min")
    # axes[3].set_title("Aggregate: Max")
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
        # axes[0].set_title("Aggregate: Average")
        # axes[1].set_title("Aggregate: Sum")
        # axes[2].set_title("Aggregate: Min")
        # axes[3].set_title("Aggregate: Max")
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
        fmt = '{:0.3f}'
        yticklabels = []
        for item in ax.get_yticklabels():
            # item.set_text(fmt.format(float(item.get_text())))
            item.set_text(fmt.format(float(item.get_text().replace('−','-'))))
            yticklabels += [item]

        ax.set_yticklabels(yticklabels)
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


    """"************************************************"""
    #epsilon
    g = sns.FacetGrid(result_log_delta, col="dataset",col_wrap=4, margin_titles=True)
    g.map(sns.lineplot, "delta", "median_epsilon", "aggregate_type")
    plt.subplots_adjust(top=0.2)
    # g.fig.suptitle('Min \u03B5  for  Time DFG  (EMD input)')
    axes = g.axes.flatten()
    # axes[0].set_title("Aggregate: Average")
    # axes[1].set_title("Aggregate: Sum")
    # axes[2].set_title("Aggregate: Min")
    # axes[3].set_title("Aggregate: Max")
    axes[0].set_xlabel("\u03B4") #delta
    for ax in axes:
        ax.set_ylabel("Log(Min \u03B5)")#epsilon
        ax.set(yscale="log")
    plt.legend()
    plt.show()
    g.savefig(os.path.join(dir, 'Input_delta_freq_dfg_epsilon_distribution.pdf'))

    #Delta
    g = sns.FacetGrid(result_log_delta, col="dataset",col_wrap=4, margin_titles=True)
    g.map(sns.lineplot, "delta", "SMAPE", "aggregate_type")
    plt.subplots_adjust(top=0.2)


    # g.fig.suptitle('Median \u03B5 for Time DFG  (EMD input)')
    axes = g.axes.flatten()
    # axes[0].set_title("Aggregate: Average")
    # axes[1].set_title("Aggregate: Sum")
    # axes[2].set_title("Aggregate: Min")
    # axes[3].set_title("Aggregate: Max")
    axes[0].set_xlabel("\u03B4") #delta
    for ax in axes:
        ax.set_ylabel("SMAPE")  # alpha
    plt.legend()
    plt.show()
    g.savefig(os.path.join(dir, 'Input_EMD_time_dfg_delta_median_distribution.pdf'))



def plot_input_alpha(result_log_alpha,dir):

    #epsilon
    g = sns.FacetGrid(result_log_alpha, col="dataset",col_wrap=4, margin_titles=True)
    g.map(sns.lineplot, "alpha", "median_epsilon", "aggregate_type")
    plt.subplots_adjust(top=0.2)
    # g.fig.suptitle('Min \u03B5  for  Time DFG  (EMD input)')
    axes = g.axes.flatten()
    # axes[0].set_title("Aggregate: Average")
    # axes[1].set_title("Aggregate: Sum")
    # axes[2].set_title("Aggregate: Min")
    # axes[3].set_title("Aggregate: Max")
    axes[0].set_xlabel("MAPE")
    for ax in axes:
        ax.set_ylabel("Log(Min \u03B5)")#epsilon
        ax.set(yscale="log")
    plt.legend()
    plt.show()
    g.savefig(os.path.join(dir, 'Input_EMD_time_dfg_epsilon_distribution.pdf'))

    #Delta
    g = sns.FacetGrid(result_log_alpha, col="dataset",col_wrap=4, margin_titles=True)
    g.map(sns.lineplot, "alpha", "delta_median", "aggregate_type")
    plt.subplots_adjust(top=0.2)


    # g.fig.suptitle('Median \u03B5 for Time DFG  (EMD input)')
    axes = g.axes.flatten()
    # axes[0].set_title("Aggregate: Average")
    # axes[1].set_title("Aggregate: Sum")
    # axes[2].set_title("Aggregate: Min")
    # axes[3].set_title("Aggregate: Max")
    axes[0].set_xlabel("MAPE")  # delta
    for ax in axes:
        ax.set_ylabel("Median \u03B4")  # alpha
    plt.legend()
    plt.show()
    g.savefig(os.path.join(dir, 'Input_EMD_time_dfg_delta_median_distribution.pdf'))



def bubble_heatmap(log_delta, log_alpha):
    log_delta.delta=log_delta.delta.astype(str)
    log_alpha.alpha = log_alpha.alpha.astype(str)


    log_delta.dataset.replace("Unrineweginfectie", "Unrin..", inplace=True)
    log_delta_filtered=log_delta.where(log_delta.aggregate_type=="AggregateType.AVG")
    log_delta_filtered.dropna(inplace=True)
    sns.scatterplot(
        data=log_delta_filtered, x="dataset", y="delta", size="MAPE_freq", hue="epsilon_freq",
        sizes=(20, 400) )
    plt.legend( title='Legend', bbox_to_anchor=(1.01, 1), loc='upper left',labelspacing=1.1)
    plt.xticks(rotation=-90)
    plt.ylabel("\u03B4") # delta
    plt.xlabel("Event Log")
    fig=plt.gcf()
    plt.show()

    loc = r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'
    fig.savefig(os.path.join(loc, 'bubble_heatmap_delta_freq.pdf'))


    g = sns.FacetGrid(log_delta, col="aggregate_type", margin_titles=True)
    g.map(sns.scatterplot, data=log_delta, x="dataset", y="delta", size="SMAPE_time", hue="epsilon_time",
        sizes=(10, 100) )
    plt.subplots_adjust(top=0.7)
    g.set_xticklabels(rotation=-90)
    # g.fig.suptitle('Max \u03B5 for Time DFG  (EMD input)')
    axes = g.axes.flatten()
    axes[0].set_title("Average")
    axes[1].set_title("Sum")
    axes[2].set_title("Min")
    axes[3].set_title("Max")

    axes[0].set_ylabel("\u03B4")
    for ax in axes:
        ax.set_xlabel("Event Log")
        # ax.set_xticks(rotation=-90)
    plt.legend(title='Legend', bbox_to_anchor=(1.01, 1), loc='upper left', labelspacing=0.6)
    # plt.xticks(rotation=-90)
    plt.show()
    loc=r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'
    g.savefig(os.path.join(loc, 'bubble_heatmap_delta_time.pdf'))


    """ For Alpha"""
    log_alpha.dataset.replace("Unrineweginfectie", "Unrin..", inplace=True)
    log_alpha_filtered = log_alpha.where(log_alpha.aggregate_type == "AggregateType.AVG")
    log_alpha_filtered.dropna(inplace=True)
    sns.scatterplot(
        data=log_alpha_filtered, x="dataset", y="alpha", size="delta_freq_median", hue="epsilon_freq",
        sizes=(20, 400))
    plt.legend(title='Legend', bbox_to_anchor=(1.01, 1), loc='upper left', labelspacing=1.1)
    plt.xticks(rotation=-90)
    plt.ylabel("MAPE")  # alpha
    plt.xlabel("Event Log")
    fig = plt.gcf()
    plt.show()

    loc = r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'
    fig.savefig(os.path.join(loc, 'bubble_heatmap_MAPE_freq.pdf'))

    g = sns.FacetGrid(log_alpha, col="aggregate_type", margin_titles=True)
    g.map(sns.scatterplot, data=log_alpha, x="dataset", y="alpha", size="delta_time_median", hue="epsilon_time",
          sizes=(10, 100))
    plt.subplots_adjust(top=0.7)
    g.set_xticklabels(rotation=-90)
    # g.fig.suptitle('Max \u03B5 for Time DFG  (EMD input)')
    axes = g.axes.flatten()
    axes[0].set_title("Average")
    axes[1].set_title("Sum")
    axes[2].set_title("Min")
    axes[3].set_title("Max")

    axes[0].set_ylabel("MAPE")
    for ax in axes:
        ax.set_xlabel("Event Log")
        # ax.set_xticks(rotation=-90)
    plt.legend(title='Legend', bbox_to_anchor=(1.01, 1), loc='upper left', labelspacing=0.6)
    # plt.xticks(rotation=-90)
    plt.show()
    loc = r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'
    g.savefig(os.path.join(loc, 'bubble_heatmap_MAPE_time.pdf'))


def plot_execution_time(execution_time_log,dir):
    execution_time_log.columns =["dataset", "parameter", "mode", "aggregate_type", "input_val", "time_diff"]
    execution_time_log.input_val.replace("delta", "\u03B4", inplace=True) # delta
    execution_time_log.input_val.replace("alpha", "MAPE", inplace=True)
    execution_time_log.dataset.replace("Unrineweginfectie", "Unrine.", inplace=True)
    execution_time_log.sort_values('time_diff', inplace=True)
    g = sns.barplot(x="dataset", y="time_diff", hue="input_val", data=execution_time_log)
    g.set_ylabel("Execution Time Log(Seconds)")  # epsilon
    g.set_xlabel("Dataset")  # delta
    plt.xticks(rotation='vertical')
    g.set(yscale="log")
    plt.legend()

    plt.savefig(os.path.join(dir, 'execution_time.pdf'))
    plt.show()



# result_log_alpha=pd.read_csv(os.path.join('../experiment_logs', "combined_result_log_alpha.csv"))
# result_log_delta= pd.read_csv(os.path.join('../experiment_logs', "result_log_delta.csv"))
# delta_logger_time=pd.read_csv(os.path.join('../experiment_logs', "delta_logger_time.csv"))
# delta_logger_freq=pd.read_csv(os.path.join('../experiment_logs', "delta_logger_freq.csv"))
# execution_time_log=pd.read_csv(os.path.join('../experiment_logs', "execution_time_combined.csv"), header=None)
# # bubble_heatmap(result_log_delta,result_log_alpha)

# dir=r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'
#
# result_log_delta=pd.read_csv(os.path.join('../experiment_logs', "combined_result_log_delta_subsetted.csv"))
# plot_input_delta(result_log_delta,dir)
# plot_execution_time(execution_time_log,dir)
# plot_results(result_log_delta,result_log_alpha,delta_logger_freq,delta_logger_time)

# plot_input_alpha(result_log_alpha,dir)