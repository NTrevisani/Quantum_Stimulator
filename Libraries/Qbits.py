# Basic class to define and manage q-bits

import math

PI = math.pi


class QBit(object):
    """Basic class for the managing of geometric shapes."""

    def __init__(self, theta, phi):
        """Initialize the qbit with its angle theta and phase phi in radians."""
        self.theta = theta
        self.phi = phi
        
    def set_theta(self, theta):
        self._theta = theta

    def get_theta(self):
        return self._theta

    theta = property(get_theta, set_theta, "The qbit angle in radians")          

    def set_phi(self, phi):
        self._phi = phi

    def get_phi(self):
        return self._phi

    phi = property(get_phi, set_phi, "The qbit phase in radians")          

    def __str__(self):
        """Print as 'A QBit with angle 'theta' and phase 'phi'."""
        self_class = type(self).__name__
        msg = "A {0} with angle {1} and phase {2}"
        return msg.format(self_class, self.theta, self.phi)

    def __repr__(self):
        """Represents as 'Qbit(theta,phi)'."""
        self_class = type(self).__name__
        msg = "{0}({1},{2})"
        return msg.format(self_class, self.theta, self.phi)
    
    
if __name__ == '__main__':
    # Print a short description of the module
    print("The module allows to create and manage "
          "quantum bits.")






    
