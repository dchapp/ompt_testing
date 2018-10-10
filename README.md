## Scripts for testing OpenMP Tool Interface (OMPT) tools

## OpenMP Tools Under Test
* Skeleton
* Event Counter
* Dependency DAG Analyzer 

## Applications Tested Against
* Barcelona OpenMP Tasks Suite
    * A. Duran, X. Teruel, R. Ferrer, X. Martorell, E. Ayguade. 
      Barcelona OpenMP Tasks Suite: A set of benchmarks targeting the exploitation of task parallelism in OpenMP. 
      In Proceedings of the International Conference on Parallel Processing (ICPP), pp. 124-131, 2009.
    * https://upcommons.upc.edu/bitstream/handle/2117/9801/nbs.pdf
* KASTORS OpenMP Benchmark Suite 
    * P. Virouleau, P. Brunet, F. Broquedis, N. Furmento, S. Thibault, O. Aumage, T. Gautier. 
      Evaluation of OpenMP dependent tasks with the KASTORS benchmark suite. 
      In Proceedings of the International Workshop on OpenMP, pp. 17-29, 2014.
    * These benchmark codes were adapated from the BOTS benchmarks
      and modified to use the `depend` clause in `task` directives
      for fine-grained task synchronization. 
    * https://gforge.inria.fr/projects/kastors/
    * https://hal.inria.fr/hal-01081974
