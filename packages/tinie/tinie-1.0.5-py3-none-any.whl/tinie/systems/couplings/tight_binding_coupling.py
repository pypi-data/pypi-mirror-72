#!/usr/bin/env python3
"""
This file contains the implementation of the TightBindingCoupling class, which
calculates coupling between a Lead and the Center region using a
juxtaposition of Monte-Carlo methods and Simpson's rule. Calculates weak
coupling, meaning that lead and center regions must not overlap.
"""

from itertools import product

import numpy as np
import vegas
import progressbar
from scipy.integrate import simps
from tinie.systems.couplings.coupling import Coupling


class TightBindingCoupling(Coupling):
    def __init__(self, Center_object, Lead_object, comm):
        """
        Parameters
        ----------
        Center_object:  Center-like object
                        Central region to be used in coupling.

        Lead_object  :  Lead-like object
                        Lead region to be used in coupling.
        """

        Coupling.__init__(self, Center_object, Lead_object)
        self.type = "TightBinding"

        self._comm = comm
        self._is_master_mpi_process = self._comm.rank == 0

        if Lead_object.alignment == "up" or Lead_object.alignment == "down":
            self._max_length_lead = Lead_object.y[1] - Lead_object.y[0]
            self._max_length_center = (
                Center_object.get_coordinates()[1][0, -1]
                - Center_object.get_coordinates()[1][0, 0]
            )

        else:
            self._max_length_lead = Lead_object.x[1] - Lead_object.x[0]
            self._max_length_center = (
                Center_object.get_coordinates()[0][-1, 0]
                - Center_object.get_coordinates()[0][0, 0]
            )

        self._length_lead = self._max_length_lead
        self._length_center = self._max_length_center

        # Initialize flag that would allow to re-use already calculated
        # coupling matrix in case the system has not been altered in any way.
        self._recalculate_coupling = True

    def get_coupling_matrix_element(self, m, n):
        """
        Calculates a coupling matrix element corresponding to the lead region
        state number m and the center region state number n. Only use for
        testing purposes, for loop iteration over all the lead/center
        states is not as efficient as get_coupling_matrix command.

        Parameters:
        -----------
        m       :   int,
                    Lead object state number

        n       :   int,
                    Center object state number

        Returns:
        --------
        coupling_value: complex,
                        Value of the coupling matrix for the following states.
        """
        assert isinstance(m, int) and isinstance(
            n, int
        ), "State numbers must be integers"

        Lead_obj = self.Lead_object
        Center_obj = self.Center_object

        assert 0 <= m <= Lead_obj.get_number_of_states() - 1, "Lead state out of bounds"
        assert (
            0 <= n <= Center_obj.get_number_of_states() - 1
        ), "Center state out of bounds"

        x_grid_center, y_grid_center = Center_obj.get_slice_coordinates(
            self._length_center, Lead_obj.alignment
        )

        g_re = np.zeros((len(x_grid_center[:, 0]), len(y_grid_center[0, :])))
        g_im = np.zeros((len(x_grid_center[:, 0]), len(y_grid_center[0, :])))

        for i, xtilde in enumerate(x_grid_center[:, 0]):
            for j, ytilde in enumerate(y_grid_center[0, :]):
                int_re = vegas.Integrator([Lead_obj.x, Lead_obj.y])
                int_im = vegas.Integrator([Lead_obj.x, Lead_obj.y])

                @vegas.batchintegrand
                def f_re(x):
                    res = np.real(
                        Lead_obj.get_state(x[:, 0], x[:, 1], m, mode='mc') / \
                        ((x[:, 0] - xtilde) ** 2 + (x[:, 1] - ytilde) ** 2) * \
                        np.exp(0.5j * Lead_obj.B * (x[:, 0] - xtilde) * (
                                    x[:, 1] + ytilde)))
                    res = res.copy(order='C')
                    return res

                @vegas.batchintegrand
                def f_im(x):
                    res = np.imag(
                        Lead_obj.get_state(x[:, 0], x[:, 1], m, mode='mc') / \
                        ((x[:, 0] - xtilde) ** 2 + (x[:, 1] - ytilde) ** 2) * \
                        np.exp(0.5j * Lead_obj.B * (x[:, 0] - xtilde) * (
                                    x[:, 1] + ytilde)))
                    res = res.copy(order='C')
                    return res

                int_re(f_re, nitn=5, neval=1000)
                int_im(f_im, nitn=5, neval=1000)

                res_re = int_re(f_re, nitn=10, neval=1000)
                res_im = int_im(f_im, nitn=10, neval=1000)
                g_re[i, j] = res_re.mean
                g_im[i, j] = res_im.mean

        g = g_re + 1j * g_im

        psi_center_n = Center_obj.get_sliced_state(
            n, self._length_center, Lead_obj.alignment
        )

        f = np.multiply(np.conjugate(psi_center_n), g)
        norm = Lead_obj.normalization(m)

        coupling_value = (-0.5 * norm * simps(simps(f,
                                                    x_grid_center[:, 0], axis=0), y_grid_center[0, :], axis=0))

        return coupling_value

    def get_coupling_matrix(self):
        """
        Calculates the coupling matrix over the defined boundary region using
        the Monte Carlo integration and Simpson's rule.

        Returns
        -------
        coupling_matrix:    np.ndarray of shape
                            (num_lead_states, num_center_states),
                            Coupling matrix.
        """

        # Check if the matrix has already been calculated for the given
        # parameters.
        if self._recalculate_coupling is not True:
            return self.coupling_matrix

        # Setting up parameters
        Center_obj = self.Center_object
        Lead_obj = self.Lead_object
        num_center_states = Center_obj.get_number_of_states()
        num_lead_states = Lead_obj.get_number_of_states()
        x_grid_center, y_grid_center = Center_obj.get_slice_coordinates(
            self._length_center, Lead_obj.alignment
        )

        if Lead_obj.boundary_type == "dir":
            delta = np.pi / 2

        else:
            delta = 0.0

        # Initialize the coupling_matrix
        coupling_matrix = np.zeros(
            (num_lead_states, num_center_states), dtype=complex)

        state_permutations = [
            s for s in product(
                range(num_lead_states),
                range(num_center_states))]
        state_permutations_split = np.array_split(
            state_permutations, self._comm.size)

        if self._is_master_mpi_process:
            bar = progressbar.ProgressBar(
                widgets=[
                    " [",
                    progressbar.Timer(),
                    "] ",
                    progressbar.Bar(),
                    " (",
                    progressbar.ETA(),
                    ") ",
                ],
                max_value=(len(state_permutations_split[self._comm.rank])),
            )
            counter = 0
            bar.start()

        # Summation over the states:
        m_previous = None
        n_previous = None

        for m, n in state_permutations_split[self._comm.rank]:

            if m != m_previous:
                norm = Lead_obj.normalization(m)
                g_re = np.zeros((len(x_grid_center[:, 0]), len(y_grid_center[0, :])))
                g_im = np.zeros((len(x_grid_center[:, 0]), len(y_grid_center[0, :])))

                for i, xtilde in enumerate(x_grid_center[:, 0]):
                    for j, ytilde in enumerate(y_grid_center[0, :]):
                        int_re = vegas.Integrator([Lead_obj.x, Lead_obj.y])
                        int_im = vegas.Integrator([Lead_obj.x, Lead_obj.y])

                        @vegas.batchintegrand
                        def f_re(x):
                            res = np.real(Lead_obj.get_state(x[:, 0], x[:, 1], m, mode='mc') / \
                                   ((x[:, 0] - xtilde) ** 2 + (x[:, 1] - ytilde) ** 2) * \
                                           np.exp(0.5j * Lead_obj.B * (x[:, 0] - xtilde) * (x[:, 1] + ytilde)))
                            res = res.copy(order='C')
                            return res

                        @vegas.batchintegrand
                        def f_im(x):
                            res = np.imag(Lead_obj.get_state(x[:, 0], x[:, 1], m, mode='mc') / \
                                   ((x[:, 0] - xtilde) ** 2 + (x[:, 1] - ytilde) ** 2) * \
                                           np.exp(0.5j * Lead_obj.B * (x[:, 0] - xtilde) * (x[:, 1] + ytilde)))
                            res = res.copy(order='C')
                            return res

                        int_re(f_re, nitn=5, neval=1000)
                        int_im(f_im, nitn=5, neval=1000)

                        res_re = int_re(f_re, nitn=10, neval=1000)
                        res_im = int_im(f_im, nitn=10, neval=1000)
                        g_re[i, j] = res_re.mean
                        g_im[i, j] = res_im.mean

                g = g_re + 1j * g_im

            if n != n_previous:
                psi_center_n = Center_obj.get_sliced_state(
                    n, self._length_center, Lead_obj.alignment
                )

                f = np.multiply(np.conjugate(psi_center_n), g)

                coupling_value = (
                    -0.5
                    * norm
                    * simps(
                        simps(f, x_grid_center[:, 0], axis=0),
                        y_grid_center[0, :],
                        axis=0,
                    )
                )

            coupling_matrix[m, n] = coupling_value

            m_previous = m
            n_previous = n

            if self._is_master_mpi_process:
                counter += 1
                bar.update(counter)

        if self._is_master_mpi_process:
            bar.finish()

        self._recalculate_coupling = False
        self.coupling_matrix = coupling_matrix

        return coupling_matrix

    def set_lead_and_center_slices(self, length_center, length_lead):
        """
        Limits the region integration of the central and lead regions down to
        length_center and length_lead correspondingly.

        Parameters:
        -----------
        length_center:  float, 0 <= length_center <= self.max_length_center
                        Length of the central region to be integrated over.

        length_lead  :  float, 0 <= length_lead <= self.max_length_lead
                        Length of the lead region to be integrated over.
        """

        # Input sanity checks:
        assert (
            0 <= length_center <= self._max_length_center
        ), "Error: Specified length of central region not in suitable range"
        assert (
            0 <= length_lead <= self._max_length_lead
        ), "Error: Specified length of lead region not in suitable range"

        if length_center != self._length_center or length_lead != self._length_lead:
            self._recalculate_coupling = True
            self._length_lead = length_lead
            self._length_center = length_center
