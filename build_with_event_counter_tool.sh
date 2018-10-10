#!/usr/bin/bash 

build_dir="/g/g17/chapp1/repos/kastors-1.1/build_event_counter_tool"
tool_dir="/g/g17/chapp1/repos/ompt_tools/event_counter/lib"
mkdir -p ${build_dir}
./configure --prefix=${build_dir} CC=clang CXX=clang++ CPPFLAGS=-I/g/g17/chapp1/repos/LLVM-openmp/build/include LDFLAGS=-L${tool_dir} LIBS=-leventcounter 
make clean
make
make install
