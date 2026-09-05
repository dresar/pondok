from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Santri
from .forms import SantriForm


def register_view(request):
    """Halaman pendaftaran santri baru"""
    if request.method == 'POST':
        form = SantriForm(request.POST)
        if form.is_valid():
            santri = form.save()
            messages.success(
                request,
                f'Pendaftaran berhasil! Silakan lanjutkan ke halaman pembayaran. Nomor pendaftaran Anda: {santri.nisn}'
            )
            return redirect('payments:create', santri_id=santri.id)
        else:
            messages.error(request, 'Terdapat kesalahan dalam pengisian form. Silakan periksa kembali.')
    else:
        form = SantriForm()
    
    return render(request, 'admissions/register.html', {'form': form})


def success_view(request):
    """Halaman sukses setelah pendaftaran"""
    return render(request, 'admissions/success.html')
