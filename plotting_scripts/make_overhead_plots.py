#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import glob
import os
import re 
import numpy as np
from scipy.stats import skew, kurtosis
import shutil 
import pprint 
from functools import wraps
import time


def timer(f):                                                                      
    @wraps(f)                                                                      
    def wrapper(*args, **kwargs):                                                  
        start = time.time()                                                             
        result = f(*args, **kwargs)                                                
        end = time.time()                                                               
        print("{} - Elapsed time: {}".format(f, end-start))
        return result                                                              
    return wrapper

time_pattern = re.compile("^Time\(sec\)::")

"""
Make a bar chart where:
- x-axis is number of threads
- y-axis is count of events
- each group of bars contains one bar for each event type traced
"""
@timer
def make_time_grouped_barchart(nthreads_to_stats, data_dir, figures_dir):
    fig, ax = plt.subplots()
    thread_counts = list(nthreads_to_stats.keys())

    #print(data_dir)
    #print(thread_counts)
    
    events = list(nthreads_to_stats[thread_counts[0]].keys())

    #print(events)
    #exit()

    n_thread_counts = len(thread_counts)
    n_events = len(events) 
    bar_width = 1.0 / n_events 

    event_to_offset = {}
    for i,event in zip(range(n_events), events):
        event_to_offset[event] = i * bar_width

    xticks = []
    xticklabels = []
    minor_xticks = []
    minor_xticklabels = []
    for nt,i in zip(thread_counts, range(n_thread_counts)):
        xticklabels.append('')
        minor_xticklabels.append(nt)
        if i == 0:
            xticks.append(i)
            minor_xticks.append(i + 0.5)
        else:
            xticks.append(xticks[i-1] + 1 + bar_width)
            minor_xticks.append(minor_xticks[i-1] + 1 + bar_width)
    nthreads_to_xtick = {nt:x for nt,x in zip(thread_counts, xticks)}

    #print(events)
    #pprint.pprint(nthreads_to_stats)
    for event in events:
        bar_positions = [ nthreads_to_xtick[nt] + event_to_offset[event] for nt in thread_counts ]
        bar_values = [ nthreads_to_stats[nt][event]["mean"] for nt in thread_counts ]
        bar_errors = [ np.sqrt(nthreads_to_stats[nt][event]["variance"]) for nt in thread_counts ]
        ax.bar(bar_positions, bar_values, bar_width, yerr=bar_errors, label=event)
    
    # Axes and annotation 
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    ax.set_xticks(minor_xticks, minor=True)
    ax.set_xticklabels(minor_xticklabels, minor=True)
    ax.set_xlabel("Number of Threads")
    ax.set_ylabel("Runtime")
    title = prettify_app_name(get_app_name_from_path(data_dir))
    ax.set_title(title)
    #ax.set_yscale("log")

    # Make external legend 
    #ax.legend(loc="best")
    ax.legend(loc = "lower left", 
              bbox_to_anchor = (1.01, 0.0),
              ncol = 1,
              borderaxespad = 0,
              frameon = False
             )
   
    #plt.show()

    # Save
    dpi = 300
    figure_name = figures_dir + "/barchart_runtimes.pdf"
    plt.savefig(figure_name, 
                dpi=300,
                transparent=True,
                bbox_inches="tight"
               )


def get_nthreads_from_path(path):
    try:
        nthreads = int(path.split("/")[-2])
        return nthreads
    except:
        ValueError("Could not get number of threads from data directory path")

def get_app_name_from_path(path):
    app_names = ["sparselu_task",
                 "sparselu_taskdep",
                 "strassen_task",
                 "strassen_taskdep"
                ]
    for x in path.split("/"):
        if x in app_names:
            return x
    print("Could not determine app name from path. Exiting.")
    exit()
        

def prettify_app_name(app_name):
    table = {"fib.clang.omp-tasks": "Fibonnaci",
             "sort.clang.omp-tasks": "Sort",
             "sparselu.clang.for-omp-tasks": "Sparse LU-Decomposition",
             "strassen.clang.omp-tasks": "Strassen Matrix Multiplication",
             "sparselu_task": "Sparse LU-Factorization (task)",
             "sparselu_taskdep": "Sparse LU-Factorization (task depend)",
             "strassen_task": "Strassen Matrix Multiplication (task)",
             "strassen_taskdep": "Strassen Matrix Multiplication (task depend)",
            }
    return table[app_name]

def get_run_from_path(path):
    run_id = int(os.path.splitext(path.split("/")[-1])[0])
    return run_id

@timer
def get_times_for_app(data_dir):
    nthreads_to_times = {}
    for thread_count_dir in glob.glob(data_dir+"/*/"):
        # ignore non-thread-count directories
        if thread_count_dir.split("/")[-2] == "figures":
            pass
        else:
            nthreads = get_nthreads_from_path(thread_count_dir)
            tool_to_times = {}
            for tool_dir in glob.glob(thread_count_dir+"/*/"):
                tool = tool_dir.split("/")[-2]
                logfile_paths = glob.glob(tool_dir+"/*.txt")
                run_to_times = {}
                for logfile in logfile_paths:
                    run = get_run_from_path(logfile)
                    times = get_time_for_run(logfile)
                    run_to_times[run] = times
                tool_to_times[tool] = run_to_times
            nthreads_to_times[nthreads] = tool_to_times
    return nthreads_to_times
        

def get_time_for_run(logfile_path):
    with open(logfile_path, "r") as logfile:
        lines = logfile.readlines()
    for line in lines:
        if time_pattern.match(line):
            return get_time_from_line(line)

def get_time_from_line(line):
    time = float(line.split(":")[3].strip())
    return time 



@timer 
def aggregate_times(nthreads_to_times):
    aggregated = {nthreads:None for nthreads in nthreads_to_times}
    for nthreads in nthreads_to_times:
        aggregated_times = {}
        tool_to_times = nthreads_to_times[nthreads]
        for tool in tool_to_times:
            aggregated_times[tool] = []
            run_to_times = tool_to_times[tool]
            for run in sorted(run_to_times):
                aggregated_times[tool].append(run_to_times[run])
        aggregated[nthreads] = aggregated_times
    return aggregated

@timer
def get_time_stats(nthreads_to_aggregate_times):
    nthreads_to_stats = {nthreads:None for nthreads in nthreads_to_aggregate_times}
    for nthreads in nthreads_to_aggregate_times:
        tool_to_times = nthreads_to_aggregate_times[nthreads]
        tool_to_stats = {}
        for tool in tool_to_times:
            times = tool_to_times[tool]
            stats = {}
            stats["min"] = np.min(times)
            stats["max"] = np.max(times)
            stats["mean"] = np.mean(times)
            stats["median"] = np.median(times)
            stats["variance"] = np.var(times)
            stats["skew"] = skew(times)
            stats["kurtosis"] = kurtosis(times)
            tool_to_stats[tool] = stats
        nthreads_to_stats[nthreads] = tool_to_stats
    return nthreads_to_stats 
            



if __name__ == "__main__":
    # Get and parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir")
    args = parser.parse_args() 

    # Validate args
    if os.path.isdir(args.data_dir):
        data_dir = args.data_dir
    else:
        print("Data source: "+args.data_dir+" is not a directory. Exiting.")
        exit()

    nthreads_to_times = get_times_for_app(data_dir)
    #pprint.pprint(nthreads_to_times)
    nthreads_to_aggregate_times = aggregate_times(nthreads_to_times)
    #pprint.pprint(nthreads_to_aggregate_times)
    nthreads_to_stats = get_time_stats(nthreads_to_aggregate_times)
    #pprint.pprint(nthreads_to_stats)

    # Set up figures dir
    figures_dir = data_dir + "/figures/"
    try:
        os.mkdir(figures_dir)
    except OSError:
        pass
        #print("Figures directory: "+figures_dir+" already exists.")

    make_time_grouped_barchart(nthreads_to_stats, data_dir, figures_dir)
