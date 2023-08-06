#!/usr/bin/env python3
"""
This file contains the implementation of the OverlapCoupling class, which
calculates coupling between a FiniteHarmonicLead and the Center region.
Could potentially be extended to include any Lead-like object, but that is a
story for another day. Calculates strong coupling, meaning that the lead and
center regions need to overlap.
"""

from itertools import product

import findiff as fd
import numpy as np
import numpy.polynomial.hermite as her
import progressbar
from findiff.vector import Laplacian
from mpi4py import MPI
from scipy.integrate import simps
from scipy.special import factorial
from tinie.systems.couplings.coupling import Coupling


class OverlapCoupling(Coupling):
    def __init__(self, Center_object, Lead_object, comm):
        """
        Parameters
        ----------
        Center_object:  Center-like object
                        Central region to be used in coupling.

        Lead_object  :  Lead-like object
                        Lead region to be used in coupling.

        comm        :   MPI.COMM_WORLD object,
                        Parallelisation communicator.
        """

        Coupling.__init__(self, Center_object, Lead_object)
        self.type = "Overlap"

        # Container for the coupling matrix once it is calculated:
        self.coupling_matrix = None

        self._comm = comm
        self._is_master_mpi_process = self._comm.rank == 0

        # Stores ranges of overlapping coordinates of center and lead regions:
        self._x_overlap, self._y_overlap = self.get_lead_center_overlap()

        # Stores an array of truth values for extraction of overlapping wave
        # function values via logical indexing in the future and the values
        # of overlapping x and y coordinates:
        (
            self._x_grid_overlap,
            self._y_grid_overlap,
            self._x_points,
            self._y_points,
        ) = self.get_grid_overlap()

        # Initialize flag that would allow to re-use already calculated
        # coupling matrix in case the system has not been altered in any way.
        self._recalculate_coupling = True

        ######################################
        #      DEBUGGING MODE VARIABLES      #
        self._test_wave_function_center = None
        self._test_wave_function_lead = None
        #        PROCEED WITH CAUTION        #
        ######################################

    def get_coupling_matrix_element(self, m, n, test=False):
        """
        Calculates a coupling matrix element corresponding to the lead region
        state number m and the center region state number n.

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

        # Input sanity checks:
        assert isinstance(m, int) and isinstance(
            n, int
        ), "State numbers must be integers"
        assert (
            0 <= m <= self.Lead_object.get_number_of_states() - 1
        ), "Lead state out of bounds"
        assert (
            0 <= n <= self.Center_object.get_number_of_states() - 1
        ), "Center state out of bounds"

        # Check if we are using the test framework or actual itp2d file for the
        # wavefunction:
        if test and self._test_wave_function_center is not None:
            psi_center_n = self._test_wave_function_center

        else:
            psi_center_n = self.Center_object.get_state(n)

        potential = self.Center_object.get_potential()
        potential_slice = potential[
            np.multiply(self._x_grid_overlap, self._y_grid_overlap)
        ]
        potential_slice = np.reshape(
            potential_slice, (len(self._x_points), len(self._y_points))
        )

        # Extract only the values that correspond to overlapping coordinates:
        psi_center_n_slice = psi_center_n[
            np.multiply(self._x_grid_overlap, self._y_grid_overlap)
        ]
        psi_center_n_slice = np.reshape(
            psi_center_n_slice, (len(self._x_points), len(self._y_points))
        )

        # Calculate the nine-point stencil Laplacian:
        dx = self._x_points[1] - self._x_points[0]
        dy = self._y_points[1] - self._y_points[0]

        # Laplacian operator:
        nabla = Laplacian(h=[dx, dy], acc=4)

        fds_psi_center_n = nabla(psi_center_n_slice)

        if test and self._test_wave_function_lead is not None:
            psi_lead_m = self._test_wave_function_lead

        else:
            # Get the lead wavefunction values on the overlapping grid:
            psi_lead_m = self.Lead_object.get_state(
                self._x_points, self._y_points, m, mode="custom"
            )

        # Calculate the coupling value:
        # Kinetic energy-related coupling term:
        cpl_kin = -0.5 * simps(
            simps(
                np.conj(psi_lead_m) * fds_psi_center_n,
                x=self._x_points,
                axis=0),
            x=self._y_points,
            axis=0,
        )

        # Potential energy-related coupling term:
        #######################################################################
        #                      DEBUGGING MODE ONLY CODE                       #
        if test:
            cpl_pot = 0.0
        #                        PROCEED WITH CAUTION                         #
        #######################################################################

        else:
            cpl_pot = simps(
                simps(
                    np.conj(psi_lead_m) * potential_slice * psi_center_n_slice,
                    x=self._x_points,
                    axis=0,
                ),
                x=self._y_points,
                axis=0,
            )

        # Magnetic field-related coupling term:
        d_dx = fd.FinDiff(0, dx, acc=4)
        B = self.Lead_object.B
        x, y = np.meshgrid(self._x_points, self._y_points, indexing="ij")

        cpl_mag = 0.5 * (B ** 2) * simps(
            simps(
                np.conj(psi_lead_m) * np.square(y) * psi_center_n_slice,
                x=self._x_points,
                axis=0,
            ),
            x=self._y_points,
            axis=0,
        ) + 0.5j * B * simps(
            simps(
                np.conj(psi_lead_m) * y * d_dx(psi_center_n_slice),
                x=self._x_points,
                axis=0,
            ),
            x=self._y_points,
            axis=0,
        )

        return cpl_kin + cpl_pot + cpl_mag

    def get_coupling_matrix(self):
        """
        Calculates the coupling matrix between strongly coupled lead and
        center regions.

        Returns
        -------
        coupling_matrix:    np.ndarray of shape
                            (num_lead_states, num_center_states),
                            Coupling matrix.
        """

        if self._recalculate_coupling is False:
            return self.coupling_matrix

        # Getting the numbers of states:
        num_center_states = self.Center_object.get_number_of_states()
        num_lead_states = self.Lead_object.get_number_of_states()

        # Setting up the coupling matrix:
        coupling_matrix = np.zeros(
            (num_lead_states, num_center_states), dtype=complex)

        # Fetching potential energy values:
        potential = self.Center_object.get_potential()
        potential_slice = potential[
            np.multiply(self._x_grid_overlap, self._y_grid_overlap)
        ]
        potential_slice = np.reshape(
            potential_slice, (len(self._x_points), len(self._y_points))
        )

        # Defining the Laplacian operator:
        dx = self._x_points[1] - self._x_points[0]
        dy = self._y_points[1] - self._y_points[0]
        nabla = Laplacian(h=[dx, dy], acc=4)

        d_dx = fd.FinDiff(0, dx, acc=4)
        B = self.Lead_object.B
        x, y = np.meshgrid(self._x_points, self._y_points, indexing="ij")

        state_permutations = [
            s for s in product(
                range(num_center_states),
                range(num_lead_states))]
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
        n_previous = None
        m_previous = None

        for n, m in state_permutations_split[self._comm.rank]:

            if n != n_previous:
                psi_center_n = self.Center_object.get_state(n)

                # Extracting the overlap center region values:
                psi_center_n_slice = psi_center_n[
                    np.multiply(self._x_grid_overlap, self._y_grid_overlap)
                ]
                psi_center_n_slice = np.reshape(
                    psi_center_n_slice, (len(
                        self._x_points), len(
                        self._y_points)))
                fds_psi_center_n = nabla(psi_center_n_slice)
                d_dx_psi_center_n = d_dx(psi_center_n_slice)

            if m != m_previous:
                # Extracting the overlap lead region values:
                psi_lead_m = self.Lead_object.get_state(
                    self._x_points, self._y_points, m, mode="custom"
                )

            cpl = simps(
                simps(
                    np.conj(psi_lead_m)
                    * (
                        -0.5 * fds_psi_center_n
                        + (potential_slice + 0.5 * (B ** 2) * np.square(y))
                        * psi_center_n_slice
                        + 0.5j * B * y * d_dx_psi_center_n
                    ),
                    x=self._x_points,
                    axis=0,
                ),
                x=self._y_points,
                axis=0,
            )

            coupling_matrix[m, n] = cpl

            n_previous = n
            m_previous = m

            if self._is_master_mpi_process:
                counter += 1
                bar.update(counter)

        if self._is_master_mpi_process:
            bar.finish()

        self._recalculate_coupling = False
        self.coupling_matrix = coupling_matrix

        return coupling_matrix

    def get_lead_center_overlap(self):
        """
        Calculates the overlap boundaries between the lead region and
        the central region.

        Returns
        -------
        x_overlap:  list ([x_min, x_max]),
                    Overlap ranges in x-direction.

        y_overlap:  list ([y_min, y_max]),
                    Overlap ranges in y-direction.
        """

        # Extract the boundaries of all regions
        center_bounds_x = [
            self.Center_object.get_coordinates()[0][0, 0],
            self.Center_object.get_coordinates()[0][-1, 0],
        ]
        center_bounds_y = [
            self.Center_object.get_coordinates()[1][0, 0],
            self.Center_object.get_coordinates()[1][0, -1],
        ]
        lead_bounds_x = self.Lead_object.x
        lead_bounds_y = self.Lead_object.y

        # Now we get the overlap boundaries:
        if self.Lead_object.alignment == "up":
            x_overlap = [
                max([center_bounds_x[0], lead_bounds_x[0]]),
                min([center_bounds_x[1], lead_bounds_x[1]]),
            ]
            y_overlap = [lead_bounds_y[0], center_bounds_y[1]]

        elif self.Lead_object.alignment == "down":
            x_overlap = [
                max([center_bounds_x[0], lead_bounds_x[0]]),
                min([center_bounds_x[1], lead_bounds_x[1]]),
            ]
            y_overlap = [center_bounds_y[0], lead_bounds_y[1]]

        elif self.Lead_object.alignment == "right":
            x_overlap = [lead_bounds_x[0], center_bounds_x[1]]
            y_overlap = [
                max([center_bounds_y[0], lead_bounds_y[0]]),
                min([center_bounds_y[1], lead_bounds_y[1]]),
            ]

        else:
            x_overlap = [center_bounds_x[0], lead_bounds_x[1]]
            y_overlap = [
                max([center_bounds_y[0], lead_bounds_y[0]]),
                min([center_bounds_y[1], lead_bounds_y[1]]),
            ]

        assert (
            0 <= x_overlap[1] - x_overlap[0]
        ), "Lead and center regions do not overlap horizontally"
        assert (
            0 <= y_overlap[1] - y_overlap[0]
        ), "Lead and center regions do not overlap vertically"

        return x_overlap, y_overlap

    def get_grid_overlap(self):
        """
        Returns the grid of the truth values of the points in xy axis that
        overlap between grid and the central region. This will be needed to
        extract the required slice of the center wavefunction. Also returns
        the overlapping xy coordinates.

        Returns
        -------
        x_grid_overlap: np.ndarray, dtype=bool, rank 2,
                        Truth value mesh of overlapping x-coordinates.

        y_grid_overlap: np.ndarray, dtype=bool, rank 2,
                        Truth value mesh of overlapping y-coordinates.

        x_points:       np.ndarray, rank 1,
                        Overlapping x-coordinates.

        y_points:       np.ndarray, rank 1,
                        Overlapping y-coordinates.
        """

        # Get the central region grid:
        x_grid, y_grid = self.Center_object.get_coordinates()

        x_points = x_grid[:, 0]
        y_points = y_grid[0, :]

        # Use logical indexing to check which grid points overlap with the
        # lead region:
        x_points_overlap = np.multiply(
            self._x_overlap[0] <= x_points, x_points <= self._x_overlap[1]
        )
        y_points_overlap = np.multiply(
            self._y_overlap[0] <= y_points, y_points <= self._y_overlap[1]
        )

        # Create a grid of logical values for their extraction later on:
        x_grid_overlap, y_grid_overlap = np.meshgrid(
            x_points_overlap, y_points_overlap, indexing="ij"
        )

        # Also get the values of the overlapping coordinates:
        x_points = x_points[x_points_overlap]
        y_points = y_points[y_points_overlap]

        return x_grid_overlap, y_grid_overlap, x_points, y_points

    ###########################################################################
    #                      DEBUGGING MODE ONLY CODE                           #
    def _set_test_wf_qhm(self, m, n):
        """
        Evaluates the 2D quantum harmonic oscillator of the state m, n on the
        points of an itp2d file. Used for testing.
        """

        x, y = self.Center_object.get_coordinate_ranges()

        # Set Hermite polynomial coefficients:
        c = np.zeros((max([m, n]) + 1, max([m, n]) + 1), dtype=float)
        c[m, n] = 1

        # Calculate the wavefunction:
        x_grid, y_grid = np.meshgrid(x, y, indexing="ij")
        norm = 1 / np.sqrt(np.pi * factorial(m) * factorial(n) * 2 ** (m + n))
        psi = (
            norm
            * her.hermval2d(x_grid, y_grid, c)
            / np.exp(0.5 * (x_grid ** 2 + y_grid ** 2))
        )
        psi = np.array(psi, dtype=complex)

        self._test_wave_function_center = psi

    def _set_custom_test_wf_center(self, f):
        """
        Evaluates a custom wavefunction f on the points of an itp2d file.
        Used for testing purposes mainly.
        """

        assert callable(f), "f must be a function"

        x, y = self.Center_object.get_coordinate_ranges()

        # Evaluate the function on the grid.
        psi = np.array([[f(x_point, y_point) for y_point in y]
                        for x_point in x])

        self._test_wave_function_center = psi

    def _set_custom_test_wf_lead(self, g):
        """
        Evaluates a custom wavefunction g on the points of an itp2d file
        and assignes them to a lead wavefunction.
        """

        assert callable(g), "g must be a function"

        # Evaluate the function on the grid.
        psi = np.array(
            [
                [g(x_point, y_point) for y_point in self._y_points]
                for x_point in self._x_points
            ]
        )

        self._test_wave_function_lead = psi

    #                        PROCEED WITH CAUTION                             #
    ###########################################################################
