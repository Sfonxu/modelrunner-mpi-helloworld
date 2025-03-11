# Examples pymodelrunner usgae in an mpi enviroment
## Currently there are 3 working examples implemented
* Printing a simple message on every worker (one param, a = # of printed messages)
* MPI_REDUCE calculation (two params, N = multiplier used in calculation, maxprocs = maximal number of workers)
* PyMPDATA_MPI carteisan 2D calculation based on [Arabas et al. 2014](https://doi.org/10.3233/SPR-140379) (three params, options = PyMPDATA options dictionary, courant field multiplier, output steps = # of time steps to calculate) 
