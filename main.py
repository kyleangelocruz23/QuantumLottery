from qrng_ticket_id import generate_random_bits, bits_to_hex, bits_to_binary_string


def main():
    num_bits = 256
    random_bits = generate_random_bits(num_bits)
    ticket_id = bits_to_hex(random_bits)
    binary_id = bits_to_binary_string(random_bits)
    print(f"Generated Ticket ID: {ticket_id}")
    print(f"Generated Binary Ticket ID: {binary_id}")


if __name__ == "__main__":
    main()