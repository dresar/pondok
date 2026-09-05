from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    """Halaman utama - Redirect ke login admin panel"""
    # Jika sudah login, redirect ke admin panel
    if request.user.is_authenticated:
        return redirect('admin-panel:index')
    # Jika belum login, redirect ke login
    return redirect('users:login')


def about(request):
    """Halaman tentang pondok - Redirect ke login admin panel"""
    # Jika sudah login, redirect ke admin panel
    if request.user.is_authenticated:
        return redirect('admin-panel:index')
    # Jika belum login, redirect ke login
    return redirect('users:login')
