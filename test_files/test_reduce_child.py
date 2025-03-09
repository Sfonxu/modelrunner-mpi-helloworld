from mpi4py import MPI
import numpy as np

comm = MPI.Comm.Get_parent()
rank = comm.Get_rank()

N = np.array(0, dtype='i')
comm.Bcast([N, MPI.INT], root=0)
OUT = np.array(rank*N, dtype='i')
print(f"My rank is {rank} : {OUT}")
comm.Reduce([OUT, MPI.INT], None, op=MPI.SUM, root=0)

comm.Disconnect()
