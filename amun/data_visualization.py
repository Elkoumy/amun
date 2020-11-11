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

    # result_log_delta=result_log_delta[result_log_delta.dataset.isin(['Traffic','CreditReq'])]
    result_log_delta = result_log_delta[result_log_delta.dataset.isin(['CreditReq'])]
    result_log_delta.aggregate_type.replace("AggregateType.AVG", "AVG", inplace=True)
    result_log_delta.aggregate_type.replace("AggregateType.MIN", "MIN", inplace=True)
    result_log_delta.aggregate_type.replace("AggregateType.MAX", "MAX", inplace=True)
    result_log_delta.aggregate_type.replace("AggregateType.SUM", "SUM", inplace=True)
    result_log_delta.aggregate_type.replace("AggregateType.FREQ", "FREQ", inplace=True)
    """"************************************************"""
    #epsilon
    # g = sns.FacetGrid(result_log_delta, col="dataset", margin_titles=True)
    # g.map(sns.lineplot, "delta", "median_epsilon", "aggregate_type")
    g=sns.lineplot("delta", "median_epsilon", "aggregate_type",data=result_log_delta)
    # plt.subplots_adjust(top=0.2)
    # g.fig.suptitle('Min \u03B5  for  Time DFG  (EMD input)')
    # axes = g.axes.flatten()
    # axes[0].set_title("Aggregate: Average")
    # axes[1].set_title("Aggregate: Sum")
    # axes[2].set_title("Aggregate: Min")
    # axes[3].set_title("Aggregate: Max")
    # axes[0].set_xlabel("\u03B4") #delta
    # for ax in axes:
    #     ax.set_ylabel("Median \u03B5")#epsilon
    #     ax.set(yscale="log")

    plt.yscale("log")
    plt.ylabel("Median \u03B5") #epsilon
    plt.xlabel("\u03B4") #delta
    # plt.legend(title="Aggregate Type")
    fig = plt.gcf()
    plt.legend(loc='upper left', bbox_to_anchor=(0.99, 0.5))
    plt.show()

    fig.savefig(os.path.join(dir, 'epsilon_distribution_for_delta_input_CreditReq.pdf'))

    # #Delta
    # g = sns.FacetGrid(result_log_delta, col="dataset",col_wrap=4, margin_titles=True)
    # g.map(sns.lineplot, "delta", "SMAPE", "aggregate_type")
    # plt.subplots_adjust(top=0.2)
    #
    #
    # # g.fig.suptitle('Median \u03B5 for Time DFG  (EMD input)')
    # axes = g.axes.flatten()
    # # axes[0].set_title("Aggregate: Average")
    # # axes[1].set_title("Aggregate: Sum")
    # # axes[2].set_title("Aggregate: Min")
    # # axes[3].set_title("Aggregate: Max")
    # axes[0].set_xlabel("\u03B4") #delta
    # for ax in axes:
    #     ax.set_ylabel("SMAPE")  # alpha
    # plt.legend()
    # plt.show()
    # g.savefig(os.path.join(dir, 'Input_EMD_time_dfg_delta_median_distribution.pdf'))



def plot_input_alpha(result_log_alpha,dir):

    # #epsilon
    # g = sns.FacetGrid(result_log_alpha, col="dataset",col_wrap=4, margin_titles=True)
    # g.map(sns.lineplot, "alpha", "median_epsilon", "aggregate_type")
    # plt.subplots_adjust(top=0.2)
    # # g.fig.suptitle('Min \u03B5  for  Time DFG  (EMD input)')
    # axes = g.axes.flatten()
    # # axes[0].set_title("Aggregate: Average")
    # # axes[1].set_title("Aggregate: Sum")
    # # axes[2].set_title("Aggregate: Min")
    # # axes[3].set_title("Aggregate: Max")
    # axes[0].set_xlabel("MAPE")
    # for ax in axes:
    #     ax.set_ylabel("Log(Min \u03B5)")#epsilon
    #     ax.set(yscale="log")
    # plt.legend()
    # plt.show()
    # g.savefig(os.path.join(dir, 'Input_EMD_time_dfg_epsilon_distribution.pdf'))

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
    import numpy as np
    log_delta.median_epsilon.replace(np.inf,log_delta.median_epsilon.quantile(0.7),inplace=True)
    # log_delta.median_epsilon=log_delta.median_epsilon*(10**7)
    log_delta.dataset.replace("Unrineweginfectie", "Unrin..", inplace=True)
    log_delta.aggregate_type.replace("AggregateType.AVG", "AVG", inplace=True)
    log_delta.aggregate_type.replace("AggregateType.MIN", "MIN", inplace=True)
    log_delta.aggregate_type.replace("AggregateType.MAX", "MAX", inplace=True)
    log_delta.aggregate_type.replace("AggregateType.SUM", "SUM", inplace=True)
    log_delta.aggregate_type.replace("AggregateType.FREQ", "FREQ", inplace=True)
    log_delta.columns = ['dataset', 'aggregate_type', 'delta', '\u03B5', 'MAPE','SMAPE']
    log_delta.loc[log_delta.SMAPE > 0.9,"SMAPE"] = 0.9
    log_delta.SMAPE=log_delta.SMAPE.round(2)
    result_log_delta.SMAPE=result_log_delta.SMAPE.astype('float')

    for agg in ["FREQ","AVG", "MIN", "MAX","SUM"]:
        log_delta_filtered=log_delta.where(log_delta.aggregate_type == agg)

        log_delta_filtered.dropna(inplace=True)


        sns.scatterplot(
            data=log_delta_filtered, x="dataset", y="delta", size="SMAPE", hue="\u03B5",palette="ch:s=.25,rot=-.25",
            sizes=(20, 400) )

        leg=plt.legend(title='Legend', bbox_to_anchor=(1.01, 1), loc='upper left', labelspacing=1.1)

        for t in leg.texts:
            # truncate label text to 4 characters
            t.set_text(t.get_text()[:5])


        plt.xticks(rotation=-90)
        plt.ylabel("\u03B4") # delta
        plt.xlabel("Event Log")
        fig=plt.gcf()
        plt.title("Distribution of \u03B4, \u03B5 and SMAPE for %s" %(agg))
        plt.show()

        loc = r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'
        fig.savefig(os.path.join(loc, 'bubble_heatmap_delta_%s.pdf'%(agg)))


    """************************* for ALPHA *************"""

    log_alpha.median_epsilon.replace(np.inf, log_alpha.median_epsilon.quantile(0.7), inplace=True)
    # log_delta.median_epsilon=log_delta.median_epsilon*(10**7)
    log_alpha.dataset.replace("Unrineweginfectie", "Unrin..", inplace=True)
    log_alpha.aggregate_type.replace("AggregateType.AVG", "AVG", inplace=True)
    log_alpha.aggregate_type.replace("AggregateType.MIN", "MIN", inplace=True)
    log_alpha.aggregate_type.replace("AggregateType.MAX", "MAX", inplace=True)
    log_alpha.aggregate_type.replace("AggregateType.SUM", "SUM", inplace=True)
    log_alpha.aggregate_type.replace("AggregateType.FREQ", "FREQ", inplace=True)


    log_alpha.loc[log_alpha.delta_median > 0.9, "delta_median"] = 0.9
    log_alpha.loc[log_alpha.delta_max > 0.9, "delta_max"] = 0.9
    # log_delta.SMAPE = log_delta.SMAPE.round(2)
    # log_alpha.delta_median = log_alpha.delta_median.astype('float')

    log_alpha.columns = ['dataset', 'aggregate_type', 'alpha', 'epsilon', '\u03B5', '\u03B4', 'delta_max']
    for agg in ["FREQ", "AVG", "MIN", "MAX", "SUM"]:
        log_alpha_filtered = log_alpha.where(log_alpha.aggregate_type == agg)

        log_alpha_filtered.dropna(inplace=True)

        sns.scatterplot(
            data=log_alpha_filtered, x="dataset", y="alpha", size="\u03B4", hue="\u03B5", palette="ch:s=.25,rot=-.25",
            sizes=(20, 400))

        leg = plt.legend(title='Legend', bbox_to_anchor=(1.01, 1), loc='upper left', labelspacing=1.1)

        for t in leg.texts:
            # truncate label text to 4 characters
            t.set_text(t.get_text()[:5])

        plt.xticks(rotation=-90)
        plt.ylabel("MAPE")  # delta
        plt.xlabel("Event Log")
        fig = plt.gcf()
        plt.title("Distribution of MAPE, \u03B5 and \u03B4 for %s" % (agg))
        plt.show()

        loc = r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'
        fig.savefig(os.path.join(loc, 'bubble_heatmap_alpha_%s.pdf' % (agg)))




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
    g = plt.gcf()
    plt.show()

    g.savefig(os.path.join(dir, 'execution_time.pdf'))



def paper_distributions(delta_logger,dir):
    delta_logger.delta=delta_logger.delta.astype('float64')
    subset= delta_logger[delta_logger.dataset == "Sepsis"]
    subset = subset[subset.aggregate_type == "AggregateType.FREQ"]
    # g = sns.FacetGrid(subset, row="dataset", margin_titles=True)
    g=sns.boxplot(data= subset,x="emd", y="delta")
    # g.fig.suptitle(' \u03B5  Distribution for  Freq DFG  (EMD input)')


    g.set_ylabel(" \u03B4")  # delta
    g.set_xlabel("MAPE")  # alpha
    plt.title("Sepsis Cases with Frequency Query")
    fig = plt.gcf()
    plt.show()
    fig.savefig(os.path.join(dir, 'Input_alpha_freq_delta_distribution_sepsis.pdf'))

    """***************************   BPIC20 **************************"""
    subset= delta_logger[delta_logger.dataset == "BPIC20"]
    subset = subset[subset.aggregate_type == "AggregateType.FREQ"]
    # g = sns.FacetGrid(subset, row="dataset", margin_titles=True)
    g=sns.boxplot(data= subset,x="emd", y="delta")
    # g.fig.suptitle(' \u03B5  Distribution for  Freq DFG  (EMD input)')


    g.set_ylabel(" \u03B4")  # delta
    g.set_xlabel("MAPE")  # alpha
    plt.title("Sepsis Cases with Sum Query")
    fig = plt.gcf()
    plt.show()
    fig.savefig(os.path.join(dir, 'Input_alpha_freq_delta_distribution_BPIC20.pdf'))


# result_log_alpha=pd.read_csv(os.path.join('../experiment_logs', "combined_result_log_alpha.csv"))
# result_log_delta= pd.read_csv(os.path.join('../experiment_logs', "result_log_delta.csv"))
# delta_logger_time=pd.read_csv(os.path.join('../experiment_logs', "delta_logger_time.csv"))
# delta_logger_freq=pd.read_csv(os.path.join('../experiment_logs', "delta_logger_freq.csv"))
# execution_time_log=pd.read_csv(os.path.join('../experiment_logs', "execution_time_combined.csv"), header=None)
# combined_delta_logger=pd.read_csv(os.path.join('../experiment_logs', "combined_delta_logger_alpha.csv"))
# # result_log_delta=pd.read_csv(os.path.join('../experiment_logs', "combined_result_log_delta_subsetted.csv"))
#
#
dir=r'C:\Gamal Elkoumy\PhD\OneDrive - Tartu Ülikool\Differential Privacy\source code\experiment_figures'
result_log_delta=pd.read_csv(os.path.join('../experiment_logs', "combined_result_log_delta_subsetted.csv"))
# result_log_alpha=pd.read_csv(os.path.join('../experiment_logs', "combined_result_log_alpha.csv"))
# bubble_heatmap(result_log_delta,result_log_alpha)
# paper_distributions(combined_delta_logger,dir)
plot_input_delta(result_log_delta,dir)
# # plot_execution_time(execution_time_log,dir)
# # plot_results(result_log_delta,result_log_alpha,delta_logger_freq,delta_logger_time)
#
# # plot_input_alpha(result_log_alpha,dir)