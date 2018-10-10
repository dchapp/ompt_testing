#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import glob
import os
import re 
import numpy as np
import shutil 

import pprint 

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


def get_params_from_filename(filename):
    params = os.path.splitext(filename)[0].split("_")
    for i,p in zip(range(len(params)), params):
        try:
            params[i] = int(params[i].split("/")[-1])
        except:
            pass
    return tuple(params)

def extract_runtime_from_line(runtime_line):
    return float(re.sub("[^0-9.]", "", runtime_line))


def get_runtime_from_filename(filename):
    runtime_pattern = re.compile("^Time Program\s+=\s+\d+\.\d+\s+seconds$")
    with open(filename, "r") as infile:
        lines = infile.readlines()
        for line in lines:
            if runtime_pattern.match(line):
                return extract_runtime_from_line(line)

def get_params_to_runtime(data_dir):
    files = glob.glob(data_dir+"/*.out")
    params_to_runtimes = {}
    for f in files:
        params = get_params_from_filename(f)
        runtime = get_runtime_from_filename(f)
        params_to_runtimes[params] = runtime 
    return params_to_runtimes

def get_params_to_callback_counts(data_dir):
    files = glob.glob(data_dir+"/*baseline-tool-callback-counts.out")
    params_to_counts = {}
    for f in files:
        params = get_params_from_filename(f)
        counts = get_counts_from_filename(f)
        params_to_counts[params] = counts

    return params_to_counts


def get_counts_from_filename(filename):
    count_pattern = re.compile("^Number of [\w\s\(\)]+ callback invocations: \d+$")
    counts = []
    callbacks = ["parallel_begin",
                 "explicit_task",
                 "implicit_task_creation",
                 "implicit_task_completion",
                 "task_dependences",
                 "task_schedule_others",
                 "task_schedule_cancel",
                 "task_schedule_yield",
                 "task_schedule_complete",
                 "task_sync_region",
                 "task_sync_region_wait"
                ]
    with open(filename, "r") as infile:
        lines = infile.readlines()
        for line in lines:
            if count_pattern.match(line):
                counts.append(extract_count(line))
    callbacks_to_counts = {k:v for k,v in zip(callbacks, counts)}
    return callbacks_to_counts


def extract_count(line):
    return int(line.split(":")[-1].strip())
        

def get_runs(params_to_runtimes, n_threads, app, config):
    out = {}
    for k in params_to_runtimes:
        if k == (n_threads, app, config):
            out[k] = params_to_runtimes[k]
    return out
            

def get_overheads_for_app(params_to_runtimes, thread_counts, configs, app):
    nthreads_to_overheads = {}
    for nt in thread_counts:
        overheads = {}
        no_tool_runs = get_runs(params_to_runtimes, nt, a, configs[0])
        no_tool_mean_runtime = np.mean(list(no_tool_runs.values()))
        for c in configs[1:]:
            config_runs = get_runs(params_to_runtimes, nt, a, c)
            config_mean_runtime = np.mean(list(config_runs.values()))
            overheads[c] = config_mean_runtime / no_tool_mean_runtime
        nthreads_to_overheads[nt] = overheads
    return nthreads_to_overheads
        

def get_runtimes_for_app(params_to_runtimes, thread_counts, configs, app):
    nthreads_to_runtimes = {}
    for nt in thread_counts:
        runtimes = {}
        no_tool_runs = get_runs(params_to_runtimes, nt, app, configs[0])
        no_tool_mean_runtime = np.mean(list(no_tool_runs.values()))
        for c in configs:
            config_runs = get_runs(params_to_runtimes, nt, app, c)
            config_mean_runtime = np.mean(list(config_runs.values()))
            runtimes[c] = config_mean_runtime
        nthreads_to_runtimes[nt] = runtimes
    return nthreads_to_runtimes 

def generate_overhead_percentages_scatterplot(params_to_runtimes,
                                              apps,
                                              thread_counts,
                                              configs,
                                              config_to_color):
    for a in apps:
        nthreads_to_overheads = get_overheads_for_app(params_to_runtimes,
                                                      thread_counts,
                                                      configs,
                                                      a)
        fig, ax = plt.subplots()
        nthreads = list(nthreads_to_overheads.keys())
        overheads = list(nthreads_to_overheads.values())
        y_upper_limit = 20
        y_limits = (0, y_upper_limit)
        yticks = [ x/2 for x in range(2*y_upper_limit) ]
        yticklabels = [ str(100*y)+"%" for y in yticks ]
        for c in configs[1:]:
            overheads_for_config = [ o[c] for o in overheads ]
            ax.scatter(nthreads, 
                       overheads_for_config, 
                       label=c, 
                       color=config_to_color[c])
            ax.set_xticks(nthreads)
            ax.set_xticklabels(nthreads)
            ax.set_yticks(yticks)
            ax.set_yticklabels(yticklabels)
            ax.set_ylim(y_limits)
            ax.legend(loc="best") 
        ax.set_title(a)
        plt.show()
  


def generate_runtimes_grouped_barchart(params_to_runtimes,
                                       apps,
                                       thread_counts,
                                       configs,
                                       config_to_color,
                                       app_to_app_name,
                                       figures_dir):
    for a in apps:
        nthreads_to_runtimes = get_runtimes_for_app(params_to_runtimes,
                                                    thread_counts,
                                                    configs,
                                                    a)
        fig, ax = plt.subplots(figsize=(11,8))
        nthreads = list(nthreads_to_runtimes.keys())
        runtimes = list(nthreads_to_runtimes.values())
        bar_width = 0.3
        config_to_bar_offset = {"no-tool":0, 
                                "baseline-tool":bar_width,
                                "full-tool":2*bar_width}
        xlabel = "Number of Threads"
        ylabel = "Runtime in Seconds"
        title = "Runtime for Application: " + app_to_app_name[a]
        xticks = [ nt+bar_width for nt in nthreads ]
        xticklabels = [ nt for nt in nthreads ]
        x_limits = (min(nthreads)-1, max(nthreads)+1)
        for c in configs:
            bar_positions = [ nt + config_to_bar_offset[c] for nt in nthreads ]
            bar_values = []
            for rd in runtimes:
                bar_values.append(rd[c])
            ax.bar(bar_positions, 
                   bar_values,
                   bar_width,
                   color = config_to_color[c],
                   label=c)
        # Axis limits
        ax.set_xlim(x_limits)
        # Ticks
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)
        # Annotate
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(loc="best")
        # Save
        figure_name = figures_dir + "barchart_runtimes_" + a.split(".")[0]
        plt.savefig(figure_name, 
                    dpi=600,
                    transparent=True,
                    bbox_inches="tight"
                   )
                                            
def get_counts_for_app(params_to_counts, thread_counts, app):
    nthreads_to_counts = {}
    callbacks = ["parallel_begin",
                 "explicit_task",
                 "implicit_task_creation",
                 "implicit_task_completion",
                 "task_dependences",
                 "task_schedule_others",
                 "task_schedule_cancel",
                 "task_schedule_yield",
                 "task_schedule_complete",
                 "task_sync_region",
                 "task_sync_region_wait"
                ]
    for nt in thread_counts:
        nthreads_to_counts[nt] = {}
        for p in params_to_counts:
            if p[0] == nt and p[1] == app:
                for k in params_to_counts[p]:
                    if k in callbacks:
                        if k not in nthreads_to_counts[nt]:
                            nthreads_to_counts[nt][k] = [ params_to_counts[p][k] ]
                        else:
                            nthreads_to_counts[nt][k].append( params_to_counts[p][k] )
    return nthreads_to_counts


def get_count_stats(nthreads_to_counts):
    nthreads_to_means = {k:{} for k in nthreads_to_counts.keys()}
    nthreads_to_stdevs = {k:{} for k in nthreads_to_counts.keys()}    
    for k in nthreads_to_counts:
        for cb in nthreads_to_counts[k]:
            nthreads_to_means[k][cb] = np.mean(nthreads_to_counts[k][cb])
            nthreads_to_stdevs[k][cb] = np.std(nthreads_to_counts[k][cb])
    return {"mean_map": nthreads_to_means,
            "stdev_map": nthreads_to_stdevs
           }


def generate_callback_counts_grouped_barchart(params_to_counts,
                                              apps,
                                              thread_counts,
                                              callback_to_color,
                                              app_to_app_name,
                                              figures_dir):
    for a in apps:
        nthreads_to_counts = get_counts_for_app(params_to_counts,
                                                thread_counts,
                                                a)

        nthreads_to_count_stats = get_count_stats(nthreads_to_counts)

        fig, ax = plt.subplots(figsize=(11,8))
        nthreads = list(nthreads_to_counts.keys())
        count_means = list(nthreads_to_count_stats["mean_map"].values())
        count_stdevs = list(nthreads_to_count_stats["stdev_map"].values())


        callbacks = [] 
        min_count = 10 # Not displaying infrequent callbacks
        for c in count_means[0]:
            if count_means[0][c] > min_count:
                callbacks.append(c)
        bar_width = 1.00 / len(callbacks)
        callback_to_bar_offset = {}
        for i,c in zip(range(len(callbacks)), callbacks):
            callback_to_bar_offset[c] = i * bar_width 
        xlabel = "Number of Threads"
        ylabel = "Number of Callback Invocations"
        title = "OMPT Callback Counts: " + app_to_app_name[a]
        xticks = [ nt+bar_width for nt in nthreads ]
        xticklabels = [ nt for nt in nthreads ]
        x_limits = (min(nthreads)-1, max(nthreads)+1)
        #callbacks = ["explicit_task",
        #             "task_schedule_others",
        #             "task_schedule_cancel",
        #             "task_schedule_yield",
        #             "task_schedule_complete",
        #             "task_sync_region",
        #             "task_sync_region_wait"
        #            ]

        for c in callbacks:
            bar_positions = [ nt + callback_to_bar_offset[c] for nt in nthreads ]
            bar_values = []
            bar_errors = []
            for cd in count_means:
                bar_values.append(cd[c])
            for cd in count_stdevs:
                bar_errors.append(cd[c])
            ax.bar(bar_positions, 
                   bar_values,
                   bar_width,
                   color = callback_to_color[c],
                   label=c,
                   yerr=bar_errors)
        # Axis limits
        ax.set_xlim(x_limits)
        # Ticks
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)
        # Annotate
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

        ax.legend(loc="best")

        # Save
        dpi = 300
        figure_name = figures_dir + "barchart_callback_counts_" + a.split(".")[0]
        plt.savefig(figure_name, 
                    dpi=300,
                    transparent=True,
                    bbox_inches="tight"
                   )




def get_counts_for_app(data_dir):
    logfile_paths = glob.glob(data_dir+"/*")
    run_to_counts = {path:get_counts_for_run(path) for path in logfile_paths} 
    pprint.pprint(run_to_counts)
    exit()
        

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

    exit()

    # Set constants 
    apps = ["sparselu_task",
            "sparselu_taskdep",
            "strassen_task",
            "strassen_taskdep"
           ]
    app_to_app_name = {"fib.clang.omp-tasks": "Fibonnaci",
                       "sort.clang.omp-tasks": "Sort",
                       "sparselu.clang.for-omp-tasks": "Sparse LU-Decomposition",
                       "strassen.clang.omp-tasks": "Strassen Matrix Multiplication",
                       "sparselu_task": "Sparse LU-Factorization (task)",
                       "sparselu_taskdep": "Sparse LU-Factorization (task depend)",
                       "strassen_task": "Strassen Matrix Multiplication (task)",
                       "strassen_taskdep": "Strassen Matrix Multiplication (task depend)",
                      }
    thread_counts = [1, 2, 4, 8, 16, 32]

        

    # Set up figures dir
    figures_dir = data_dir + "/figures/"
    try:
        os.mkdir(figures_dir)
    except OSError:
        print("Figures directory: "+figures_dir+" already exists.")

    


    make_event_counts_grouped_barchart(params_to_counts,
                                       apps,
                                       thread_counts,
                                       callback_to_color,
                                       app_to_app_name,
                                       figures_dir)


            
            
        

