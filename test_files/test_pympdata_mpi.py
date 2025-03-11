from modelrunner import ModelBase

import numba
import numpy as np
import matplotlib.pyplot as plt

import numba_mpi as mpi
from PyMPDATA import ScalarField, Stepper, VectorField, Solver, Options
from PyMPDATA.boundary_conditions import Periodic
from PyMPDATA.impl.domain_decomposition import make_subdomain
from PyMPDATA.impl.enumerations import INNER, OUTER

from PyMPDATA_MPI.domain_decomposition import mpi_indices
from PyMPDATA_MPI.mpi_periodic import MPIPeriodic
subdomain = make_subdomain(jit_flags={})

class Scenario():
    """Test case based on [Arabas et al. 2014]"""
    
    def __init__(
            self,
            *,
            mpdata_options,
            n_threads,
            grid=(64,32),
            rank,
            size,
            courant_field_multiplier,
            mpi_dim,
    ):
        halo = mpdata_options.n_halo

        xyi = mpi_indices(grid=grid, rank=rank, size=size, mpi_dim=mpi_dim)
        nx, ny = xyi[mpi_dim].shape

        mpi_periodic = MPIPeriodic(size=size, mpi_dim=mpi_dim)
        periodic = Periodic()
        boundary_conditions = (
            mpi_periodic if mpi_dim == OUTER else periodic,
            mpi_periodic if mpi_dim == INNER else periodic,
        )
        advectee = ScalarField(
            data=self.initial_condition(*xyi, (64,32)),
            halo=halo,
            boundary_conditions=boundary_conditions,
        )

        advector = VectorField(
            data=(
                np.full((nx+1,ny), courant_field_multiplier[0]),
                np.full((nx,ny+1), courant_field_multiplier[1]),
            ),
            halo=halo,
            boundary_conditions=boundary_conditions,
        )
        stepper = Stepper(
            options=mpdata_options,
            n_dims=2,
            n_threads=n_threads,
            left_first=tuple([rank%2 ==0]*2),
            buffer_size=(
                (ny if mpi_dim == OUTER else nx + 2 * halo) * halo
                ) * 2 * 2 * (2 if mpi_dim == OUTER else n_threads),
            )
        self.solver = Solver(stepper=stepper, advectee=advectee, advector=advector)
    
    @staticmethod
    def initial_condition(xi, yi, grid):
        """returns advectee array for a given grid indices"""
        # pylint: disable=invalid-name
        nx, ny = grid
        x0 = nx / 2
        y0 = ny / 2

        psi = np.exp(
            -((xi + 0.5 - x0) ** 2) / (2 * (nx / 10) ** 2)
            - (yi + 0.5 - y0) ** 2 / (2 * (ny / 10) ** 2)
        )
        return psi
    
    
    def advance(self, output_steps, mpi_range):
        """Logic for performing simulation. Returns wall time of one timestep (in clock ticks)"""
        steps_done = 0
        wall_time = 0
        for index, output_step in enumerate(output_steps):
            n_steps = output_step - steps_done
            if n_steps > 0:
                wall_time_per_timestep = self._solver_advance(n_steps=n_steps)
                wall_time += wall_time_per_timestep * n_steps
                steps_done += n_steps
                data = self.solver.advectee.get()
                plt.plot(data)
                plt.savefig(f"../output_files/frame_{n_steps}.jpeg")
                plt.close()
        return wall_time

    def _solver_advance(self,n_steps):
        return self.solver.advance(n_steps=n_steps)
        
    def __getitem__(self, _):
        return self.solver.advectee.get()


class Model(ModelBase):
    parameters_default = {"options": {"n_iters": 1}, "courant_field_multiplier": (0.25,0.5), "output_steps": range(0,24,2)}

    def __call__(self):
        mpdata_options = Options(**self.parameters["options"])
        n_threads = numba.get_num_threads()
        grid = (64, 32)
        rank = mpi.rank() 
        size = mpi.size()
        courant_field_multiplier = self.parameters["courant_field_multiplier"]
        mpi_dim = INNER

        model = Scenario(
            mpdata_options=mpdata_options,
            n_threads=n_threads,
            grid=(64,32),
            rank=rank,
            size=size,
            courant_field_multiplier=courant_field_multiplier,
            mpi_dim=mpi_dim
        )

        mpi_range = slice(
                    *subdomain(grid[mpi_dim], rank, size)
                )
        model.advance(self.parameters["output_steps"], mpi_range)
