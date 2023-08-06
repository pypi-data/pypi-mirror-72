#!/usr/bin/env python3
"""
This file contains the Lead class, which is the parent class of all possible
Lead-like classes. Any class that would wish to inherit Lead-like properties
must have all of the given methods implemented. Note that if you wish to
implement a Lead-like object with a defined set of quantum numbers, those
quantum numbers would need to be stored in locally defined containers inside
that daughter class, so that the state_num in the abstract class corresponds
to a unique combination of quantum numbers. Also note that eval_state function
assumes knowledge of the analytical form of the lead wavefunction.
"""

from abc import ABC, abstractmethod


class Lead(ABC):
    def __init__(self):
        """
        Initializer method.
        """

        # Arrays for containing the x-limits, y-limits and E-limits
        self.type = "BaseAbstract"
        self.x = None
        self.y = None
        self.E = None
        self.delta_E = None

        # Magnetic field strength of the system
        self.B = 0.0

        self._num_states = 0

    def __instancecheck__(self, instance):
        """
        Checks whether the instance defines the required methods
        for it to pass as an instance of Lead.
        """

        B_setter = getattr(instance, "set_magnetic_field_strength", None)
        if not callable(B_setter):
            return False

        delta_E_setter = getattr(instance, "set_energy_spacing", None)
        if not callable(delta_E_setter):
            return False

        type_params_getter = getattr(
            instance, "get_type_sensitive_parameters", None)
        if not callable(type_params_getter):
            return False

        energy_getter = getattr(instance, "get_energies", None)
        if not callable(energy_getter):
            return False

        state_point_getter = getattr(instance, "get_state_point", None)
        if not callable(state_point_getter):
            return False

        state_getter = getattr(instance, "get_state", None)
        if not callable(state_getter):
            return False

        state_num_getter = getattr(instance, "get_number_of_states", None)
        if not callable(state_num_getter):
            return False

        boundary_state_getter = getattr(instance, "get_boundary_state", None)
        if not callable(boundary_state_getter):
            return False

        boundary_getter = getattr(instance, "get_boundary", None)
        if not callable(boundary_getter):
            return False

        return True

    @abstractmethod
    def set_magnetic_field_strength(self, B):
        """
        Set a different magnetic field strength.
        """

        ...

    @abstractmethod
    def set_energy_spacing(self, delta_E):
        """
        Set a different energy discretization.
        """

        ...

    @abstractmethod
    def get_quantum_numbers(self, state_num):
        """
        Get quantum numbers l, k of state state_num.

        Parameters
        ----------
        state_num   :   int,
                        State number.
        """

        ...

    @abstractmethod
    def get_type_sensitive_parameters(self):
        """
        Returns parameters specific to some class, which inherits from Lead.
        """

        ...

    @abstractmethod
    def get_energies(self):
        """
        Get all eigenenergies.

        Returns
        -------
        energies:   np.ndarray,
                    Eigenenergies of the lead.

        """

        ...

    @abstractmethod
    def get_state_point(self, x, y, n):
        """
        Evaluates lead wavefunction in a state n at the point x, y.

        Parameters
        ----------
        x       :   float,
                    x-coordinate at which the state is evaluated.

        y       :   float,
                    y-coordinate at which the state is evaluated.

        n        :  int,
                    State index corresponding to a unique set of quantum
                    numbers of a Lead-like object.

        Returns
        -------
        state_val:  complex,
                    Value of the eigenfunction evaluated at the point (x,y).
        """

        ...

    @abstractmethod
    def get_state(self, x_points, y_points, n, mode):
        """
        Returns the lead wavefunction in a state n on a 2D grid
        discretized by x_points and y_points.

        Parameters
        ----------
        x_points    :   int or 1D array,
                        x-axis discretization or x-axis coordinates

        y_points    :   int or 1D array,
                        y-axis discretization or y-axis coordinates

        n           :   int,
                        State index corresponding to a unique set of quantum
                        numbers of a Lead-like object.

        mode        :   str, 'spacing' or 'custom',
                        State evaluation mode. 'spacing' for specifying the
                        spacing in x and y directions and 'custom' for
                        custom grid.

        Returns
        -------
        state:          np.ndarray, dtype=complex,
                        Eigenfunction of the lead evaluated at the specified
                        grid.
        """

        ...

    @abstractmethod
    def get_number_of_states(self):
        """
        Get the number of states in the Lead object.

        Returns
        -------
        num_states: int,
                    Number of states in the Lead object.
        """

        ...

    @abstractmethod
    def get_boundary_state(self, n, num_boundary_points):
        """
        Returns the 1D lead boundary wavefunction array corresponding to the
        energy state number state_num.

        Parameters
        ----------
        num_boundary_points:    int,
                                Number of points in the boundary grid.

        n:              int,
                        State index corresponding to a unique set of quantum
                        numbers of a Lead-like object.

        Returns
        -------
        state:          np.ndarray of shape (num_boundary_points, ),
                        nth eigenfunction of the lead evaluated at the
                        boundary.
        """

        ...

    @abstractmethod
    def get_boundary(self, num_boundary_points):
        """
        Returns the 1D lead boundary ndarray with a discretization
        num_boundary_points.

        Parameters
        -----------
        num_boundary_points:    int
                                Number of points in the boundary grid.

        Returns
        -------
        boundary:       np.ndarray of shape (num_boundary_points, ),
                        Boundary coordinates of the lead.
        """

        ...
