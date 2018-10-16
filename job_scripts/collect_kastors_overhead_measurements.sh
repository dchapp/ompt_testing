#!/usr/bin/env bash 

n_trials=$1

# Apps and inputs
kastors_dir="${HOME}/repos/kastors-1.1/"
apps=("sparselu_task"
      "sparselu_taskdep"
      "strassen_task"
      "strassen_taskdep"
     )
tools=("skeleton"
       "event_counter" 
       "ancestry_tracker"
      )
thread_counts=(1 2 4 8 16 32)

# Copy all executables to staging dir
staging_dir="${HOME}/repos/OMPT_Testing/bin/kastors"
mkdir -p ${staging_dir}
for bin in ${kastors_dir}/build_no_tool/bin/* 
do  
    bin_name=`basename "${bin}"`
    cp ${bin} ${staging_dir}"/"${bin_name}"_no_tool"
    #echo ${bin} ${staging_dir}"/"${bin_name}"_no_tool"
done

exit

for tool in ${tools[@]}
do 
    for bin in ${kastors_dir}/build_${tool}_tool/bin/*
    do
        bin_name=`basename "${bin}"`
        cp ${bin} ${staging_dir}"/"${bin_name}"_"${tool}
        #echo ${bin} ${staging_dir}"/"${bin}"_"${tool}
    done
done


# Set up result storage
root_result_dir="${HOME}/repos/OMPT_Testing/results/kastors/overhead_measurements/"
mkdir -p ${root_result_dir}

cd ${kastors_dir}
for tool in ${tools[@]}
do 
    for app in ${apps[@]}
    do
        for nt in ${thread_count[@]}
        do 
            
        done
    done
done

