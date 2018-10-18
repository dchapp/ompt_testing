#!/usr/bin/env python3

import os
import re
import glob
import argparse
import shutil 
import pprint 

c_flags_pattern = re.compile("^OMPC_FLAGS=.+$")
link_flags_pattern = re.compile("^OMPLINK_FLAGS=.+$")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bots")
    parser.add_argument("--omp", nargs="?", default="/g/g17/chapp1/repos/LLVM-openmp/build/")
    parser.add_argument("--cflags", nargs="?", default=None, type=str)
    parser.add_argument("--linkflags", nargs="?", default=None, type=str)
    args = parser.parse_args()

    # Read in contents of existing make.config file
    bots_dir = os.path.abspath(args.bots)
    base_config_path = bots_dir + "/config/make.config"
    base_config_lines = []
    print("Reading contents of base config file: %s" % base_config_path) 
    with open(base_config_path, "r") as config:
        base_config_lines = config.readlines()
  
    # Rename base make.config so we can restore it after the build is done
    temp_config_path = base_config_path + ".tmp" 
    print("Moving base config from %s to %s" % (base_config_path, temp_config_path))
    #shutil.move(base_config_path, temp_config_path)

    # Write a new make.config file with specified link flags 
    new_config_path = bots_dir + "/config/make.config.new"
    print("Writing new config path to %s" % new_config_path)
    with open(new_config_path, "w") as new_config:
        for line in base_config_lines:
            if c_flags_pattern.match(line):
                omp_include_flag = "-I/" + args.omp + "/include"
                c_flags_line = "OMPCFLAGS= " + omp_include_flag + " "
                if args.cflags:
                    c_flags_line += args.cflags
                c_flags_line += "\n"
                new_config.write(c_flags_line)
            elif link_flags_pattern.match(line):
                omp_link_flag = "-L/" + args.omp + "/lib" 
                link_flags_line = "OMPLINK_FLAGS= " + omp_link_flag + " "
                if args.linkflags:
                    link_flags_line += args.linkflags
                link_flags_line += "\n"
                new_config.write(link_flags_line)
            else:
                new_config.write(line)
    
