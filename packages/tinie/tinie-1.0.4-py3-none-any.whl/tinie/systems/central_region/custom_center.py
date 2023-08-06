#!/usr/bin/env python3
"""
This file contains the implementation of the CustomCenter class, which is
a bare-bones version of the Center class, meant to just store the custom-made
center Hamiltonian, which the class reads as a 1D array from some .npy file.
"""

import numpy as np
from tinie.systems.central_region.center import Center


class CustomCenter(Center):
    def __init__(self, filename):
        assert (
            filename.split(".")[-1] == "npy"
        ), "CustomLead reads its Hamiltonian from a .npy file"
        assert (
            np.load(filename).ndim == 1
        ), "Center region Hamiltonian must be a 1D array of eigenvalues"

        Center.__init__(self)
        self.type = "Custom"
        self._H = np.load(filename)
        self._num_states = len(self._H)

    def get_type_sensitive_parameters(self):
        """
        Returns parameters specific to CustomCenter.
        """

        return str({})

    def get_energies(self):
        """
        Get all eigenenergies.

        Returns
        -------
        energies:   np.ndarray,
                    Eigenenergies of the uncoupled system

        """

        return self._H

    def get_number_of_states(self):
        """
        Get the number of states in the Center object.

        Returns
        -------
        num_states: int,
                    Number of states in the Center object.
        """

        return self._num_states

    ###########################################################################
    #             THESE METHODS ARE UNUSED IN THE CUSTOM CLASS                #
    def get_potential(self):
        return 0.0

    def get_state(self, n):
        return None

    def get_states(self):
        return None

    def get_sliced_state(self, n, width, side):
        return None

    def get_sliced_states(self, width, side):
        return None

    def get_boundary_state(self, n, side):
        return None

    def get_coordinate_ranges(self):
        return None

    def get_coordinates(self):
        return None

    def get_slice_coordinates(self, width, side):
        return None

    def get_boundary_coordinates(self, side):
        return None

    #                                                                         #
    ###########################################################################
