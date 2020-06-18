# Basic class to define and manage q-bits

import math
import random
import numpy as np

PI = math.pi

class QBit(object):
    """Basic class for the managing of qbits."""

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

    # Qbit angles

    def set_theta(self, theta):
        """Ensures 0 < theta < PI"""
        while theta > 2*PI:
            theta = theta - 2*PI
        while theta < 0:
            theta = theta + 2*PI
        if theta > PI and theta < 2*PI:
            theta = 2*PI - theta
        if theta < 0.001: # is this cheating?
            theta = 0
        self._theta = np.around(theta, 8)

    def get_theta(self):
        return self._theta

    theta = property(get_theta, set_theta, "The qbit angle in radians")          

    def set_phi(self, phi):
        """Ensures 0 < phi < 2*PI"""
        while phi >= 2*PI:
            phi = phi - 2*PI
        while phi < 0:
            phi = phi + 2*PI
        if phi < 0.001: # is this cheating?
            phi = 0
        self._phi = np.around(phi, 8)

    def get_phi(self):
        return self._phi

    phi = property(get_phi, set_phi, "The qbit phi phase in radians")          

    # Qbit measurement
    
    def measure(self):
        """Measures the qbit state in the canonical base.

        A random number between 0 and 1 is generated. If it is smaller than
        the cosine of theta, then the qbit is measured in the |0> state,
        otherwise it is measured in the |1> state.
        After the measurement, the theta and phi values of the qbit are
        updated accordingly. 
        If the qbit is in the |0> state, the function returns 0, if it is in
        the |1> state, it returns 1.
        """
        random_number = random.uniform(0, 1)
        if random_number < np.cos(self.theta):
            self.theta = 0
            self.phi = 0
            return 0
        else:
            self.theta = PI
            self.phi = 0
            return 1
            
    def get_state(self):
        """Prints the qbit state.

        The qbit is measured and the state is printed.
        """
        if self.measure() == 0:
            print("The qbit is in the |0> state")
        else:
            print("The qbit is in the |1> state")
            
    # Support representations

    def as_vector(self):
        """Represents a qbit state as a vector.

        The qbit state takes the form:
        |       cos (theta/2)      |
        | exp(i phi) sin (theta/2) |
        """
        qbit_vector = np.array([[np.around(np.cos(self.theta/2),8)],
                                [np.around(np.exp(self.phi*1j)*np.sin(self.theta/2),8)]])
        return qbit_vector

    def from_vector(vector_repr):
        """Returns a qbit from its vector representation."""
        new_theta = float(np.real(2*np.arccos(vector_repr[0])))
        #print("New_theta = ",new_theta)
        if np.sin(new_theta/2) < 0.0001: # is this cheating?
            new_phi = 0
        else:
            new_phi   = float(np.angle(vector_repr[1] / np.sin(new_theta/2)))
        #print("New_phi = ", new_phi)
        support_qbit = QBit()
        support_qbit.theta = new_theta
        support_qbit.phi   = new_phi
        return support_qbit
        
    # 1-qbit gates
    
    def general_qbit_gate(self, l, t, p):
        """Applies a general transformation to target qbit.
        
        The x gate is represented as a matrix with three parameters:
        - lambda (l)
        - theta  (t)
        - phi    (p)

        | cos(theta/2)               -exp(i lambda) sin(theta/2)        |
        | exp(i phi) sin(theta/2)     exp[i (lamda + phi)] cos(theta/2) |
        """
        general_gate_matrix = np.array([[np.cos(t/2),                  -np.exp(l * 1j) * np.sin(t/2)],
                                        [np.exp(p * 1j) * np.sin(t/2),  np.exp((l + p)*1j) * np.cos(t/2)]])
        product = np.dot(general_gate_matrix,  self.as_vector())
        support = QBit.from_vector(product)
        self.theta = support.theta
        self.phi   = support.phi  
        

    def x_gate(self):
        """Applies a 'x' gate to target qbit.
        
        The x gate is represented as a matrix:
        | 0 1 |
        | 1 0 |

        It is obtained from 'general_qbit_gate' with:
        l = 0
        t = PI
        p = 0
        """
        self.general_qbit_gate(0, PI, 0)

    def h_gate(self):
        """Applies a 'h' (hadamard) gate to target qbit.
        
        The h gate is represented as a matrix:
           1     | 1  1 | 
        sqrt(2)  | 1 -1 |

        It is obtained from 'general_qbit_gate' with:
        l = PI
        t = PI/2
        p = 0
        """
        self.general_qbit_gate(PI, PI/2, 0)

    def u1_gate(self, l):
        """Applies a 'u1' gate to target qbit.
        
        The h gate is represented as a matrix:
        | 1        0       | 
        | 0  exp(i lambda) |

        It is obtained from 'general_qbit_gate' with:
        l = lamda
        t = 0
        p = 0
        """
        self.general_qbit_gate(l, 0, 0)

    def u2_gate(self, l, p):
        """Applies a 'u2' gate to target qbit.
        
        The h gate is represented as a matrix:
           1     |     1          -exp(i lambda)   | 
        sqrt(2)  | exp(i phi)  exp[i(lambda + phi) |

        It is obtained from 'general_qbit_gate' with:
        l = lamda
        t = 0
        p = phi
        """
        self.general_qbit_gate(l, 0, p)

    def u3_gate(self, l, t, p):
        """Applies a 'u3' gate to target qbit.
        
        It corresponds to the general_qbit_gate, 
        so it just calls it.
        """
        self.general_qbit_gate(l, t, p)

    # DEPRECATED VERSION
    #    def x_gate(self):
    #        """Applies a 'x' gate to target qbit.
    #        
    #        The x gate is represented as a matrix:
    #        | 0 1 |
    #        | 1 0 |
    #        """
    #        x_gate_matrix = np.array([[0, 1],
    #                                  [1, 0]])
    #        product = np.dot(x_gate_matrix,  self.as_vector())
    #        support = QBit.from_vector(product)
    #        self.theta = support.theta
    #        self.phi   = support.phi  

    # DEPRECATED VERSION
    #    def h_gate(self):
    #        """Applies a 'h' (hadamard) gate to target qbit.
    #        
    #        The h gate is represented as a matrix:
    #           1     | 1  1 | 
    #        sqrt(2)  | 1 -1 |
    #        """
    #        h_gate_matrix = 1/np.sqrt(2)*np.array([[1,  1],
    #                                               [1, -1]])
    #        product = np.dot(h_gate_matrix,  self.as_vector())
    #        support = QBit.from_vector(product)
    #        self.theta = support.theta
    #        self.phi   = support.phi  

    # Print and Repr
    
    def __str__(self):
        """Print as 'A QBit with angle 'theta' and phase 'phi'."""
        self_class = type(self).__name__
        # \u03C0 is pi in unicode
        msg = "A {0} with angle {1}\u03C0 and phase {2}\u03C0."
        return msg.format(self_class, np.around(self.theta / PI, 2), np.around(self.phi / PI,2))

    def __repr__(self):
        """Represents as 'Qbit(theta,phi)'."""
        self_class = type(self).__name__
        msg = "{0}({1},{2})"
        return msg.format(self_class, np.around(self.theta / PI, 2), np.around(self.phi / PI,2))
    
    
if __name__ == '__main__':
    # Print a short description of the module
    print("The module allows to create and manage "
          "quantum bits.")


