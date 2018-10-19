#!/usr/bin/env bash 

n_trials=$1

# Apps and inputs
kastors_dir="${HOME}/repos/kastors-1.1/"
apps=("sparselu_task"
      "sparselu_taskdep"
      "strassen_task"
      "strassen_taskdep"
     )
tools=("no"
       "skeleton"
       "event_counter" 
       "ancestry_tracker"
       "dependency_tracker" 
      )
#thread_counts=(1 2 4 8 16 32)
thread_counts=(16 32)

# Copy all executables to staging dir
staging_dir="${HOME}/repos/OMPT_Testing/bin/kastors"
mkdir -p ${staging_dir}
#for bin in ${kastors_dir}/build_no_tool/bin/* 
#do  
#    bin_name=`basename "${bin}"`
#    cp ${bin} ${staging_dir}"/"${bin_name}"_no_tool"
#done

for tool in ${tools[@]}
do 
    for bin in ${kastors_dir}/build_${tool}_tool/bin/*
    do
        bin_name=`basename "${bin}"`
        cp ${bin} ${staging_dir}"/"${bin_name}"_"${tool}
    done
done


# Set up result storage
root_result_dir="${HOME}/repos/OMPT_Testing/results/kastors/overhead_measurements/"
mkdir -p ${root_result_dir}

cd ${kastors_dir}
for app in ${apps[@]}
do 
    echo "Working on application: ${app}"
    #mkdir -p "${root_result_dir}/${apps}"
    for nt in ${thread_counts[@]}
    do 
        echo "Working on ${nt}-thread runs"
        export OMP_NUM_THREADS=${nt}
        #mkdir -p "${root_result_dir}/${apps}/${nt}"
        for tool in ${tools[@]}
        do
            echo "Working on runs with tool: ${tool}"
            ldd ${staging_dir}/${app}_${tool}
            results_dir="${root_result_dir}/${app}/${nt}/${tool}"
            mkdir -p ${results_dir}
            for run in `seq -s " " -f %04g ${n_trials}`
            do
                echo "Run ${run} in progress..."
                export TASK_TREE_DOTFILE="${results_dir}/tree_${run}.dot"
                export TASK_DAG_DOTFILE="${results_dir}/dag_${run}.dot"
                #echo "${staging_dir}/${app}_${tool} >& ${root_result_dir}/${apps}/${nt}/${tool}"
                "${staging_dir}/${app}_${tool}" >& "${results_dir}/${run}.txt"
            done
        done
    done
done


