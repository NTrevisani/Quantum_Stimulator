# Basic class to define and manage q-bits

import math
import random
import numpy as np

PI = math.pi

class QBit(object):
    """Basic class for the managing of geometric shapes."""

    # sould we initialize all the
    # angles to 0? Does it make sense to have direct access to
    # them? Or should they be changed only through gates? 
    def __init__(self): 
        """Initialize the qbit. 

        The qbit is initialized in the |0> state, with its angle theta and phase
        phi set to 0. The two parameters are expressed in radians.
        """ 
        self.theta = 0
        self.phi = 0
        
    def set_theta(self, theta):
        self._theta = theta

    def get_theta(self):
        return self._theta

    theta = property(get_theta, set_theta, "The qbit angle in radians")          

    def set_phi(self, phi):
        self._phi = phi

    def get_phi(self):
        return self._phi

    phi = property(get_phi, set_phi, "The qbit phi phase in radians")          

    def measure(self):
        """Measures the qbit state in the canonical base.

        A random number between 0 and 1 is generated. If it is smaller than
        the cosine of theta, then the qbit is measured in the |0> state,
        otherwise it is measured in the |1> state.
        After the measurement, the theta and phi values of the qbit are
        updated accordingly. 
        """
        random_number = random.uniform(0, 1)
        if random_number < np.cos(self.theta):
            print("The qbit is in the |0> state")
            self.theta = 0
            self.phi = 0
        else:
            print("The qbit is in the |1> state")
            self.theta = PI
            self.phi = 0
    
    def __str__(self):
        """Print as 'A QBit with angle 'theta' and phase 'phi'."""
        self_class = type(self).__name__
        # \u03C0 is pi in unicode
        msg = "A {0} with angle {1}\u03C0 and phase {2}\u03C0."
        return msg.format(self_class, self.theta / PI, self.phi / PI)

    def __repr__(self):
        """Represents as 'Qbit(theta,phi)'."""
        self_class = type(self).__name__
        msg = "{0}({1},{2})"
        return msg.format(self_class, self.theta / PI, self.phi / PI)
    
    
if __name__ == '__main__':
    # Print a short description of the module
    print("The module allows to create and manage "
          "quantum bits.")


