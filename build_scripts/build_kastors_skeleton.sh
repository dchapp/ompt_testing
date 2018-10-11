#!/usr/bin/bash 

kastors_dir="/g/g17/chapp1/repos/kastors-1.1/"
build_dir="${kastors_dir}/build_skeleton_tool"
tool_dir="/g/g17/chapp1/repos/ompt_tools/skeleton/lib"
cd ${kastors_dir} 
mkdir -p ${build_dir}
./configure --prefix=${build_dir} CC=clang CXX=clang++ CPPFLAGS=-I/g/g17/chapp1/repos/LLVM-openmp/build/include LDFLAGS=-L${tool_dir} LIBS=-lskeletontool 
make clean
make
make install
