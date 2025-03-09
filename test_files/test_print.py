from modelrunner import ModelBase
from mpi4py import MPI

import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

class TestClass(ModelBase):
    parameters_default = {"a": 1}

    def __call__(self):
        for it in np.arange(self.parameters["a"]):
            print(f"Hello World!, it={it}")

model = TestClass()
