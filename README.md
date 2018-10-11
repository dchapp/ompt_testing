# Scripts for testing OpenMP Tool Interface (OMPT) tools

## Overview

### OpenMP Tools Under Test
* Skeleton
* Event Counter (https://github.com/TauferLab/OMPT_event_counter)
* Dependency DAG Analyzer 

### Applications Tested Against
* Barcelona OpenMP Tasks Suite (https://github.com/bsc-pm/bots)
    * A. Duran, X. Teruel, R. Ferrer, X. Martorell, E. Ayguade. 
      Barcelona OpenMP Tasks Suite: A set of benchmarks targeting the exploitation of task parallelism in OpenMP. 
      In Proceedings of the International Conference on Parallel Processing (ICPP), pp. 124-131, 2009.
    * https://upcommons.upc.edu/bitstream/handle/2117/9801/nbs.pdf
* KASTORS OpenMP Benchmark Suite (https://gitlab.inria.fr/openmp/kastors) 
    * P. Virouleau, P. Brunet, F. Broquedis, N. Furmento, S. Thibault, O. Aumage, T. Gautier. 
      Evaluation of OpenMP dependent tasks with the KASTORS benchmark suite. 
      In Proceedings of the International Workshop on OpenMP (IWOMP), pp. 17-29, 2014.
    * These benchmark codes were adapated from the BOTS benchmarks
      and modified to use the `depend` clause in `task` directives
      for fine-grained task synchronization. 
    * https://gforge.inria.fr/projects/kastors/
    * https://hal.inria.fr/hal-01081974

## Popper

This repository contains [Popper](https://github.com/systemslab/popper)
pipelines. To show a list of available pipelines using the
[`popper` CLI tool](https://github.com/systemslab/popper):

```bash
cd OMPT_Testing
popper ls
```

to execute one of the pipelines:

```bash
popper run <pipeline-name>
```

where `<pipeline-name>` is one of the pipelines in the repository.
For more on what other information from this repository is available,
you can run:

```bash
popper --help
```
