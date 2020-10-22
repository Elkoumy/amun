"""
In this file, we implement the parameterized job to run over slurm HPC.

"""

from amun.differental_privacy_module import *
# from GUI_module import *
from amun.input_module import *
import pandas as pd
from amun.data_visualization import plot_results
from statistics import median
from amun.model_visualization import view_model
import os

def run_experiment(data="Sepsis",parameter="0.1", mode="nonpruning",aggregate_type=AggregateType.FREQ, input_val="delta",iteration=0):
    """Parameters to the script"""
    input_dataset=data
    input_alpha_delta=float(parameter)
    '''**********************'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    process_model_dir=os.path.join(dir_path,"experiment_figures","process_models")
    data_dir =os.path.join(dir_path,"data")
    figures_dir=os.path.join(dir_path,'experiment_figures')
    log_dir=os.path.join(dir_path,'experiment_logs')

    # datasets=["Sepsis Cases - Event Log","CreditRequirement","Road_Traffic_Fine_Management_Process"]

    # datasets=["Road_Traffic_Fine_Management_Process"]
    result_log_delta = []  # holds the delta as input exeperiment
    # vales is exp_index, delta, epsilon_freq, epsilon_time, emd_freq, emd_time

    result_log_alpha=[] # holds the alpha or EMD as input exeperiment
    # delta_per_distance={}

    delta_logger=[]


    result_log_APE=[]
    result_log_SMAPE = []
    result_log_epsilon=[]


    # no_of_experiments=1
    precision=0.5
    dataset = input_dataset



    print("Dataset: "+ dataset)
    print("Aggregate Type: "+ str(aggregate_type))
    # delta=0.05
    # dfg_freq, dfg_time = read_xes(data_dir,dataset, aggregate_type,mode)
    dfg = read_xes(data_dir, dataset, aggregate_type, mode)
    # view_model(dfg_freq,os.path.join( process_model_dir , r"/fig_input_unprotected_" + dataset))




    SMAPE_tot=0

    MAPE_tot=0
    epsilon_min=0

    # making the scope of variable outside the for loop
    APE_dist=0
    APE_dist=0

    if input_val=="delta":
        delta = input_alpha_delta

        # dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, MAPE_freq, SMAPE_freq, APE_dist_freq, MAPE_time, SMAPE_time, APE_dist_time = differential_privacy_with_risk(dfg_freq, dfg_time, delta=delta,precision=precision,aggregate_type=aggregate_type)


        dfg_new, dfg_new, epsilon, MAPE, SMAPE, APE_dist, SMAPE_dist = differential_privacy_with_risk(dfg, delta=delta,
                                                                                              precision=precision,
                                                                                              aggregate_type=aggregate_type)
        # calculating the average MAPE and SMAPE for the number of experiments
        SMAPE_tot+=SMAPE
        SMAPE_tot += SMAPE

        MAPE_tot+=MAPE
        MAPE_tot+=MAPE

        if aggregate_type==AggregateType.FREQ:
            epsilon_min+=epsilon
        else:
            epsilon_min += min(epsilon.values())



        # result_log_delta.append([dataset,i,delta,epsilon_freq,min(epsilon_time.values()), emd_freq, emd_time]) # logging the min epsilon for time as it is the maximum added noise
        # view_model(dfg_freq_new,process_model_dir+r"/fig_input_delta_"+str(delta)+"_"+dataset+"_"+str(aggregate_type)+"_"+str(i))
        print("avg MAPE  is " + str(MAPE_tot))
        print("avg SMAPE  is " + str(SMAPE_tot ))


        result_log_delta.append([dataset,aggregate_type,  delta, epsilon, epsilon_min, MAPE_tot,
                                 SMAPE_tot ])  # logging the min epsilon for time as it is the maximum added noise

        #logging the distribution of APE
        for edge in APE_dist:
            result_log_APE.append([dataset,aggregate_type,  delta, edge, APE_dist[edge] ])
        for edge in SMAPE_dist:
            result_log_SMAPE.append([dataset,aggregate_type,  delta, edge, SMAPE_dist[edge]])


        if aggregate_type != AggregateType.FREQ:
            for edge in epsilon:
                result_log_epsilon.append([dataset,aggregate_type,  delta, edge, epsilon[edge] ])

            result_log_epsilon = pd.DataFrame.from_records(result_log_epsilon,
                                                       columns=["dataset", "aggregate_type", "delta", "edge",
                                                                "epsilon"])

            result_log_epsilon.to_csv(os.path.join(log_dir, "result_log_epsilon_%s_%s_%s_%s_%s_%s.csv" % (
            input_dataset, str(input_alpha_delta), mode, aggregate_type, input_val, str(iteration))), index=False)


        """logging results in output files"""
        result_log_delta = pd.DataFrame.from_records(result_log_delta,
                                                     columns=["dataset", "aggregate_type", "delta", "epsilon",
                                                              "min_epsilon", "MAPE", "SMAPE"])

        # result_log_delta.to_csv(os.path.join(log_dir, "result_log_delta_" + input_dataset + "_" + str(
        #     input_alpha_delta) + "_" + mode + "_" + aggregate_type + "_" + input_val + ".csv"), index=False)

        result_log_delta.to_csv(os.path.join(log_dir, "result_log_delta_%s_%s_%s_%s_%s_%s.csv"%(input_dataset,str(input_alpha_delta), mode, aggregate_type,input_val,str(iteration))), index=False)


        result_log_APE = pd.DataFrame.from_records(result_log_APE,
                                                   columns=["dataset", "aggregate_type", "delta", "edge", "APE"])



        result_log_SMAPE.to_csv(os.path.join(log_dir, "result_log_SMAPE_%s_%s_%s_%s_%s_%s.csv"%(input_dataset,str(input_alpha_delta), mode, aggregate_type,input_val,str(iteration))), index=False)


        result_log_SMAPE = pd.DataFrame.from_records(result_log_SMAPE,
                                                   columns=["dataset", "aggregate_type", "delta", "edge", "SMAPE"])

        result_log_APE.to_csv(os.path.join(log_dir, "result_log_APE_%s_%s_%s_%s_%s_%s.csv" % (
        input_dataset, str(input_alpha_delta), mode, aggregate_type, input_val, str(iteration))), index=False)

        result_log_SMAPE.to_csv(os.path.join(log_dir, "result_log_SMAPE_%s_%s_%s_%s_%s_%s.csv" % (
            input_dataset, str(input_alpha_delta), mode, aggregate_type, input_val, str(iteration))), index=False)
    else:
        epsilon_logger=[]
        emd=input_alpha_delta
        if aggregate_type== AggregateType.FREQ:
            dfg_new, epsilon, delta, delta_dfg = differential_privacy_with_accuracy(dfg, precision=precision,
                                                                                    distance=emd,
                                                                                    aggregate_type=aggregate_type)
        else:
            dfg_new, epsilon, delta, delta_dfg, delta_per_event = differential_privacy_with_accuracy(dfg, precision=precision,
                                                                                    distance=emd,

                                                                                    aggregate_type=aggregate_type)
            delta_per_event_logger= []
            for item in delta_per_event:
                delta_per_event_logger.append([dataset, aggregate_type, emd,item[0],item[1]])

            delta_per_event_logger=pd.DataFrame.from_records(delta_per_event_logger,columns=["dataset", "aggregate_type", "emd","edge", "risk"])
            delta_per_event_logger.to_csv(os.path.join(log_dir, "delta_per_event_logger_%s_%s_%s_%s_%s.csv" % (
                input_dataset, str(input_alpha_delta), mode, aggregate_type, input_val)), index=False)

        # delta_per_distance[emd] = delta_time_dfg
        for edge in delta_dfg.keys():
            delta_logger.append([dataset, aggregate_type, emd,edge,delta_dfg[edge]])
        for edge in epsilon.key():
            epsilon_logger.append([dataset, aggregate_type, emd,edge,epsilon[edge]])

        result_log_alpha.append([dataset,aggregate_type,emd,min(list(epsilon.values())), median(list(epsilon.values())) , median(list(delta_dfg.values())) , max(list(delta_dfg.values())) ])
        # view_model(dfg_freq_new, process_model_dir + r"/fig_input_emd_" + str(emd) + "_" + dataset + "_" + str(aggregate_type))
        print("delta for the freq is "+ str(delta))



        """logging results in output files"""
        result_log_alpha = pd.DataFrame.from_records(result_log_alpha,
                                                     columns=["dataset", "aggregate_type", "alpha", "epsilon", "median_epsilon",
                                                               "delta_median", "delta_max"])
        result_log_alpha.to_csv(os.path.join(log_dir, "result_log_alpha_%s_%s_%s_%s_%s.csv" % (
        input_dataset, str(input_alpha_delta), mode, aggregate_type, input_val)), index=False)


        epsilon_logger=pd.DataFrame(epsilon_logger, columns=["dataset", "aggregate_type", "emd","edge", "epsilon"])
        epsilon_logger.to_csv(os.path.join(log_dir, "epsilon_logger_%s_%s_%s_%s_%s.csv" % (
            input_dataset, str(input_alpha_delta), mode, aggregate_type, input_val)), index=False)

        delta_logger = pd.DataFrame(delta_logger, columns=["dataset", "aggregate_type", "emd","edge", "delta"])
        delta_logger.to_csv(os.path.join(log_dir, "delta_logger_%s_%s_%s_%s_%s.csv" % (
            input_dataset, str(input_alpha_delta), mode, aggregate_type, input_val)), index=False)




    # plot_delta_distribution_times(delta_logger_time)




    #plot the results
    # plot_results(result_log_delta,result_log_alpha,delta_logger_freq,delta_logger_time, figures_dir)




"""**********************************************************************"""
"""***************** old version ****************************************"""
def run_experiment_old(data="Sepsis Cases - Event Log",parameter="0.1", mode="nonpruning"):
    """Parameters to the script"""
    input_dataset=data
    input_alpha_delta=float(parameter)
    '''**********************'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    process_model_dir=os.path.join(dir_path,"experiment_figures","process_models")
    data_dir =os.path.join(dir_path,"data")
    figures_dir=os.path.join(dir_path,'experiment_figures')
    log_dir=os.path.join(dir_path,'experiment_logs')

    # datasets=["Sepsis Cases - Event Log","CreditRequirement","Road_Traffic_Fine_Management_Process"]
    datasets=[input_dataset]
    # datasets=["Road_Traffic_Fine_Management_Process"]
    result_log_delta = []  # holds the delta as input exeperiment
    # vales is exp_index, delta, epsilon_freq, epsilon_time, emd_freq, emd_time

    result_log_alpha=[] # holds the alpha or EMD as input exeperiment
    # delta_per_distance={}

    delta_logger_time=[]
    delta_logger_freq=[]

    result_log_APE_freq=[]
    result_log_APE_time=[]


    no_of_experiments=10
    precision=0.5
    for dataset in datasets:

        # aggregate_types=[AggregateType.AVG, AggregateType.SUM]
        aggregate_types = [ AggregateType.AVG, AggregateType.SUM,AggregateType.MIN,AggregateType.MAX]
        # aggregate_types = [AggregateType.MIN]
        for aggregate_type in aggregate_types:
            print("Dataset: "+ dataset)
            print("Aggregate Type: "+ str(aggregate_type))
            # delta=0.05
            dfg_freq, dfg_time = read_xes(data_dir,dataset, aggregate_type,mode)
            # view_model(dfg_freq,os.path.join( process_model_dir , r"/fig_input_unprotected_" + dataset))

            # dfg_freq, dfg_time = read_xes( data_dir + "\\" + dataset + ".xes", aggregate_type)
            # view_model(dfg_freq, process_model_dir + r"/fig_input_unprotected_" + dataset )
            # deltas=[0.01,0.05, 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
            deltas = [ input_alpha_delta]
            for delta in deltas:
                SMAPE_freq_tot=0
                SMAPE_time_tot = 0
                MAPE_freq_tot=0
                MAPE_time_tot = 0
                epsilon_time_min=0

                # making the scope of variable outside the for loop
                APE_dist_freq=0
                APE_dist_time=0

                for i in range(0,no_of_experiments):
                    dfg_freq_new, dfg_time_new, epsilon_freq,epsilon_time, MAPE_freq, SMAPE_freq, APE_dist_freq, MAPE_time, SMAPE_time, APE_dist_time = differential_privacy_with_risk(dfg_freq, dfg_time, delta=delta,precision=precision,aggregate_type=aggregate_type)
                    # calculating the average MAPE and SMAPE for the number of experiments
                    SMAPE_freq_tot+=SMAPE_freq
                    SMAPE_time_tot += SMAPE_time

                    MAPE_freq_tot+=MAPE_freq
                    MAPE_time_tot+=MAPE_time


                    epsilon_time_min+=min(epsilon_time.values())


                    # result_log_delta.append([dataset,i,delta,epsilon_freq,min(epsilon_time.values()), emd_freq, emd_time]) # logging the min epsilon for time as it is the maximum added noise
                    # view_model(dfg_freq_new,process_model_dir+r"/fig_input_delta_"+str(delta)+"_"+dataset+"_"+str(aggregate_type)+"_"+str(i))
                print("avg MAPE for freq is " + str(MAPE_freq_tot/no_of_experiments))
                print("avg MAPE for time is " + str(MAPE_time_tot/no_of_experiments))

                print("avg SMAPE for freq is " + str(SMAPE_freq_tot / no_of_experiments))
                print("avg SMAPE for time is " + str(SMAPE_time_tot / no_of_experiments))

                result_log_delta.append([dataset,aggregate_type,  delta, epsilon_freq, epsilon_time_min/no_of_experiments, MAPE_freq_tot/no_of_experiments,
                                         SMAPE_freq_tot / no_of_experiments, MAPE_time_tot/no_of_experiments, SMAPE_time_tot / no_of_experiments])  # logging the min epsilon for time as it is the maximum added noise

                #logging the distribution of APE
                for edge in APE_dist_freq:
                    result_log_APE_freq.append([dataset,aggregate_type,  delta, edge, APE_dist_freq[edge] ])

                for edge in APE_dist_time:
                    result_log_APE_time.append([dataset,aggregate_type,  delta, edge, APE_dist_time[edge] ])

            # emd=1000
            # emds=[0.01, 0.05, 0.1,0.2,0.3,0.4,0.5,0.6, 0.7,0.8,0.9]
            emds=[input_alpha_delta]
            for emd in emds:


                dfg_freq_new, dfg_time_new, epsilon_freq, epsilon_time, delta_freq , delta_time, delta_freq_dfg, delta_time_dfg=differential_privacy_with_accuracy(dfg_freq, dfg_time,precision=precision, distance=emd, aggregate_type=aggregate_type)
                # delta_per_distance[emd] = delta_time_dfg
                for edge in delta_time_dfg.keys():
                    delta_logger_time.append([dataset, aggregate_type, emd,delta_time_dfg[edge]])

                for edge in delta_freq_dfg.keys():
                    delta_logger_freq.append([dataset, aggregate_type, emd,delta_freq_dfg[edge]])
                result_log_alpha.append([dataset,aggregate_type,emd,min(list(epsilon_freq.values())), min(list(epsilon_time.values())) , median(list(delta_freq_dfg.values())), median(list(delta_time_dfg.values())) , max(list(delta_freq_dfg.values())), max(list(delta_time_dfg.values())) ])
                # view_model(dfg_freq_new, process_model_dir + r"/fig_input_emd_" + str(emd) + "_" + dataset + "_" + str(aggregate_type))
                print("delta for the freq is "+ str(delta_freq))
                print("delta for the time is "+ str(delta_time))




    # transform results into dataframes
    result_log_delta=pd.DataFrame.from_records(result_log_delta,columns=["dataset","aggregate_type", "delta", "epsilon_freq", "epsilon_time", "MAPE_freq","SMAPE_freq", "MAPE_time", "SMAPE_time"])
    result_log_delta.to_csv(os.path.join(log_dir,"result_log_delta_"+input_dataset+"_"+str(input_alpha_delta)+"_"+mode+".csv"),index=False)
    result_log_alpha=pd.DataFrame.from_records(result_log_alpha, columns =["dataset","aggregate_type", "alpha", "epsilon_freq", "epsilon_time", "delta_freq_median", "delta_time_median", "delta_freq_max", "delta_time_max"])
    result_log_alpha.to_csv(os.path.join(log_dir,"result_log_alpha_"+input_dataset+"_"+str(input_alpha_delta)+"_"+mode+".csv"),index=False)

    # #the delta distribution from emd as input
    delta_logger_time=pd.DataFrame(delta_logger_time, columns=["dataset","aggregate_type","emd","delta"])
    delta_logger_time.to_csv(os.path.join(log_dir,"delta_logger_time_"+input_dataset+"_"+str(input_alpha_delta)+"_"+mode+".csv"), index=False)

    delta_logger_freq=pd.DataFrame(delta_logger_freq, columns=["dataset","aggregate_type","emd","delta"])
    delta_logger_freq.to_csv(os.path.join(log_dir,"delta_logger_freq_"+input_dataset+"_"+str(input_alpha_delta)+"_"+mode+".csv"), index=False)
    # plot_delta_distribution_times(delta_logger_time)

    result_log_APE_freq= pd.DataFrame.from_records(result_log_APE_freq, columns=["dataset","aggregate_type", "delta", "edge", "APE_freq"])
    result_log_APE_freq.to_csv(os.path.join(log_dir,"result_log_APE_freq_"+input_dataset+"_"+str(input_alpha_delta)+"_"+mode+".csv"), index=False)

    result_log_APE_time= pd.DataFrame.from_records(result_log_APE_time, columns=["dataset","aggregate_type", "delta", "edge", "APE_time"])
    result_log_APE_time.to_csv(os.path.join(log_dir,"result_log_APE_time_"+input_dataset+"_"+str(input_alpha_delta)+"_"+mode+".csv"), index=False)
    #plot the results
    # plot_results(result_log_delta,result_log_alpha,delta_logger_freq,delta_logger_time, figures_dir)


if __name__ == "__main__":

    data=os.sys.argv[1]
    parameter=os.sys.argv[2]
    mode = os.sys.argv[3]
    aggregate_type= os.sys.argv[4]
    input_val=os.sys.argv[5]
    iteration=os.sys.argv[6]


    if aggregate_type=="AggregateType.FREQ":
        aggregate_type=AggregateType.FREQ
    elif aggregate_type=="AggregateType.MIN":
        aggregate_type= AggregateType.MIN
    elif aggregate_type=="AggregateType.MAX":
        aggregate_type=AggregateType.MAX
    elif aggregate_type=="AggregateType.AVG":
        aggregate_type=AggregateType.AVG
    elif aggregate_type=="AggregateType.SUM":
        aggregate_type=AggregateType.SUM


    run_experiment(data=data,parameter=parameter,mode=mode, aggregate_type=aggregate_type,input_val=input_val,iteration=iteration)

