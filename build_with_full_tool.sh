#!/usr/bin/bash 

build_dir="/g/g17/chapp1/repos/kastors-1.1/build_full_tool"
tool_dir="/g/g17/chapp1/repos/ompt_tools/dagtool/lib"
mkdir -p ${build_dir}
./configure --prefix=${build_dir} CC=clang CXX=clang++ CPPFLAGS=-I/g/g17/chapp1/repos/LLVM-openmp/build/include LDFLAGS=-L${tool_dir} LIBS=-ldagtool 
make clean
make
make install
