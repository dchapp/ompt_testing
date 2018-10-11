#!/usr/bin/bash 

kastors_dir="/g/g17/chapp1/repos/kastors-1.1/"
build_dir="${kastors_dir}/build_no_tool"
cd ${kastors_dir}
mkdir -p ${build_dir}
./configure --prefix=${build_dir} CC=clang CXX=clang++ CPPFLAGS=-I/g/g17/chapp1/repos/LLVM-openmp/build/include
make clean
make
make install
