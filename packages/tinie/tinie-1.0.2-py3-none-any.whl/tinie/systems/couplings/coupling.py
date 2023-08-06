#!/usr/bin/env python3
"""
This file contains the Coupling class, which is the parent class of all
possible Coupling-like classes. Any class that wishes to inherit Coupling-like
properties would need to have all of the given methods implemented.
"""

from abc import ABC, abstractmethod

from tinie.systems.central_region.center import Center
from tinie.systems.leads.lead import Lead


class Coupling(ABC):
    """
    An interface for handling the coupling region.
    """

    @abstractmethod
    def __init__(self, Center_object, Lead_object):
        """
        Parameters
        ----------
        Center_object:  Center-like object,
                        Central region to be used in coupling.

        Lead_object  :  Lead-like object,
                        Lead region to be used in coupling.
        """

        # Input sanity checks
        assert isinstance(
            Center_object, Center
        ), "Error: Center_obj not a member of Center class"
        assert isinstance(
            Lead_object, Lead
        ), "Error: Lead_obj not a member of Lead class"

        self.type = "BaseAbstract"
        self.coupling_matrix = None
        self.Center_object = Center_object
        self.Lead_object = Lead_object

    def __instancecheck__(self, instance):
        """
        Checks whether the instance defines the required methods
        for it to pass as an instance of Coupling.
        """

        cpl_elem_getter = getattr(
            instance, "get_coupling_matrix_element", None)
        if not callable(cpl_elem_getter):
            return False

        cpl_mat_getter = getattr(instance, "get_coupling_matrix", None)
        if not callable(cpl_mat_getter):
            return False

        return True

    @abstractmethod
    def get_coupling_matrix_element(self, lead_state, center_state):
        """
        Method for calculating a specific matrix element, mostly for testing
        purposes.

        Parameters
        ----------
        lead_state:     int,
                        Lead state number.

        center_state:   int,
                        Center state number.

        Returns
        -------
        coupling_value: complex,
                        Value of coupling between two states.
        """

        ...

    @abstractmethod
    def get_coupling_matrix(self):
        """
        Method for calculating the coupling matrix.

        Returns
        -------
        coupling_matrix:    np.ndarray of shape
                            (num_lead_states, num_center_states),
                            Coupling matrix.
        """

        ...
