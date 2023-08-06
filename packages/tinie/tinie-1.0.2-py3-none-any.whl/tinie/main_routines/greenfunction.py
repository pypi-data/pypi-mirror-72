#!/usr/bin/env python3
"""
Interface for calculating the advanced and retarded Green's functions.
"""

import numpy as np
import scipy.linalg as la


class GreenFunction:
    """
    Implementation of central region Green's function in
    energy eigenbasis of the central region.
    """

    def __init__(self, energies, self_energies, wide_band=False):
        """
        Parameters
        ----------
        energies:      list/np.array of floats,
                       Eigenenergies of the uncoupled central region.

        self_energies: list/np.array of SelfEnergy-instances,
                       Embedding self-energies for the leads.

        wide_band:     bool,
                       Wide band approximation mode.
        """

        self.energies = energies
        self.self_energies = self_energies
        self.omega = 0.0

        ############################
        # WIDE BAND MODE VARIABLES #
        self._wide_band = wide_band
        self._wide_band_self_energy = None
        #                          #
        ############################

    def _get_inverse_retarded(self):
        """
        Returns the inverse of retarded Green's function.
        """

        Grinv = np.diag(self.omega - self.energies).astype(dtype=np.complex128)

        #######################################################################
        #                     DEBUGGING MODE ONLY CODE                        #
        if self._wide_band:
            for self_energy in self._wide_band_self_energy:
                Grinv -= self_energy
        #                       PROCEED WITH CAUTION                          #
        #######################################################################

        else:
            for self_energy in self.self_energies:
                Grinv -= self_energy.retarded()
        return Grinv

    def set_omega(self, omega):
        """"
        Sets the energy omega at which the Green's function is evaluated.
        """

        self.omega = omega

        for self_energy in self.self_energies:
            self_energy.set_omega(self.omega)

    def apply_retarded(self, M):
        """
        Multiplies matrix or vector M from left with retarded
        Green's function.
        """

        Grinv = self._get_inverse_retarded()
        return la.solve(Grinv, M, overwrite_a=True)

    def apply_advanced(self, M):
        """
        Multiplies matrix or vector M from left with advanced
        Green's function.
        """

        Gainv = np.conj(np.transpose(self._get_inverse_retarded()))
        return la.solve(Gainv, M, overwrite_a=True)

    def get_retarded(self):
        """
        Calculates and returns the retarded Green's function.
        """

        Grinv = self._get_inverse_retarded()
        return la.inv(Grinv, overwrite_a=True)

    ###########################################################################
    #                      DEBUGGING MODE ONLY CODE                           #
    def set_wide_band_self_energy(self, self_energy):
        """
        Sets a test self-energy matrix for the leads.
        """

        self._wide_band_self_energy = self_energy

    #                         PROCEED WITH CAUTION                            #
    ###########################################################################
