#!/usr/bin/env python3
"""
This file contains implementation of OctopusCenter class, which reads the data
of the central region obtained via octopus and processes it for use in
transport calculations.
"""

from tinie.systems.central_region.center import Center


class OctopusCenter(Center):
    def __init__(self):
        Center.__init__(self)
