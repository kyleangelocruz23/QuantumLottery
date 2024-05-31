import cirq
import numpy as np


class QRNG:
    measure_gate_name = 'qrng_measure'
    qubit_name_prefix = 'qrng_'

    def __init__(self, simulator=None):
        if simulator is None:
            simulator = cirq.Simulator()
        self.simulator = simulator

    def generate_binary_array(self, length):
        qubits = cirq.NamedQubit.range(length, prefix=QRNG.qubit_name_prefix)
        h_gates = [cirq.H(qubit) for qubit in qubits]
        measure_gate = cirq.measure(qubits, key=QRNG.measure_gate_name)
        qrng_circuit = cirq.Circuit(h_gates, measure_gate)
        print(qrng_circuit)

        result = self.simulator.simulate(qrng_circuit)
        return result.measurements[QRNG.measure_gate_name]

    def winning_draw_numbers(self, numLength, numLimit):
        winningDraw = []
        while not len(winningDraw) == numLength:
            generateBin = qrng.generate_binary_array(7)
            binString = ""
            for bit in generateBin:
                binString += str(bit)
            randomBinInt = int(binString, 2)

            if (randomBinInt <= numLimit) and (randomBinInt not in winningDraw) and (randomBinInt != 0):
                winningDraw.append(randomBinInt)
        return winningDraw


qrng = QRNG()
input_length = int(input("Enter array length: "))
input_max = int(input("Enter max number: "))
generated_result = qrng.winning_draw_numbers(input_length, input_max)
print(generated_result)

