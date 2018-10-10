#!/bin/bash 

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
result_dir="${HOME}/repos/OMPT_Testing/kastors_event_counts/"
mkdir -p ${result_dir}

cd ${kastors_bin_dir}
for app in ${apps[@]}
do 
    app_result_dir="${result_dir}/${app}/"
    mkdir -p ${app_result_dir}
    echo "Working on application: ${app}"
    
    for t in ${thread_counts[@]}
    do
        echo "Working on ${t}-thread cases"
        export OMP_NUM_THREADS=$t
        
        for trial_idx in `seq -s " " -f %04g ${n_trials}`
        do
            echo "Executing trial: ${trial_idx}"
            ./${app} >& "${app_result_dir}/nthreads${t}_trial${trial_idx}.txt"
        done 

    done

done

