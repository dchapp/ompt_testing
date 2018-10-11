#!/usr/bin/env bash
# [wf] execute run stage

job_scripts="../../job_scripts/"

# Set the number of trials to run for each app for each thread count
# and launch all of the jobs
event_counts_n_trials=10
# [wf] Running KASTORS apps with event-counter tool 
${job_scripts}/collect_kastors_event_counts.sh ${event_counts_n_trials} 
