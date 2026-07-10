from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator 
import matplotlib.pyplot as plt


#setting up the number of qubits in the circuit

number_of_qubits = 8

simulator = AerSimulator()  

#creating a n qubit circuit and n bit string to describe the state
circuit = QuantumCircuit(number_of_qubits, number_of_qubits)


#our initial state is going to be  |00000001> 
circuit.initialize('00000001', [0,1,2,3,4,5,6,7])


circuit.h(0)


circuit.measure([0,1,2,3,4,5,6,7], [0,1,2,3,4,5,6,7])


job = simulator.run(circuit, shots=1024)
result = job.result()
counts = result.get_counts(circuit)
print("resultados:", counts)

fig = circuit.draw(output="mpl")

plt.show()