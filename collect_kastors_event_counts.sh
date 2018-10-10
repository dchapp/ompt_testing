#!/bin/bash 

n_trials=$1

# Apps and inputs
app_dir="${HOME}/repos/kastors-1.1/build_event_counter_tool/bin"
apps=("sparselu_task"
      "sparselu_taskdep"
      "strassen_task"
      "strassen_taskdep"
     )
#thread_counts=(2 4 6 8 10 12 14 16 18 20 22 24)
thread_counts=(1 2 4 8 16 32)

# Set up result storage
result_dir="${HOME}/repos/OMPT_Testing/kastors_event_counts/"
mkdir -p ${result_dir}

cd ${app_dir}
for t in ${thread_counts[@]}
do
    echo "Working on ${t}-thread cases"
    export OMP_NUM_THREADS=$t
    for app in ${apps[@]}
    do
        echo "Working on application: ${app}"
        for trial_idx in `seq -s " " -f %04g ${n_trials}`
        do
            echo "Executing trial: ${trial_idx}"
            ./${app} >& "${result_dir}/${app}_nthreads${t}_trial${trial_idx}.txt"
        done 
    done
done

