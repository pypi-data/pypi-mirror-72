#!/usr/bin/env python3
"""
This file contains the implementation of the CustomCoupling class, which is
a bare-bones version of the Coupling class, meant to just store the custom-made
Couplings, which the class reads as a 2D array from some .npz file. Can only be
used in conjunction with CustomLead and CustomCenter classes.
"""

import numpy as np
from mpi4py import MPI
from tinie.systems.central_region.custom_center import CustomCenter
from tinie.systems.couplings.coupling import Coupling
from tinie.systems.leads.custom_lead import CustomLead


class CustomCoupling(Coupling):
    def __init__(self, Center_object, Lead_object, filename, comm):
        """
        Parameters
        ----------
        Center_object:  Center-like object
                        Central region to be used in coupling.

        Lead_object  :  Lead-like object
                        Lead region to be used in coupling.
        """

        # Input sanity checks
        assert (
            filename.split(".")[-1] == "npy"
        ), "Error: CustomCoupling reads the coupling matrix from a .npy file"
        assert (
            np.load(filename).ndim == 2
        ), "Error: coupling matrix must be a 2D array of coupling values"
        assert isinstance(
            Lead_object, CustomLead
        ), "Error: Lead object must be of type 'custom'"
        assert isinstance(
            Center_object, CustomCenter
        ), "Error: Lead object must be of type 'custom'"

        Coupling.__init__(self, Center_object, Lead_object)
        self.type = "Custom"
        self.coupling_matrix = np.load(filename)
        num_states_ctr = len(self.Center_object.get_energies())
        num_states_ld = len(self.Lead_object.get_energies())
        assert self.coupling_matrix.shape == (
            num_states_ld,
            num_states_ctr,
        ), "Error: dimensions of the coupling matrix inconsistent with lead and center"
        self._comm = comm

    def get_coupling_matrix_element(self, lead_state, center_state):
        """
        Method for calculating a specific matrix element, mostly for testing
        purposes.

        Parameters:
        -----------
        lead_state:     int,
                        Lead state number.

        center_state:   int,
                        Center state number.

        Returns:
        --------
        coupling_value: complex,
                        Value of coupling between two states.
        """

        return self.coupling_matrix[lead_state, center_state]

    def get_coupling_matrix(self):
        """
        Method for calculating the coupling matrix.

        Returns
        -------
        coupling_matrix:    np.ndarray of shape
                            (num_lead_states, num_center_states),
                            Coupling matrix.
        """

        return self.coupling_matrix
