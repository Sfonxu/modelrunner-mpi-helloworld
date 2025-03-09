import sys

from modelrunner import ModelBase
from mpi4py import MPI
import numpy as np

"""The idea is that the model holds all the variables and all
   the calculation is defined inside of it """
class CalcModel(ModelBase):
    #arange
    parameters_default = {"N": 100, "maxprocs": 5}
    def __call__(self):
        #act
        comm = MPI.COMM_SELF.Spawn(sys.executable,
                                   args=["test_reduce_child.py"],
                                   maxprocs=self.parameters["maxprocs"])

        N = np.array(self.parameters["N"], dtype='i')
        comm.Bcast([N, MPI.INT], root=MPI.ROOT)
        OUT = np.array(0, dtype='i')
        comm.Reduce(None, [OUT, MPI.INT], op=MPI.SUM, root=MPI.ROOT)
        comm.Disconnect()

        #assert
        comparison_out = 0
        for it in np.arange(self.parameters["maxprocs"]):
            comparison_out += it*self.parameters["N"] 
        assert OUT == comparison_out
        print(OUT)
        return 0;
