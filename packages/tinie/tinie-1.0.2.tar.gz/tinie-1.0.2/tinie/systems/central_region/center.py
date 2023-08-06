#!/usr/bin/env python3
"""
This file contains the Center class, which is the parent class of all possible
Center-like classes. Any class that wishes to inherit Center-like properties
would need to have all of the given methods implemented.
"""

from abc import ABC, abstractmethod


class Center(ABC):
    """
    An interface for handling the central quantum-dot region.
    """

    def __init__(self):
        """
        Initializer method.
        """

        self.type = "BaseAbstract"
        self._num_states = 0

    def __instancecheck__(self, instance):
        """
        Checks whether the instance defines the required methods
        for it to pass as an instance of Center.
        """

        type_params_getter = getattr(
            instance, "get_type_sensitive_parameters", None)
        if not callable(type_params_getter):
            return False

        energy_getter = getattr(instance, "get_energies", None)
        if not callable(energy_getter):
            return False

        potential_getter = getattr(instance, "get_potential", None)
        if not callable(potential_getter):
            return False

        state_getter = getattr(instance, "get_state", None)
        if not callable(state_getter):
            return False

        states_getter = getattr(instance, "get_states", None)
        if not callable(states_getter):
            return False

        state_num_getter = getattr(instance, "get_number_of_states", None)
        if not callable(state_num_getter):
            return False

        sliced_state_getter = getattr(instance, "get_sliced_state", None)
        if not callable(sliced_state_getter):
            return False

        sliced_states_getter = getattr(instance, "get_sliced_states", None)
        if not callable(sliced_states_getter):
            return False

        boundary_state_getter = getattr(instance, "get_boundary_state", None)
        if not callable(boundary_state_getter):
            return False

        coordinate_ranges_getter = getattr(
            instance, "get_coordinate_ranges", None)
        if not callable(coordinate_ranges_getter):
            return False

        coordinates_getter = getattr(instance, "get_coordinates", None)
        if not callable(coordinates_getter):
            return False

        slice_coordinates_getter = getattr(
            instance, "get_slice_coordinates", None)
        if not callable(slice_coordinates_getter):
            return False

        boundary_coordinates_getter = getattr(
            instance, "get_boundary_coordinates", None
        )
        if not callable(boundary_coordinates_getter):
            return False

        return True

    @abstractmethod
    def get_type_sensitive_parameters(self):
        """
        Returns parameters specific to some class, which inherits from Center.
        """

        ...

    @abstractmethod
    def get_energies(self):
        """
        Get all eigenenergies.

        Returns
        -------
        energies:   np.ndarray,
                    Eigenenergies of the uncoupled system.

        """

        ...

    @abstractmethod
    def get_potential(self):
        """
        Get potential energy values at the region grid.

        Returns
        -------
        potential:  np.ndarray, rank 2,
                    Value of potential energy on the grid of the region.
        """

        ...

    @abstractmethod
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

        ...

    @abstractmethod
    def get_states(self):
        """
        Get all wavefunctions in an xy-grid.

        Returns
        -------
        states:     np.ndarray of dtype np.complex,
                    shape (x_grid_points, y_grid_points, num_states),
                    All the eigenfunctions in the central region.
        """

        ...

    @abstractmethod
    def get_number_of_states(self):
        """
        Get the number of states in the Center object.

        Returns
        -------
        num_states: int,
                    Number of states in the Center object.
        """

        ...

    @abstractmethod
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

        ...

    @abstractmethod
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

        ...

    @abstractmethod
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

        ...

    @abstractmethod
    def get_coordinate_ranges(self):
        """
        Get the x and y coordinates as 1D arrays.

        Returns
        -------
        x:      np.ndarray, rank 1,
                x-coordinate ranges.

        y:      np.ndarray, rank 1,
                y-coordinate ranges.
        """

        ...

    @abstractmethod
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

        ...

    @abstractmethod
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

        ...

    @abstractmethod
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

        ...
