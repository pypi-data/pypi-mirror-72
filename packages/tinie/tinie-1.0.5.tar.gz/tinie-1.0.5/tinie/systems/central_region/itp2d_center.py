#!/usr/bin/env python3
"""
This file contains the implementation of Itp2dCenter class, which reads the
data of the central region obtained through itp2d and processes it for use
in transport calculations.
"""

from pathlib import Path

import h5py
import numpy as np
from tinie.systems.central_region.center import Center


class Itp2dCenter(Center):
    def __init__(self, filename, states=(0, -1)):
        """
        Initializer method.

        Parameters
        ----------
        filename   :    string,
                        Path to itp2d save file.

        states     :    tuple,
                        State numbers to import.
        """

        Center.__init__(self)
        self.type = "Itp2dCenter"
        self.filename = filename
        self.states_to_import = states

        self._num_states = self.states_to_import[1] - \
            self.states_to_import[0] + 1
        self._check_input_sanity()

    def _check_input_sanity(self):
        """
        Checks sanity of input arguments with respect to the calculated data.
        Raises Exceptions if something is awry.
        """

        # Check that save file exists
        file_path = Path(self.filename)
        if not file_path.is_file():
            raise RuntimeError(
                "Given path ("
                + repr(file_path.absolute())
                + " to itp2d savefile does not exist!"
            )

        # Check number of states in the itp2d simulation and compare to
        # what we want to import
        with h5py.File(self.filename, "r") as hfile:
            attrs = hfile.attrs

            num_states = attrs["num_states"]
            num_converged_states = attrs["num_converged"]

            if self.states_to_import[1] == -1:
                self.states_to_import = (
                    self.states_to_import[0], num_states - 1)

            if self.states_to_import[1] >= num_states:
                raise RuntimeError("Last state too high.")

            if self.states_to_import[0] >= num_states:
                raise RuntimeError("First state too high.")

            if self.states_to_import[0] > self.states_to_import[1]:
                raise RuntimeError("Requested state interval not in order.")

            if self.states_to_import[1] >= num_converged_states:
                raise UserWarning(
                    "Imported higher states than were converged by itp2d."
                )

    def _get_slice_limits(self, width, side):
        """
        Return indices for selecting a slice of the wavefunction on one
        side of the rectangular coordinate grid.
        """

        x, y = self.get_coordinate_ranges()

        # Get the ranges
        if side == "up" or side == "down":

            if width > y[-1] - y[0]:
                raise RuntimeError("Boundary width exceeds region width.")

            ind_x0 = 0
            ind_x1 = len(x)

            if side == "down":
                ind_y0 = 0
                ind_y1 = np.where((y - y[0]) <= width)[0][-1] + 1

            elif side == "up":
                ind_y0 = np.where((y[-1] - y) <= width)[0][0]
                ind_y1 = len(y)

        elif side == "left" or side == "right":

            if width > x[-1] - x[0]:
                raise RuntimeError("Boundary width exceeds region width.")

            ind_y0 = 0
            ind_y1 = len(y)

            if side == "left":
                ind_x0 = 0
                ind_x1 = np.where((x - x[0]) <= width)[0][-1] + 1

            elif side == "right":
                ind_x0 = np.where((x[-1] - x) <= width)[0][0]
                ind_x1 = len(x)

        else:
            raise RuntimeError("`side` was not up/down/left/right")

        return (ind_x0, ind_x1), (ind_y0, ind_y1)

    def get_type_sensitive_parameters(self):
        """
        Returns parameters specific to Itp2dCenter.
        """

        return str({"filename": self.filename,
                    "states_to_import": self.states_to_import})

    def get_energies(self):
        """
        Get all eigenenergies.

        Returns
        -------
        energies:   np.ndarray,
                    Eigenenergies of the uncoupled system

        """

        with h5py.File(self.filename, "r") as hfile:
            return hfile["final_energies"][
                self.states_to_import[0]: self.states_to_import[1] + 1
            ]

    def get_number_of_states(self):
        """
        Get the number of states in the Center object.

        Returns
        -------
        num_states: int,
                    Number of states in the Center object.
        """

        return self._num_states

    def get_potential(self):
        """
        Get potential energy values at the region grid.

        Returns
        -------
        potential:  np.ndarray, rank 2,
                    Value of potential energy on the grid of the region.
        """

        with h5py.File(self.filename, "r") as hfile:
            return hfile["potential_values"][()]

    def get_state(self, n):
        """
        Get nth energy eigenstate.

        Parameters
        ----------
        n:          int,
                    State number.

        Returns
        -------
        state:      np.ndarray of dtype np.complex,
                    shape(x_grid_points, y_grid_points)
                    nth eigenfunction of the central region.
        """

        assert n < self._num_states, "Not so many states loaded"
        with h5py.File(self.filename, "r") as hfile:
            return np.swapaxes(hfile["states"][-1]
                               [n - self.states_to_import[0]], 0, 1)

    def get_states(self):
        """
        Get all wavefunctions in an xy-grid.

        Returns
        -------
        states:     np.ndarray of dtype np.complex,
                    shape (x_grid_points, y_grid_points, num_states),
                    All the eigenfunctions in the central region.
        """

        with h5py.File(self.filename, "r") as hfile:
            return np.swapaxes(
                hfile["states"][-1][
                    self.states_to_import[0]: self.states_to_import[1] + 1, :, :
                ],
                0,
                2,
            )

    def get_sliced_state(self, n, width, side):
        """
        Get a boundary slice of a state.

        Parameters
        ----------
        n:          int,
                    State number.

        width:      float,
                    Width of the slice.

        side:       string ('up'/'down'/'left'/'right'),
                    Which boundary to take.

        Returns
        -------
        state:      np.ndarray of dtype np.complex,
                    nth eigenfunction of the central region sliced as
                    requested.
        """

        xi, yi = self._get_slice_limits(width, side)
        with h5py.File(self.filename, "r") as hfile:
            return np.swapaxes(
                hfile["states"][-1][
                    n - self.states_to_import[0], yi[0]: yi[1], xi[0]: xi[1]
                ],
                0,
                1,
            )

    def get_sliced_states(self, width, side):
        """
        Get a boundary slice of all the states.

        Parameters
        ----------
        width:      float,
                    Width of the slice.

        side:       string ('up'/'down'/'left'/'right'),
                    Which boundary to take.

        Returns
        -------
        states:     np.ndarray of dtype np.complex,
                    shape (x_grid_slice, y_grid_slice, num_states),
                    All the eigenfunctions in the central region sliced as
                    requested.
        """

        xi, yi = self._get_slice_limits(width, side)
        with h5py.File(self.filename, "r") as hfile:
            return np.swapaxes(
                hfile["states"][-1][
                    self.states_to_import[0]: self.states_to_import[1] + 1,
                    yi[0]: yi[1],
                    xi[0]: xi[1],
                ],
                0,
                2,
            )

    def get_boundary_state(self, n, side):
        """
        Get the wavefunction corresponding to the state number num_state
        evaluated at the boundary of alignment side (up/down/left/right).

        Parameters
        ----------
        side:       string ('up'/'down'/'left'/'right'),
                    Boundary side.

        n:          int,
                    Number of state we wish to extract.

        Returns
        -------
        state:      np.ndarray, rank 1,
                    nth eigenfunction at a boundary.

        """

        with h5py.File(self.filename, "r") as hfile:
            if side == "left":
                return np.squeeze(
                    hfile["states"][-1][n - self.states_to_import[0], :, 0]
                )
            elif side == "right":
                return np.squeeze(
                    hfile["states"][-1][n - self.states_to_import[0], :, -1]
                )
            elif side == "down":
                return np.squeeze(
                    hfile["states"][-1][n - self.states_to_import[0], 0, :]
                )
            else:
                return np.squeeze(
                    hfile["states"][-1][n - self.states_to_import[0], -1, :]
                )

    def get_coordinate_ranges(self):
        """
        Returns the x- and y-coordinate ranges (1D arrays)
        """

        with h5py.File(self.filename, "r") as hfile:
            attrs = hfile.attrs

            grid_delta = attrs["grid_delta"]
            grid_pts_x = attrs["grid_sizex"]
            grid_pts_y = attrs["grid_sizey"]

            # 1D ranges
            x = 0.5 * (2 * np.arange(grid_pts_x) + 1 - grid_pts_x) * grid_delta
            y = 0.5 * (2 * np.arange(grid_pts_y) + 1 - grid_pts_y) * grid_delta

            return x, y

    def get_coordinates(self):
        """
        Get coordinate meshes in a grid corresponding to the states.

        Returns
        -------
        X:      np.ndarray, shape (x_points, y_points),
                x-coordinate mesh grid.

        Y:      np.ndarray, shape (x_points, y_points),
                y-coordinate mesh grid.
        """

        x, y = self.get_coordinate_ranges()

        # Set up meshgrid
        X, Y = np.meshgrid(x, y, indexing="ij")
        return X, Y

    def get_slice_coordinates(self, width, side):
        """
        Get coordinate meshes for the boundary slice.

        Parameters
        ----------
        width:      float,
                    Width of the slice.

        side:       string ('up'/'down'/'left'/'right'),
                    Which boundary to take.

        Returns
        -------
        x:      np.ndarray, shape (x_points, y_points),
                x-coordinate slice mesh grid.

        y:      np.ndarray, shape (x_points, y_points),
                y-coordinate slice mesh grid.

        """

        xi, yi = self._get_slice_limits(width, side)
        X, Y = self.get_coordinates()
        return X[xi[0]: xi[1], yi[0]: yi[1]], Y[xi[0]: xi[1], yi[0]: yi[1]]

    def get_boundary_coordinates(self, side):
        """
        Get xy-coordinates corresponding to the boundary of the side
        "side" (up/down/left/right).

        Parameters
        ----------
        side:       string,
                    Boundary side.

        Returns
        -------
        bound:      np.ndarray, rank 1,
                    Boundary coordinates.
        """

        if side == "up" or side == "down":
            return self.get_coordinate_ranges()[0]
        else:
            return self.get_coordinate_ranges()[1]
