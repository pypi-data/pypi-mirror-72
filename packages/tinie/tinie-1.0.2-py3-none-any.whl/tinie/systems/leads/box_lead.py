#!/usr/bin/env python3
"""
This file contains the implementation of the BoxLead class, which
models a rectangular lead with dimensions [x_min, x_max] by [y_min, y_max].
Probe energy ranges are set as [E_min, E_max]. The wavefunction of the lead
corresponds to the 2D particle in a box.
"""

import numpy as np
from tinie.systems.leads.lead import Lead


class BoxLead(Lead):
    def __init__(
            self,
            x_limits,
            y_limits,
            E_limits,
            delta_E=0.0,
            alignment="left"):
        """
        Lead object is initialized with the following parameters:

        Parameters
        ----------
        x_limits :  list, [x_min, x_max]
                    x-axis range.

        y_limits :  list, [y_min, y_max]
                    y_axis range.

        E_limits :  float, [E_min, E_max]
                    Energy range.

        delta_E :   float
                    Lead energy discretization.

        alignment:  string,
                    Lead alignment, up/down/left/right
        """

        Lead.__init__(self)

        # Input sanity checks:
        assert isinstance(x_limits[0], float) and isinstance(
            x_limits[1], float
        ), "Bad x_min/x_max type, expected float"
        assert isinstance(y_limits[0], float) and isinstance(
            y_limits[1], float
        ), "Bad y_min/y_max type, expected float"
        assert isinstance(E_limits[0], float) and isinstance(
            E_limits[1], float
        ), "Bad y_min/y_max type, expected float"
        assert x_limits[0] <= x_limits[1], "x_min greater than x_max"
        assert y_limits[0] <= y_limits[1], "y_min greater than y_max"
        assert E_limits[0] <= E_limits[1], "E_min greater than E_max"

        self.type = "Box"
        self.x = x_limits  # Stores x-axis boundaries
        self.y = y_limits  # Stores y-axis boundaries
        self.E = E_limits  # Stores probe energy boundaries
        self.delta_E = delta_E  # Stores energy spacing
        self.alignment = alignment
        self._quantum_numbers = {"k": [], "l": []}
        self.B = 0.0

        # Boundary parameters
        self._x0 = (self.x[1] + self.x[0]) / 2
        self._y0 = (self.y[1] + self.y[0]) / 2
        self._Lx = self.x[1] - self.x[0]
        self._Ly = self.y[1] - self.y[0]

        self._H = self.get_energies()  # Stores eigenenergy values
        self._num_states = len(self._H)
        self.delta_E = np.min(np.diff(self._H))

    def set_magnetic_field_strength(self, B):
        """
        Set magnetic field B in the lead.

        Parameters
        ----------
        B       :   float
                    Magnetic field strength.
        """

        # Input sanity check:
        assert isinstance(B, float), "B must be a floating point number"

        self.B = B
        self._H = self.get_energies()

    def set_energy_spacing(self, delta_E):
        """
        Set a different energy discretization.

        Parameters
        ----------
        delta_E :   float
                    Energy spacing for the lead probe energies.
        """

        self.delta_E = delta_E
        self._H = self.get_energies()

    def get_quantum_numbers(self, state_num):
        """
        Get quantum numbers l, k of state state_num.

        Parameters
        ----------
        state_num   :   int,
                        State number.
        """

        return [
            self._quantum_numbers["l"][state_num],
            self._quantum_numbers["k"][state_num],
        ]

    def get_type_sensitive_parameters(self):
        """
        Returns parameters specific to BoxLead.
        """

        return str({"alignment": self.alignment})

    def get_energies(self):
        """
        Calculates the lead Hamiltonian based on lead energies and the
        corresponding possible values of m and n.

        Returns
        -------
        H       :   np.ndarray,
                    Hamiltonian of the lead with the provided probe energies.
        """

        self._quantum_numbers = {"k": [], "l": []}
        # List for storing the eigenenergies of the system
        H = []

        k_min = np.ceil(np.sqrt(2 * self.E[0]) * self._Lx / np.pi)
        l_min = np.ceil(np.sqrt(2 * self.E[0]) * self._Ly / np.pi)
        k_max = np.floor(np.sqrt(2 * self.E[1]) * self._Lx / np.pi)
        l_max = np.floor(np.sqrt(2 * self.E[1]) * self._Ly / np.pi)

        k_range = np.arange(k_min, k_max + 1)
        l_range = np.arange(l_min, l_max + 1)

        for k in k_range:
            for l in l_range:
                E = 0.5 * np.pi ** 2 * \
                    ((k / self._Lx) ** 2 + (l / self._Ly) ** 2)
                if (self.E[0] <= E) and (
                        E <= self.E[1]) and (k != 0) and (l != 0):
                    self._quantum_numbers["k"].append(k)
                    self._quantum_numbers["l"].append(l)
                    H.append(E)

        idx_sort = sorted(range(len(H)), key=lambda i: H[i])
        H_sort = [H[i] for i in idx_sort]
        k_sort = [self._quantum_numbers["k"][i] for i in idx_sort]
        l_sort = [self._quantum_numbers["l"][i] for i in idx_sort]

        self._quantum_numbers["k"] = k_sort
        self._quantum_numbers["l"] = l_sort

        return np.array(H_sort)

    def get_number_of_states(self):
        """
        Get the number of states in the lead object.

        Returns
        -------
        num_states: int,
                    Number of states in the lead object.
        """

        return self._num_states

    def get_state_point(self, x, y, state_num):
        """
        Evaluates lead wavefunction in a state state_num at the point x, y.
        Note that the wavefunction is not normalized, if you wish to evaluate
        state at a single point and get normalizaed results, use normalization
        function afterwards.

        Parameters
        ----------
        x       :   float
                    x-coordinate at which the state is evaluated.

        y       :   float
                    y-coordinate at which the state is evaluated.

        state_num:  int or np.int_,
                    State index corresponding to a unique set of quantum
                    numbers n and k of the lead.

        Returns
        -------
        state_val:  complex,
                    Value of the eigenfunction evaluated at the point (x,y).
        """

        # Input sanity checks:
        assert isinstance(state_num, int) or isinstance(
            state_num, np.int_
        ), "state_num must be an integer"
        assert 0 <= state_num <= self._num_states - 1, "n out of range of states"

        # Set up quantum numbers
        k = self._quantum_numbers["k"][state_num]
        l = self._quantum_numbers["l"][state_num]

        psi_x = np.sin((k * np.pi / self._Lx) * (x - self._x0 + self._Lx / 2))
        psi_y = np.sin((l * np.pi / self._Ly) * (y - self._y0 + self._Ly / 2))

        return psi_x * psi_y

    def get_state(self, x_points, y_points, state_num, mode="spacing"):
        """
        Returns the lead wavefunction in a state state_num on a 2D grid
        discretized by x_points and y_points, or evaluated at a grid of
        x_points and y-points. Wavefunction is normalized.

        Parameters
        ----------
        x_points    :   int
                        x-axis discretization.

        y_points    :   int
                        y-axis discretization.

        state_num   :   int or np.int_,
                        State index corresponding to a unique set of quantum
                        numbers n and k of the lead.

        mode        :   str, 'spacing', 'custom' or 'mc'
                        State evaluation mode. 'spacing' for specifying the
                        spacing in x and y directions and 'custom' for
                        custom grid.

        Returns
        -------
        state:          np.ndarray, dtype=complex,
                        Eigenfunction of the lead evaluated at the specified
                        grid.
        """

        # Input sanity checks:
        assert isinstance(state_num, int) or isinstance(
            state_num, np.int_
        ), "state_num must be an integer"
        assert 0 <= state_num <= self._num_states - 1, "n out of range of states"
        assert (isinstance(x_points, int) and isinstance(y_points, int)) or (
            isinstance(x_points, np.ndarray) and isinstance(y_points, np.ndarray)
        ), "x_points and y_points must be either an integer or an array"
        assert (
            mode == "spacing" or mode == "custom" or mode == "mc"
        ), "Invalid evaluation mode, use either 'spacing', 'custom' or 'mc'"

        # Set up the grid
        if mode == "spacing":
            x_grid = np.linspace(self.x[0], self.x[1], x_points)
            y_grid = np.linspace(self.y[0], self.y[1], y_points)
            X, Y = np.meshgrid(x_grid, y_grid, indexing="ij")

        elif mode == "custom":
            x_grid = x_points
            y_grid = y_points
            X, Y = np.meshgrid(x_grid, y_grid, indexing="ij")

        else:
            X = x_points
            Y = y_points

        X, Y = np.meshgrid(x_grid, y_grid, indexing="ij")

        norm = np.sqrt(4 / (self._Lx * self._Ly))

        return self.get_state_point(X, Y, state_num) * norm

    def get_boundary_state(self, state_num, num_boundary_points):
        """
        Returns the 1D lead boundary wavefunction array corresponding to the
        energy state number state_num.

        Parameters
        ----------
        num_boundary_points:    int,
                                Number of points in the boundary grid.

        state_num   :   int or np.int_,
                        State index corresponding to a unique set of quantum
                        numbers n and k of the lead.

        Returns
        -------
        state:          np.ndarray of shape (num_boundary_points, ),
                        nth eigenfunction of the lead evaluated at the
                        boundary.
        """

        # Input sanity checks:
        assert isinstance(state_num, int) or isinstance(
            state_num, np.int_
        ), "state_num must be an integer"
        assert 0 <= state_num <= self._num_states - 1, "n out of range of states"

        boundary = self.get_boundary(num_boundary_points)
        if self.alignment == "right":
            return np.array([self.get_state_point(
                self.x[0], y, state_num) for y in boundary])
        elif self.alignment == "left":
            return np.array([self.get_state_point(
                self.x[1], y, state_num) for y in boundary])
        elif self.alignment == "up":
            return np.array([self.get_state_point(
                x, self.y[0], state_num) for x in boundary])
        else:
            return np.array([self.get_state_point(
                x, self.y[1], state_num) for x in boundary])

    def get_boundary(self, num_boundary_points):
        """
        Returns the 1D lead boundary ndarray with a discretization
        num_boundary_points.

        Parameters
        ----------
        num_boundary_points:    int
                                Lead boundary point discretization.

        Returns
        -------
        boundary:       np.ndarray of shape (num_boundary_points, ),
                        Boundary coordinates of the lead.
        """

        if self.alignment == "right" or self.alignment == "left":
            return np.linspace(self.y[0], self.y[1], num_boundary_points)
        else:
            return np.linspace(self.x[0], self.x[1], num_boundary_points)
