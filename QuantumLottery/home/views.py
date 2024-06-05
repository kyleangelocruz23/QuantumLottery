from django.shortcuts import render
from .qrng_ticket_id import generate_ticket_id, generate_qr_code
import os
import hvac
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def encrypt_data_aes(data: str, key: str) -> str:
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return f"{iv}:{ct}"


def decrypt_data_aes(data: str, key: str) -> str:
    iv, ct = data.split(':')
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')


def hash_ticket_id(ticket_id: str) -> str:
    sha256_hash = hashlib.sha256(ticket_id.encode()).hexdigest()
    return sha256_hash


def generate_unique_ticket_id(client) -> str:
    while True:
        ticket_id = generate_ticket_id()
        hashed_ticket_id = hash_ticket_id(ticket_id)
        secret_path = f'tickets/{hashed_ticket_id}'
        try:
            client.secrets.kv.v2.read_secret_version(path=secret_path)
        except hvac.exceptions.InvalidPath:
            # If the path does not exist, it's a unique ticket ID
            return ticket_id, hashed_ticket_id


def index(request):
    if request.method == "POST":
        selected_numbers = request.POST.get('selected_numbers')

        # Connect to Vault
        client = hvac.Client(url=os.getenv('VAULT_ADDR'), token=os.getenv('VAULT_TOKEN'))

        # Generate a unique ticket ID
        ticket_id, hashed_ticket_id = generate_unique_ticket_id(client)

        # Encrypt the selected numbers with AES-256 using the unhashed ticket ID
        encrypted_numbers = encrypt_data_aes(selected_numbers, ticket_id[:32])  # AES-256 requires a 32-byte key

        # Store the hashed ticket ID and encrypted numbers in Vault
        secret_path = f'tickets/{hashed_ticket_id}'
        client.secrets.kv.v2.create_or_update_secret(
            path=secret_path,
            secret={
                'ticket_id': hashed_ticket_id,
                'encrypted_numbers': encrypted_numbers
            }
        )

        # Ensure the directory for QR codes exists
        qr_code_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        if not os.path.exists(qr_code_dir):
            os.makedirs(qr_code_dir)
            print(f"Created directory: {qr_code_dir}")

        # Generate QR code with URL
        qr_code_url = f"http://127.0.0.1:8000/check-results/{ticket_id}"
        qr_code_path = os.path.join(qr_code_dir, f'ticket_qr_{ticket_id}.png')
        print(f"Generating QR code at: {qr_code_path} with URL: {qr_code_url}")  # Debugging statement
        generate_qr_code(qr_code_url, qr_code_path)

        # Check if the QR code file was created
        if os.path.exists(qr_code_path):
            print(f"QR code successfully generated at: {qr_code_path}")
        else:
            print(f"Failed to generate QR code at: {qr_code_path}")

        qr_code_url = f"/static/ticket_qr_{ticket_id}.png"
        print(f"QR code URL for rendering: {qr_code_url}")  # Debugging statement

        return render(request, 'home/result.html', {
            'selected_numbers': selected_numbers,
            'ticket_id': ticket_id,
            'qr_code_url': qr_code_url
        })
    return render(request, 'home/index.html')


def check_results(request, ticket_id=None):
    if request.method == "POST" or ticket_id:
        if not ticket_id:
            ticket_id = request.POST.get('ticket_id')

        # Hash the ticket ID with SHA-256
        hashed_ticket_id = hash_ticket_id(ticket_id)

        # Connect to Vault
        client = hvac.Client(url=os.getenv('VAULT_ADDR'), token=os.getenv('VAULT_TOKEN'))

        # Retrieve the secret from Vault
        secret_path = f'tickets/{hashed_ticket_id}'
        try:
            secret = client.secrets.kv.v2.read_secret_version(path=secret_path)
            encrypted_numbers = secret['data']['data']['encrypted_numbers']

            # Decrypt the numbers using the unhashed ticket ID
            decrypted_numbers = decrypt_data_aes(encrypted_numbers, ticket_id[:32])  # AES-256 requires a 32-byte key

            return render(request, 'home/check_results.html', {
                'decrypted_numbers': decrypted_numbers,
                'ticket_id': ticket_id
            })
        except hvac.exceptions.InvalidPath:
            return render(request, 'home/check_results.html', {
                'error': 'Invalid ticket ID. Please check your ticket ID and try again.'
            })
    return render(request, 'home/check_results.html')
