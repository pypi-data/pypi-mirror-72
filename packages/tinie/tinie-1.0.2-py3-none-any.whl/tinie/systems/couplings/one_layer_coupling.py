#!/usr/bin/env python3
"""
This file contains the implementation of the OneLayerCoupling class, which
calculates coupling between a discrete Lead object boundary and the Center
region by coupling a desired amount of points from the central region that
are the closest to some lead point to that lead point. Could be potentially
extended to any 1D lead slice instead of just the boundary, but that is a
story for another day. Calculates weak coupling, meaning that the lead and
center regions must not overlap.
"""

import cmath

import numpy as np
import progressbar
from tinie.systems.couplings.coupling import Coupling


class OneLayerCoupling(Coupling):
    def __init__(self, Center_object, Lead_object):
        """
        Parameters:
        -----------
        Center_object:  Center-like object
                        Central region to be used in coupling.

        Lead_object  :  Lead-like object
                        Lead region to be used in coupling.
        """

        Coupling.__init__(self, Center_object, Lead_object)
        self.type = "OneLayer"

        # Initialize flag that would allow to re-use already calculated
        # coupling matrix in case the system has not been altered in any way.
        self._recalculate_coupling = True

        # Set initial number of points from the central region to be coupled
        # to a single point in the lead region.
        self._num_coupling_points = 1

        # Set lead discretization parameters.
        self._num_lead_points = 25

        # Calculate the distance between the center and the lead (we assume
        # the are parallel to each other).
        self._lead_center_distance = self.calculate_lead_center_distance()

    def get_coupling_matrix_element(self, m, n):
        """
        Calculates a coupling matrix element corresponding to the lead region
        state number m and the center region state number n. Only use for
        testing purposes, for loop iteration over all the lead/center
        states is not as efficient as get_coupling_matrix command.

        Parameters:
        -----------
        m       :   int,
                    Lead object state number

        n       :   int,
                    Center object state number

        Returns:
        --------
        coupling_value: complex,
                        Value of the coupling matrix for the following states.
        """

        assert isinstance(m, int) and isinstance(
            n, int
        ), "State numbers must be integers"

        Lead_obj = self.Lead_object
        Center_obj = self.Center_object

        assert 0 <= m <= Lead_obj.get_number_of_states() - 1, "Lead state out of bounds"
        assert (
            0 <= n <= Center_obj.get_number_of_states() - 1
        ), "Center state out of bounds"

        lead_boundary = Lead_obj.get_boundary(self._num_lead_points)
        center_boundary = Center_obj.get_boundary(Lead_obj.alignment)

        lead_center_distance = self._lead_center_distance
        lead_spacing = lead_boundary[1] - lead_boundary[0]

        psi_lead_m = Lead_obj.get_boundary_state(m, self._num_lead_points)
        psi_center_n = Center_obj.get_boundary_state(n, Lead_obj.alignment)
        coupling_value = 0

        # Summation over the coordinates of the lead_boundary.
        for i in range(self._num_lead_points):

            # Distance array is made to pick the points from
            # center_boundary that are the closest to a point
            # in lead_boundary for the coupling.
            distance = np.array(
                [
                    abs(lead_boundary[i] - center_boundary[k])
                    for k in range(len(center_boundary[:]))
                ]
            )

            coupling_idx = np.argpartition(
                distance, self._num_coupling_points)[
                0: self._num_coupling_points]

            # Summation over the points from center_boundary that are
            # coupled to a point in lead_boundary.
            for j in coupling_idx:
                lead_point_center_point_distance = distance[j]
                theta = (
                    -(Lead_obj.B / 2)
                    * lead_center_distance
                    * lead_point_center_point_distance
                )
                t = (
                    (-1)
                    * ((lead_center_distance * lead_spacing) ** 2)
                    * 0.5
                    / (
                        lead_center_distance ** 2
                        + lead_point_center_point_distance ** 2
                    )
                )

                coupling_value += (
                    np.conj(psi_lead_m[i])
                    * psi_center_n[j]
                    * t
                    * cmath.exp(complex(0, -1) * theta)
                )

        return coupling_value

    def get_coupling_matrix(self):
        """
        Calculates the coupling matrix over the boundary slices.

        Returns
        -------
        coupling_matrix:    np.ndarray of shape
                            (num_lead_states, num_center_states),
                            Coupling matrix.
        """

        # Check if the matrix has already been calculated for the given
        # parameters.
        if self._recalculate_coupling is not True:
            return self.coupling_matrix

        # Setting up parameters
        Center_obj = self.Center_object
        Lead_obj = self.Lead_object

        lead_boundary = Lead_obj.get_boundary(self._num_lead_points)
        center_boundary = Center_obj.get_boundary(Lead_obj.alignment)

        lead_center_distance = self._lead_center_distance
        lead_spacing = lead_boundary[1] - lead_boundary[0]

        num_center_states = Center_obj.get_number_of_states()
        num_lead_states = Lead_obj.get_number_of_states()

        # Set up progress bar
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
            max_value=(num_center_states * num_lead_states),
        )

        coupling_matrix = np.zeros(
            (num_lead_states, num_center_states), dtype=complex)

        counter = 0
        bar.start()

        # Summation over the energy states of psi_lead.
        for m in range(num_lead_states):
            psi_lead_m = Lead_obj.get_boundary_state(m, self._num_lead_points)

            # Summation over the energy states of psi_center.
            for n in range(num_center_states):
                psi_center_n = Center_obj.get_boundary_state(
                    n, Lead_obj.alignment)
                coupling_value = 0

                # Summation over the coordinates of the lead_boundary.
                for i in range(self._num_lead_points):

                    # Distance array is made to pick the points from
                    # center_boundary that are the closest to a point
                    # in lead_boundary for the coupling.
                    distance = np.array(
                        [
                            abs(lead_boundary[i] - center_boundary[k])
                            for k in range(len(center_boundary[:]))
                        ]
                    )

                    coupling_idx = np.argpartition(distance, self._num_coupling_points)[
                        0: self._num_coupling_points]

                    # Summation over the points from center_boundary that are
                    # coupled to a point in lead_boundary.
                    for j in coupling_idx:

                        lead_point_center_point_distance = distance[j]
                        theta = (
                            -(Lead_obj.B / 2)
                            * lead_center_distance
                            * lead_point_center_point_distance
                        )
                        t = (
                            (-1)
                            * ((lead_center_distance * lead_spacing) ** 2)
                            * 0.5
                            / (
                                lead_center_distance ** 2
                                + lead_point_center_point_distance ** 2
                            )
                        )

                        coupling_value += (
                            np.conj(psi_lead_m[i])
                            * psi_center_n[j]
                            * t
                            * cmath.exp(complex(0, -1) * theta)
                        )

                coupling_matrix[m, n] = coupling_value
                counter += 1
                bar.update()

        bar.finish()
        self.coupling_matrix = coupling_matrix
        self._recalculate_coupling = False

        return coupling_matrix

    def set_num_coupling_points(self, num_coupling_points):
        """
        Change self.num_coupling_points.

        Parameters
        ----------
        num_coupling_points:    int,
                                New number of points in the central region to
                                be coupled to each individual lead point.
        """

        # Input sanity check:
        assert isinstance(
            num_coupling_points, int
        ), "Error: number of coupling points must be an integer"

        if self._num_coupling_points != num_coupling_points:
            self._num_coupling_points = num_coupling_points
            self._recalculate_coupling = True

    def set_num_lead_points(self, num_lead_points):
        """
        Change lead region discretization.

        Parameters
        ----------
        num_lead_points:    int,
                            New number of points in the lead slice.
        """

        # Input sanity check:
        assert isinstance(
            num_lead_points, int
        ), "Error: number of lead points on the boundary must be an integer"

        if self._num_lead_points != num_lead_points:
            self._num_lead_points = num_lead_points
            self._recalculate_coupling = True

    def calculate_lead_center_distance(self):
        """
        Calculate the distance between the lead region boundary and the
        central region boundary.

        Returns
        -------
        distance:       float,
                        Distance between the lead region boundary and the
                        central region boundary.
        """

        if self.Lead_object.alignment == "up":
            distance = (
                self.Lead_object.y[0] - self.Center_object.get_coordinates()[1][0, -1]
            )

        elif self.Lead_object.alignment == "down":
            distance = (self.Center_object.get_coordinates()
                        [1][0, 0] - self.Lead_object.y[1])

        elif self.Lead_object.alignment == "right":
            distance = (
                self.Lead_object.x[0] - self.Center_object.get_coordinates()[0][-1, 0]
            )

        else:
            distance = (self.Center_object.get_coordinates()
                        [0][0, 0] - self.Lead_object.x[1])

        assert 0 <= distance, "Error: lead and center regions overlap"
        self._lead_center_distance = distance

        return distance
