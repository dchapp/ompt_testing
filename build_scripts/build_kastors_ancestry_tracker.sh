#!/usr/bin/env bash

kastors_dir="/g/g17/chapp1/repos/kastors-1.1/"
build_dir="${kastors_dir}/build_ancestry_tracker_tool"
tool_dir="/g/g17/chapp1/repos/ompt_tools/ancestry_tracker/lib"
cd ${kastors_dir}
mkdir -p ${build_dir}
make clean
./configure --prefix=${build_dir} CC=clang CXX=clang++ CPPFLAGS=-I/g/g17/chapp1/repos/LLVM-openmp/build/include LDFLAGS=-L${tool_dir} LIBS=-lancestry_tracker
make
make install
