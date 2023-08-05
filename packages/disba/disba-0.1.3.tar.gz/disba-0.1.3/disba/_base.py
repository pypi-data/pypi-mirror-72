from abc import ABC

import numpy


class BaseDispersion(ABC):
    def __init__(self, thickness, velocity_p, velocity_s, density, algorithm, dc):
        """Base class for surface wave dispersion."""
        self._thickness = numpy.asarray(thickness)
        self._velocity_p = numpy.asarray(velocity_p)
        self._velocity_s = numpy.asarray(velocity_s)
        self._density = numpy.asarray(density)
        self._algorithm = algorithm
        self._dc = dc

    @property
    def thickness(self):
        """Return layer thickness (in km)."""
        return self._thickness

    @property
    def velocity_p(self):
        """Return layer P-wave velocity (in km/s)."""
        return self._velocity_p

    @property
    def velocity_s(self):
        """Return layer S-wave velocity (in km/s)."""
        return self._velocity_s

    @property
    def density(self):
        """Return layer density (in g/cm3)."""
        return self._density

    @property
    def algorithm(self):
        """Return algorithm to use for computation of Rayleigh-wave dispersion."""
        return self._algorithm

    @property
    def dc(self):
        """Return phase velocity increment for root finding."""
        return self._dc
