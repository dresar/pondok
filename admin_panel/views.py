"""
Views untuk Admin Panel dengan HTMX Support
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg, Max, Min
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRefresh, HttpResponseClientRedirect
from decimal import Decimal
from admissions.models import Santri
from payments.models import Payment, BankAccount
from core.models import WebsiteSettings, BagianJabatan, TenagaPengajar
from .models import ConvertedImage, BugNote
from .forms import SantriForm, PaymentForm, PaymentVerificationForm, WebsiteSettingsForm, SantriSearchFilterForm, PaymentSearchFilterForm, BankAccountForm, UserProfileForm, UserAccountForm, UserChangePasswordForm, StaffForm, BagianJabatanForm, TenagaPengajarForm, ImageConverterForm
from .utils import DataExporter, DataImporter, BulkActionHandler


def is_admin(user):
    """Check if user is admin or superuser"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(is_admin)
def index(request):
    """Dashboard utama admin panel"""
    # Statistik
    total_santri = Santri.objects.count()
    pending_payment = Payment.objects.filter(status='pending').count()
    verified_payment = Payment.objects.filter(status='verified').count()
    accepted_santri = Santri.objects.filter(status='accepted').count()
    
    # Recent data
    recent_santri = Santri.objects.all()[:5]
    pending_verifications = Payment.objects.filter(status='pending').order_by('-created_at')[:5]
    
    context = {
        'total_santri': total_santri,
        'pending_payment': pending_payment,
        'verified_payment': verified_payment,
        'accepted_santri': accepted_santri,
        'recent_santri': recent_santri,
        'pending_verifications': pending_verifications,
    }
    
    return render(request, 'admin-panel/index.html', context)


@login_required
@user_passes_test(is_admin)
def santri_list(request):
    """List semua santri dengan search dan filter"""
    form = SantriSearchFilterForm(request.GET)
    
    queryset = Santri.objects.all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(nama_lengkap__icontains=search) |
            Q(nisn__icontains=search) |
            Q(no_hp__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Filter status
    status = request.GET.get('status', '')
    if status:
        queryset = queryset.filter(status=status)
    
    # Order by
    order_by = request.GET.get('order_by', '-created_at')
    if order_by:
        queryset = queryset.order_by(order_by)
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'santri_list': page_obj,
        'santri': page_obj,  # Alias untuk template
        'search_query': search,
        'status_filter': status,
        'order_by': order_by,
    }
    
    # AJAX request - return partial template
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'admin-panel/santri/partial_list.html', context)
    
    return render(request, 'admin-panel/santri/list.html', context)


@login_required
@user_passes_test(is_admin)
def santri_create(request):
    """Create santri baru"""
    if request.method == 'POST':
        form = SantriForm(request.POST, request.FILES)
        
        if form.is_valid():
            santri = form.save()
            
            # Handle payment form jika ada data
            # Cek apakah ada data pembayaran yang diisi (minimal salah satu field penting)
            has_payment_data = any([
                request.POST.get('rekening_tujuan'),
                request.POST.get('bank_pengirim'),
                request.POST.get('nama_pemilik_rekening'),
                request.POST.get('jumlah_transfer'),
                request.FILES.get('bukti_transfer')
            ])
            
            if has_payment_data:
                payment_form = PaymentForm(request.POST, request.FILES)
                if payment_form.is_valid():
                    payment = payment_form.save(commit=False)
                    payment.santri = santri
                    # Set default status jika belum diisi
                    if not payment.status:
                        payment.status = 'pending'
                    payment.save()
            
            messages.success(request, f'Santri {santri.nama_lengkap} berhasil ditambahkan.')
            if request.htmx:
                return HttpResponseClientRedirect(f'/admin-panel/santri/{santri.id}/')
            return redirect('admin-panel:santri_detail', santri_id=santri.id)
    else:
        form = SantriForm()
        payment_form = PaymentForm()
    
    context = {'form': form, 'payment_form': payment_form, 'action': 'Tambah'}
    return render(request, 'admin-panel/santri/form.html', context)


@login_required
@user_passes_test(is_admin)
def santri_detail(request, santri_id):
    """Detail santri"""
    santri = get_object_or_404(Santri, id=santri_id)
    payment = getattr(santri, 'payment', None)
    
    context = {
        'santri': santri,
        'payment': payment,
    }
    return render(request, 'admin-panel/santri/detail.html', context)


@login_required
@user_passes_test(is_admin)
def santri_pdf(request, santri_id):
    """Redirect ke aplikasi documents untuk generate PDF"""
    # Redirect ke halaman documents dengan santri dipilih
    from django.contrib import messages
    messages.info(request, 'Fitur PDF sudah dipindahkan ke menu Dokumen PDF.')
    return redirect('documents:list')


@login_required
@user_passes_test(is_admin)
def santri_update(request, santri_id):
    """Update santri"""
    santri = get_object_or_404(Santri, id=santri_id)
    payment = getattr(santri, 'payment', None)
    
    if request.method == 'POST':
        form = SantriForm(request.POST, request.FILES, instance=santri)
        
        if form.is_valid():
            santri = form.save()
            
            # Handle payment form
            # Cek apakah ada data pembayaran yang diisi (minimal salah satu field penting)
            has_payment_data = any([
                request.POST.get('rekening_tujuan'),
                request.POST.get('bank_pengirim'),
                request.POST.get('nama_pemilik_rekening'),
                request.POST.get('jumlah_transfer'),
                request.FILES.get('bukti_transfer')
            ])
            
            if has_payment_data:
                payment_form = PaymentForm(request.POST, request.FILES, instance=payment)
                if payment_form.is_valid():
                    payment = payment_form.save(commit=False)
                    payment.santri = santri
                    # Set default status jika belum diisi
                    if not payment.status:
                        payment.status = 'pending'
                    payment.save()
            elif payment:
                # Jika payment sudah ada tapi semua field dikosongkan, tetap simpan dengan data yang ada
                # Atau bisa juga dihapus jika diperlukan
                pass
            
            messages.success(request, f'Data santri {santri.nama_lengkap} berhasil diupdate.')
            if request.htmx:
                return HttpResponseClientRedirect(f'/admin-panel/santri/{santri.id}/')
            return redirect('admin-panel:santri_detail', santri_id=santri.id)
    else:
        form = SantriForm(instance=santri)
        payment_form = PaymentForm(instance=payment)
    
    context = {'form': form, 'payment_form': payment_form, 'santri': santri, 'action': 'Edit'}
    return render(request, 'admin-panel/santri/form.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def santri_delete(request, santri_id):
    """Delete santri"""
    santri = get_object_or_404(Santri, id=santri_id)
    nama = santri.nama_lengkap
    santri.delete()
    messages.success(request, f'Santri {nama} berhasil dihapus.')
    
    if request.htmx:
        return HttpResponseClientRefresh()
    return redirect('admin-panel:santri_list')


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def update_santri_status(request, santri_id):
    """Update status santri"""
    santri = get_object_or_404(Santri, id=santri_id)
    new_status = request.POST.get('status')
    
    if new_status in dict(Santri.STATUS_CHOICES):
        santri.status = new_status
        santri.save()
        messages.success(request, f'Status santri berhasil diupdate menjadi {santri.get_status_display()}.')
        
        if request.htmx:
            return HttpResponseClientRedirect(f'/admin-panel/santri/{santri.id}/')
        return redirect('admin-panel:santri_detail', santri_id=santri.id)
    
    messages.error(request, 'Status tidak valid.')
    return redirect('admin-panel:santri_detail', santri_id=santri.id)


@login_required
@user_passes_test(is_admin)
def santri_export(request):
    """Export data santri"""
    format_type = request.GET.get('format', 'excel')
    queryset = Santri.objects.all()
    
    # Field lengkap untuk Excel/CSV
    fields_full = [
        'nama_lengkap', 'nisn', 'tempat_lahir', 'tanggal_lahir', 'jenis_kelamin',
        'agama', 'golongan_darah', 'tinggi_badan', 'berat_badan',
        'nama_ayah', 'nik_ayah', 'nama_ibu', 'nik_ibu',
        'pekerjaan_ayah', 'pekerjaan_ibu', 'no_hp_ayah', 'no_hp_ibu', 'alamat_orangtua',
        'alamat', 'no_hp', 'email',
        'asal_sekolah', 'kelas_terakhir', 'tahun_lulus', 'no_ijazah',
        'status', 'created_at'
    ]
    
    headers_full = [
        'Nama Lengkap', 'NISN', 'Tempat Lahir', 'Tanggal Lahir', 'Jenis Kelamin',
        'Agama', 'Golongan Darah', 'Tinggi Badan (cm)', 'Berat Badan (kg)',
        'Nama Ayah', 'NIK Ayah', 'Nama Ibu', 'NIK Ibu',
        'Pekerjaan Ayah', 'Pekerjaan Ibu', 'No. HP Ayah', 'No. HP Ibu', 'Alamat Orang Tua',
        'Alamat', 'No. HP', 'Email',
        'Asal Sekolah', 'Kelas Terakhir', 'Tahun Lulus', 'No. Ijazah/SKHUN',
        'Status', 'Tanggal Daftar'
    ]
    
    # Field minimal untuk PDF (hanya yang penting)
    fields_pdf = [
        'nama_lengkap', 'nisn', 'jenis_kelamin',
        'nama_ayah', 'nama_ibu', 'no_hp',
        'asal_sekolah', 'status', 'created_at'
    ]
    
    headers_pdf = [
        'Nama Lengkap', 'NISN', 'Jenis Kelamin',
        'Nama Ayah', 'Nama Ibu', 'No. HP',
        'Asal Sekolah', 'Status', 'Tanggal Daftar'
    ]
    
    if format_type == 'csv':
        return DataExporter.export_to_csv(queryset, 'Santri', fields_full, headers_full)
    elif format_type == 'pdf':
        return DataExporter.export_to_pdf(queryset, 'Santri', fields_pdf, headers_pdf, 'Data Santri')
    else:
        return DataExporter.export_to_excel(queryset, 'Santri', fields_full, headers_full)


@login_required
@user_passes_test(is_admin)
def santri_dokumen_list(request):
    """List semua dokumen santri"""
    queryset = Santri.objects.filter(
        Q(foto_santri__isnull=False, foto_santri__gt='') | 
        Q(foto_ktp__isnull=False, foto_ktp__gt='') | 
        Q(foto_akta__isnull=False, foto_akta__gt='') | 
        Q(foto_ijazah__isnull=False, foto_ijazah__gt='') | 
        Q(surat_sehat__isnull=False, surat_sehat__gt='')
    )
    
    # Search
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(nama_lengkap__icontains=search) |
            Q(nisn__icontains=search)
        )
    
    # Filter dokumen type
    doc_type = request.GET.get('doc_type', '')
    if doc_type:
        if doc_type == 'foto_santri':
            queryset = queryset.filter(foto_santri__isnull=False).exclude(foto_santri='')
        elif doc_type == 'foto_ktp':
            queryset = queryset.filter(foto_ktp__isnull=False).exclude(foto_ktp='')
        elif doc_type == 'foto_akta':
            queryset = queryset.filter(foto_akta__isnull=False).exclude(foto_akta='')
        elif doc_type == 'foto_ijazah':
            queryset = queryset.filter(foto_ijazah__isnull=False).exclude(foto_ijazah='')
        elif doc_type == 'surat_sehat':
            queryset = queryset.filter(surat_sehat__isnull=False).exclude(surat_sehat='')
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'santri_list': page_obj,
        'search_query': search,
        'doc_type': doc_type,
    }
    return render(request, 'admin-panel/santri/dokumen_list.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def santri_approve_dokumen(request, santri_id):
    """Approve dokumen santri"""
    santri = get_object_or_404(Santri, id=santri_id)
    doc_type = request.POST.get('doc_type')
    
    if doc_type == 'foto_santri':
        santri.foto_santri_approved = True
        messages.success(request, 'Foto Santri berhasil disetujui.')
    elif doc_type == 'foto_ktp':
        santri.foto_ktp_approved = True
        messages.success(request, 'Foto KTP/KK berhasil disetujui.')
    elif doc_type == 'foto_akta':
        santri.foto_akta_approved = True
        messages.success(request, 'Foto Akta Kelahiran berhasil disetujui.')
    elif doc_type == 'foto_ijazah':
        santri.foto_ijazah_approved = True
        messages.success(request, 'Foto Ijazah/SKHUN berhasil disetujui.')
    elif doc_type == 'surat_sehat':
        santri.surat_sehat_approved = True
        messages.success(request, 'Surat Keterangan Sehat berhasil disetujui.')
    else:
        messages.error(request, 'Jenis dokumen tidak valid.')
        return redirect('admin-panel:santri_dokumen_list')
    
    santri.save()
    
    if request.htmx:
        return HttpResponseClientRefresh()
    return redirect('admin-panel:santri_dokumen_list')


@login_required
@user_passes_test(is_admin)
def santri_import(request):
    """Import data santri dari Excel/CSV"""
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            messages.error(request, 'File tidak ditemukan.')
            return redirect('admin-panel:santri_import')
        
        field_mapping = {
            'nama_lengkap': 'nama_lengkap',
            'nisn': 'nisn',
            'tempat_lahir': 'tempat_lahir',
            'tanggal_lahir': 'tanggal_lahir',
            'jenis_kelamin': 'jenis_kelamin',
            'agama': 'agama',
            'golongan_darah': 'golongan_darah',
            'tinggi_badan': 'tinggi_badan',
            'berat_badan': 'berat_badan',
            'nama_ayah': 'nama_ayah',
            'nik_ayah': 'nik_ayah',
            'nama_ibu': 'nama_ibu',
            'nik_ibu': 'nik_ibu',
            'pekerjaan_ayah': 'pekerjaan_ayah',
            'pekerjaan_ibu': 'pekerjaan_ibu',
            'no_hp_ayah': 'no_hp_ayah',
            'no_hp_ibu': 'no_hp_ibu',
            'alamat_orangtua': 'alamat_orangtua',
            'alamat': 'alamat',
            'no_hp': 'no_hp',
            'email': 'email',
            'asal_sekolah': 'asal_sekolah',
            'kelas_terakhir': 'kelas_terakhir',
            'tahun_lulus': 'tahun_lulus',
            'no_ijazah': 'no_ijazah',
        }
        
        try:
            if file.name.endswith('.csv'):
                result = DataImporter.import_from_csv(file, Santri, field_mapping)
            else:
                result = DataImporter.import_from_excel(file, Santri, field_mapping)
            
            messages.success(request, f'Berhasil mengimport {result["imported"]} data santri.')
            if result['errors']:
                messages.warning(request, f'Ada {len(result["errors"])} error saat import.')
            
            return redirect('admin-panel:santri_list')
        except Exception as e:
            messages.error(request, f'Error saat import: {str(e)}')
            return redirect('admin-panel:santri_import')
    
    return render(request, 'admin-panel/santri/import.html')


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def santri_bulk_action(request):
    """Bulk action untuk santri"""
    action = request.POST.get('action')
    ids = request.POST.getlist('ids')
    
    if not ids:
        messages.error(request, 'Tidak ada santri yang dipilih.')
        return redirect('admin-panel:santri_list')
    
    queryset = Santri.objects.filter(id__in=ids)
    
    if action == 'delete':
        result = BulkActionHandler.bulk_delete(queryset, ids)
        messages.success(request, f'Berhasil menghapus {result["deleted"]} santri.')
    elif action == 'accept':
        result = BulkActionHandler.bulk_update(queryset, ids, {'status': 'accepted'})
        messages.success(request, f'Berhasil menerima {result["updated"]} santri.')
    elif action == 'reject':
        result = BulkActionHandler.bulk_update(queryset, ids, {'status': 'rejected'})
        messages.success(request, f'Berhasil menolak {result["updated"]} santri.')
    else:
        messages.error(request, 'Action tidak valid.')
    
    if request.htmx:
        return HttpResponseClientRefresh()
    return redirect('admin-panel:santri_list')


@login_required
@user_passes_test(is_admin)
def keuangan_dashboard(request):
    """Dashboard keuangan"""
    currency = request.GET.get('currency', 'IDR')
    
    # Statistik pembayaran total
    total_payment = Payment.objects.aggregate(
        total=Sum('jumlah_transfer'),
        count=Count('id'),
        avg=Avg('jumlah_transfer')
    )
    
    # Statistik per status
    verified_total = Payment.objects.filter(status='verified').aggregate(
        total=Sum('jumlah_transfer'),
        count=Count('id')
    )
    
    pending_total = Payment.objects.filter(status='pending').aggregate(
        total=Sum('jumlah_transfer'),
        count=Count('id')
    )
    
    rejected_total = Payment.objects.filter(status='rejected').aggregate(
        total=Sum('jumlah_transfer'),
        count=Count('id')
    )
    
    # Statistik hari ini
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_payments = Payment.objects.filter(created_at__gte=today_start).aggregate(
        total=Sum('jumlah_transfer'),
        count=Count('id')
    )
    
    # Statistik bulan ini
    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_payments = Payment.objects.filter(created_at__gte=month_start).aggregate(
        total=Sum('jumlah_transfer'),
        count=Count('id')
    )
    
    # Pembayaran per status (untuk chart)
    payment_by_status = Payment.objects.values('status').annotate(
        total=Sum('jumlah_transfer'),
        count=Count('id')
    ).order_by('-total')
    
    # Tambahkan display name untuk status
    status_choices = dict(Payment.STATUS_CHOICES)
    for item in payment_by_status:
        item['status_display'] = status_choices.get(item['status'], item['status'])
    
    # Pembayaran per bank
    payment_by_bank = Payment.objects.values('bank_pengirim').annotate(
        total=Sum('jumlah_transfer'),
        count=Count('id')
    ).order_by('-total')
    
    # Top 10 pembayaran terbesar
    top_payments = Payment.objects.select_related('santri').order_by('-jumlah_transfer')[:10]
    
    # Recent payments
    recent_payments = Payment.objects.select_related('santri').order_by('-created_at')[:10]
    
    context = {
        'currency': currency,
        'total_payment': total_payment,
        'verified_total': verified_total,
        'pending_total': pending_total,
        'rejected_total': rejected_total,
        'today_payments': today_payments,
        'month_payments': month_payments,
        'payment_by_status': payment_by_status,
        'payment_by_bank': payment_by_bank,
        'top_payments': top_payments,
        'recent_payments': recent_payments,
    }
    
    return render(request, 'admin-panel/keuangan/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def payment_list(request):
    """List semua pembayaran"""
    form = PaymentSearchFilterForm(request.GET)
    
    queryset = Payment.objects.select_related('santri').all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(santri__nama_lengkap__icontains=search) |
            Q(santri__nisn__icontains=search) |
            Q(nama_pemilik_rekening__icontains=search)
        )
    
    # Filter status
    status = request.GET.get('status', '')
    if status:
        queryset = queryset.filter(status=status)
    
    # Order by
    order_by = request.GET.get('order_by', '-created_at')
    if order_by:
        queryset = queryset.order_by(order_by)
    
    # Currency
    currency = request.GET.get('currency', 'IDR')
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'payment_list': page_obj,
        'payments': page_obj,  # Alias untuk template
        'search_query': search,
        'status_filter': status,
        'order_by': order_by,
        'currency': currency,
    }
    
    # HTMX partial response - gunakan template yang sama untuk sekarang
    # TODO: Buat partial_list.html untuk optimasi HTMX
    return render(request, 'admin-panel/pembayaran/list.html', context)


@login_required
@user_passes_test(is_admin)
def payment_detail(request, payment_id):
    """Detail pembayaran"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    context = {
        'payment': payment,
    }
    return render(request, 'admin-panel/pembayaran/detail.html', context)


@login_required
@user_passes_test(is_admin)
def payment_verify(request, payment_id):
    """Verifikasi pembayaran - GET untuk form, POST untuk submit"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        catatan = request.POST.get('catatan', '')
        
        if new_status in dict(Payment.STATUS_CHOICES):
            payment.status = new_status
            payment.verified_by = request.user
            payment.verified_at = timezone.now()
            if catatan:
                payment.catatan = catatan
            payment.save()
            
            # Update status santri jika pembayaran terverifikasi
            if payment.status == 'verified':
                payment.santri.status = 'verified'
                payment.santri.save()
                messages.success(request, 'Pembayaran berhasil diverifikasi dan status santri telah diupdate.')
            elif payment.status == 'rejected':
                messages.success(request, 'Pembayaran ditolak.')
            else:
                messages.success(request, 'Status pembayaran berhasil diupdate.')
            
            if request.htmx:
                return HttpResponseClientRefresh()
            return redirect('admin-panel:payment_detail', payment_id=payment.id)
        else:
            messages.error(request, 'Status tidak valid.')
            return redirect('admin-panel:payment_detail', payment_id=payment.id)
    
    # GET request - tampilkan form verifikasi
    from .forms import PaymentVerificationForm
    form = PaymentVerificationForm(instance=payment)
    
    context = {
        'payment': payment,
        'santri': payment.santri,
        'form': form,
    }
    return render(request, 'admin-panel/pembayaran/verify.html', context)


@login_required
@user_passes_test(is_admin)
def payment_export(request):
    """Export data pembayaran"""
    format_type = request.GET.get('format', 'excel')
    queryset = Payment.objects.select_related('santri').all()
    
    fields = [
        'santri__nama_lengkap', 'santri__nisn', 'bank_pengirim', 'nama_pemilik_rekening',
        'jumlah_transfer', 'status', 'created_at', 'verified_at'
    ]
    
    headers = [
        'Nama Santri', 'NISN', 'Bank Pengirim', 'Nama Pemilik Rekening',
        'Jumlah Transfer', 'Status', 'Tanggal Upload', 'Tanggal Verifikasi'
    ]
    
    if format_type == 'csv':
        return DataExporter.export_to_csv(queryset, 'Pembayaran', fields, headers)
    elif format_type == 'pdf':
        return DataExporter.export_to_pdf(queryset, 'Pembayaran', fields, headers, 'Data Pembayaran')
    else:
        return DataExporter.export_to_excel(queryset, 'Pembayaran', fields, headers)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def payment_bulk_action(request):
    """Bulk action untuk pembayaran"""
    action = request.POST.get('action')
    ids = request.POST.getlist('ids')
    
    if not ids:
        messages.error(request, 'Tidak ada pembayaran yang dipilih.')
        return redirect('admin-panel:payment_list')
    
    queryset = Payment.objects.filter(id__in=ids)
    
    if action == 'verify':
        result = BulkActionHandler.bulk_update(queryset, ids, {'status': 'verified'})
        messages.success(request, f'Berhasil memverifikasi {result["updated"]} pembayaran.')
    elif action == 'reject':
        result = BulkActionHandler.bulk_update(queryset, ids, {'status': 'rejected'})
        messages.success(request, f'Berhasil menolak {result["updated"]} pembayaran.')
    else:
        messages.error(request, 'Action tidak valid.')
    
    if request.htmx:
        return HttpResponseClientRefresh()
    return redirect('admin-panel:payment_list')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def settings_view(request):
    """Settings website (hanya superuser)"""
    settings, created = WebsiteSettings.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        form = WebsiteSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            from admin_panel.models import ConvertedImage
            
            settings_obj = form.save(commit=False)
            
            # Handle selected_image_id dari image picker untuk logo
            selected_logo_id = request.POST.get('selected_logo_id')
            if selected_logo_id:
                try:
                    converted_image = ConvertedImage.objects.get(id=selected_logo_id)
                    if converted_image.webp_image:
                        settings_obj.logo = converted_image.webp_image
                except ConvertedImage.DoesNotExist:
                    pass
            
            # Handle selected_image_id untuk header_mobile_image
            selected_header_mobile_image_id = request.POST.get('selected_header_mobile_image_id')
            if selected_header_mobile_image_id:
                try:
                    converted_image = ConvertedImage.objects.get(id=selected_header_mobile_image_id)
                    if converted_image.webp_image:
                        settings_obj.header_mobile_image = converted_image.webp_image
                except ConvertedImage.DoesNotExist:
                    pass
            
            # Handle selected_image_id untuk favicon
            selected_favicon_id = request.POST.get('selected_favicon_id')
            if selected_favicon_id:
                try:
                    converted_image = ConvertedImage.objects.get(id=selected_favicon_id)
                    if converted_image.webp_image:
                        settings_obj.favicon = converted_image.webp_image
                except ConvertedImage.DoesNotExist:
                    pass
            
            settings_obj.save()
            messages.success(request, 'Pengaturan website berhasil diupdate.')
            return redirect('admin-panel:settings')
    else:
        form = WebsiteSettingsForm(instance=settings)
    
    context = {
        'form': form,
        'settings': settings,
    }
    return render(request, 'admin-panel/settings/general.html', context)


@login_required
@user_passes_test(is_admin)
def user_settings_view(request):
    """Settings untuk Role & Staff Management"""
    from users.models import User
    
    # Demo credentials
    demo_admin_username = 'admin'
    demo_admin_password = 'admin123'
    demo_user_username = 'user'
    demo_user_password = 'user123'
    
    # Create demo users if not exist
    if request.method == 'POST' and 'create_demo' in request.POST:
        # Create demo admin
        if not User.objects.filter(username=demo_admin_username).exists():
            User.objects.create_superuser(
                username=demo_admin_username,
                email='admin@pondok.com',
                password=demo_admin_password,
                first_name='Admin',
                last_name='Demo'
            )
            messages.success(request, 'Demo admin user berhasil dibuat!')
        else:
            messages.info(request, 'Demo admin user sudah ada.')
        
        # Create demo user
        if not User.objects.filter(username=demo_user_username).exists():
            User.objects.create_user(
                username=demo_user_username,
                email='user@pondok.com',
                password=demo_user_password,
                first_name='User',
                last_name='Demo',
                is_staff=False,
                is_superuser=False
            )
            messages.success(request, 'Demo user berhasil dibuat!')
        else:
            messages.info(request, 'Demo user sudah ada.')
        
        return redirect('admin-panel:user_settings')
    
    # Get stats untuk Staff & Role
    staff_users = User.objects.filter(is_staff=True).count()
    superuser_count = User.objects.filter(is_superuser=True).count()
    
    context = {
        'total_users': superuser_count,  # Untuk superuser stat
        'staff_users': staff_users,
        'regular_users': User.objects.filter(is_staff=False, is_superuser=False).count(),
        'demo_admin_username': demo_admin_username,
        'demo_admin_password': demo_admin_password,
        'demo_user_username': demo_user_username,
        'demo_user_password': demo_user_password,
    }
    return render(request, 'admin-panel/settings/users.html', context)


@login_required
@user_passes_test(is_admin)
def bank_account_list(request):
    """List semua rekening bank dengan CRUD dalam 1 halaman"""
    banks = BankAccount.objects.all().order_by('order', 'nama_bank', 'nomor_rekening')
    
    # Handle form submission (create/update)
    form = None
    editing_id = None
    
    if request.method == 'POST':
        bank_id = request.POST.get('bank_id')
        
        if bank_id:  # Update
            bank = get_object_or_404(BankAccount, id=bank_id)
            form = BankAccountForm(request.POST, instance=bank)
            if form.is_valid():
                form.save()
                messages.success(request, 'Rekening bank berhasil diupdate.')
                return redirect('admin-panel:bank_account_list')
            editing_id = int(bank_id)
        else:  # Create
            form = BankAccountForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Rekening bank berhasil ditambahkan.')
                return redirect('admin-panel:bank_account_list')
    else:
        # Check if editing
        edit_id = request.GET.get('edit')
        if edit_id:
            bank = get_object_or_404(BankAccount, id=edit_id)
            form = BankAccountForm(instance=bank)
            editing_id = int(edit_id)
        else:
            form = BankAccountForm()
    
    context = {
        'banks': banks,
        'form': form,
        'editing_id': editing_id,
    }
    return render(request, 'admin-panel/keuangan/bank_list.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def bank_account_delete(request, bank_id):
    """Delete rekening bank"""
    bank = get_object_or_404(BankAccount, id=bank_id)
    bank_name = bank.get_display_name()
    bank.delete()
    messages.success(request, f'Rekening bank {bank_name} berhasil dihapus.')
    
    if request.htmx:
        return HttpResponseClientRefresh()
    return redirect('admin-panel:bank_account_list')


@login_required
@user_passes_test(is_admin)
def user_profile(request):
    """Profil user dengan CRUD dalam 1 halaman - form read-only sampai klik edit"""
    from users.models import LoginHistory
    from django.db.models import Count, Q
    from django.core.paginator import Paginator
    
    user = request.user
    is_editing = request.GET.get('edit') == '1'
    
    # Get login history untuk user ini
    login_history_query = LoginHistory.objects.filter(user=user).order_by('-created_at')
    
    # Statistics
    total_logins = login_history_query.count()
    successful_logins = login_history_query.filter(status='success').count()
    failed_logins = login_history_query.filter(status='failed').count()
    
    # Pagination untuk login history
    paginator = Paginator(login_history_query, 10)
    page = request.GET.get('page', 1)
    login_history_page = paginator.get_page(page)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user, edit_mode=True)
        if form.is_valid():
            # Simpan nilai original untuk field yang disabled
            original_role = request.user.role
            original_username = request.user.username
            old_avatar_name = user.avatar.name if user.avatar else None
            
            # Save form dengan commit=False untuk memastikan file tidak ditutup
            # File dari cleaned_data masih terbuka saat ini
            try:
                user = form.save(commit=False)
                
                # Restore disabled fields sebelum save
                user.role = original_role
                user.username = original_username
                
                # Save user (termasuk file avatar jika ada)
                # Django akan handle file upload secara otomatis saat save()
                user.save()
                
                # Hapus avatar lama jika ada file baru yang diupload
                if old_avatar_name and 'avatar' in form.cleaned_data:
                    try:
                        from django.core.files.storage import default_storage
                        # Pastikan file baru berbeda dengan file lama
                        if old_avatar_name != user.avatar.name and default_storage.exists(old_avatar_name):
                            default_storage.delete(old_avatar_name)
                    except Exception as e:
                        print(f"Error deleting old avatar: {e}")
                        # Continue anyway, file baru sudah tersimpan
                
                messages.success(request, 'Profil berhasil diupdate.')
                return redirect('admin-panel:user_profile')
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                print(f"Error saving profile: {error_detail}")
                messages.error(request, f'Terjadi kesalahan saat menyimpan profil: {str(e)}')
                # Get login history untuk context error
                from users.models import LoginHistory
                from django.core.paginator import Paginator
                login_history_query = LoginHistory.objects.filter(user=user).order_by('-created_at')
                total_logins = login_history_query.count()
                successful_logins = login_history_query.filter(status='success').count()
                failed_logins = login_history_query.filter(status='failed').count()
                paginator = Paginator(login_history_query, 10)
                page = request.GET.get('page', 1)
                login_history_page = paginator.get_page(page)
                
                return render(request, 'admin-panel/settings/profile.html', {
                    'form': form,
                    'user': user,
                    'is_editing': True,
                    'login_history': login_history_page,
                    'total_logins': total_logins,
                    'successful_logins': successful_logins,
                    'failed_logins': failed_logins,
                })
        else:
            # Show form errors to user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserProfileForm(instance=user, edit_mode=is_editing)
    
    context = {
        'form': form,
        'user': user,
        'is_editing': is_editing,
    }
    return render(request, 'admin-panel/settings/profile.html', context)


# ==================== USER ACCOUNT MANAGEMENT ====================

@login_required
@user_passes_test(is_admin)
def user_account_list(request):
    """List semua user dengan filter dan search - bisa diakses oleh semua staff"""
    from users.models import User
    
    # Search dan filter - Hanya user biasa (bukan staff/admin)
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Hanya tampilkan user biasa (bukan staff/admin)
    users = User.objects.filter(is_staff=False, is_superuser=False)
    
    # Filter berdasarkan search
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Filter berdasarkan status
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(users.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_users': User.objects.filter(is_staff=False, is_superuser=False).count(),
        'active_users': User.objects.filter(is_staff=False, is_superuser=False, is_active=True).count(),
        'staff_users': User.objects.filter(is_staff=True).count(),
    }
    return render(request, 'admin-panel/users/list.html', context)


@login_required
@user_passes_test(is_admin)
def user_account_create(request):
    """Create user baru, bisa ambil data dari Santri"""
    from users.models import User
    
    if request.method == 'POST':
        form = UserAccountForm(request.POST, request.FILES, is_edit=False)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Set default role untuk user (bukan staff)
            user.role = 'petugaspendaftaran'  # Default role
            user.is_staff = False  # User biasa, bukan staff
            user.is_superuser = False  # Bukan superuser
            
            # Generate username jika kosong (dari nama awal + random 2 digit)
            if not user.username and user.first_name:
                import random
                base_username = user.first_name.lower().replace(' ', '').replace('-', '').replace('_', '')
                # Hanya ambil karakter alphanumeric
                base_username = ''.join(c for c in base_username if c.isalnum())
                random_code = str(random.randint(10, 99))
                user.username = base_username + random_code
                
                # Pastikan username unik
                from users.models import User as UserModel
                original_username = user.username
                counter = 1
                while UserModel.objects.filter(username=user.username).exists():
                    user.username = original_username + str(counter)
                    counter += 1
            
            user.save()
            
            # Jika ada santri_id, link dengan santri
            santri_id = form.cleaned_data.get('santri_id')
            if santri_id:
                santri = get_object_or_404(Santri, id=santri_id)
                messages.success(request, f'User {user.username} berhasil dibuat dari data Santri {santri.nama_lengkap}.')
            else:
                messages.success(request, f'User {user.username} berhasil dibuat.')
            
            return redirect('admin-panel:user_account_list')
    else:
        # Pre-fill dari Santri jika ada santri_id di GET
        initial_data = {}
        santri_id = request.GET.get('santri_id')
        if santri_id:
            try:
                import random
                santri = Santri.objects.get(id=santri_id)
                # Generate username dari nama awal + random 2 digit
                name_parts = santri.nama_lengkap.split() if santri.nama_lengkap else []
                first_name = name_parts[0] if name_parts else ''
                base_username = first_name.lower().replace(' ', '').replace('-', '').replace('_', '')
                base_username = ''.join(c for c in base_username if c.isalnum())
                random_code = str(random.randint(10, 99))
                generated_username = base_username + random_code
                
                initial_data = {
                    'santri_id': santri.id,
                    'username': generated_username,
                    'email': santri.email or '',
                    'first_name': first_name,
                    'last_name': ' '.join(name_parts[1:]) if len(name_parts) > 1 else '',
                    'phone': santri.no_hp or '',
                }
            except Santri.DoesNotExist:
                pass
        
        form = UserAccountForm(initial=initial_data, is_edit=False)
    
    # Get list Santri untuk dropdown
    santri_list = Santri.objects.all().order_by('-created_at')[:50]  # Limit untuk performa
    
    context = {
        'form': form,
        'santri_list': santri_list,
        'user_obj': None,  # Untuk template check (jangan pakai 'user' karena akan override request.user)
    }
    return render(request, 'admin-panel/users/form.html', context)


@login_required
@user_passes_test(is_admin)
def user_account_update(request, user_id):
    """Update user"""
    from users.models import User
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserAccountForm(request.POST, request.FILES, instance=user, is_edit=True)
        if form.is_valid():
            user = form.save(commit=False)
            # Pastikan user tetap user biasa (bukan staff)
            user.role = 'petugaspendaftaran'  # Default role untuk user
            user.is_staff = False  # User biasa, bukan staff
            user.is_superuser = False  # Bukan superuser
            user.save()
            messages.success(request, f'User {user.username} berhasil diupdate.')
            return redirect('admin-panel:user_account_list')
    else:
        form = UserAccountForm(instance=user, is_edit=True)
    
    # Get list Santri untuk dropdown (jika diperlukan)
    santri_list = Santri.objects.all().order_by('-created_at')[:50]
    
    context = {
        'form': form,
        'user_obj': user,  # Gunakan user_obj untuk menghindari konflik dengan request.user
        'santri_list': santri_list,
    }
    return render(request, 'admin-panel/users/form.html', context)


@login_required
@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def user_account_delete(request, user_id):
    """Delete user"""
    from users.models import User
    
    user = get_object_or_404(User, id=user_id)
    
    # Jangan bisa delete user sendiri
    if user.id == request.user.id:
        messages.error(request, 'Anda tidak bisa menghapus akun sendiri.')
        return redirect('admin-panel:user_account_list')
    
    username = user.username
    user.delete()
    messages.success(request, f'User {username} berhasil dihapus.')
    return redirect('admin-panel:user_account_list')


@login_required
@user_passes_test(is_admin)
def user_account_change_password(request, user_id):
    """Change password user"""
    from users.models import User
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, f'Password untuk user {user.username} berhasil diubah.')
            return redirect('admin-panel:user_account_list')
    else:
        form = UserChangePasswordForm()
    
    context = {
        'form': form,
        'user_obj': user,  # Gunakan user_obj untuk menghindari konflik dengan request.user
    }
    return render(request, 'admin-panel/users/change_password.html', context)


@login_required
@user_passes_test(is_admin)
def santri_json_detail(request, santri_id):
    """JSON endpoint untuk mengambil data Santri (untuk form user)"""
    santri = get_object_or_404(Santri, id=santri_id)
    
    data = {
        'id': santri.id,
        'nama_lengkap': santri.nama_lengkap,
        'nisn': santri.nisn,
        'email': santri.email or '',
        'no_hp': santri.no_hp or '',
    }
    
    return JsonResponse(data)


@login_required
@user_passes_test(is_admin)
def santri_search_api(request):
    """API endpoint untuk search Santri (autocomplete)"""
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
    
    # Search by nama_lengkap, nisn, email, atau no_hp
    santri_list = Santri.objects.filter(
        Q(nama_lengkap__icontains=query) |
        Q(nisn__icontains=query) |
        Q(email__icontains=query) |
        Q(no_hp__icontains=query)
    )[:10]  # Limit 10 results
    
    results = []
    for santri in santri_list:
        results.append({
            'id': santri.id,
            'text': f'{santri.nama_lengkap} (NISN: {santri.nisn})',
            'nama_lengkap': santri.nama_lengkap,
            'nisn': santri.nisn,
            'email': santri.email or '',
            'no_hp': santri.no_hp or '',
        })
    
    return JsonResponse({'results': results})


# ==================== STAFF MANAGEMENT ====================

@login_required
@user_passes_test(is_admin)
def staff_list(request):
    """List semua Staff dengan filter dan search"""
    from users.models import User
    
    # Search dan filter
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')
    
    # Hanya tampilkan Staff (is_staff=True)
    users = User.objects.filter(is_staff=True)
    
    # Filter berdasarkan search
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Filter berdasarkan role
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Filter berdasarkan status
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    elif status_filter == 'superuser':
        users = users.filter(is_superuser=True)
    
    # Pagination
    paginator = Paginator(users.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Stats
    total_staff = User.objects.filter(is_staff=True).count()
    active_staff = User.objects.filter(is_staff=True, is_active=True).count()
    superadmin_count = User.objects.filter(is_staff=True, role='superadmin').count()
    bendahara_count = User.objects.filter(is_staff=True, role='bendahara').count()
    petugas_count = User.objects.filter(is_staff=True, role='petugaspendaftaran').count()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'total_staff': total_staff,
        'active_staff': active_staff,
        'superadmin_count': superadmin_count,
        'bendahara_count': bendahara_count,
        'petugas_count': petugas_count,
    }
    return render(request, 'admin-panel/staff/list.html', context)


@login_required
@user_passes_test(is_admin)
def staff_create(request):
    """Create staff baru"""
    from users.models import User
    
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, is_edit=False)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Staff {user.username} berhasil dibuat.')
            return redirect('admin-panel:staff_list')
    else:
        form = StaffForm(is_edit=False)
    
    context = {
        'form': form,
        'staff_obj': None,
    }
    return render(request, 'admin-panel/staff/form.html', context)


@login_required
@user_passes_test(is_admin)
def staff_update(request, staff_id):
    """Update staff"""
    from users.models import User
    
    staff = get_object_or_404(User, id=staff_id, is_staff=True)
    
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff, is_edit=True)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Staff {user.username} berhasil diupdate.')
            return redirect('admin-panel:staff_list')
    else:
        form = StaffForm(instance=staff, is_edit=True)
    
    context = {
        'form': form,
        'staff_obj': staff,
    }
    return render(request, 'admin-panel/staff/form.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def staff_delete(request, staff_id):
    """Delete staff"""
    from users.models import User
    
    staff = get_object_or_404(User, id=staff_id, is_staff=True)
    
    # Jangan bisa delete user sendiri
    if staff.id == request.user.id:
        messages.error(request, 'Anda tidak bisa menghapus akun sendiri.')
        return redirect('admin-panel:staff_list')
    
    username = staff.username
    staff.delete()
    messages.success(request, f'Staff {username} berhasil dihapus.')
    return redirect('admin-panel:staff_list')


@login_required
@user_passes_test(is_admin)
def staff_change_password(request, staff_id):
    """Change password staff"""
    from users.models import User
    
    staff = get_object_or_404(User, id=staff_id, is_staff=True)
    
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            staff.set_password(new_password)
            staff.save()
            messages.success(request, f'Password untuk staff {staff.username} berhasil diubah.')
            return redirect('admin-panel:staff_list')
    else:
        form = UserChangePasswordForm()
    
    context = {
        'form': form,
        'staff_obj': staff,
    }
    return render(request, 'admin-panel/staff/change_password.html', context)


# ==================== TENAGA PENGAJAR MANAGEMENT ====================

@login_required
@user_passes_test(is_admin)
def bagian_jabatan_list(request):
    """List semua bagian/jabatan"""
    bagian_list = BagianJabatan.objects.all().order_by('order', 'nama')
    
    # Handle form submission (create/update)
    form = None
    editing_id = None
    
    if request.method == 'POST':
        bagian_id = request.POST.get('bagian_id')
        
        if bagian_id:  # Update
            bagian = get_object_or_404(BagianJabatan, id=bagian_id)
            form = BagianJabatanForm(request.POST, instance=bagian)
            if form.is_valid():
                form.save()
                messages.success(request, 'Bagian/Jabatan berhasil diupdate.')
                return redirect('admin-panel:bagian_jabatan_list')
            editing_id = int(bagian_id)
        else:  # Create
            form = BagianJabatanForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Bagian/Jabatan berhasil ditambahkan.')
                return redirect('admin-panel:bagian_jabatan_list')
    else:
        # Check if editing
        edit_id = request.GET.get('edit')
        if edit_id:
            bagian = get_object_or_404(BagianJabatan, id=edit_id)
            form = BagianJabatanForm(instance=bagian)
            editing_id = int(edit_id)
        else:
            form = BagianJabatanForm()
    
    context = {
        'bagian_list': bagian_list,
        'form': form,
        'editing_id': editing_id,
    }
    return render(request, 'admin-panel/tenaga-pengajar/bagian_list.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def bagian_jabatan_delete(request, bagian_id):
    """Delete bagian/jabatan"""
    bagian = get_object_or_404(BagianJabatan, id=bagian_id)
    nama = bagian.nama
    bagian.delete()
    messages.success(request, f'Bagian/Jabatan {nama} berhasil dihapus.')
    
    if request.htmx:
        return HttpResponseClientRefresh()
    return redirect('admin-panel:bagian_jabatan_list')


@login_required
@user_passes_test(is_admin)
def tenaga_pengajar_list(request):
    """List semua tenaga pengajar dengan search dan filter"""
    queryset = TenagaPengajar.objects.select_related('bagian_jabatan').all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        queryset = queryset.filter(
            Q(nama_lengkap__icontains=search) |
            Q(nama_panggilan__icontains=search) |
            Q(bidang_keahlian__icontains=search) |
            Q(mata_pelajaran__icontains=search)
        )
    
    # Filter bagian/jabatan
    bagian_id = request.GET.get('bagian', '')
    if bagian_id:
        queryset = queryset.filter(bagian_jabatan_id=bagian_id)
    
    # Filter jenis kelamin
    jenis_kelamin = request.GET.get('jenis_kelamin', '')
    if jenis_kelamin:
        queryset = queryset.filter(jenis_kelamin=jenis_kelamin)
    
    # Filter published
    published = request.GET.get('published', '')
    if published == 'yes':
        queryset = queryset.filter(is_published=True)
    elif published == 'no':
        queryset = queryset.filter(is_published=False)
    
    # Order by
    order_by = request.GET.get('order_by', 'order')
    if order_by:
        queryset = queryset.order_by(order_by, 'nama_lengkap')
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all bagian for filter
    bagian_list = BagianJabatan.objects.filter(is_active=True).order_by('order', 'nama')
    
    context = {
        'page_obj': page_obj,
        'tenaga_pengajar_list': page_obj,
        'search_query': search,
        'bagian_filter': bagian_id,
        'jenis_kelamin_filter': jenis_kelamin,
        'published_filter': published,
        'order_by': order_by,
        'bagian_list': bagian_list,
    }
    
    return render(request, 'admin-panel/tenaga-pengajar/list.html', context)


@login_required
@user_passes_test(is_admin)
def tenaga_pengajar_create(request):
    """Create tenaga pengajar baru"""
    if request.method == 'POST':
        form = TenagaPengajarForm(request.POST, request.FILES)
        
        if form.is_valid():
            tenaga_pengajar = form.save()
            messages.success(request, f'Tenaga pengajar {tenaga_pengajar.nama_lengkap} berhasil ditambahkan.')
            if request.htmx:
                return HttpResponseClientRedirect(f'/admin-panel/tenaga-pengajar/{tenaga_pengajar.id}/')
            return redirect('admin-panel:tenaga_pengajar_detail', pengajar_id=tenaga_pengajar.id)
    else:
        form = TenagaPengajarForm()
    
    context = {'form': form, 'action': 'Tambah'}
    return render(request, 'admin-panel/tenaga-pengajar/form.html', context)


@login_required
@user_passes_test(is_admin)
def tenaga_pengajar_detail(request, pengajar_id):
    """Detail tenaga pengajar"""
    pengajar = get_object_or_404(TenagaPengajar, id=pengajar_id)
    
    context = {
        'pengajar': pengajar,
    }
    return render(request, 'admin-panel/tenaga-pengajar/detail.html', context)


@login_required
@user_passes_test(is_admin)
def tenaga_pengajar_update(request, pengajar_id):
    """Update tenaga pengajar"""
    pengajar = get_object_or_404(TenagaPengajar, id=pengajar_id)
    
    if request.method == 'POST':
        form = TenagaPengajarForm(request.POST, request.FILES, instance=pengajar)
        
        if form.is_valid():
            pengajar = form.save()
            messages.success(request, f'Data tenaga pengajar {pengajar.nama_lengkap} berhasil diupdate.')
            if request.htmx:
                return HttpResponseClientRedirect(f'/admin-panel/tenaga-pengajar/{pengajar.id}/')
            return redirect('admin-panel:tenaga_pengajar_detail', pengajar_id=pengajar.id)
    else:
        form = TenagaPengajarForm(instance=pengajar)
    
    context = {'form': form, 'pengajar': pengajar, 'action': 'Edit'}
    return render(request, 'admin-panel/tenaga-pengajar/form.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def tenaga_pengajar_delete(request, pengajar_id):
    """Delete tenaga pengajar"""
    pengajar = get_object_or_404(TenagaPengajar, id=pengajar_id)
    nama = pengajar.nama_lengkap
    pengajar.delete()
    messages.success(request, f'Tenaga pengajar {nama} berhasil dihapus.')
    
    if request.htmx:
        return HttpResponseClientRefresh()
    return redirect('admin-panel:tenaga_pengajar_list')


@login_required
@user_passes_test(is_admin)
def image_converter(request):
    """View untuk konversi gambar JPG/PNG ke WebP"""
    from PIL import Image
    import os
    from django.conf import settings
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    from io import BytesIO
    
    form = ImageConverterForm()
    converted_image = None
    original_size = None
    converted_size = None
    compression_ratio = None
    
    if request.method == 'POST':
        form = ImageConverterForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                image_file = form.cleaned_data['image']
                quality = 85  # Default quality untuk kompresi optimal
                resize = True  # Selalu resize untuk optimasi
                max_width = 1920  # Default max width
                max_height = 1080  # Default max height
                
                # Buka gambar dengan PIL
                img = Image.open(image_file)
                
                # Konversi ke RGB jika mode bukan RGB (untuk PNG dengan alpha channel)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Buat background putih untuk gambar dengan transparansi
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize jika diminta
                if resize:
                    # Hitung ukuran baru dengan mempertahankan aspect ratio
                    original_width, original_height = img.size
                    ratio = min(max_width / original_width, max_height / original_height)
                    
                    if ratio < 1:  # Hanya resize jika lebih besar dari max
                        new_width = int(original_width * ratio)
                        new_height = int(original_height * ratio)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Simpan ukuran asli
                original_size = image_file.size
                
                # Konversi ke WebP
                output = BytesIO()
                img.save(output, format='WEBP', quality=quality, method=6)  # method=6 untuk kompresi maksimal
                output.seek(0)
                
                # Generate nama file singkat dengan hash (untuk menghindari duplikat dan nama panjang)
                import hashlib
                import time
                import random
                
                # Generate hash dari timestamp + random + content hash
                content_hash = hashlib.md5(output.read()).hexdigest()[:8]  # 8 karakter pertama
                output.seek(0)  # Reset untuk dibaca lagi
                timestamp_hash = hashlib.md5(f"{time.time()}{random.randint(1000, 9999)}".encode()).hexdigest()[:6]  # 6 karakter
                
                # Nama file singkat: hash pendek (total 14 karakter)
                short_filename = f"{timestamp_hash}{content_hash}.webp"
                
                # Pastikan tidak ada duplikat - cek apakah file sudah ada
                base_path = f'converted/{short_filename}'
                counter = 1
                while default_storage.exists(base_path):
                    # Jika ada duplikat, tambahkan counter
                    name_part = f"{timestamp_hash}{content_hash}"
                    short_filename = f"{name_part}_{counter}.webp"
                    base_path = f'converted/{short_filename}'
                    counter += 1
                
                # Simpan file WebP dengan nama singkat
                webp_path = default_storage.save(base_path, ContentFile(output.read()))
                
                converted_size = default_storage.size(webp_path)
                converted_image_url = default_storage.url(webp_path)
                
                # Hitung rasio kompresi
                if original_size > 0:
                    compression_ratio = ((original_size - converted_size) / original_size) * 100
                
                # Simpan ke database
                judul = form.cleaned_data.get('judul', os.path.splitext(os.path.basename(image_file.name))[0])
                converted_image_obj = ConvertedImage.objects.create(
                    judul=judul,
                    original_filename=os.path.basename(image_file.name),  # Simpan nama asli untuk referensi
                    webp_image=webp_path,
                    original_size=original_size,
                    converted_size=converted_size,
                    compression_ratio=compression_ratio if compression_ratio else 0,
                    quality=85,  # Default quality
                    width=img.size[0],
                    height=img.size[1],
                    created_by=request.user
                )
                
                converted_image = converted_image_obj
                
                # FILE ASLI TIDAK DISIMPAN - hanya WebP yang disimpan
                # File asli (InMemoryUploadedFile) akan otomatis dihapus setelah request selesai
                # Tidak ada jejak file asli di storage, hanya WebP yang tersimpan
                
                messages.success(request, f'Gambar berhasil dikonversi! Ukuran berkurang {compression_ratio:.1f}%' if compression_ratio else 'Gambar berhasil dikonversi!')
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error saat konversi: {str(e)}')
    
    context = {
        'form': form,
        'converted_image': converted_image,
        'original_size': original_size,
        'converted_size': converted_size,
        'compression_ratio': compression_ratio,
    }
    
    return render(request, 'admin-panel/tools/image_converter.html', context)


@login_required
@user_passes_test(is_admin)
def save_converted_image(request, image_id):
    """View untuk menyimpan gambar yang dikonversi (update metadata)"""
    from .forms import SaveConvertedImageForm
    
    converted_image = get_object_or_404(ConvertedImage, id=image_id)
    
    if request.method == 'POST':
        form = SaveConvertedImageForm(request.POST, instance=converted_image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gambar berhasil disimpan!')
            return JsonResponse({'success': True, 'message': 'Gambar berhasil disimpan!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def cdn_image_view(request, image_id):
    """View untuk CDN akses publik gambar WebP"""
    from django.http import HttpResponse, Http404, FileResponse
    from django.conf import settings
    from django.core.files.storage import default_storage
    import os
    
    try:
        converted_image = ConvertedImage.objects.get(id=image_id)
        
        if not converted_image.webp_image:
            raise Http404("Gambar tidak ditemukan")
        
        # Baca file menggunakan FileResponse untuk efisiensi
        if hasattr(converted_image.webp_image, 'path'):
            file_path = converted_image.webp_image.path
        else:
            file_path = default_storage.path(converted_image.webp_image.name)
        
        if not os.path.exists(file_path):
            raise Http404("File tidak ditemukan")
        
        response = FileResponse(open(file_path, 'rb'), content_type='image/webp')
        response['Content-Disposition'] = f'inline; filename="{converted_image.original_filename}.webp"'
        response['Cache-Control'] = 'public, max-age=31536000'  # Cache 1 tahun
        response['Access-Control-Allow-Origin'] = '*'  # Allow CORS untuk CDN
        return response
            
    except ConvertedImage.DoesNotExist:
        raise Http404("Gambar tidak ditemukan")
    except Exception as e:
        raise Http404(f"Error: {str(e)}")


@login_required
@user_passes_test(is_admin)
def converted_image_list(request):
    """View untuk list gambar yang sudah dikonversi"""
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    
    # Query gambar yang dikonversi
    images = ConvertedImage.objects.all()
    
    # Filter berdasarkan search (judul atau original_filename)
    if search_query:
        images = images.filter(
            Q(judul__icontains=search_query) | Q(original_filename__icontains=search_query)
        )
    
    # Order by created_at descending
    images = images.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(images, 20)  # 20 gambar per halaman
    try:
        images_page = paginator.page(page)
    except:
        images_page = paginator.page(1)
    
    context = {
        'images': images_page,
        'search_query': search_query,
        'total_images': images.count(),
        'total_size_saved': sum(img.get_savings_mb() for img in images) if images.exists() else 0,
    }
    
    return render(request, 'admin-panel/tools/converted_image_list.html', context)


@login_required
@user_passes_test(is_admin)
def converted_image_search_api(request):
    """API endpoint untuk search gambar (AJAX)"""
    from django.http import JsonResponse
    
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 20))
    
    images = ConvertedImage.objects.all().order_by('-created_at')
    
    if search:
        images = images.filter(
            Q(judul__icontains=search) | Q(original_filename__icontains=search)
        )
    
    paginator = Paginator(images, per_page)
    page_obj = paginator.get_page(page)
    
    data = {
        'images': [
            {
                'id': img.id,
                'judul': img.judul or img.original_filename,
                'gambar_url': img.webp_image.url if img.webp_image else '',
                'original_filename': img.original_filename,
                'dimensions': f"{img.width}x{img.height}px" if img.width and img.height else '-',
                'file_size': img.get_converted_size_kb(),
            }
            for img in page_obj
        ],
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'page': page,
        'total_pages': paginator.num_pages,
        'total_count': paginator.count,
    }
    
    return JsonResponse(data)


@login_required
@user_passes_test(is_admin)
def converted_image_detail_json(request, image_id):
    """JSON endpoint untuk detail gambar yang dikonversi"""
    converted_image = get_object_or_404(ConvertedImage, id=image_id)
    
    data = {
        'id': converted_image.id,
        'judul': converted_image.judul or converted_image.original_filename,
        'original_filename': converted_image.original_filename,
        'webp_url': converted_image.webp_image.url if converted_image.webp_image else '',
        'cdn_url': f'/cdn/image/{converted_image.id}/',
        'original_size_mb': converted_image.get_original_size_mb(),
        'original_size_formatted': f"{converted_image.original_size:,} bytes",
        'converted_size_kb': converted_image.get_converted_size_kb(),
        'converted_size_formatted': f"{converted_image.converted_size:,} bytes",
        'savings_mb': converted_image.get_savings_mb(),
        'compression_ratio': f"{converted_image.compression_ratio:.1f}%",
        'quality': converted_image.quality,
        'width': converted_image.width,
        'height': converted_image.height,
        'created_at': converted_image.created_at.strftime('%d %B %Y %H:%M'),
        'created_by': converted_image.created_by.get_full_name() if converted_image.created_by else 'System',
    }
    
    return JsonResponse(data)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def converted_image_delete(request, image_id):
    """View untuk menghapus gambar yang dikonversi"""
    converted_image = get_object_or_404(ConvertedImage, id=image_id)
    
    # Hapus file dari storage
    if converted_image.webp_image:
        try:
            converted_image.webp_image.delete(save=False)
        except:
            pass
    
    # Hapus dari database
    converted_image.delete()
    
    messages.success(request, 'Gambar berhasil dihapus!')
    
    if request.htmx:
        return HttpResponseClientRefresh()
    return redirect('admin-panel:converted_image_list')


# Bug Notes
@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def bug_note_create(request):
    """Simpan catatan bug singkat dari floating button."""
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    page_url = request.POST.get('page_url', '').strip()
    status = request.POST.get('status', 'open')
    
    if not title:
        messages.error(request, 'Judul bug wajib diisi.')
        return redirect(request.META.get('HTTP_REFERER', 'admin-panel:index'))
    
    if status not in dict(BugNote.STATUS_CHOICES):
        status = 'open'
    
    BugNote.objects.create(
        title=title,
        description=description,
        page_url=page_url,
        status=status,
        created_by=request.user if request.user.is_authenticated else None,
    )
    messages.success(request, 'Catatan bug berhasil disimpan.')
    return redirect(request.META.get('HTTP_REFERER', 'admin-panel:index'))


@login_required
@user_passes_test(is_admin)
def bug_note_list(request):
    """Dashboard sederhana untuk melihat catatan bug."""
    status_filter = request.GET.get('status', '')
    qs = BugNote.objects.select_related('created_by').all()
    if status_filter in dict(BugNote.STATUS_CHOICES):
        qs = qs.filter(status=status_filter)
    qs = qs.order_by('-created_at')
    
    context = {
        'bug_notes': qs,
        'status_filter': status_filter,
    }
    return render(request, 'admin-panel/tools/bug_notes.html', context)


@login_required
@user_passes_test(is_admin)
def bug_note_export(request):
    """Export catatan bug ke txt atau md."""
    fmt = request.GET.get('format', 'txt')
    qs = BugNote.objects.select_related('created_by').order_by('-created_at')
    
    lines = []
    for bug in qs:
        user = bug.created_by.get_full_name() if bug.created_by else 'System'
        line_md = f"- [{bug.get_status_display()}] **{bug.title}** — {bug.created_at:%Y-%m-%d %H:%M} — oleh {user}"
        if bug.page_url:
            line_md += f" — URL: {bug.page_url}"
        if bug.description:
            line_md += f"\n  {bug.description}"
        lines.append(line_md)
    
    if fmt == 'md':
        content = "# Catatan Bug\n\n" + "\n".join(lines)
        filename = "bug-notes.md"
        content_type = "text/markdown"
    else:
        content = "Catatan Bug\n\n" + "\n".join([l.replace("**", "").replace("[", "").replace("]", "") for l in lines])
        filename = "bug-notes.txt"
        content_type = "text/plain"
    
    response = HttpResponse(content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
@user_passes_test(is_admin)
def media_files_manager(request):
    """View untuk mengelola file media dan menemukan file yang tidak terpakai"""
    from django.conf import settings
    from django.core.files.storage import default_storage
    import os
    from pathlib import Path
    
    # Scan semua file di media
    media_root = Path(settings.MEDIA_ROOT)
    all_files = []
    unused_files = []
    used_files = set()
    file_usage = {}  # Dictionary untuk menyimpan info penggunaan file
    
    # Kumpulkan semua file yang digunakan dari model
    if media_root.exists():
        # Scan semua file di media
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(media_root)
                file_url = default_storage.url(str(relative_path))
                file_size = file_path.stat().st_size
                
                all_files.append({
                    'path': str(relative_path),
                    'url': file_url,
                    'size': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2),
                    'size_kb': round(file_size / 1024, 2),
                    'modified': os.path.getmtime(file_path),
                })
        
        # Cek file yang digunakan dari semua model dengan ImageField/FileField
        from django.apps import apps
        from django.db import models as db_models
        
        def normalize_path(path):
            """Normalize path untuk perbandingan yang konsisten"""
            if not path:
                return ''
            # Convert to string dan replace backslash dengan forward slash
            path_str = str(path).replace('\\', '/')
            # Hapus leading slash
            if path_str.startswith('/'):
                path_str = path_str[1:]
            # Hapus trailing slash
            if path_str.endswith('/'):
                path_str = path_str[:-1]
            return path_str.lower()  # Case insensitive comparison
        
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                for field in model._meta.get_fields():
                    if isinstance(field, (db_models.ImageField, db_models.FileField)):
                        try:
                            # Ambil semua instance yang memiliki file (gunakan Q object untuk lebih fleksibel)
                            from django.db.models import Q
                            
                            # Query untuk mendapatkan semua instance dengan file yang tidak kosong
                            queryset = model.objects.filter(
                                ~Q(**{f'{field.name}': ''}),
                                ~Q(**{f'{field.name}__isnull': True})
                            )
                            
                            for instance in queryset:
                                field_file = getattr(instance, field.name, None)
                                if field_file and hasattr(field_file, 'name'):
                                    file_name = field_file.name
                                    if file_name and file_name.strip():
                                        # Normalize path untuk perbandingan
                                        normalized_name = normalize_path(file_name)
                                        if normalized_name:  # Pastikan tidak kosong setelah normalize
                                            used_files.add(normalized_name)
                                            
                                            # Simpan info penggunaan dengan path asli
                                            if normalized_name not in file_usage:
                                                file_usage[normalized_name] = []
                                            file_usage[normalized_name].append({
                                                'model': model.__name__,
                                                'app': app_config.name,
                                                'field': field.name,
                                                'instance_id': instance.pk,
                                                'instance_str': str(instance)[:50]
                                            })
                        except Exception as e:
                            # Skip jika ada error (misalnya model belum migrated)
                            pass
        
        # Identifikasi file yang tidak terpakai dan tambahkan info penggunaan
        for file_info in all_files:
            file_path = file_info['path']
            # Normalize path untuk perbandingan
            normalized_path = normalize_path(file_path)
            
            # Cek apakah file digunakan dengan perbandingan yang konsisten
            is_used = normalized_path in used_files
            
            if is_used:
                # File digunakan, tambahkan info penggunaan
                file_info['is_used'] = True
                file_info['usage'] = file_usage.get(normalized_path, [])
            else:
                # File tidak terpakai - hanya tambahkan ke unused_files jika benar-benar tidak digunakan
                file_info['is_used'] = False
                file_info['usage'] = []
                unused_files.append(file_info)
    
    # Sort by size descending
    unused_files.sort(key=lambda x: x['size'], reverse=True)
    all_files.sort(key=lambda x: x['size'], reverse=True)
    
    # Calculate totals
    total_size = sum(f['size'] for f in all_files)
    unused_size = sum(f['size'] for f in unused_files)
    
    # Pagination untuk unused files
    page = request.GET.get('page', 1)
    paginator = Paginator(unused_files, 50)  # 50 file per halaman
    try:
        unused_files_page = paginator.page(page)
    except:
        unused_files_page = paginator.page(1)
    
    # Separate used and unused files for display (hanya ambil yang benar-benar used)
    used_files_list = [f for f in all_files if f.get('is_used') is True]
    
    context = {
        'all_files': all_files,
        'used_files': used_files_list[:50],  # Limit untuk performa
        'unused_files': unused_files_page,
        'total_files': len(all_files),
        'total_used': len(used_files_list),
        'total_unused': len(unused_files),
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'unused_size_mb': round(unused_size / (1024 * 1024), 2),
        'unused_size_kb': round(unused_size / 1024, 2),
    }
    
    return render(request, 'admin-panel/tools/media_files_manager.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def delete_unused_files(request):
    """View untuk menghapus file yang tidak terpakai"""
    from django.conf import settings
    from django.core.files.storage import default_storage
    import os
    from pathlib import Path
    
    deleted_count = 0
    deleted_size = 0
    errors = []
    
    # Get list of files to delete from POST data
    files_to_delete = request.POST.getlist('files[]')
    
    # Handle comma-separated string (from JavaScript)
    if len(files_to_delete) == 1 and ',' in files_to_delete[0]:
        files_to_delete = files_to_delete[0].split(',')
    
    if not files_to_delete or (len(files_to_delete) == 1 and not files_to_delete[0]):
        messages.error(request, 'Tidak ada file yang dipilih untuk dihapus!')
        return redirect('admin-panel:media_files_manager')
    
    media_root = Path(settings.MEDIA_ROOT)
    
    for file_path in files_to_delete:
        if not file_path or not file_path.strip():
            continue
            
        try:
            file_path = file_path.strip()
            # Handle both relative and absolute paths
            if os.path.isabs(file_path):
                full_path = Path(file_path)
            else:
                full_path = media_root / file_path
            
            if full_path.exists() and full_path.is_file():
                # Verify it's within media root for security
                try:
                    full_path.relative_to(media_root)
                except ValueError:
                    errors.append(f"{file_path}: File di luar media root")
                    continue
                
                file_size = full_path.stat().st_size
                os.remove(str(full_path))
                deleted_count += 1
                deleted_size += file_size
            else:
                errors.append(f"{file_path}: File tidak ditemukan")
        except PermissionError:
            errors.append(f"{file_path}: Permission denied")
        except Exception as e:
            errors.append(f"{file_path}: {str(e)}")
    
    if deleted_count > 0:
        messages.success(request, f'{deleted_count} file berhasil dihapus! Penghematan: {round(deleted_size / (1024 * 1024), 2)} MB')
    if errors:
        for error in errors[:5]:  # Show first 5 errors
            messages.warning(request, error)
        if len(errors) > 5:
            messages.warning(request, f'... dan {len(errors) - 5} error lainnya')
    
    if request.htmx:
        return HttpResponseClientRefresh()
    return redirect('admin-panel:media_files_manager')


@login_required
@user_passes_test(is_admin)
def login_statistics(request):
    """Halaman Statistik Login Detail"""
    from users.models import LoginHistory
    from datetime import datetime, timedelta
    
    # Get date range from request
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Default to last 30 days
    if not date_from:
        date_from = (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not date_to:
        date_to = timezone.now().strftime('%Y-%m-%d')
    
    # Parse dates
    try:
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
    except ValueError:
        date_from_obj = timezone.now().date() - timedelta(days=30)
        date_to_obj = timezone.now().date()
    
    # Filter login history
    login_history = LoginHistory.objects.filter(
        created_at__date__gte=date_from_obj,
        created_at__date__lte=date_to_obj
    ).order_by('-created_at')
    
    # Statistics
    total_logins = login_history.count()
    successful_logins = login_history.filter(status='success').count()
    failed_logins = login_history.filter(status='failed').count()
    
    # Group by user
    user_stats = login_history.values('user__username', 'user__first_name', 'user__last_name').annotate(
        total=Count('id'),
        success=Count('id', filter=Q(status='success')),
        failed=Count('id', filter=Q(status='failed'))
    ).order_by('-total')
    
    # Group by IP
    ip_stats = login_history.values('ip_address').annotate(
        total=Count('id'),
        success=Count('id', filter=Q(status='success')),
        failed=Count('id', filter=Q(status='failed'))
    ).order_by('-total')[:20]
    
    # Group by date
    daily_stats = login_history.extra(
        select={'date': "DATE(created_at)"}
    ).values('date').annotate(
        total=Count('id'),
        success=Count('id', filter=Q(status='success')),
        failed=Count('id', filter=Q(status='failed'))
    ).order_by('date')
    
    # Pagination
    paginator = Paginator(login_history, 50)
    page = request.GET.get('page', 1)
    login_history_page = paginator.get_page(page)
    
    # Locked out users - menggunakan failures_since_start >= AXES_FAILURE_LIMIT
    locked_out_users = []
    try:
        from axes.models import AccessAttempt
        from django.conf import settings
        failure_limit = getattr(settings, 'AXES_FAILURE_LIMIT', 5)
        locked_out_users = AccessAttempt.objects.filter(
            failures_since_start__gte=failure_limit
        ).order_by('-attempt_time')[:20]
    except (ImportError, AttributeError):
        pass
    
    context = {
        'login_history': login_history_page,
        'total_logins': total_logins,
        'successful_logins': successful_logins,
        'failed_logins': failed_logins,
        'user_stats': user_stats,
        'ip_stats': ip_stats,
        'daily_stats': daily_stats,
        'locked_out_users': locked_out_users,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'admin-panel/login_statistics.html', context)
