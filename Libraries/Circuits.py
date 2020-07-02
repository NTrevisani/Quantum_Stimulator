# Class to define circuits as lists of qbits

from Libraries.Qbits import QBit
import numpy as np

PI = np.pi

class Circuit(object):
    """Class to define circuits as lists of gates.

    The circuit object itself is a list of instructions
    that correspond to gates operating on the circuit qbits.
    """

    def __init__(self, qbits = []):
        """Initialize the circuit.

        A circuit is defined by its qbits and the gates
        operating on the qbits. Both are represented as lists.
        """
        self.qbits = qbits
        self.gates = []#np.array([])

    # Circuit qbits

    def set_qbits(self, qbits):
        """Qbits must be presented as a list."""
        for qbit in qbits:
            if isinstance(qbit, QBit) == False:
                raise TypeError("Qbits must be of class QBit")
        self._qbits = qbits

    def get_qbits(self):
        return self._qbits

    def delete_qbits(self):
        self.qbits = None
            
    qbits = property(get_qbits, set_qbits, delete_qbits, "The circuit qbits")

    # Circuit gates
    # 1-qbit gates
    
    def x_gate(self, q):
        """Applies a 'x' gate to target qbit q.
        
        Gates are identified by numbers.
        'x' gate number is 1.
        """
        instruction = (1, q)
        self.gates.append(instruction)

    def h_gate(self, q):
        """Applies a 'h' gate to target qbit q.
        
        Gates are identified by numbers.
        'h' gate number is 2.
        """
        instruction = (2, q)
        self.gates.append(instruction)

    def u1_gate(self, q, l):
        """Applies a 'u1' gate to target qbit q.
        
        Gates are identified by numbers.
        'u1' gate number is 3.
        """
        instruction = (3, q, l)
        self.gates.append(instruction)

    def u2_gate(self, q, l, p):
        """Applies a 'u2' gate to target qbit q.
        
        Gates are identified by numbers.
        'u2' gate number is 4.
        """
        instruction = (4, q, l, p)
        self.gates.append(instruction)

    def u3_gate(self, q, l, t, p):
        """Applies a 'u3' gate to target qbit q.
        
        Gates are identified by numbers.
        'u2' gate number is 5.
        """
        instruction = (5, q, l, t, p)
        self.gates.append(instruction)

    # 2-qbit gates

    def c_not_gate(self, q_ctrl, q_target):
        """Applies a 'c-not' gate to a pair of qbits.

        'q_ctrl' is the control qbit,
        'q_target' is the target qbit.

        Gates are identified by numbers.
        'c_not' gate number is 6.
        """
        instruction = (6, q_ctrl, q_target)
        self.gates.append(instruction)
    
    def c_h_gate(self, q_ctrl, q_target):
        """Applies a 'c-hadamard' gate to a pair of qbits.

        'q_ctrl' is the control qbit,
        'q_target' is the target qbit.

        Gates are identified by numbers.
        'c_h' gate number is 7.
        """
        instruction = (7, q_ctrl, q_target)
        self.gates.append(instruction)
    
    def c_u1_gate(self, q_ctrl, q_target, l):
        """Applies a 'c-u1' gate to a pair of qbits.
        
        'q_ctrl' is the control qbit,
        'q_target' is the target qbit.

        Gates are identified by numbers.
        'c-u1' gate number is 8.
        """
        instruction = (8, q_ctrl, q_target, l)
        self.gates.append(instruction)

    def c_u2_gate(self, q_ctrl, q_target, l, p):
        """Applies a 'c-u2' gate to a pair of qbits.
        
        'q_ctrl' is the control qbit,
        'q_target' is the target qbit.

        Gates are identified by numbers.
        'c-u2' gate number is 9.
        """
        instruction = (9, q_ctrl, q_target, l, p)
        self.gates.append(instruction)

    def c_u3_gate(self, q_ctrl, q_target, l, t, p):
        """Applies a 'c-u3' gate to a pair of qbits.
        
        'q_ctrl' is the control qbit,
        'q_target' is the target qbit.

        Gates are identified by numbers.
        'c-u3' gate number is 10.
        """
        instruction = (10, q_ctrl, q_target, l, t, p)
        self.gates.append(instruction)

    # Run the circuit
    def run(self):
        """Run the circuit."""
        # reset qbits values
        for qbit in self.qbits:
            qbit.theta = 0
            qbit.phi   = 0
        for gate in self.gates:
            #print(gate)
            # Case 1: 'x' gate
            if gate[0] == 1:
                QBit.x_gate(gate[1])
            # Case 2: 'h' gate
            elif gate[0] == 2:
                QBit.h_gate(gate[1])
            # Case 3: 'u1' gate
            elif gate[0] == 3:
                QBit.u1_gate(gate[1], gate[2])
            # Case 4: 'u2' gate
            elif gate[0] == 4:
                QBit.u2_gate(gate[1], gate[2], gate[3])
            # Case 5: 'u3' gate
            elif gate[0] == 5:
                QBit.u3_gate(gate[1], gate[2], gate[3], gate[4])
            # Case 6: 'c-not' gate
            elif gate[0] == 6:
                QBit.c_not_gate(gate[1], gate[2])
            # Case 7: 'c-hadamard' gate
            elif gate[0] == 7:
                QBit.c_h_gate(gate[1], gate[2])
            # Case 8: 'c-u1' gate
            elif gate[0] == 8:
                QBit.c_u1_gate(gate[1], gate[2], gate[3])
            # Case 9: 'c-u2' gate
            elif gate[0] == 9:
                QBit.c_u2_gate(gate[1], gate[2], gate[3], gate[4])
            # Case 10: 'c-u3' gate
            elif gate[0] == 10:
                QBit.c_u2_gate(gate[1], gate[2], gate[3], gate[4], gate[5])
            else:
                raise ValueError("The gate you selected is not available.")
        result = []
        for qbit in self.qbits:
            result.append(QBit.measure(qbit))
        return str(''.join(map(str, result)))

    # Execute the circuit
    def execute(self, N):
        """Run the circuit N times.
        
        The results are given as a dictionary
        of measurements-frequency.
        """
        output = {}
        for i in range(N):
            res = self.run()
            if res in output.keys():
                output[res] += 1                
            else:
                output[res] = 1
        return output
            
