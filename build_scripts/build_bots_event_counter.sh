#!/usr/bin/env bash

bots_root="${HOME}/repos/bots/"
#bots_make_config="${bots_root}/config/make.config"
omp="${HOME}/repos/LLVM-openmp/build/"
event_counter_linkflags="-L${HOME}/repos/ompt_tools/event_counter/lib/ -leventcounter"
config_customizer="./set_bots_config.py" 
${config_customizer} ${bots_root} --omp="${omp}" --linkflags="${event_counter_linkflags}"
cd ${bots_root}
make clean
make
