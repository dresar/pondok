from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db import models
from django.utils import timezone
from django.core.paginator import Paginator
from .models import User, LoginHistory
from admissions.models import Santri
from payments.models import BankAccount, Payment


def login_view(request):
    """Halaman Login untuk Admin dan User"""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin-panel:index')
        else:
            return redirect('users:dashboard')
    
    if request.method == 'POST':
        # Handle Register
        if request.POST.get('register_submit'):
            # Register new user
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            
            # Validasi
            errors = []
            
            if not username:
                errors.append('Username wajib diisi.')
            elif User.objects.filter(username=username).exists():
                errors.append('Username sudah digunakan.')
            
            if not email:
                errors.append('Email wajib diisi.')
            elif User.objects.filter(email=email).exists():
                errors.append('Email sudah terdaftar.')
            else:
                from django.core.validators import validate_email
                from django.core.exceptions import ValidationError
                try:
                    validate_email(email)
                except ValidationError:
                    errors.append('Format email tidak valid.')
            
            if not password1:
                errors.append('Password wajib diisi.')
            elif len(password1) < 8:
                errors.append('Password minimal 8 karakter.')
            elif password1 != password2:
                errors.append('Password dan konfirmasi password tidak cocok.')
            
            if not first_name:
                errors.append('Nama depan wajib diisi.')
            
            if errors:
                for error in errors:
                    messages.error(request, error)
            else:
                try:
                    # Buat user baru (bukan staff/admin)
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password1,
                        first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        is_staff=False,
                        is_superuser=False,
                        role='user'  # Set role sebagai user biasa, bukan petugas pendaftaran
                    )
                    # Auto-login setelah registrasi berhasil
                    login(request, user)
                    # Record successful login dari registrasi
                    try:
                        ip_address = get_client_ip(request)
                        user_agent = request.META.get('HTTP_USER_AGENT', '')
                        LoginHistory.objects.create(
                            username=username,
                            user=user,
                            ip_address=ip_address,
                            user_agent=user_agent,
                            status='success'
                        )
                    except Exception as e:
                        # Log error tapi jangan gagalkan registrasi
                        import logging
                        import traceback
                        logger = logging.getLogger(__name__)
                        logger.error(f'Error recording login history for {username} (registration): {e}')
                        logger.error(traceback.format_exc())
                        # Juga print ke console untuk debugging
                        print(f'ERROR: Failed to record login history for {username} (registration): {e}')
                        print(traceback.format_exc())
                    messages.success(request, f'Registrasi berhasil! Selamat datang, {user.get_full_name() or user.username}!')
                    return redirect('users:dashboard')
                except Exception as e:
                    messages.error(request, f'Terjadi kesalahan saat registrasi: {str(e)}')
            
            # Get WebsiteSettings for context
            from core.models import WebsiteSettings
            settings = WebsiteSettings.load()
            return render(request, 'users/login.html', {'settings': settings})
        
        # Handle Login (Universal - auto detect admin or user)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Get IP address and user agent
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Check for axes lockout before attempting login
        try:
            from axes.utils import is_locked
            if is_locked(request, credentials={'username': username}):
                LoginHistory.objects.create(
                    username=username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    status='failed',
                    error_message='Akun terkunci karena terlalu banyak percobaan login gagal'
                )
                messages.error(request, 'Akun Anda terkunci karena terlalu banyak percobaan login gagal. Silakan coba lagi nanti.')
                # Get WebsiteSettings for context
                from core.models import WebsiteSettings
                settings = WebsiteSettings.load()
                return render(request, 'users/login.html', {'settings': settings})
        except ImportError:
            pass  # Axes not installed, skip lockout check
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Record successful login
            try:
                LoginHistory.objects.create(
                    username=username,
                    user=user,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    status='success'
                )
            except Exception as e:
                # Log error tapi jangan gagalkan login
                import logging
                import traceback
                logger = logging.getLogger(__name__)
                logger.error(f'Error recording login history for {username}: {e}')
                logger.error(traceback.format_exc())
                # Juga print ke console untuk debugging
                print(f'ERROR: Failed to record login history for {username}: {e}')
                print(traceback.format_exc())
            
            # Auto redirect berdasarkan role
            if user.is_staff or user.is_superuser:
                messages.success(request, f'Selamat datang, {user.username}!')
                return redirect('admin-panel:index')
            else:
                messages.success(request, f'Selamat datang, {user.get_full_name() or user.username}!')
                return redirect('users:dashboard')
        else:
            # Record failed login (wrong credentials)
            try:
                LoginHistory.objects.create(
                    username=username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    status='failed',
                    error_message='Username atau password salah'
                )
            except Exception as e:
                # Log error tapi jangan gagalkan proses
                import logging
                import traceback
                logger = logging.getLogger(__name__)
                logger.error(f'Error recording failed login history for {username}: {e}')
                logger.error(traceback.format_exc())
                # Juga print ke console untuk debugging
                print(f'ERROR: Failed to record failed login history for {username}: {e}')
                print(traceback.format_exc())
            messages.error(request, 'Username atau password salah.')
    
    # Get WebsiteSettings for context
    from core.models import WebsiteSettings
    settings = WebsiteSettings.load()
    return render(request, 'users/login.html', {'settings': settings})


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    
    # Return None if IP is empty or invalid
    if not ip or ip == '':
        return None
    return ip


def register_view(request):
    """Halaman Registrasi untuk User Public (Calon Santri/Orang Tua) - DEPRECATED: Gunakan form di login.html"""
    # Redirect ke login page dengan tab register
    return redirect('users:login')
    
    # Kode di bawah ini tidak akan pernah dieksekusi, hanya untuk referensi
    if False and request.user.is_authenticated:
        return redirect('admin-panel:index')
    
    if False and request.method == 'POST':
        from admissions.models import Santri
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        
        # Data Akun
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Data Pribadi Santri
        nama_lengkap = request.POST.get('nama_lengkap', '').strip()
        nisn = request.POST.get('nisn', '').strip()
        tempat_lahir = request.POST.get('tempat_lahir', '').strip()
        tanggal_lahir = request.POST.get('tanggal_lahir', '')
        jenis_kelamin = request.POST.get('jenis_kelamin', '')
        agama = request.POST.get('agama', 'Islam')  # Wajib Islam
        golongan_darah = request.POST.get('golongan_darah', '')
        tinggi_badan = request.POST.get('tinggi_badan', '') or None
        berat_badan = request.POST.get('berat_badan', '') or None
        
        # Data Orang Tua
        nama_ayah = request.POST.get('nama_ayah', '').strip()
        nama_ibu = request.POST.get('nama_ibu', '').strip()
        nik_ayah = request.POST.get('nik_ayah', '').strip()
        nik_ibu = request.POST.get('nik_ibu', '').strip()
        pekerjaan_ayah = request.POST.get('pekerjaan_ayah', '').strip()
        pekerjaan_ibu = request.POST.get('pekerjaan_ibu', '').strip()
        no_hp_ayah = request.POST.get('no_hp_ayah', '').strip()
        no_hp_ibu = request.POST.get('no_hp_ibu', '').strip()
        alamat_orangtua = request.POST.get('alamat_orangtua', '').strip()
        
        # Kontak & Alamat
        alamat = request.POST.get('alamat', '').strip()
        no_hp = request.POST.get('no_hp', '').strip()
        santri_email = request.POST.get('santri_email', '').strip()
        
        # Data Sekolah
        asal_sekolah = request.POST.get('asal_sekolah', '').strip()
        kelas_terakhir = request.POST.get('kelas_terakhir', '').strip()
        tahun_lulus = request.POST.get('tahun_lulus', '').strip()
        no_ijazah = request.POST.get('no_ijazah', '').strip()
        
        # Catatan
        catatan = request.POST.get('catatan', '').strip()
        
        # Validasi
        errors = []
        
        # Validasi Akun
        if not username:
            errors.append('Username wajib diisi.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username sudah digunakan.')
        
        if not email:
            errors.append('Email wajib diisi.')
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append('Format email tidak valid.')
            if User.objects.filter(email=email).exists():
                errors.append('Email sudah terdaftar.')
        
        if not password1:
            errors.append('Password wajib diisi.')
        elif len(password1) < 8:
            errors.append('Password minimal 8 karakter.')
        elif password1 != password2:
            errors.append('Password dan konfirmasi password tidak cocok.')
        
        # Validasi Data Santri
        if not nama_lengkap:
            errors.append('Nama lengkap santri wajib diisi.')
        
        if not nisn:
            errors.append('NISN wajib diisi.')
        elif len(nisn) != 10 or not nisn.isdigit():
            errors.append('NISN harus 10 digit angka.')
        elif Santri.objects.filter(nisn=nisn).exists():
            errors.append('NISN sudah terdaftar.')
        
        if not tempat_lahir:
            errors.append('Tempat lahir wajib diisi.')
        
        if not tanggal_lahir:
            errors.append('Tanggal lahir wajib diisi.')
        
        if not jenis_kelamin:
            errors.append('Jenis kelamin wajib diisi.')
        
        if agama != 'Islam':
            errors.append('Agama harus Islam.')
        
        if not nama_ayah:
            errors.append('Nama ayah wajib diisi.')
        
        if not nama_ibu:
            errors.append('Nama ibu wajib diisi.')
        
        if not alamat:
            errors.append('Alamat wajib diisi.')
        
        if not no_hp:
            errors.append('No. HP wajib diisi.')
        
        if not asal_sekolah:
            errors.append('Asal sekolah wajib diisi.')
        
        if not kelas_terakhir:
            errors.append('Kelas terakhir wajib diisi.')
        
        # Jika ada error, tampilkan dan return
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # Buat user baru (bukan staff/admin)
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=nama_lengkap.split()[0] if nama_lengkap else '',
                    last_name=' '.join(nama_lengkap.split()[1:]) if len(nama_lengkap.split()) > 1 else '',
                    phone=no_hp,
                    is_staff=False,
                    is_superuser=False
                )
                
                # Buat data Santri (dengan semua field lengkap)
                santri_data = {
                    'nama_lengkap': nama_lengkap,
                    'nama_panggilan': request.POST.get('nama_panggilan', '') or '',
                    'nisn': nisn,
                    'tempat_lahir': tempat_lahir,
                    'tanggal_lahir': tanggal_lahir,
                    'jenis_kelamin': jenis_kelamin,
                    'agama': 'Islam',
                    'kewarganegaraan': request.POST.get('kewarganegaraan', 'WNI'),
                    'anak_ke': int(request.POST.get('anak_ke', 0)) if request.POST.get('anak_ke') else None,
                    'jumlah_saudara': int(request.POST.get('jumlah_saudara', 0)) if request.POST.get('jumlah_saudara') else None,
                    'bahasa_sehari_hari': request.POST.get('bahasa_sehari_hari', 'Indonesia'),
                    'golongan_darah': golongan_darah or None,
                    'tinggi_badan': int(tinggi_badan) if tinggi_badan else None,
                    'berat_badan': int(berat_badan) if berat_badan else None,
                    'riwayat_penyakit': request.POST.get('riwayat_penyakit', '') or '',
                    'tinggal_dengan': request.POST.get('tinggal_dengan', '') or '',
                    'nama_ayah': nama_ayah,
                    'nama_ibu': nama_ibu,
                    'nik_ayah': nik_ayah or '',
                    'nik_ibu': nik_ibu or '',
                    'tempat_lahir_ayah': request.POST.get('tempat_lahir_ayah', '') or '',
                    'tanggal_lahir_ayah': request.POST.get('tanggal_lahir_ayah') or None,
                    'agama_ayah': request.POST.get('agama_ayah', 'Islam'),
                    'kewarganegaraan_ayah': request.POST.get('kewarganegaraan_ayah', 'WNI'),
                    'pendidikan_ayah': request.POST.get('pendidikan_ayah', '') or '',
                    'pekerjaan_ayah': pekerjaan_ayah or '',
                    'no_hp_ayah': no_hp_ayah or '',
                    'status_ayah': request.POST.get('status_ayah', 'HIDUP'),
                    'tempat_lahir_ibu': request.POST.get('tempat_lahir_ibu', '') or '',
                    'tanggal_lahir_ibu': request.POST.get('tanggal_lahir_ibu') or None,
                    'agama_ibu': request.POST.get('agama_ibu', 'Islam'),
                    'kewarganegaraan_ibu': request.POST.get('kewarganegaraan_ibu', 'WNI'),
                    'pendidikan_ibu': request.POST.get('pendidikan_ibu', '') or '',
                    'pekerjaan_ibu': pekerjaan_ibu or '',
                    'no_hp_ibu': no_hp_ibu or '',
                    'status_ibu': request.POST.get('status_ibu', 'HIDUP'),
                    'alamat_orangtua': alamat_orangtua or '',
                    'alamat': alamat,
                    'desa': request.POST.get('desa', '') or '',
                    'kecamatan': request.POST.get('kecamatan', '') or '',
                    'kabupaten': request.POST.get('kabupaten', '') or '',
                    'provinsi': request.POST.get('provinsi', '') or '',
                    'kode_pos': request.POST.get('kode_pos', '') or '',
                    'no_hp': no_hp,
                    'email': santri_email or '',
                    'asal_sekolah': asal_sekolah,
                    'npsn_sekolah': request.POST.get('npsn_sekolah', '') or '',
                    'kelas_terakhir': kelas_terakhir,
                    'tahun_lulus': tahun_lulus or '',
                    'no_ijazah': no_ijazah or '',
                    'kelas_diterima': request.POST.get('kelas_diterima', '') or '',
                    'tanggal_diterima': request.POST.get('tanggal_diterima') or None,
                    'catatan': catatan or '',
                    'status': 'pending',
                }
                
                # Handle file uploads
                if 'foto_santri' in request.FILES:
                    santri_data['foto_santri'] = request.FILES['foto_santri']
                if 'foto_ktp' in request.FILES:
                    santri_data['foto_ktp'] = request.FILES['foto_ktp']
                if 'foto_akta' in request.FILES:
                    santri_data['foto_akta'] = request.FILES['foto_akta']
                if 'foto_ijazah' in request.FILES:
                    santri_data['foto_ijazah'] = request.FILES['foto_ijazah']
                if 'surat_sehat' in request.FILES:
                    santri_data['surat_sehat'] = request.FILES['surat_sehat']
                
                # Link user dengan santri (jika ada field user di model Santri)
                santri = Santri.objects.create(**santri_data)
                
                messages.success(request, 'Registrasi berhasil! Silakan login untuk melanjutkan.')
                return redirect('users:login')
                
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan saat registrasi: {str(e)}')
    
    return render(request, 'users/register.html')


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'Anda telah berhasil logout.')
    return redirect('users:login')


@login_required
def dashboard(request):
    """User Dashboard"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    context = {
        'user': request.user,
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def profile(request):
    """User Profile dengan statistik lengkap"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    user = request.user
    is_editing = request.GET.get('edit') == '1'
    
    # Cari data santri terkait
    santri = None
    if user.email:
        santri = Santri.objects.filter(email=user.email).first()
    if not santri and user.phone:
        santri = Santri.objects.filter(no_hp=user.phone).first()
    
    # Statistik pembayaran (OneToOneField dengan Santri)
    payment = None
    if santri:
        try:
            payment = Payment.objects.filter(santri=santri).first()
        except:
            pass
    
    # Untuk kompatibilitas dengan template, buat list
    payments = [payment] if payment else []
    
    payment_stats = {
        'total': 1 if payment else 0,
        'verified': 1 if payment and payment.status == 'verified' else 0,
        'pending': 1 if payment and payment.status == 'pending' else 0,
        'rejected': 1 if payment and payment.status == 'rejected' else 0,
        'total_amount': payment.jumlah_transfer if payment and payment.status == 'verified' else 0
    }
    
    # Hitung hari sejak bergabung
    days_since_joined = None
    if user.date_joined:
        from django.utils import timezone
        days_since_joined = (timezone.now() - user.date_joined).days
    
    # Hitung hari sejak login terakhir
    days_since_login = None
    if user.last_login:
        days_since_login = (timezone.now() - user.last_login).days
    
    # Get login history - termasuk yang user=None (login gagal dengan username salah)
    # Login history untuk user ini (baik yang user=user atau username=user.username)
    from django.db.models import Q
    
    # Filter berdasarkan status jika ada parameter
    status_filter = request.GET.get('status', '')
    login_history_query = LoginHistory.objects.filter(
        Q(user=user) | Q(username=user.username)
    )
    
    # Apply status filter
    if status_filter == 'success':
        login_history_query = login_history_query.filter(status='success')
    elif status_filter == 'failed':
        login_history_query = login_history_query.filter(status='failed')
    
    # Order by created_at descending
    login_history_query = login_history_query.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(login_history_query, 20)  # 20 items per page
    page_number = request.GET.get('page', 1)
    login_history_page = paginator.get_page(page_number)
    
    # Hitung login berhasil (hanya yang user=user karena login berhasil pasti ada user)
    successful_logins = LoginHistory.objects.filter(
        user=user, 
        status='success'
    ).count()
    
    # Hitung login gagal (bisa user=user atau username=user.username karena login gagal bisa username salah)
    failed_logins = LoginHistory.objects.filter(
        Q(user=user) | Q(username=user.username),
        status='failed'
    ).count()
    
    # Get recent login attempts (last 30 days)
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    recent_successful = LoginHistory.objects.filter(
        user=user, 
        status='success',
        created_at__gte=thirty_days_ago
    ).count()
    recent_failed = LoginHistory.objects.filter(
        Q(user=user) | Q(username=user.username),
        status='failed',
        created_at__gte=thirty_days_ago
    ).count()
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            # Delete old avatar if exists
            if user.avatar:
                try:
                    user.avatar.delete(save=False)
                except:
                    pass
            user.avatar = request.FILES['avatar']
        
        user.save()
        messages.success(request, 'Profil berhasil diperbarui!')
        return redirect('users:profile')
    
    context = {
        'user': user,
        'santri': santri,
        'payment': payment,
        'payment_stats': payment_stats,
        'days_since_joined': days_since_joined,
        'days_since_login': days_since_login,
        'login_history': login_history_page,
        'login_history_all': login_history_query,  # For total count
        'successful_logins': successful_logins,
        'failed_logins': failed_logins,
        'recent_successful': recent_successful,
        'recent_failed': recent_failed,
        'is_editing': is_editing,
        'status_filter': status_filter,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def pendaftaran(request):
    """Form Pendaftaran Santri"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    from admissions.models import Santri
    
    # Cek apakah sudah ada data santri
    santri = None
    if request.user.email:
        santri = Santri.objects.filter(email=request.user.email).first()
    if not santri and request.user.phone:
        santri = Santri.objects.filter(no_hp=request.user.phone).first()
    
    # Mode edit (dari query parameter)
    edit_mode = request.GET.get('edit', 'false') == 'true'
    
    if request.method == 'POST':
        from admissions.models import Santri
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        
        # Data Pribadi Santri
        nama_lengkap = request.POST.get('nama_lengkap', '').strip()
        nisn = request.POST.get('nisn', '').strip()
        tempat_lahir = request.POST.get('tempat_lahir', '').strip()
        tanggal_lahir = request.POST.get('tanggal_lahir', '')
        jenis_kelamin = request.POST.get('jenis_kelamin', '')
        agama = request.POST.get('agama', 'Islam')  # Wajib Islam
        golongan_darah = request.POST.get('golongan_darah', '')
        tinggi_badan = request.POST.get('tinggi_badan', '') or None
        berat_badan = request.POST.get('berat_badan', '') or None
        
        # Data Orang Tua
        nama_ayah = request.POST.get('nama_ayah', '').strip()
        nama_ibu = request.POST.get('nama_ibu', '').strip()
        nik_ayah = request.POST.get('nik_ayah', '').strip()
        nik_ibu = request.POST.get('nik_ibu', '').strip()
        pekerjaan_ayah = request.POST.get('pekerjaan_ayah', '').strip()
        pekerjaan_ibu = request.POST.get('pekerjaan_ibu', '').strip()
        no_hp_ayah = request.POST.get('no_hp_ayah', '').strip()
        no_hp_ibu = request.POST.get('no_hp_ibu', '').strip()
        alamat_orangtua = request.POST.get('alamat_orangtua', '').strip()
        
        # Kontak & Alamat
        alamat = request.POST.get('alamat', '').strip()
        no_hp = request.POST.get('no_hp', '').strip()
        santri_email = request.POST.get('santri_email', '').strip()
        
        # Data Sekolah
        asal_sekolah = request.POST.get('asal_sekolah', '').strip()
        kelas_terakhir = request.POST.get('kelas_terakhir', '').strip()
        tahun_lulus = request.POST.get('tahun_lulus', '').strip()
        no_ijazah = request.POST.get('no_ijazah', '').strip()
        
        # Catatan
        catatan = request.POST.get('catatan', '').strip()
        
        # Validasi
        errors = []
        
        # Validasi Data Santri
        if not nama_lengkap:
            errors.append('Nama lengkap santri wajib diisi.')
        
        if not nisn:
            errors.append('NISN wajib diisi.')
        elif len(nisn) != 10 or not nisn.isdigit():
            errors.append('NISN harus 10 digit angka.')
        elif santri:
            # Jika edit mode, skip validasi NISN jika sama dengan yang lama
            if santri.nisn != nisn and Santri.objects.filter(nisn=nisn).exists():
                errors.append('NISN sudah terdaftar.')
        elif Santri.objects.filter(nisn=nisn).exists():
            errors.append('NISN sudah terdaftar.')
        
        if not tempat_lahir:
            errors.append('Tempat lahir wajib diisi.')
        
        if not tanggal_lahir:
            errors.append('Tanggal lahir wajib diisi.')
        
        if not jenis_kelamin:
            errors.append('Jenis kelamin wajib diisi.')
        
        if agama != 'Islam':
            errors.append('Agama harus Islam.')
        
        if not nama_ayah:
            errors.append('Nama ayah wajib diisi.')
        
        if not nama_ibu:
            errors.append('Nama ibu wajib diisi.')
        
        if not alamat:
            errors.append('Alamat wajib diisi.')
        
        if not no_hp:
            errors.append('No. HP wajib diisi.')
        
        if not asal_sekolah:
            errors.append('Asal sekolah wajib diisi.')
        
        if not kelas_terakhir:
            errors.append('Kelas terakhir wajib diisi.')
        
        # Jika ada error, tampilkan dan return
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                # Buat data Santri (dengan semua field lengkap)
                santri_data = {
                    'nama_lengkap': nama_lengkap,
                    'nama_panggilan': nama_panggilan or '',
                    'nisn': nisn,
                    'tempat_lahir': tempat_lahir,
                    'tanggal_lahir': tanggal_lahir,
                    'jenis_kelamin': jenis_kelamin,
                    'agama': 'Islam',  # Wajib Islam
                    'kewarganegaraan': kewarganegaraan,
                    'anak_ke': int(anak_ke) if anak_ke else None,
                    'jumlah_saudara': int(jumlah_saudara) if jumlah_saudara else None,
                    'bahasa_sehari_hari': bahasa_sehari_hari,
                    'golongan_darah': golongan_darah or None,
                    'tinggi_badan': int(tinggi_badan) if tinggi_badan else None,
                    'berat_badan': int(berat_badan) if berat_badan else None,
                    'riwayat_penyakit': riwayat_penyakit or '',
                    'tinggal_dengan': tinggal_dengan or '',
                    'nama_ayah': nama_ayah,
                    'nama_ibu': nama_ibu,
                    'nik_ayah': nik_ayah or '',
                    'nik_ibu': nik_ibu or '',
                    'tempat_lahir_ayah': tempat_lahir_ayah or '',
                    'tanggal_lahir_ayah': tanggal_lahir_ayah,
                    'agama_ayah': agama_ayah,
                    'kewarganegaraan_ayah': kewarganegaraan_ayah,
                    'pendidikan_ayah': pendidikan_ayah or '',
                    'pekerjaan_ayah': pekerjaan_ayah or '',
                    'no_hp_ayah': no_hp_ayah or '',
                    'status_ayah': status_ayah,
                    'tempat_lahir_ibu': tempat_lahir_ibu or '',
                    'tanggal_lahir_ibu': tanggal_lahir_ibu,
                    'agama_ibu': agama_ibu,
                    'kewarganegaraan_ibu': kewarganegaraan_ibu,
                    'pendidikan_ibu': pendidikan_ibu or '',
                    'pekerjaan_ibu': pekerjaan_ibu or '',
                    'no_hp_ibu': no_hp_ibu or '',
                    'status_ibu': status_ibu,
                    'alamat_orangtua': alamat_orangtua or '',
                    'alamat': alamat,
                    'desa': desa or '',
                    'kecamatan': kecamatan or '',
                    'kabupaten': kabupaten or '',
                    'provinsi': provinsi or '',
                    'kode_pos': kode_pos or '',
                    'no_hp': no_hp,
                    'email': santri_email or '',
                    'asal_sekolah': asal_sekolah,
                    'npsn_sekolah': npsn_sekolah or '',
                    'kelas_terakhir': kelas_terakhir,
                    'tahun_lulus': tahun_lulus or '',
                    'no_ijazah': no_ijazah or '',
                    'kelas_diterima': kelas_diterima or '',
                    'tanggal_diterima': tanggal_diterima,
                    'catatan': catatan or '',
                    'status': 'pending',
                }
                
                # Handle file uploads
                if 'foto_santri' in request.FILES:
                    santri_data['foto_santri'] = request.FILES['foto_santri']
                if 'foto_ktp' in request.FILES:
                    santri_data['foto_ktp'] = request.FILES['foto_ktp']
                if 'foto_akta' in request.FILES:
                    santri_data['foto_akta'] = request.FILES['foto_akta']
                if 'foto_ijazah' in request.FILES:
                    santri_data['foto_ijazah'] = request.FILES['foto_ijazah']
                if 'surat_sehat' in request.FILES:
                    santri_data['surat_sehat'] = request.FILES['surat_sehat']
                
                # Update atau create santri
                if santri:
                    # Update data santri yang sudah ada
                    for key, value in santri_data.items():
                        setattr(santri, key, value)
                    santri.save()
                    messages.success(request, 'Data pendaftaran berhasil diperbarui!')
                else:
                    # Buat santri baru
                    santri = Santri.objects.create(**santri_data)
                    # Link dengan user (update email/no_hp jika belum ada)
                    if not santri.email and request.user.email:
                        santri.email = request.user.email
                        santri.save()
                    if not santri.no_hp and request.user.phone:
                        santri.no_hp = request.user.phone
                        santri.save()
                    messages.success(request, 'Pendaftaran santri berhasil! Data Anda sedang dalam proses verifikasi.')
                
                return redirect('users:pendaftaran')
                
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan saat pendaftaran: {str(e)}')
    
    context = {
        'santri': santri,
        'has_santri': santri is not None,
        'edit_mode': edit_mode,
    }
    return render(request, 'users/pendaftaran.html', context)


@login_required
def status(request):
    """Status Pendaftaran"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    from admissions.models import Santri
    
    # Cek sederhana: cari santri dengan email atau no_hp yang sama dengan user
    santri = None
    if request.user.email:
        santri = Santri.objects.filter(email=request.user.email).first()
    if not santri and request.user.phone:
        santri = Santri.objects.filter(no_hp=request.user.phone).first()
    
    # Cek payment jika ada santri
    payment = None
    if santri:
        try:
            payment = santri.payment
        except:
            pass
    
    context = {
        'santri': santri,
        'has_santri': santri is not None,
        'payment': payment,
    }
    return render(request, 'users/status.html', context)


@login_required
def dokumen(request):
    """Dokumen User"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    # Cari santri berdasarkan email atau phone user
    santri = None
    if request.user.email:
        santri = Santri.objects.filter(email=request.user.email).first()
    if not santri and request.user.phone:
        santri = Santri.objects.filter(no_hp=request.user.phone).first()
    
    context = {
        'santri': santri,
    }
    return render(request, 'users/dokumen.html', context)


@login_required
def dokumen_download(request, doc_type):
    """Download individual dokumen/gambar"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    # Validasi doc_type
    valid_doc_types = ['foto_santri', 'foto_ktp', 'foto_akta', 'foto_ijazah', 'surat_sehat']
    if doc_type not in valid_doc_types:
        messages.error(request, 'Jenis dokumen tidak valid.')
        return redirect('users:dokumen')
    
    # Cari santri
    santri = None
    if request.user.email:
        santri = Santri.objects.filter(email=request.user.email).first()
    if not santri and request.user.phone:
        santri = Santri.objects.filter(no_hp=request.user.phone).first()
    
    if not santri:
        messages.error(request, 'Data santri tidak ditemukan.')
        return redirect('users:dokumen')
    
    # Get image field
    image_field = getattr(santri, doc_type, None)
    if not image_field:
        messages.error(request, 'Dokumen tidak ditemukan.')
        return redirect('users:dokumen')
    
    # Return file response
    from django.http import FileResponse
    import os
    
    try:
        file_path = image_field.path
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'), content_type='image/jpeg')
            filename = f"{doc_type.replace('_', '_').title()}_{santri.nama_lengkap.replace(' ', '_')}.jpg"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            messages.error(request, 'File tidak ditemukan.')
            return redirect('users:dokumen')
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
        return redirect('users:dokumen')


@login_required
def dokumen_upload(request, doc_type):
    """Upload/Edit Dokumen"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    # Validasi doc_type
    valid_doc_types = ['foto_santri', 'foto_ktp', 'foto_akta', 'foto_ijazah', 'surat_sehat']
    if doc_type not in valid_doc_types:
        messages.error(request, 'Jenis dokumen tidak valid.')
        return redirect('users:dokumen')
    
    # Cari santri
    santri = None
    if request.user.email:
        santri = Santri.objects.filter(email=request.user.email).first()
    if not santri and request.user.phone:
        santri = Santri.objects.filter(no_hp=request.user.phone).first()
    
    if not santri:
        messages.error(request, 'Data santri tidak ditemukan. Silakan lengkapi pendaftaran terlebih dahulu.')
        return redirect('users:pendaftaran')
    
    if request.method == 'POST':
        if doc_type in request.FILES:
            file = request.FILES[doc_type]
            # Validasi ukuran file (max 5MB)
            if file.size > 5 * 1024 * 1024:
                messages.error(request, f'Ukuran file terlalu besar. Maksimal 5MB.')
                return redirect('users:dokumen')
            
            # Simpan file
            setattr(santri, doc_type, file)
            # Reset approval status saat dokumen diubah
            approval_field = f'{doc_type}_approved'
            setattr(santri, approval_field, False)
            santri.save()
            
            messages.success(request, f'Dokumen berhasil diupload.')
        else:
            messages.error(request, 'File tidak ditemukan.')
        
        return redirect('users:dokumen')
    
    return redirect('users:dokumen')


@login_required
def pembayaran(request):
    """Pembayaran"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    # Cari santri
    santri = None
    if request.user.email:
        santri = Santri.objects.filter(email=request.user.email).first()
    if not santri and request.user.phone:
        santri = Santri.objects.filter(no_hp=request.user.phone).first()
    
    # Cek apakah sudah ada payment
    payment = None
    if santri:
        try:
            payment = santri.payment
        except:
            pass
    
    # Ambil bank yang aktif
    banks = BankAccount.objects.filter(is_active=True).order_by('order', 'nama_bank')
    
    if request.method == 'POST':
        if not santri:
            messages.error(request, 'Data santri tidak ditemukan. Silakan lengkapi pendaftaran terlebih dahulu.')
            return redirect('users:pendaftaran')
        
        if payment:
            messages.info(request, 'Anda sudah mengupload bukti pembayaran. Silakan tunggu verifikasi.')
            return redirect('users:pembayaran')
        
        # Validasi dokumen sudah lengkap
        required_docs = ['foto_santri', 'foto_ktp', 'foto_akta', 'foto_ijazah', 'surat_sehat']
        missing_docs = []
        for doc in required_docs:
            if not getattr(santri, doc, None):
                missing_docs.append(doc.replace('_', ' ').title())
        
        if missing_docs:
            messages.error(request, f'Dokumen belum lengkap. Silakan upload: {", ".join(missing_docs)}')
            return redirect('users:dokumen')
        
        # Ambil data dari form
        bank_account_id = request.POST.get('bank_account')
        bank_pengirim = request.POST.get('bank_pengirim')
        no_rekening_pengirim = request.POST.get('no_rekening_pengirim', '')
        nama_pemilik_rekening = request.POST.get('nama_pemilik_rekening')
        jumlah_transfer = request.POST.get('jumlah_transfer')
        catatan = request.POST.get('catatan', '')
        bukti_transfer = request.FILES.get('bukti_transfer')
        
        # Validasi
        if not bank_account_id:
            messages.error(request, 'Pilih rekening tujuan pembayaran.')
            return redirect('users:pembayaran')
        
        if not bank_pengirim:
            messages.error(request, 'Pilih bank pengirim.')
            return redirect('users:pembayaran')
        
        if not nama_pemilik_rekening:
            messages.error(request, 'Nama pemilik rekening wajib diisi.')
            return redirect('users:pembayaran')
        
        if not jumlah_transfer:
            messages.error(request, 'Jumlah transfer wajib diisi.')
            return redirect('users:pembayaran')
        
        if not bukti_transfer:
            messages.error(request, 'Bukti transfer wajib diupload.')
            return redirect('users:pembayaran')
        
        # Validasi ukuran file
        if bukti_transfer.size > 5 * 1024 * 1024:
            messages.error(request, 'Ukuran file terlalu besar. Maksimal 5MB.')
            return redirect('users:pembayaran')
        
        try:
            bank_account = BankAccount.objects.get(id=bank_account_id, is_active=True)
            jumlah_transfer_decimal = float(jumlah_transfer)
            
            # Buat payment
            payment = Payment.objects.create(
                santri=santri,
                bank_pengirim=bank_pengirim,
                no_rekening_pengirim=no_rekening_pengirim,
                nama_pemilik_rekening=nama_pemilik_rekening,
                rekening_tujuan=bank_account.nomor_rekening,
                jumlah_transfer=jumlah_transfer_decimal,
                bukti_transfer=bukti_transfer,
                catatan=catatan,
                status='pending'
            )
            
            messages.success(request, 'Bukti pembayaran berhasil diupload! Silakan tunggu verifikasi dari admin.')
            return redirect('users:pembayaran')
        except BankAccount.DoesNotExist:
            messages.error(request, 'Rekening bank tidak ditemukan.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
    
    context = {
        'santri': santri,
        'payment': payment,
        'banks': banks,
    }
    return render(request, 'users/pembayaran.html', context)


@login_required
def riwayat(request):
    """Riwayat"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    return render(request, 'users/riwayat.html')


@login_required
def notifikasi(request):
    """Notifikasi"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    return render(request, 'users/notifikasi.html')


@login_required
def change_password(request):
    """Ubah Password"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        user = request.user
        
        if not user.check_password(old_password):
            messages.error(request, 'Password lama tidak benar.')
        elif new_password1 != new_password2:
            messages.error(request, 'Password baru tidak cocok.')
        elif len(new_password1) < 8:
            messages.error(request, 'Password minimal 8 karakter.')
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password berhasil diubah!')
            return redirect('users:profile')
    
    return redirect('users:profile')


@login_required
def pendaftaran_pdf(request):
    """Redirect ke aplikasi documents - fungsi lama sudah dipindah"""
    from django.contrib import messages
    messages.info(request, 'Fitur PDF sudah dipindahkan. Silakan hubungi admin untuk download dokumen.')
    return redirect('users:pendaftaran')


@login_required
def riwayat(request):
    """Riwayat"""
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin-panel:index')
    
    return render(request, 'users/riwayat.html')
