#!/usr/bin/env python3
"""
This file contains the implementation of the CustomLead class, which is
a bare-bones version of the Lead class, meant to just store the custom-made
lead Hamiltonian, which the class reads as a 1D array from some .npy file.
"""

import numpy as np
from tinie.systems.leads.lead import Lead


class CustomLead(Lead):
    def __init__(self, x_lims, y_lims, E_lims, delta_E, filename):
        assert (
            filename.split(".")[-1] == "npy"
        ), "Error: CustomLead reads its Hamiltonian from a .npy file"
        assert (
            np.load(filename).ndim == 1
        ), "Error: lead region Hamiltonian must be a 1D array of eigenvalues"

        Lead.__init__(self)
        self.type = "Custom"
        self.x = x_lims  # Stores x-axis boundaries
        self.y = y_lims  # Stores y-axis boundaries
        self.E = E_lims  # Stores probe energy boundaries
        self.H = np.load(filename)
        self.delta_E = delta_E

        self._num_states = len(self.H)

    ###########################################################################
    #             THESE METHODS ARE UNUSED IN THE CUSTOM CLASS                #
    def set_magnetic_field_strength(self, B):
        return None

    def set_energy_spacing(self, delta_E):
        return None

    #                                                                         #
    ###########################################################################

    def get_type_sensitive_parameters(self):
        """
        Returns parameters specific to CustomLead.
        """

        return str({})

    def get_energies(self):
        """
        Get all eigenenergies.

        Returns
        -------
        energies:   np.ndarray,
                    Eigenenergies of the lead.

        """

        return self.H

    def get_number_of_states(self):
        """
        Get the number of states in the lead object.

        Returns
        -------
        num_states: int,
                    Number of states in the lead object.
        """

        return self._num_states

    ###########################################################################
    #             THESE METHODS ARE UNUSED IN THE CUSTOM CLASS                #
    def get_quantum_numbers(self, state_num):
        return None

    def get_state_point(self, x, y, n):
        return None

    def get_state(self, x_points, y_points, state_num, mode):
        return None

    def get_boundary_state(self, n, num_boundary_points):
        return None

    def get_boundary(self, num_boundary_points):
        return None

    #                                                                         #
    ###########################################################################
