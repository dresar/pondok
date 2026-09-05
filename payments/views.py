from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from admissions.models import Santri
from .models import Payment
from .forms import PaymentForm


def create_payment_view(request, santri_id):
    """Halaman upload bukti pembayaran"""
    santri = get_object_or_404(Santri, id=santri_id)
    
    # Cek apakah sudah ada payment untuk santri ini
    if hasattr(santri, 'payment'):
        messages.info(request, 'Anda sudah mengupload bukti pembayaran. Silakan tunggu verifikasi.')
        return redirect('payments:detail', payment_id=santri.payment.id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.santri = santri
            payment.save()
            messages.success(
                request,
                'Bukti pembayaran berhasil diupload! Silakan tunggu verifikasi dari panitia.'
            )
            return redirect('payments:detail', payment_id=payment.id)
        else:
            messages.error(request, 'Terdapat kesalahan dalam pengisian form. Silakan periksa kembali.')
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'santri': santri,
    }
    return render(request, 'payments/create.html', context)


def payment_detail_view(request, payment_id):
    """Halaman detail pembayaran"""
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'payments/detail.html', {'payment': payment})
