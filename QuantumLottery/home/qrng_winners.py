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

    def winning_draw_numbers(self, num_length=6, num_limit=58):
        winning_draw = []
        while not len(winning_draw) == num_length:
            generate_bin = self.generate_binary_array(7)
            bin_string = ""
            for bit in generate_bin:
                bin_string += str(bit)
            random_bin_int = int(bin_string, 2)

            if (random_bin_int <= num_limit) and (random_bin_int not in winning_draw) and (random_bin_int != 0):
                winning_draw.append(random_bin_int)
        return winning_draw
