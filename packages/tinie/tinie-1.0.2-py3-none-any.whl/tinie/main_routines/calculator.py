#!/usr/bin/env python3
"""
Calculator interface which is used for calculating the partial currents and
transmission of the transport system.
"""

from itertools import product

import numpy as np
import progressbar
from mpi4py import MPI
from scipy.integrate import simps
from tinie.main_routines.misc import FT, fd
from tinie.systems.read_write.system import System

from .greenfunction import GreenFunction
from .selfenergy import SelfEnergy


class Calculator:
    def __init__(
        self,
        chem_pot,
        temperature,
        potentials,
        system,
        delta_omega,
        delta_lead_energy,
        eta,
        comm,
        wide_band=False,
    ):
        """
        Initializes the transport calculator.

        Parameters
        ----------
        chem_pot:           float
                            Chemical potential of the system.

        temperature:        float
                            Temperature of the system.

        potentials:         list or np.array of floats
                            Each element corresponds to the potential in the
                            corresponding lead.

        system:             System object,
                            an object which is an interface for calculating:
                            (1) the center region energies
                            (2) lead energies
                            (3) lead-center coupling matrix.

        delta_omega:        float,
                            Discretization of energy integrals.

        delta_lead_energy:  float,
                            Discretization of lead energies.

        eta:                float,
                            A small number needed for calculating Green's
                            functions.

        wide_band:          bool,
                            Wide-band approximation mode, takes the self
                            energies as the parameters for the transport
                            calculation.

        """

        assert isinstance(chem_pot, float)
        assert isinstance(temperature, float)
        assert isinstance(potentials, (list, np.ndarray))
        for potential in potentials:
            assert isinstance(potential, float)
        assert isinstance(system, System)
        assert isinstance(delta_omega, float)
        assert isinstance(delta_lead_energy, float)
        assert isinstance(eta, float)

        if delta_omega > eta / 2:
            raise UserWarning("Your delta_omega > eta/2.")
        if delta_lead_energy > delta_omega:
            raise UserWarning("Your delta_lead_energy > delta_omega")

        self.chem_pot = chem_pot
        self.temperature = temperature
        self.potentials = potentials
        self.system = system
        self.delta_omega = delta_omega
        self.delta_lead_energy = delta_lead_energy
        self.eta = eta
        self.num_leads = system.get_num_leads()

        # Initializing variables
        self.self_energies = None
        self.green_function = None
        self.omega_limits = None
        self._comm = comm
        self._is_master_mpi_process = self._comm.rank == 0

        ############################
        # WIDE BAND MODE VARIABLES #
        self._wide_band = wide_band
        self._wide_band_gamma = None
        self._wide_band_self_energy = None
        #                          #
        ############################

        self._prepare_calculator()

    def _check_variable_float_or_pair_of_floats(self, var, var_name):
        """
        Checks whether a variable is a float or a pair of floats.
        """

        assert (isinstance(var, float)) or (
            isinstance(var, tuple)
            and len(var) == 2
            and isinstance(var[0], float)
            and isinstance(var[1], float)
        ), ("Wrong type for " + var_name + ".")

    def _check_variable_consistency_with_initialization(
        self, var_in, var_init, var_name
    ):
        """
        Checks that parameter values are consistent with initialization of this
        class.

        Parameters
        ----------
        var_in      float or list/np.array of floats,
                    Variable value(s) to check.

        var_init    float or list/np.array of floats,
                    Variable value(s) set at __init__.

        var_name    string,
                    Name of the variable for error output.

        Returns
        -------
        var_in      float or list/np.array of floats,
                    Returns either the same value that was inputted,
                    or the value with which the calculator was initialized.
        """

        assert isinstance(var_in, float) or var_in is None, (
            "Given " + var_name + " is of wrong type."
        )
        if isinstance(var_init, tuple) and len(var_init) == 2:
            assert (var_in >= var_init[0]) and (var_in <= var_init[1]), (
                "Given "
                + var_name
                + " not consistent with initialization of this transport calculator."
            )
        else:
            assert var_in is None or var_in == var_init, (
                "Given "
                + var_name
                + " not consistent with initialization of this transport calculator."
            )
        return var_init if var_in is None else var_in

    def _prepare_calculator(self):
        """
        Prepares and calculates the required matrix elements for
          (1) The center region energies
          (2) Lead energies
          (3) Lead-Center coupling
        using self.system.

        These are not saved but are used to construct the embedding
        self-energies in the list self.self_energies, and the center
        region Green's function in the variable self.green_function.

        The simulation energies are estimated from:
          (1) self.chem_pot -- chemical potential
          (2) self.temperature -- temperature
          (3) self.potentials -- potential for each lead.
        """

        self.omega_limits = self._estimate_smart_integration_limits(
            self.chem_pot, self.temperature, self.potentials
        )
        self.self_energies = []

        for i in range(self.num_leads):
            HL = self.system.get_lead_energies(i)
            VL = self.system.get_center_lead_coupling_mat(i)
            self.self_energies.append(SelfEnergy(HL, VL, eta=self.eta))

        HC = self.system.get_center_energies()

        if not self._wide_band:
            self.green_function = GreenFunction(HC, self.self_energies)

    def _estimate_smart_integration_limits(
            self, chem_pot, temperature, potentials):
        """
        Estimates the integration limits for calculating the current for a given chemical
        potential, temperature, and potentials of the leads.

        Parameters
        ----------
        chem_pot:      float,
                       Value of the chemical potential.

        temperature:   float,
                       Temperature.

        potentials:    np.array of rank 1 or list, floats,
                       Potential values for each lead.

        Returns
        -------
        omega_limits:  (float, float),
                       Integration limits for energy.
        """
        fermi_max = chem_pot + np.max(potentials)
        fermi_min = chem_pot + np.min(potentials)

        omega_limits = (
            fermi_min - 10 * temperature - 10 * self.delta_omega,
            fermi_max + 10 * temperature + 10 * self.delta_omega,
        )

        return omega_limits

    def _partial_currents(self, w, mu, T, potentials):
        """
        Calculates the pairwise currents between two leads for
        a given energy (and system parameters).

        Parameters
        ----------
        w:              float,
                        Energy.

        mu:             float,
                        Chemical potential.

        T:              float,
                        Temperature.

        potentials:     list or np.array of floats,
                        Potentials for leads.

        Returns
        -------
        currents_mat:   np.array with shape (num_leads, num_leads),
                        Currents between lead pairs for the given energy.

        trans_mat:      np.array of shape (num_leads, num_leads),
                        Transmission matrix between lead pairs for the given
                        energy.
        """

        # Transmission matrix
        trans_mat = self.transmission_matrix(w, potentials)

        # Difference between the FD distributions
        fd_mat = np.zeros((self.num_leads, self.num_leads))
        for i in range(self.num_leads):
            for j in range(self.num_leads):
                fd_mat[i, j] = fd(w - mu - potentials[i], T) - fd(
                    w - mu - potentials[j], T
                )

        currents_mat = 2 / (2 * np.pi) * fd_mat * trans_mat

        return currents_mat, trans_mat

    def get_omega_range(self):
        """
        Returns the range of omega values to probe.
        """

        return np.arange(
            self.omega_limits[0],
            self.omega_limits[1] + self.delta_omega / 2.0,
            self.delta_omega,
        )

    def get_retarded_green(self):
        """
        Calculates the retarded Green's functions over the probe energy range.

        Returns
        -------
        Gr      : np.array of shape (ctr_E, ctr_E, probe_E),
                  Retarded Green's functions at each probe energy.
        """

        omega_values = self.get_omega_range()
        omega_idx = np.arange(len(omega_values))
        omega_idx_split = np.array_split(omega_idx, self._comm.size)

        num_ctr_E = self.green_function.energies.shape[0]
        num_probe_E = len(omega_values)

        Gr = np.zeros((num_ctr_E, num_ctr_E, num_probe_E), dtype=np.complex128)
        Gr_split = np.zeros(
            (num_ctr_E, num_ctr_E, num_probe_E), dtype=np.complex128)

        for i in omega_idx_split[self._comm.rank]:
            self.green_function.set_omega(omega_values[i])
            Gr_split[:, :, i] = self.green_function.get_retarded()

        self._comm.Barrier()

        self._comm.Reduce(Gr_split, Gr, MPI.SUM, 0)
        self._comm.Bcast(Gr, root=0)

        self._comm.Barrier()

        return Gr

    def get_dos(self):
        """
        Calculates the density of states over the probe energy range.

        Returns
        -------
        dos_values: np.array of shape (num_energies, ),
                    Values of density of states.
        """

        omega_values = self.get_omega_range()
        omega_idx = np.arange(len(omega_values))
        omega_idx_split = np.array_split(omega_idx, self._comm.size)
        dos_values = np.zeros(omega_values.shape)
        dos_values_split = np.zeros(omega_values.shape)

        if self._is_master_mpi_process:
            print("Computing DOS...")
            bar = progressbar.ProgressBar(
                widgets=[
                    " [",
                    progressbar.Timer(),
                    "] ",
                    progressbar.Bar(),
                    " (",
                    progressbar.ETA(),
                    ") ",
                ],
                max_value=(len(omega_idx_split[self._comm.rank])),
            )
            counter = 0
            bar.start()

        for i in omega_idx_split[self._comm.rank]:
            self.green_function.set_omega(omega_values[i])
            dos_values_split[i] = self.green_function.get_retarded(
            ).imag.trace()

            if self._is_master_mpi_process:
                counter += 1
                bar.update(counter)

        if self._is_master_mpi_process:
            bar.finish()

        self._comm.Barrier()

        self._comm.Reduce(dos_values_split, dos_values, MPI.SUM, 0)
        self._comm.Bcast(dos_values, root=0)

        self._comm.Barrier()

        return -dos_values / np.pi

    def get_ldos(self, psi, omega):
        """
        Calculates the local density of states at the specified energies.

        Returns
        -------
        ldos_values:    np.array of shape
                        Values of local density of states.
        """

        x_points = psi.shape[1]
        y_points = psi.shape[0]
        num_states = psi.shape[2]
        ldos_values = np.zeros((x_points, y_points, omega.shape[0]))
        state_permutations = [
            s for s in product(
                range(num_states),
                range(num_states))]
        state_permutations_split = np.array_split(
            state_permutations, self._comm.size)

        if self._is_master_mpi_process:
            print("Computing LDOS...")
            bar = progressbar.ProgressBar(
                widgets=[
                    " [",
                    progressbar.Timer(),
                    "] ",
                    progressbar.Bar(),
                    " (",
                    progressbar.ETA(),
                    ") ",
                ],
                max_value=(len(omega) * len(state_permutations_split[self._comm.rank])),
            )
            counter = 0
            bar.start()

        for i, w in enumerate(omega):
            self.green_function.set_omega(w)
            Gr = self.green_function.get_retarded()
            m_prev = None
            n_prev = None

            for m, n in state_permutations_split[self._comm.rank]:

                if m != m_prev:
                    ctr_m = psi[:, :, m].T

                if n != n_prev:
                    ctr_n = psi[:, :, n].T

                ldos_values[:, :, i] += np.imag(
                    Gr[m, n] * np.multiply(np.conjugate(ctr_m), ctr_n)
                )

                m_prev = m
                n_prev = n

                if self._is_master_mpi_process:
                    counter += 1
                    bar.update(counter)

        if self._is_master_mpi_process:
            bar.finish()

        return -ldos_values / np.pi

    def transmission_matrix(self, omega, potentials):
        """
        Calculates the transmission matrix for a given energy.

        Parameters
        ----------
        omega:     float,
                   The energy at which the transmission matrix is calculated.

        Returns
        -------
        Tr:         N x N array of complex numbers,
                    Transmission matrix.
        """

        assert len(potentials) == self.num_leads, (
            "Number of potential values is inconsistent " "with the number of leads"
        )

        Tr = np.zeros((self.num_leads, self.num_leads), dtype=np.complex128)

        for i in range(len(potentials)):
            self.self_energies[i].set_potential(potentials[i])

        self.green_function.set_omega(omega)

        # Loop over all lead pairs and calculate the transmission matrix.
        if self._wide_band:
            ###################################################################
            #                WIDE BAND MODE ONLY CODE                         #
            assert (
                self._wide_band_self_energy is not None
            ), "Wide band self energy has not been set"

            for i in range(self.num_leads):
                for j in range(self.num_leads):

                    if i == j:
                        gamma = self._wide_band_gamma[i]
                        I = np.identity(gamma.shape[0], dtype=np.complex128)
                        GR = self.green_function.apply_retarded(I)
                        Tr[i, j] = np.trace((I - 1j * gamma @ GR) @
                                            np.conj(I - 1j * gamma @ GR).T
                        )
                    else:
                        GgammaR = self.green_function.apply_retarded(
                            self._wide_band_gamma[j]
                        )
                        GgammaA = self.green_function.apply_advanced(
                            self._wide_band_gamma[i]
                        )
                        Tr[i, j] = np.trace(GgammaR @ GgammaA)
            #                                                                 #
            ###################################################################
        else:
            self.green_function.set_omega(omega)

            for i in range(self.num_leads):
                for j in range(self.num_leads):

                    if i == j:
                        gamma = self.green_function.self_energies[i].get_gamma(
                        )
                        I = np.identity(gamma.shape[0], dtype=np.complex128)
                        GR = self.green_function.apply_retarded(I)
                        Tr[i, j] = np.trace((I - 1j * gamma @ GR) @
                                            np.conj(I - 1j * gamma @ GR).T
                        )
                    else:
                        GgammaR = self.green_function.apply_retarded(
                            self.green_function.self_energies[j].get_gamma()
                        )
                        GgammaA = self.green_function.apply_advanced(
                            self.green_function.self_energies[i].get_gamma()
                        )
                        Tr[i, j] = np.trace(GgammaR @ GgammaA)

        return Tr

    def currents(self):
        """
        Calculates the partial and total currents for given value
        of chemical potential, temperature, and potentials in the leads.

        Returns
        -------
        I_tot:      np.array of complex numbers,
                    shape (num_leads, ),
                    Matrix of total currents (integrated over energy).

        Iw_tot:     np.array of complex numbers,
                    shape (num_leads, num_energies),
                    Total currents as a function of energy.

        i_par:      np.array of complex numbers,
                    shape (num_leads, num_leads),
                    Matrix of partial currents (integrated over energy).

        iw_par:     np.array of complex numbers,
                    shape (num_leads, num_leads, num_energies),
                    Partial currents as a function of energy.

        Tw:         np.array of complex numbers,
                    shape (num_leads, num_leads, num_energies),
                    Transmission matrices as a function of energy.

        Gw:         np.array of complex numbers,
                    shape (num_leads, num_leads, num_energies),
                    Conductance as the function of the probe energy.

        w:          np.array of floats, shape num_energies
                    Values of energy where we have sampled the
                    transmissions and currents.

        NOTE: Many of the return values are COMPLEX. The imaginary part should
        be close to zero. Non-zero imaginary part represents numerical
        (or implementation) errors.
        """

        chem_pot = self.chem_pot
        temperature = self.temperature
        potentials = self.potentials

        # Sampling energies
        self._estimate_smart_integration_limits(
            chem_pot, temperature, potentials)
        w = self.get_omega_range()
        w_idx = np.arange(len(w))
        w_idx_split = np.array_split(w_idx, self._comm.size)

        iw_par = np.zeros((self.num_leads, self.num_leads, len(w)),
                          dtype=np.complex128)

        iw_par_split = np.zeros((self.num_leads, self.num_leads, len(w)),
                                dtype=np.complex128)

        Tw = np.zeros((self.num_leads, self.num_leads, len(w)),
                      dtype=np.complex128)

        Tw_split = np.zeros((self.num_leads, self.num_leads, len(w)),
                            dtype=np.complex128)

        Gw = np.zeros((self.num_leads, self.num_leads, len(w)),
                      dtype=np.complex128)

        if self._is_master_mpi_process:
            bar = progressbar.ProgressBar(
                widgets=[
                    " [",
                    progressbar.Timer(),
                    "] ",
                    progressbar.Bar(),
                    " (",
                    progressbar.ETA(),
                    ") ",
                ],
                max_value=(len(w_idx_split[self._comm.rank])),
            )
            counter = 0
            bar.start()

        for i in w_idx_split[self._comm.rank]:
            (
                iw_par_split[:, :, i],
                Tw_split[:, :, i],
            ) = self._partial_currents(
                w[i], chem_pot, temperature, potentials
            )

            if self._is_master_mpi_process:
                counter += 1
                bar.update(counter)

        if self._is_master_mpi_process:
            bar.finish()

        self._comm.Barrier()

        self._comm.Reduce(iw_par_split, iw_par, MPI.SUM, 0)
        self._comm.Bcast(iw_par, root=0)

        self._comm.Reduce(Tw_split, Tw, MPI.SUM, 0)
        self._comm.Bcast(Tw, root=0)

        self._comm.Barrier()

        Iw_tot = np.sum(iw_par, axis=1)
        i_par = simps(iw_par, x=w, axis=-1)
        I_tot = np.sum(i_par, axis=1)

        broadening_range = np.arange(
            -5 * self.delta_omega - 10 * temperature,
            10 * temperature + 5 * self.delta_omega + self.delta_omega / 2.0,
            self.delta_omega,
        )

        for i in range(self.num_leads):
            for j in range(self.num_leads):
                Gw[i, j, :] = (2 / (2 * np.pi)) * \
                              np.convolve(Tw[i, j, :], FT(broadening_range, temperature),
                    mode="same",
                )

        return (I_tot, Iw_tot, i_par, iw_par, Tw, Gw, w)

    ###########################################################################
    #                       WIDE BAND MODE ONLY CODE                          #
    def set_wide_band_self_energy(self, self_energy):
        """
        Sets up a list of wide band self energies for the leads.
        """

        self._wide_band_self_energy = self_energy
        self.green_function = GreenFunction(
            self.system.get_center_energies(),
            self.self_energies,
            wide_band=True)
        self.green_function.set_wide_band_self_energy(
            self._wide_band_self_energy)

    def set_wide_band_gamma(self, gamma):
        """
        Sets up a list of wide band gammas for the leads.
        """

        self._wide_band_gamma = gamma

    #                         PROCEED WITH CAUTION                            #
    ###########################################################################
