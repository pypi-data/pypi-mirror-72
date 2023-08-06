#!/usr/bin/env python3
"""
Interface for calculating advanced and retarded self-energies of the
reservoirs, as well as the rate operators.
"""

import numpy as np


class SelfEnergy:
    """
    Implementation of retarded self-energy for the reservoirs.
    We assume to have a diagonal Hamiltonian for the reservoirs.
    """

    def __init__(
            self,
            reservoir_energies,
            reservoir_center_coupling,
            eta=1e-6):
        """
        Parameters
        ----------
        reservoir_energies:     np.array of floats, shape (num_lead_energies),
                                Energies of the uncoupled reservoir.

        reservoir_center_coupling:   np.array of complexes, shape
                                     (num_lead_energies, num_center_energies),
                                     The coupling matrix between the reservoir
                                     and center.
        """

        self.reservoir_energies = reservoir_energies
        self.reservoir_center_coupling = reservoir_center_coupling
        self.reservoir_center_coupling_dagger = np.conj(
            np.transpose(self.reservoir_center_coupling)
        )

        self.ieta = eta * 1j
        self.reta = eta
        self.omega = 0.0
        self.potential = 0.0

        # This flag is set to true when
        self._already_calculated = False

        self._retarded = None
        self._advanced = None
        self._gamma = None

    def _reset(self):
        """
        Resets the self-energies in case omega or potential have been changed.
        """

        self._already_calculated = False
        self._retarded = None
        self._advanced = None
        self._gamma = None

    def set_omega(self, omega):
        """
        Sets the energy at which the self-energy matrix is evaluated.
        """

        if omega != self.omega:
            self._reset()
        self.omega = omega

    def set_potential(self, potential):
        """
        Sets the potential of the reservoir.
        """

        if potential != self.potential:
            self._reset()
        self.potential = potential

    def retarded(self):
        """
        Returns retarded self-energy.
        """

        if self._already_calculated and self._retarded is not None:
            return self._retarded
        else:
            self._retarded = (
                self.reservoir_center_coupling_dagger
                @ (
                    1.0
                    / (
                        self.omega
                        - self.potential
                        + self.ieta
                        - self.reservoir_energies
                    )
                    * self.reservoir_center_coupling.T
                ).T
            )
            self._already_calculated = True
            return self._retarded

    def advanced(self):
        """
        Returns advanced self-energy.
        """

        if self._already_calculated and self._advanced is not None:
            return self._advanced
        else:
            self._advanced = np.conj(np.transpose(self.retarded()))
            self._already_calculated = True
            return self._advanced

    def get_gamma(self):
        """
        Returns rate operator.
        """

        if self._already_calculated and self._gamma is not None:
            return self._gamma
        else:
            self._gamma = 1j * (self.retarded() - self.advanced())
            self._already_calculated = True
            return self._gamma
