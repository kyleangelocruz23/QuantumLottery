# home/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .qrng_ticket_id import generate_ticket_id, generate_qr_code
import os

def index(request):
    if request.method == "POST":
        selected_numbers = request.POST.get('selected_numbers')
        ticket_id = generate_ticket_id()
        qr_code_path = os.path.join('static', 'ticket_qr.png')
        generate_qr_code(ticket_id, qr_code_path)
        return render(request, 'home/result.html', {
            'selected_numbers': selected_numbers,
            'ticket_id': ticket_id,
            'qr_code_path': qr_code_path
        })
    return render(request, 'home/index.html')
