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

event_count_pattern = re.compile("^Number of [\w\s]+:\s[\d]+$")
events = ["thread_begin",
          "thread_end",
          "parallel_begin",
          "parallel_end",
          "explicit_task_begin",
          "implicit_task_begin",
          "implicit_task_end",
          "task_dependences", 
          "task_dependence",
          "task_schedule_others",
          "task_schedule_cancel",
          "task_schedule_yield",
          "task_schedule_complete",
          "task_sync_region_begin_barrier",
          "task_sync_region_begin_taskwait",
          "task_sync_region_begin_taskgroup",
          "task_sync_region_end_barrier",
          "task_sync_region_end_taskwait",
          "task_sync_region_end_taskgroup",
          "task_sync_region_wait_begin_barrier",
          "task_sync_region_wait_begin_taskwait",
          "task_sync_region_wait_begin_taskgroup",
          "task_sync_region_wait_end_barrier",
          "task_sync_region_wait_end_taskwait", 
          "task_sync_region_wait_end_taskgroup",
         ]

"""
Make a bar chart where:
- x-axis is number of threads
- y-axis is count of events
- each group of bars contains one bar for each event type traced
"""
@timer
def make_event_counts_grouped_barchart(nthreads_to_stats, data_dir, figures_dir):
    fig, ax = plt.subplots()
    thread_counts = list(nthreads_to_stats.keys())
    events = list(nthreads_to_stats[thread_counts[0]].keys())
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
    ax.set_ylabel("Number of Events")
    title = prettify_app_name(get_app_name_from_path(data_dir))
    ax.set_title(title)
    ax.set_yscale("log")

    # Make external legend 
    #ax.legend(loc="best")
    ax.legend(loc = "lower left", 
              bbox_to_anchor = (1.01, 0.0),
              ncol = 1,
              borderaxespad = 0,
              frameon = False
             )
    
    # Save
    dpi = 300
    figure_name = figures_dir + "/barchart_event_counts.pdf"
    plt.savefig(figure_name, 
                dpi=300,
                transparent=True,
                bbox_inches="tight"
               )


def get_nthreads_from_path(path):
    try:
        nthreads = int(path.split("/")[-2])
    except:
        ValueError("Could not get number of threads from data directory path")
    return nthreads

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
    return int(os.path.splitext(path.split("/")[-1])[0])

@timer
def get_counts_for_app(data_dir):
    nthreads_to_counts = {}
    for thread_count_dir in glob.glob(data_dir+"/data/*/"):
        nthreads = get_nthreads_from_path(thread_count_dir)
        logfile_paths = glob.glob(thread_count_dir+"/*")
        run_to_counts = {}
        for logfile in logfile_paths:
            run = get_run_from_path(logfile)
            counts = get_counts_for_run(logfile)
            run_to_counts[run] = counts
        nthreads_to_counts[nthreads] = run_to_counts
    return nthreads_to_counts
        

def get_counts_for_run(logfile_path):
    with open(logfile_path, "r") as logfile:
        lines = logfile.readlines()
    counts = []
    for line in lines:
        if event_count_pattern.match(line):
            counts.append(get_count_from_line(line))
    return { event:count for event,count in zip(events,counts) }

def get_count_from_line(line):
    count = int(line.split(":")[-1].strip())
    return count
    
@timer 
def aggregate_counts(nthreads_to_counts):
    aggregated = {nthreads:None for nthreads in nthreads_to_counts}
    for nthreads in nthreads_to_counts:
        aggregated_counts = {}
        counts = nthreads_to_counts[nthreads]
        for trial in counts:
            for event in counts[trial]:
                if event not in aggregated_counts:
                    aggregated_counts[event] = [counts[trial][event]]
                else:
                    aggregated_counts[event].append(counts[trial][event])
        aggregated[nthreads] = aggregated_counts
    return aggregated

@timer
def get_event_count_stats(nthreads_to_aggregate_counts):
    nthreads_to_stats = {nthreads:None for nthreads in nthreads_to_aggregate_counts}
    for nthreads in nthreads_to_aggregate_counts:
        event_counts = nthreads_to_aggregate_counts[nthreads]
        event_to_stats = {}
        for event in event_counts:
            counts = event_counts[event]
            stats = {}
            stats["min"] = np.min(counts)
            stats["max"] = np.max(counts)
            stats["mean"] = np.mean(counts)
            stats["median"] = np.median(counts)
            stats["variance"] = np.var(counts)
            stats["skew"] = skew(counts)
            stats["kurtosis"] = kurtosis(counts)
            event_to_stats[event] = stats
        nthreads_to_stats[nthreads] = event_to_stats
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

    nthreads_to_counts = get_counts_for_app(data_dir)
    nthreads_to_aggregate_counts = aggregate_counts(nthreads_to_counts)
    nthreads_to_stats = get_event_count_stats(nthreads_to_aggregate_counts)

    # Set up figures dir
    figures_dir = data_dir + "/figures/"
    try:
        os.mkdir(figures_dir)
    except OSError:
        print("Figures directory: "+figures_dir+" already exists.")

    make_event_counts_grouped_barchart(nthreads_to_stats, data_dir, figures_dir)
