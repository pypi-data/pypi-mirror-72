#!/usr/bin/env python3
"""
This file contains the implementation of SystemWrite class, which is used to
calculate the system couplings and Hamiltonians and dump then to an hdf5 file
for subsequent electron transport calculations.
"""

import os
import warnings
from shutil import move

import h5py
import numpy as np
from mpi4py import MPI
from tinie.systems.central_region.center import Center
from tinie.systems.couplings.coupling import Coupling
from tinie.systems.read_write.system import System


class SystemWrite(System):
    """
    An interface for handling system-dependent code
    such as implementation of leads, lead-center coupling,
    center-region energies etc.
    """

    def __init__(self, comm):
        """
        Initializer method.
        """

        System.__init__(self)
        self.file = None
        self.center = None
        self.couplings = []
        self._comm = comm
        self._is_master_mpi_process = self._comm.rank == 0

        ################################
        #   DEBUGGING MODE VARIABLES   #
        self.coupling_perturbation = 0.0
        #     PROCEED WITH CAUTION     #
        ################################

    def _check_write_file_path(self):
        """
        Checks whether user specified a dump file path prior to any method
        calls.
        """

        if self.file_path is None:
            warnings.warn("Write file path not set")

    def set_file_path(self, file_path):
        """
        Sets file path to dump data into.
        """

        System.set_file_path(self, file_path)
        if os.path.exists(file_path) and self._is_master_mpi_process:
            old_file_path = file_path
            new_file_path = (
                file_path.rsplit(
                    ".",
                    1)[0] +
                "_backup." +
                file_path.rsplit(
                    ".",
                    1)[1])
            print("File with same path detected, moving to " + new_file_path)
            move(old_file_path, new_file_path)

    def get_center_energies(self):
        """
        Returns energies of the central region in the transport setup.
        """

        return self.center.get_energies()

    def get_center_potential(self):
        """
        Returns potential energy at a grid of the central region.
        """

        return self.center.get_potential()

    def get_lead_energies(self, lead_nbr):
        """
        Returns energies of the lead 'lead_nbr' with discretization step
        `delta_energy`.
        """

        return self.couplings[lead_nbr].Lead_object.get_energies()

    def get_num_leads(self):
        """
        Returns the number of leads.
        """

        return len(self.couplings)

    def get_num_couplings(self):
        """
        Returns the number of couplings.
        """

        return len(self.couplings)

    def get_center_lead_coupling_mat(self, cpl_nbr):
        """
        Returns the coupling matrix between central region and a lead.
        """

        return (
            self.couplings[cpl_nbr].get_coupling_matrix() +
            self.coupling_perturbation)

    def get_center_type(self):
        """
        Returns type of the central region.
        """

        return self.center.type

    def add_central_region(self, Center_object):
        assert isinstance(
            Center_object, Center
        ), "Error: object does not belong to Center class"
        self.center = Center_object

    def add_coupling_region(self, Coupling_object):
        assert isinstance(
            Coupling_object, Coupling
        ), "Error: object does not belong to Coupling class"
        assert (
            Coupling_object.Center_object == self.center
        ), "Error: Coupling object doesn't couple to the same center"

        self.couplings.append(Coupling_object)

    def dump(self):
        """
        Dumps all the necessary transport system information into our file.
        """

        # Basic sanity checks
        self._check_write_file_path()

        assert self.center is not None, "Error: no central region assigned!"
        assert len(self.couplings) != 0, "Error: no couplings in the system!"

        # Creating the file:
        if self._is_master_mpi_process:
            self.file = h5py.File(self.file_path, "w")
            self.file.attrs["type"] = "PREPTINIEFile"

            # Setting up the file structure:
            self.file.create_group("leads")
            self.file.create_group("center")
            self.file.create_group("couplings")

            # First, we take care of the central region:
            self.file["/center"].create_dataset(
                "hamiltonian",
                data=self.get_center_energies(),
                chunks=True,
                compression="gzip",
            )
            self.file["/center"].create_dataset(
                "potential",
                data=self.get_center_potential(),
                chunks=True,
                compression="gzip",
            )
            self.file["/center"].attrs["parameters"] = str(
                self.center.get_type_sensitive_parameters()
            )
            self.file["/center"].attrs["num_states"] = len(
                self.get_center_energies())
            self.file["/center"].attrs["type"] = self.center.type

            # Then the leads:
            for i in range(self.get_num_leads()):
                self.file.create_group("leads/lead_" + str(i))
                self.file["leads/lead_" + str(i)].create_dataset(
                    "hamiltonian",
                    data=self.get_lead_energies(i),
                    chunks=True,
                    compression="gzip",
                )
                self.file["leads/lead_" + str(i)].create_dataset(
                    "x_axis_limits", data=self.couplings[i].Lead_object.x
                )
                self.file["leads/lead_" + str(i)].create_dataset(
                    "y_axis_limits", data=self.couplings[i].Lead_object.y
                )
                self.file["leads/lead_" + str(i)].create_dataset(
                    "energy_limits", data=self.couplings[i].Lead_object.E
                )

                self.file["leads/lead_" + str(i)].attrs[
                    "energy_spacing"
                ] = self.couplings[i].Lead_object.delta_E
                self.file["leads/lead_" + str(i)].attrs["parameters"] = str(
                    self.couplings[i].Lead_object.get_type_sensitive_parameters()
                )
                self.file["leads/lead_" + str(i)].attrs["num_states"] = len(
                    self.get_lead_energies(i)
                )
                self.file["leads/lead_" +
                          str(i)].attrs["type"] = self.couplings[i].Lead_object.type

            self.file["/leads"].attrs["num_leads"] = self.get_num_leads()
            self.file["/couplings"].attrs["num_couplings"] = self.get_num_couplings()

        self._comm.Barrier()

        V_cpl = []

        # Then the couplings:
        for i in range(self.get_num_leads()):

            partial_cpl = self.get_center_lead_coupling_mat(i)
            total_cpl = np.zeros(partial_cpl.shape, dtype=np.complex128)
            self._comm.Reduce(partial_cpl, total_cpl, MPI.SUM, 0)
            V_cpl.append(total_cpl)

            if self._is_master_mpi_process:
                print("Coupling matrix", i, "calculated...")

        self._comm.Barrier()

        if self._is_master_mpi_process:
            for i in range(self.get_num_leads()):
                self.file.create_group("couplings/coupling_" + str(i))
                self.file["couplings/coupling_" + str(i)].create_dataset(
                    "coupling_matrix", data=V_cpl[i], chunks=True, compression="gzip"
                )
                self.file["couplings/coupling_" + str(i)].attrs[
                    "type"
                ] = self.couplings[i].type
            print("Data written...")
            self.file.close()

    ###########################################################################
    #                      DEBUGGING MODE ONLY CODE                           #
    def set_coupling_perturbation(self, delta):
        """
        Setting up small perturbation for the coupling for stability testing
        purposes
        """

        self.coupling_perturbation = delta

    #                        PROCEED WITH CAUTION                             #
    ###########################################################################
