from modelrunner import ModelBase
from mpi4py import MPI

import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

class TestClass(ModelBase):
    parameters_default = {"a": 1}

    def __call__(self):
        text_out = []
        for it in np.arange(self.parameters["a"]):
            text_out.append(f"Hello World!, it={it}")
        return text_out

model = TestClass()
