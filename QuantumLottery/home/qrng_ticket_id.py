import cirq
import numpy as np
import qrcode
import os

def generate_random_bits(num_bits: int) -> np.ndarray:
    qubits = cirq.LineQubit.range(num_bits)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(cirq.measure(*qubits, key='result'))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    measured_bits = result.measurements['result'][0]
    return measured_bits

def bits_to_hex(bits: np.ndarray) -> str:
    bit_string = ''.join(str(bit) for bit in bits)
    hex_string = hex(int(bit_string, 2))[2:]
    return hex_string.zfill(64)

def generate_ticket_id() -> str:
    num_bits = 256
    random_bits = generate_random_bits(num_bits)
    ticket_id = bits_to_hex(random_bits)
    return ticket_id

def generate_qr_code(data: str, file_path: str) -> None:
    print(f"Generating QR code with data: {data} at path: {file_path}")  # Debugging statement
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(file_path)
    print(f"QR code generated and saved at: {file_path}")  # Debugging statement

if __name__ == "__main__":
    ticket_id = generate_ticket_id()
    print(f"Generated Ticket ID: {ticket_id}")
    qr_code_url = f"http://127.0.0.1:8000/check-results/{ticket_id}"
    generate_qr_code(qr_code_url, "ticket_qr.png")
    print(f"QR Code generated and saved as ticket_qr.png")
