#!/usr/bin/env python3
"""
This file contains the implementation of the FiniteHarmonicLead class, which
models a rectangular lead with dimensions [x_min, x_max] by [y_min, y_max].
Probe energy ranges are set as [E_min, E_max] with spacing delta_E. Depending
on the alignment of the lead, wavefunctions along the different axes
are different. In horizontal alignments, the lead wavefunction corresponds to
potential well in x-axis and quantum harmonic oscillator in y-axis, and vice
versa in vertical alignments.
"""

import numpy as np
from numpy.polynomial.hermite import hermval
from scipy.special import factorial
from tinie.systems.leads.lead import Lead


class FiniteHarmonicLead(Lead):
    def __init__(
        self,
        x_limits,
        y_limits,
        E_limits,
        delta_E=None,
        alignment="left",
        w0=1.0,
        boundary_type="dir",
    ):
        """
        Lead object is initialized with the following parameters:

        Parameters:
        -----------
        x_limits   :  list, [x_min, x_max],
                      x-axis range.

        y_limits   :  list, [y_min, y_max],
                      y_axis range.

        E_limits   :  float, [E_min, E_max],
                      Energy range.

        delta_E :   float,
                    Lead energy discretization.

        alignment:  string,
                    Lead alignment, up/down/left/right.

        w0:         float,
                    Energy of the quantum harmonic oscillator.

        boundary_type:   string,
                         Boundary type of the lead, dir/neu.
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
        assert (
            alignment == "left"
            or alignment == "right"
            or alignment == "down"
            or alignment == "up"
        ), "Bad alignment, expected left/right/up/down"

        self.type = "FiniteHarmonic"
        self.x = x_limits  # Stores x-axis boundaries
        self.y = y_limits  # Stores y-axis boundaries
        self.E = E_limits  # Stores probe energy boundaries
        self.alignment = alignment  # Stores alignment
        self.delta_E = delta_E  # Stores energy spacing
        self._H = None  # Stores eigenenergy values
        self._quantum_numbers = {"k": [], "l": []}

        self.boundary_type = boundary_type
        self.w0 = w0
        self.B = 0.0

        if delta_E is not None:
            self._H = self.get_energies()

        # Boundary parameters
        self._x0 = None
        self._y0 = None
        self._L = None
        self._gauge_angle = None

        self._set_alignment_parameters()

    def _set_alignment_parameters(self):
        """
        Sets alignment specific parameters.
        """

        # Determining boundary parameters due to alignment.
        if self.alignment == "left":
            self._x0 = self.x[1]
            self._y0 = (self.y[1] + self.y[0]) / 2
            self._L = self.x[1] - self.x[0]
            self._gauge_angle = np.pi

        elif self.alignment == "down":
            self._x0 = (self.x[1] + self.x[0]) / 2
            self._y0 = self.y[1]
            self._L = self.y[1] - self.y[0]
            self._gauge_angle = 3 * np.pi / 2

        elif self.alignment == "right":
            self._x0 = self.x[0]
            self._y0 = (self.y[1] + self.y[0]) / 2
            self._L = self.x[1] - self.x[0]
            self._gauge_angle = 0

        elif self.alignment == "up":
            self._x0 = (self.x[1] + self.x[0]) / 2
            self._y0 = self.y[0]
            self._L = self.y[1] - self.y[0]
            self._gauge_angle = np.pi / 2

    def _set_oscillator_frequency(self, w0):
        """
        Set the frequency of the quantum harmonic oscillator in the lead.

        Parameters
        ----------
        w0      :   float,
                    Quantum harmonic oscillator frequency.
        """

        # Input sanity check:
        assert isinstance(w0, float), "w0 must be a floating point number"

        self.w0 = w0
        self._H = self.get_energies()

    def _set_boundary_type(self, boundary_type):
        """
        Set lead boundary conditions, 'dir' for Dirichlet boundary conditions
        and 'neu' for von Neumann boundary conditions.

        Parameters
        ----------
        boundary_type:  str, 'dir' or 'neu',
                        Boundary conditions of the lead.
        """

        # Input sanity checks:
        assert isinstance(boundary_type, str), "boundary_type must be a string"
        assert boundary_type == "dir" or boundary_type == "neu", "Invalid boundary type"

        self.boundary_type = boundary_type

    def set_magnetic_field_strength(self, B):
        """
        Set magnetic field B in the lead.

        Parameters
        ----------
        B       :   float,
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
        delta_E :   float,
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
        Returns parameters specific to FiniteHarmonicLead.
        """

        return str(
            {
                "alignment": self.alignment,
                "w0": self.w0,
                "boundary_type": self.boundary_type,
            }
        )

    def get_energies(self):
        """
        Calculates the lead Hamiltonian based on lead energies and the
        corresponding possible values of n and k.

        Returns
        -------
        H       :   np.ndarray,
                    Hamiltonian of the lead with the provided probe energies.
        """

        assert (
            self.delta_E is not None
        ), "Energy discretization was not set by set_energy_spacing"

        E = np.arange(self.E[0], self.E[1] + self.delta_E, self.delta_E)
        self._quantum_numbers = {"k": [], "l": []}

        # List for storing the eigenenergies of the system
        H = []

        wc = self.B
        wc0 = (self.w0 ** 2 + wc ** 2) ** 0.5

        for energy in E:

            l_max = int(np.floor(energy / wc0 - 0.5))

            if l_max == energy / wc0 - 0.5:
                l_max -= 1

            # List for the allowed values of l.
            allowed_l = []

            # List for the allowed values of k.
            allowed_k = []

            for l in range(0, l_max + 1):
                allowed_l += 2 * [l]
                allowed_k += [2 ** 0.5 * (wc0 / self.w0)
                              * (energy - (l + 0.5) * wc0) ** 0.5]
                allowed_k += [-(2 ** 0.5) * (wc0 / self.w0)
                              * (energy - (l + 0.5) * wc0) ** 0.5]

            # Twice the n-states as k can be positive and negative.
            self._quantum_numbers["l"] += allowed_l
            self._quantum_numbers["k"] += allowed_k
            H += [energy] * len(allowed_l)

        self._num_states = len(H)

        return np.array(H)

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
        state at a single point and get normalized results, use normalization
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
        l = self._quantum_numbers["l"][state_num]
        k = self._quantum_numbers["k"][state_num]

        if self.boundary_type == "dir":
            delta = np.pi / 2

        else:
            delta = 0.0

        wc = self.B
        wc0 = (wc ** 2 + self.w0 ** 2) ** 0.5

        well_coord = (x - self._x0) * np.cos(self._gauge_angle) + (
            y - self._y0
        ) * np.sin(self._gauge_angle)
        osc_coord = -(x - self._x0) * np.sin(self._gauge_angle) + (
            y - self._y0
        ) * np.cos(self._gauge_angle)

        if self.B == 0:
            osc_coord_k = 0

        else:
            osc_coord_k = -k / self.B

        q = (wc0 ** 0.5) * (osc_coord + (wc ** 2 / wc0 ** 2) * osc_coord_k)
        phi_well = np.cos(k * well_coord + delta)
        phi_oscillator = np.exp((-0.5) * q ** 2) * hermval(q, [0] * l + [1])

        return phi_well * phi_oscillator

    def get_state(self, x_points, y_points, state_num, mode="spacing"):
        """
        Returns the lead wavefunction in a state state_num on a 2D grid
        discretized by x_points and y_points, or evaluated at a grid of
        x_points and y-points. Wavefunction is normalized.

        Parameters
        ----------
        x_points    :   int
                        x-axis discretization

        y_points    :   int
                        y-axis discretization

        state_num   :   int or np.int_,
                        State index corresponding to a unique set of quantum
                        numbers n and k of the lead.

        mode        :   str, 'spacing', 'custom' or 'mc',
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

        # Set up the grid:
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

        # Calculate magnetic field gauge transformation:
        gauge = X * Y * np.sin(self._gauge_angle) ** 2 - 0.25 * (
            Y ** 2 - X ** 2
        ) * np.sin(2 * self._gauge_angle)
        f = np.exp(1j * self.B * gauge)

        # Calculate normalization:
        norm = self.normalization(state_num)

        return f * norm * self.get_state_point(X, Y, state_num)

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
        assert (
            0 <= state_num <= self._num_states - 1
        ), "state_num out of range of states"

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
        num_boundary_points:    int,
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

    def normalization(self, state_num):
        """
        Returns normalization for a particular state number state_num.
        """

        l = self._quantum_numbers["l"][state_num]
        k = self._quantum_numbers["k"][state_num]
        wc = self.B
        wc0 = (wc ** 2 + self.w0 ** 2) ** 0.5

        if self.boundary_type == "dir":
            delta = np.pi / 2

        else:
            delta = 0.0

        if self.alignment == "left" or self.alignment == "down":
            bound = -1.0

        else:
            bound = 1.0

        M = (
            2
            / (
                self._L
                + (1 / k)
                * np.cos(k * self._L + 2 * bound * delta)
                * np.sin(k * self._L)
            )
        ) ** 0.5

        N = (wc0 / np.pi) ** 0.25 * 1 / ((2 ** l) * factorial(l)) ** 0.5

        norm = M * N
        return norm
