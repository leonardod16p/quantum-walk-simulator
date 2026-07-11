from qiskit import transpile
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator 
import matplotlib.pyplot as plt

from qiskit.quantum_info import Operator
from qiskit.circuit.library import XGate, YGate
from qiskit.circuit.library import HamiltonianGate

import numpy as np
from math import pi 

#setting up the number of qubits in the circuit

number_of_qubits = 8


J = 2*pi * 1.0e6
time_evolution = pi / (4*J)


simulator = AerSimulator()  

#creating a n qubit circuit and n bit string to describe the state
circuit = QuantumCircuit(number_of_qubits, number_of_qubits)


#our initial state is going to be  |00000001> 
circuit.initialize('00000001', [0,1,2,3,4,5,6,7])


# we need to construct our coupling dynamic operator xixj + yiyj
# it is exist to permit the energy exchange between qubits



# constructing operations that depend on indexes
i = 0
j = 1

# defining gates X and Y
porta_x = XGate()
porta_y = YGate()

# we need to tell Operator the size of the matrix input and output. Each state is describe by a 2x1 matrix so we have the size of (2,2,2,2,2,2,2,2) 8*2
dimensoes_do_sistema = (2,) * number_of_qubits

identidade_global = Operator(np.eye(2**number_of_qubits), input_dims=dimensoes_do_sistema, output_dims=dimensoes_do_sistema)

xi = identidade_global.compose(porta_x, qargs=[i])
# operating with X or Y on the qubit of index i or j

#xi = circuit.x(i)
#xi = Operator(porta_x, input_dims=dimensoes_do_sistema, output_dims=dimensoes_do_sistema, qargs=[i])
# xj = circuit.x(j)
#xj = Operator(porta_x, input_dims=dimensoes_do_sistema, output_dims=dimensoes_do_sistema, qargs=[j])
xj = identidade_global.compose(porta_x, qargs=[j])
yi = identidade_global.compose(porta_y, qargs=[i])
yj = identidade_global.compose(porta_y, qargs=[j])

# yi = circuit.y(i)
#yi = Operator(porta_j, input_dims=dimensoes_do_sistema, output_dims=dimensoes_do_sistema, qargs=[i])
# yj = circuit.y(j)
#yj = Operator(porta_j, input_dims=dimensoes_do_sistema, output_dims=dimensoes_do_sistema, qargs=[j])


## i need to select where each XGate and YGate acts

## we can covert x gates to Operator, this will permit us to realize multiplication and sum to get our coupling operator

# op_xi = Operator(circuit)
# op_xj = Operator(circuit)

#op_yi = Operator(yi)
#op_yj = Operator(yj)

H = J * (xi @ xj + yi @ yj)

print(H)

#transformando hamiltoniana num operador unitario
gate_evolution = HamiltonianGate(H.data, time=time_evolution)


circuit.append(gate_evolution, [0,1,2,3,4,5,6,7])

circuit.measure([0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7])

circuit.measure([0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7])


step_type = input("Diga qual grupo de pares voce quer (w0 ou w1): ")

# create the step dynamics 
# it divides the 8 qubits into 2 groups of pairs that are permit to exchange energy 
# we select which one is 
if step_type == "w0":

    pairs = [(1,2), (3,4), (5,6), (7,8)]
    print(pairs)

elif step_type == "w1":
    pairs = [(2,3), (4,5), (6,7)]
    print(pairs)
else:
    # erro("You must select W0 or W1")
    # colocar algum tratamento de erro
    print("teste")

# return complete hamiltonian
# H_total = 


# criar vetor de probabilidades de tamanho number_of_qubits
#probs = 

# iterar sobre cada qubits e medir a probabilidade associada ao auto estado do operador Z
# para cada i no vetor estado (cada qubit do produto estado)
# atuo com o operador z no indice i
# calculo o valor esperado do vetor atuado com esse operador
# converto a probabilidade em i para probs[i] = (1 - o valor esperado calculado no passo anterior) / 2


#we are going to transpile the circuit to the matrix language that the simulator understands
translated_circuit = transpile(circuit, simulator)


job = simulator.run(translated_circuit, shots=1024)
result = job.result()
counts = result.get_counts(circuit)
print("resultados:", counts)

fig = circuit.draw(output="mpl")

plt.show()