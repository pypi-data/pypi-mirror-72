#!/usr/bin/env python3
"""
This file contains the implementation of System class, which is the parent of
the SystemWrite class, used to write transport system information to and hdf5
file and SystemRead class, used to read transport system information from that
hdf5 file to perform transport calculations.
"""

from abc import ABC, abstractmethod


class System(ABC):
    """
    An interface for handling system-dependent code
    such as implementation of leads, lead-center coupling,
    center-region energies etc.
    """

    def __init__(self):
        """
        Initializer method.
        """

        self.file = None
        self.file_path = None

    def __instancecheck__(self, instance):
        """
        Checks whether the instance defines the required methods
        for it to pass as an instance of System.
        """

        center_energies_getter = getattr(instance, "get_center_energies", None)
        if not callable(center_energies_getter):
            return False

        center_potential_getter = getattr(
            instance, "get_center_potential", None)
        if not callable(center_potential_getter):
            return False

        lead_energies_getter = getattr(instance, "get_lead_energies", None)
        if not callable(lead_energies_getter):
            return False

        coupling_getter = getattr(
            instance, "get_lead_center_coupling_mat", None)
        if not callable(coupling_getter):
            return False

        lead_num_getter = getattr(instance, "get_num_leads", None)
        if not callable(lead_num_getter):
            return False

        coupling_num_getter = getattr(instance, "get_num_couplings", None)
        if not callable(coupling_num_getter):
            return False

        self_energy_getter = getattr(instance, "get_self_energy", None)
        if not callable(self_energy_getter):
            return False

        rate_operator_getter = getattr(instance, "get_rate_operator", None)
        if not callable(self_energy_getter):
            return False

        return True

    def set_file_path(self, file_path):
        """
        Sets file path to dump to/fetch from.
        """
        self.file_path = file_path

    @abstractmethod
    def get_center_energies(self):
        """
        Returns energies of the central region in the transport setup.
        """

        ...

    @abstractmethod
    def get_center_potential(self):
        """
        Returns potential energy at a grid of the central region.
        """

        ...

    @abstractmethod
    def get_lead_energies(self, lead_nbr):
        """
        Returns energies of the lead 'lead_nbr' with discretization step
        `delta_energy`.
        """

        ...

    @abstractmethod
    def get_center_lead_coupling_mat(self, cpl_nbr):
        """
        Returns the coupling matrix between central region and a lead.
        """

        ...

    @abstractmethod
    def get_num_leads(self):
        """
        Returns the number of leads.
        """

        ...

    @abstractmethod
    def get_num_couplings(self):
        """
        Returns the number of couplings.
        """

        ...

    @abstractmethod
    def get_center_type(self):
        """
        Returns type of the central region.
        """

        ...
