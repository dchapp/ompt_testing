#!/usr/bin/env bash 

n_trials=$1

# Apps and inputs
kastors_bin_dir="${HOME}/repos/kastors-1.1/build_event_counter_tool/bin"
apps=("sparselu_task"
      "sparselu_taskdep"
      "strassen_task"
      "strassen_taskdep"
     )
thread_counts=(1 2 4 8 16 32)

# Set up result storage
root_result_dir="${HOME}/repos/OMPT_Testing/results/kastors/event_counts/"
mkdir -p ${root_result_dir}

cd ${kastors_bin_dir}
for app in ${apps[@]}
do 
    echo "Working on application: ${app}"
    
    for n_threads in ${thread_counts[@]}
    do
        echo "Working on ${n_threads}-thread cases"
        export OMP_NUM_THREADS=${n_threads}
        result_dir="${root_result_dir}/${app}/data/${n_threads}/"
        mkdir -p ${result_dir}
        
        for trial_idx in `seq -s " " -f %04g ${n_trials}`
        do
            echo "Executing trial: ${trial_idx}"
            ./${app} >& "${result_dir}/${trial_idx}.txt"
        done 

    done

done

