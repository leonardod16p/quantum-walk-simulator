from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator 


simulator = AerSimulator()  


circuit = QuantumCircuit(2, 2)


circuit.h(0)
circuit.h(1)

circuit.measure([0, 1], [0, 1])


job = simulator.run(circuit, shots=1024)
result = job.result()
counts = result.get_counts(circuit)
print("resultados:", counts)

circuit.draw(output="mpl")