"""
CRUD Views untuk FAQ, Program, WhatsApp Template, Kontak, dan Website Settings - Semua dalam 1 file
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Max as db_models_Max
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRefresh, HttpResponseClientRedirect
from .models import (
    FAQ, Program, WhatsAppTemplate, WhatsAppTemplateKategori, Kontak, HeroSection, SejarahTimeline, SejarahTimelineImage,
    VisiMisi, ProgramPendidikan, ProgramPendidikanImage, Fasilitas, Ekstrakurikuler, EkstrakurikulerImage, JadwalHarian,
    Persyaratan, AlurPendaftaran, BiayaPendidikan, ContactPerson, SocialMedia,
    Seragam, KMI, Statistik, Media, Dokumentasi, DokumentasiImage, InformasiTambahan
)
from .forms import (
    FAQForm, ProgramForm, WhatsAppTemplateForm, KontakForm, HeroSectionForm,
    SejarahTimelineForm, SejarahTimelineImageForm, VisiMisiForm, ProgramPendidikanForm, FasilitasForm,
    EkstrakurikulerForm, JadwalHarianForm, PersyaratanForm, AlurPendaftaranForm,
    BiayaPendidikanForm, ContactPersonForm, SocialMediaForm, SeragamForm, KMIForm, StatistikForm, MediaForm,
    DokumentasiForm, InformasiTambahanForm
)


def is_staff_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def is_htmx_request(request):
    return request.headers.get('HX-Request') == 'true'


# ==================== FAQ CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def faq_list(request):
    """List semua FAQ dengan modal untuk create/edit"""
    faqs = FAQ.objects.all().order_by('order', 'kategori', 'pertanyaan')
    search = request.GET.get('search', '')
    kategori = request.GET.get('kategori', '')
    
    if search:
        faqs = faqs.filter(Q(pertanyaan__icontains=search) | Q(jawaban__icontains=search))
    if kategori:
        faqs = faqs.filter(kategori=kategori)
    
    paginator = Paginator(faqs, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    # Handle form untuk modal
    faq_id = request.GET.get('edit', None)
    form = None
    faq_obj = None
    if faq_id:
        faq_obj = get_object_or_404(FAQ, id=faq_id)
        form = FAQForm(instance=faq_obj)
    else:
        form = FAQForm()
    
    return render(request, 'admin-panel/core/faq_list.html', {
        'faqs': page,
        'search': search,
        'kategori': kategori,
        'form': form,
        'faq_obj': faq_obj,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def faq_create(request):
    """Create FAQ via modal"""
    form = FAQForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'FAQ berhasil ditambahkan!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:faq_list')
    
    # Jika GET, redirect ke list dengan form di modal
    return redirect('core:faq_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def faq_update(request, faq_id):
    """Update FAQ via modal"""
    faq = get_object_or_404(FAQ, id=faq_id)
    form = FAQForm(request.POST or None, instance=faq)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'FAQ berhasil diupdate!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:faq_list')
    
    # Jika GET, redirect ke list dengan form di modal
    return redirect('core:faq_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def faq_delete(request, faq_id):
    """Delete FAQ"""
    faq = get_object_or_404(FAQ, id=faq_id)
    pertanyaan = faq.pertanyaan
    faq.delete()
    messages.success(request, f'FAQ "{pertanyaan}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:faq_list')


# ==================== PROGRAM CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def program_list(request):
    """List semua program"""
    programs = Program.objects.all().order_by('order', '-created_at')
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    # Get statistics
    total_count = Program.objects.count()
    published_count = Program.objects.filter(status='published').count()
    draft_count = Program.objects.filter(status='draft').count()
    
    if search:
        programs = programs.filter(Q(nama__icontains=search) | Q(deskripsi__icontains=search))
    if status:
        programs = programs.filter(status=status)
    
    paginator = Paginator(programs, 12)
    page = paginator.get_page(request.GET.get('page', 1))
    
    return render(request, 'admin-panel/core/program_list.html', {
        'programs': page,
        'search': search,
        'status': status,
        'total_count': total_count,
        'published_count': published_count,
        'draft_count': draft_count,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def program_form(request, program_id=None):
    """Create/Update program"""
    from admin_panel.models import ConvertedImage
    from django.core.files import File
    import os
    
    if program_id:
        program = get_object_or_404(Program, id=program_id)
        form = ProgramForm(request.POST or None, request.FILES or None, instance=program)
        title = 'Edit Program'
    else:
        program = None
        form = ProgramForm(request.POST or None, request.FILES or None)
        title = 'Tambah Program'
    
    if request.method == 'POST' and form.is_valid():
        # Handle selected_image_id dari image picker
        selected_image_id = request.POST.get('selected_image_id')
        if selected_image_id:
            try:
                converted_image = ConvertedImage.objects.get(id=selected_image_id)
                # Langsung gunakan path dari media/converted tanpa copy file
                if converted_image.webp_image:
                    program_obj = form.save(commit=False)
                    # Set path langsung dari ConvertedImage (tidak copy file)
                    program_obj.gambar = converted_image.webp_image
                    program_obj.save()
                    messages.success(request, f'Program berhasil {"diupdate" if program_id else "ditambahkan"}!')
                    if is_htmx_request(request):
                        return HttpResponseClientRefresh()
                    return redirect('core:program_list')
            except ConvertedImage.DoesNotExist:
                pass
        
        form.save()
        messages.success(request, f'Program berhasil {"diupdate" if program_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:program_list')
    
    return render(request, 'admin-panel/core/program_form.html', {
        'form': form,
        'program': program,
        'title': title,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def program_delete(request, program_id):
    """Delete program"""
    program = get_object_or_404(Program, id=program_id)
    nama = program.nama
    program.delete()
    messages.success(request, f'Program "{nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:program_list')


# ==================== WHATSAPP TEMPLATE CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def whatsapp_template_list(request):
    """List semua WhatsApp template"""
    templates = WhatsAppTemplate.objects.select_related('kategori').all().order_by('tipe', 'order', 'kategori', 'nama')
    search = request.GET.get('search', '')
    kategori = request.GET.get('kategori', '')
    tipe = request.GET.get('tipe', '')
    
    if search:
        templates = templates.filter(Q(nama__icontains=search) | Q(pesan__icontains=search))
    if kategori:
        templates = templates.filter(kategori_id=kategori)
    if tipe:
        templates = templates.filter(tipe=tipe)
    
    paginator = Paginator(templates, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    # Get all active categories for filter
    categories = WhatsAppTemplateKategori.objects.filter(is_active=True).order_by('order', 'nama')
    
    return render(request, 'admin-panel/core/whatsapp_template_list.html', {
        'templates': page,
        'search': search,
        'kategori': kategori,
        'tipe': tipe,
        'categories': categories,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def whatsapp_template_form(request, template_id=None):
    """Create/Update WhatsApp template"""
    if template_id:
        template = get_object_or_404(WhatsAppTemplate, id=template_id)
        form = WhatsAppTemplateForm(request.POST or None, instance=template)
        title = 'Edit Template WhatsApp'
    else:
        template = None
        form = WhatsAppTemplateForm(request.POST or None)
        title = 'Tambah Template WhatsApp'
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Template WhatsApp berhasil {"diupdate" if template_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:whatsapp_template_list')
    
    # Get all active categories for dropdown
    categories = WhatsAppTemplateKategori.objects.filter(is_active=True).order_by('order', 'nama')
    
    return render(request, 'admin-panel/core/whatsapp_template_form.html', {
        'form': form,
        'template': template,
        'title': title,
        'categories': categories,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def whatsapp_template_kategori_create(request):
    """Create kategori baru via AJAX"""
    from core.forms import WhatsAppTemplateKategoriForm
    from django.http import JsonResponse
    import json
    
    try:
        data = json.loads(request.body)
        form = WhatsAppTemplateKategoriForm(data)
        if form.is_valid():
            kategori = form.save()
            return JsonResponse({
                'success': True,
                'id': kategori.id,
                'nama': kategori.nama,
                'message': 'Kategori berhasil ditambahkan!'
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': {'__all__': [str(e)]}
        }, status=400)


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def whatsapp_template_delete(request, template_id):
    """Delete WhatsApp template"""
    template = get_object_or_404(WhatsAppTemplate, id=template_id)
    nama = template.nama
    template.delete()
    messages.success(request, f'Template WhatsApp "{nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:whatsapp_template_list')


# ==================== KONTAK CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def kontak_list(request):
    """List semua kontak/inquiry"""
    kontak = Kontak.objects.all().order_by('-created_at')
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    if search:
        kontak = kontak.filter(
            Q(nama__icontains=search) |
            Q(email__icontains=search) |
            Q(subjek__icontains=search) |
            Q(pesan__icontains=search)
        )
    if status:
        kontak = kontak.filter(status=status)
    
    paginator = Paginator(kontak, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    return render(request, 'admin-panel/core/kontak_list.html', {
        'kontak': page,
        'search': search,
        'status': status,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def kontak_form(request, kontak_id=None):
    """View/Update kontak"""
    kontak = get_object_or_404(Kontak, id=kontak_id)
    form = KontakForm(request.POST or None, instance=kontak)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kontak berhasil diupdate!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:kontak_list')
    
    return render(request, 'admin-panel/core/kontak_form.html', {
        'form': form,
        'kontak': kontak,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def kontak_delete(request, kontak_id):
    """Delete kontak"""
    kontak = get_object_or_404(Kontak, id=kontak_id)
    nama = kontak.nama
    kontak.delete()
    messages.success(request, f'Kontak "{nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:kontak_list')


# ==================== WHATSAPP BROADCAST ====================
@login_required
@user_passes_test(is_staff_user)
def whatsapp_broadcast(request):
    """Halaman untuk broadcast WhatsApp manual"""
    from admissions.models import Santri
    
    # Hanya ambil template system untuk broadcast
    templates = WhatsAppTemplate.objects.filter(tipe='system').order_by('kategori', 'nama')
    santri_list = Santri.objects.filter(no_hp__isnull=False).exclude(no_hp='').values_list('id', 'nama_lengkap', 'no_hp')
    
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        selected_santri = request.POST.getlist('santri_ids')
        pesan_custom = request.POST.get('pesan_custom', '')
        
        template = None
        if template_id:
            template = get_object_or_404(WhatsAppTemplate, id=template_id, tipe='system')
            pesan = template.pesan
        else:
            pesan = pesan_custom
        
        if not pesan:
            messages.error(request, 'Pesan tidak boleh kosong!')
            return render(request, 'admin-panel/core/whatsapp_broadcast.html', {
                'templates': templates,
                'santri_list': santri_list,
            })
        
        if not selected_santri:
            messages.error(request, 'Pilih minimal 1 santri!')
            return render(request, 'admin-panel/core/whatsapp_broadcast.html', {
                'templates': templates,
                'santri_list': santri_list,
            })
        
        # Generate WhatsApp links untuk setiap santri
        broadcast_links = []
        for santri_id in selected_santri:
            santri = Santri.objects.get(id=santri_id)
            if santri.no_hp:
                nomor = ''.join(filter(str.isdigit, santri.no_hp.replace('+', '').replace(' ', '')))
                if nomor:
                    # Render pesan dengan variabel dari template atau manual
                    # Siapkan semua variabel yang tersedia
                    from datetime import datetime
                    import locale
                    
                    # Set locale untuk format tanggal Indonesia
                    try:
                        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
                    except:
                        try:
                            locale.setlocale(locale.LC_TIME, 'Indonesian')
                        except:
                            pass
                    
                    # Format tanggal Indonesia
                    bulan_indonesia = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                                      'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
                    
                    def format_tanggal_indonesia(date_obj):
                        if date_obj:
                            return f"{date_obj.day} {bulan_indonesia[date_obj.month]} {date_obj.year}"
                        return ''
                    
                    def format_tanggal_short(date_obj):
                        if date_obj:
                            return date_obj.strftime('%d/%m/%Y')
                        return ''
                    
                    variabel_dict = {
                        # Data Pribadi
                        'nama': santri.nama_lengkap,
                        'nama_lengkap': santri.nama_lengkap,
                        'nama_santri': santri.nama_lengkap,
                        'nisn': str(santri.nisn) if santri.nisn else '',
                        'nisn_santri': str(santri.nisn) if santri.nisn else '',
                        'tempat_lahir': santri.tempat_lahir or '',
                        'tanggal_lahir': format_tanggal_indonesia(santri.tanggal_lahir),
                        'tanggal_lahir_short': format_tanggal_short(santri.tanggal_lahir),
                        'jenis_kelamin': santri.get_jenis_kelamin_display() if hasattr(santri, 'get_jenis_kelamin_display') else (santri.jenis_kelamin or ''),
                        'agama': santri.agama or '',
                        'golongan_darah': santri.golongan_darah or '',
                        'tinggi_badan': str(santri.tinggi_badan) if santri.tinggi_badan else '',
                        'berat_badan': str(santri.berat_badan) if santri.berat_badan else '',
                        # Data Orang Tua
                        'nama_ayah': santri.nama_ayah or '',
                        'nik_ayah': santri.nik_ayah or '',
                        'nama_ibu': santri.nama_ibu or '',
                        'nik_ibu': santri.nik_ibu or '',
                        'pekerjaan_ayah': santri.pekerjaan_ayah or '',
                        'pekerjaan_ibu': santri.pekerjaan_ibu or '',
                        'no_hp_ayah': santri.no_hp_ayah or '',
                        'no_hp_ibu': santri.no_hp_ibu or '',
                        'alamat_orangtua': santri.alamat_orangtua or '',
                        # Kontak
                        'alamat': santri.alamat or '',
                        'no_hp': santri.no_hp or '',
                        'email': santri.email or '',
                        # Data Sekolah
                        'asal_sekolah': santri.asal_sekolah or '',
                        'kelas_terakhir': santri.kelas_terakhir or '',
                        'tahun_lulus': santri.tahun_lulus or '',
                        'no_ijazah': santri.no_ijazah or '',
                        # Status
                        'status': santri.get_status_display() if hasattr(santri, 'get_status_display') else (santri.status or ''),
                        # Tanggal
                        'tanggal_daftar': format_tanggal_indonesia(santri.created_at),
                        'tanggal_daftar_short': format_tanggal_short(santri.created_at),
                        'tanggal_hari_ini': format_tanggal_indonesia(datetime.now()),
                        'tanggal_hari_ini_short': format_tanggal_short(datetime.now()),
                    }
                    
                    if template_id and template:
                        # Gunakan method render_pesan dari template
                        pesan_rendered = template.render_pesan(**variabel_dict)
                    else:
                        # Manual replace untuk pesan custom - replace semua variabel
                        pesan_rendered = pesan
                        for key, value in variabel_dict.items():
                            pesan_rendered = pesan_rendered.replace(f'{{{key}}}', str(value))
                    
                    from urllib.parse import quote
                    pesan_encoded = quote(pesan_rendered)
                    whatsapp_link = f"https://wa.me/{nomor}?text={pesan_encoded}"
                    broadcast_links.append({
                        'santri': santri,
                        'link': whatsapp_link,
                        'pesan': pesan_rendered
                    })
        
        return render(request, 'admin-panel/core/whatsapp_broadcast_result.html', {
            'broadcast_links': broadcast_links,
            'pesan': pesan,
        })
    
    return render(request, 'admin-panel/core/whatsapp_broadcast.html', {
        'templates': templates,
        'santri_list': santri_list,
    })


# ==================== WEBSITE SETTINGS CRUD ====================
# Hero Section
@login_required
@user_passes_test(is_staff_user)
def hero_section_list(request):
    """List semua hero section"""
    heroes = HeroSection.objects.all().order_by('order', '-created_at')
    search = request.GET.get('search', '')
    if search:
        heroes = heroes.filter(title__icontains=search)
    
    paginator = Paginator(heroes, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    hero_id = request.GET.get('edit', None)
    form = None
    hero = None
    if hero_id:
        hero = get_object_or_404(HeroSection, id=hero_id)
        form = HeroSectionForm(instance=hero)
    else:
        form = HeroSectionForm()
    
    # Get active heroes for preview (max 3)
    # Filter hero yang aktif dan memiliki gambar
    active_heroes = HeroSection.objects.filter(is_active=True).exclude(image__isnull=True).exclude(image='').order_by('order', '-created_at')[:3]
    
    return render(request, 'admin-panel/core/hero_section_list.html', {
        'heroes': page,
        'search': search,
        'form': form,
        'hero': hero,
        'active_heroes': active_heroes,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def hero_section_form(request, hero_id=None):
    """Create/Update hero section"""
    from admin_panel.models import ConvertedImage
    from django.core.files import File
    import os
    
    if hero_id:
        hero = get_object_or_404(HeroSection, id=hero_id)
        form = HeroSectionForm(request.POST, request.FILES, instance=hero)
    else:
        form = HeroSectionForm(request.POST, request.FILES)
    
    # Handle selected_image_id dari image picker (cek sebelum validasi form)
    selected_image_id = request.POST.get('selected_image_id')
    
    # Validasi: jika create baru, pastikan ada image (dari upload atau gallery)
    if not hero_id:
        has_uploaded_image = 'image' in request.FILES and request.FILES['image']
        if not has_uploaded_image and not selected_image_id:
            messages.error(request, 'Gambar wajib diisi. Pilih dari gallery atau upload manual.')
            if is_htmx_request(request):
                return HttpResponseClientRefresh()
            return redirect('core:hero_section_list')
    
    if form.is_valid():
        # Handle selected_image_id dari image picker (prioritas dari gallery)
        if selected_image_id:
            try:
                converted_image = ConvertedImage.objects.get(id=selected_image_id)
                # Langsung gunakan path dari media/converted tanpa copy file
                if converted_image.webp_image:
                    hero_section = form.save(commit=False)
                    # Set path langsung dari ConvertedImage (tidak copy file)
                    hero_section.image = converted_image.webp_image
                    
                    # Validasi maksimal 3 gambar aktif
                    is_active = form.cleaned_data.get('is_active', False)
                    if is_active:
                        active_count = HeroSection.objects.filter(is_active=True).count()
                        if hero_id and hero and hero.is_active:
                            active_count -= 1
                        if active_count >= 3:
                            messages.error(request, 'Maksimal hanya 3 hero section yang dapat aktif! Silakan nonaktifkan salah satu terlebih dahulu.')
                            if is_htmx_request(request):
                                return HttpResponseClientRefresh()
                            return redirect('core:hero_section_list')
                    
                    hero_section.save()
                    messages.success(request, f'Hero Section berhasil {"diupdate" if hero_id else "ditambahkan"}!')
                    if is_htmx_request(request):
                        return HttpResponseClientRefresh()
                    return redirect('core:hero_section_list')
            except ConvertedImage.DoesNotExist:
                messages.error(request, 'Gambar yang dipilih tidak ditemukan!')
                if is_htmx_request(request):
                    return HttpResponseClientRefresh()
                return redirect('core:hero_section_list')
        
        # Validasi maksimal 3 gambar aktif
        is_active = form.cleaned_data.get('is_active', False)
        if is_active:
            active_count = HeroSection.objects.filter(is_active=True).count()
            if hero_id:
                # Jika edit, kurangi 1 jika hero yang diedit sudah aktif
                if hero and hero.is_active:
                    active_count -= 1
            if active_count >= 3:
                messages.error(request, 'Maksimal hanya 3 hero section yang dapat aktif! Silakan nonaktifkan salah satu terlebih dahulu.')
                if is_htmx_request(request):
                    return HttpResponseClientRefresh()
                return redirect('core:hero_section_list')
        
        form.save()
        messages.success(request, f'Hero Section berhasil {"diupdate" if hero_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:hero_section_list')
    
    return redirect('core:hero_section_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def hero_section_delete(request, hero_id):
    """Delete hero section"""
    hero = get_object_or_404(HeroSection, id=hero_id)
    title = hero.title or f'Hero {hero.id}'
    hero.delete()
    messages.success(request, f'Hero Section "{title}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:hero_section_list')


# Sejarah Timeline
@login_required
@user_passes_test(is_staff_user)
def sejarah_timeline_list(request):
    """List semua timeline sejarah"""
    timelines = SejarahTimeline.objects.prefetch_related('gambar').all().order_by('order', '-created_at')
    search = request.GET.get('search', '')
    if search:
        timelines = timelines.filter(judul__icontains=search)
    
    paginator = Paginator(timelines, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    timeline_id = request.GET.get('edit', None)
    form = None
    timeline = None
    if timeline_id:
        timeline = get_object_or_404(SejarahTimeline.objects.prefetch_related('gambar'), id=timeline_id)
        form = SejarahTimelineForm(instance=timeline)
    else:
        form = SejarahTimelineForm()
    
    return render(request, 'admin-panel/core/sejarah_timeline_list.html', {
        'timelines': page,
        'search': search,
        'form': form,
        'timeline': timeline,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def sejarah_timeline_form(request, timeline_id=None):
    """Create/Update timeline sejarah"""
    if timeline_id:
        timeline = get_object_or_404(SejarahTimeline, id=timeline_id)
        form = SejarahTimelineForm(request.POST, instance=timeline)
    else:
        form = SejarahTimelineForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Timeline Sejarah berhasil {"diupdate" if timeline_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:sejarah_timeline_list')
    
    return redirect('core:sejarah_timeline_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def sejarah_timeline_delete(request, timeline_id):
    """Delete timeline sejarah"""
    timeline = get_object_or_404(SejarahTimeline, id=timeline_id)
    judul = timeline.judul
    timeline.delete()
    messages.success(request, f'Timeline Sejarah "{judul}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:sejarah_timeline_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def sejarah_timeline_image_add(request, timeline_id):
    """Add image to timeline sejarah"""
    from admin_panel.models import ConvertedImage
    
    timeline = get_object_or_404(SejarahTimeline, id=timeline_id)
    
    # Handle selected_image_id dari image picker
    selected_sejarah_gambar_id = request.POST.get('selected_sejarah_gambar_id')
    if selected_sejarah_gambar_id:
        try:
            converted_image = ConvertedImage.objects.get(id=selected_sejarah_gambar_id)
            if converted_image.webp_image:
                order = int(request.POST.get('order', 0))
                SejarahTimelineImage.objects.create(
                    timeline=timeline,
                    gambar=converted_image.webp_image,
                    order=order
                )
                messages.success(request, 'Gambar berhasil ditambahkan dari gallery!')
                if is_htmx_request(request):
                    return HttpResponseClientRefresh()
                return redirect('core:sejarah_timeline_list')
        except ConvertedImage.DoesNotExist:
            messages.error(request, 'Gambar yang dipilih dari gallery tidak ditemukan!')
            if is_htmx_request(request):
                return HttpResponseClientRefresh()
            return redirect('core:sejarah_timeline_list')
        except (ValueError, TypeError):
            messages.error(request, 'Urutan harus berupa angka!')
            if is_htmx_request(request):
                return HttpResponseClientRefresh()
            return redirect('core:sejarah_timeline_list')
    
    # Fallback: upload manual
    has_uploaded_file = 'gambar' in request.FILES and request.FILES['gambar']
    if not has_uploaded_file:
        messages.error(request, 'Silakan pilih gambar dari gallery atau upload file gambar!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:sejarah_timeline_list')
    
    form = SejarahTimelineImageForm(request.POST, request.FILES)
    
    if form.is_valid():
        image = form.save(commit=False)
        image.timeline = timeline
        image.save()
        messages.success(request, 'Gambar berhasil ditambahkan!')
    else:
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{form.fields[field].label}: {error}")
        messages.error(request, 'Gagal menambahkan gambar. ' + ' '.join(error_messages))
    
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:sejarah_timeline_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def sejarah_timeline_image_delete(request, image_id):
    """Delete image from timeline sejarah"""
    image = get_object_or_404(SejarahTimelineImage, id=image_id)
    image.delete()
    messages.success(request, 'Gambar berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:sejarah_timeline_list')


# Visi Misi
@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def visi_misi_form(request):
    """Create/Update Visi Misi (Singleton)"""
    visi_misi = VisiMisi.load()
    form = VisiMisiForm(request.POST or None, instance=visi_misi)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Visi Misi berhasil diupdate!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:visi_misi_form')
    
    return render(request, 'admin-panel/core/visi_misi_form.html', {
        'form': form,
        'visi_misi': visi_misi,
    })


# Program Pendidikan
@login_required
@user_passes_test(is_staff_user)
def program_pendidikan_list(request):
    """List semua program pendidikan"""
    programs = ProgramPendidikan.objects.prefetch_related('gambar_program').all().order_by('order', 'nama')
    search = request.GET.get('search', '')
    if search:
        programs = programs.filter(nama__icontains=search)
    
    paginator = Paginator(programs, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    program_id = request.GET.get('edit', None)
    form = None
    program = None
    if program_id:
        program = get_object_or_404(ProgramPendidikan.objects.prefetch_related('gambar_program'), id=program_id)
        form = ProgramPendidikanForm(instance=program)
    else:
        form = ProgramPendidikanForm()
    
    return render(request, 'admin-panel/core/program_pendidikan_list.html', {
        'programs': page,
        'search': search,
        'form': form,
        'program': program,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def program_pendidikan_form(request, program_id=None):
    """Create/Update program pendidikan"""
    from admin_panel.models import ConvertedImage
    
    if program_id:
        program = get_object_or_404(ProgramPendidikan, id=program_id)
        form = ProgramPendidikanForm(request.POST, request.FILES, instance=program)
    else:
        form = ProgramPendidikanForm(request.POST, request.FILES)
    
    if form.is_valid():
        # Handle selected_image_id dari image picker
        selected_program_pendidikan_gambar_id = request.POST.get('selected_program_pendidikan_gambar_id')
        if selected_program_pendidikan_gambar_id:
            try:
                converted_image = ConvertedImage.objects.get(id=selected_program_pendidikan_gambar_id)
                if converted_image.webp_image:
                    program_obj = form.save(commit=False)
                    program_obj.gambar = converted_image.webp_image
                    program_obj.save()
                    messages.success(request, f'Program Pendidikan berhasil {"diupdate" if program_id else "ditambahkan"}!')
                    if is_htmx_request(request):
                        return HttpResponseClientRefresh()
                    return redirect('core:program_pendidikan_list')
            except ConvertedImage.DoesNotExist:
                pass
        
        form.save()
        messages.success(request, f'Program Pendidikan berhasil {"diupdate" if program_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:program_pendidikan_list')
    
    return redirect('core:program_pendidikan_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def program_pendidikan_delete(request, program_id):
    """Delete program pendidikan"""
    program = get_object_or_404(ProgramPendidikan, id=program_id)
    nama = program.nama
    program.delete()
    messages.success(request, f'Program Pendidikan "{nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:program_pendidikan_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def program_pendidikan_image_add(request, program_id):
    """Tambah gambar untuk program pendidikan (maksimal 3)"""
    program = get_object_or_404(ProgramPendidikan, id=program_id)
    
    # Cek jumlah gambar yang sudah ada
    existing_count = program.gambar_program.count()
    if existing_count >= 3:
        messages.error(request, 'Maksimal 3 gambar per program!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:program_pendidikan_list')
    
    # Ambil file dari request
    if 'gambar' in request.FILES:
        gambar = request.FILES['gambar']
        alt_text = request.POST.get('alt_text', '')
        
        # Buat order baru
        max_order = program.gambar_program.aggregate(db_models_Max('order'))['order__max'] or 0
        
        ProgramPendidikanImage.objects.create(
            program=program,
            gambar=gambar,
            alt_text=alt_text,
            order=max_order + 1
        )
        messages.success(request, 'Gambar berhasil ditambahkan!')
    else:
        messages.error(request, 'Gambar tidak ditemukan!')
    
    # Selalu redirect untuk refresh data
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:program_pendidikan_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def program_pendidikan_image_delete(request, image_id):
    """Hapus gambar program pendidikan"""
    image = get_object_or_404(ProgramPendidikanImage, id=image_id)
    program_nama = image.program.nama
    image.delete()
    messages.success(request, f'Gambar untuk "{program_nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:program_pendidikan_list')


# Fasilitas
@login_required
@user_passes_test(is_staff_user)
def fasilitas_list(request):
    """List semua fasilitas"""
    fasilitas = Fasilitas.objects.all().order_by('order', 'nama')
    search = request.GET.get('search', '')
    if search:
        fasilitas = fasilitas.filter(nama__icontains=search)
    
    paginator = Paginator(fasilitas, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    fasilitas_id = request.GET.get('edit', None)
    form = None
    fasilitas_obj = None
    if fasilitas_id:
        fasilitas_obj = get_object_or_404(Fasilitas, id=fasilitas_id)
        form = FasilitasForm(instance=fasilitas_obj)
    else:
        form = FasilitasForm()
    
    return render(request, 'admin-panel/core/fasilitas_list.html', {
        'fasilitas': page,
        'search': search,
        'form': form,
        'fasilitas_obj': fasilitas_obj,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def fasilitas_form(request, fasilitas_id=None):
    """Create/Update fasilitas"""
    from admin_panel.models import ConvertedImage
    
    if fasilitas_id:
        fasilitas = get_object_or_404(Fasilitas, id=fasilitas_id)
        form = FasilitasForm(request.POST, request.FILES, instance=fasilitas)
    else:
        form = FasilitasForm(request.POST, request.FILES)
    
    if form.is_valid():
        # Handle selected_image_id dari image picker
        selected_fasilitas_gambar_id = request.POST.get('selected_fasilitas_gambar_id')
        if selected_fasilitas_gambar_id:
            try:
                converted_image = ConvertedImage.objects.get(id=selected_fasilitas_gambar_id)
                if converted_image.webp_image:
                    fasilitas_obj = form.save(commit=False)
                    fasilitas_obj.gambar = converted_image.webp_image
                    fasilitas_obj.save()
                    messages.success(request, f'Fasilitas berhasil {"diupdate" if fasilitas_id else "ditambahkan"}!')
                    if is_htmx_request(request):
                        return HttpResponseClientRefresh()
                    return redirect('core:fasilitas_list')
            except ConvertedImage.DoesNotExist:
                pass
        
        form.save()
        messages.success(request, f'Fasilitas berhasil {"diupdate" if fasilitas_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:fasilitas_list')
    
    return redirect('core:fasilitas_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def fasilitas_delete(request, fasilitas_id):
    """Delete fasilitas"""
    fasilitas = get_object_or_404(Fasilitas, id=fasilitas_id)
    nama = fasilitas.nama
    fasilitas.delete()
    messages.success(request, f'Fasilitas "{nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:fasilitas_list')


# Ekstrakurikuler
@login_required
@user_passes_test(is_staff_user)
def ekstrakurikuler_list(request):
    """List semua ekstrakurikuler"""
    ekstra = Ekstrakurikuler.objects.prefetch_related('gambar_ekstrakurikuler').all().order_by('order', 'nama')
    search = request.GET.get('search', '')
    if search:
        ekstra = ekstra.filter(nama__icontains=search)
    
    paginator = Paginator(ekstra, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    ekstra_id = request.GET.get('edit', None)
    form = None
    ekstra_obj = None
    if ekstra_id:
        ekstra_obj = get_object_or_404(Ekstrakurikuler.objects.prefetch_related('gambar_ekstrakurikuler'), id=ekstra_id)
        form = EkstrakurikulerForm(instance=ekstra_obj)
    else:
        form = EkstrakurikulerForm()
    
    return render(request, 'admin-panel/core/ekstrakurikuler_list.html', {
        'ekstra': page,
        'search': search,
        'form': form,
        'ekstra_obj': ekstra_obj,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def ekstrakurikuler_form(request, ekstra_id=None):
    """Create/Update ekstrakurikuler"""
    if ekstra_id:
        ekstra = get_object_or_404(Ekstrakurikuler, id=ekstra_id)
        form = EkstrakurikulerForm(request.POST, instance=ekstra)
    else:
        form = EkstrakurikulerForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Ekstrakurikuler berhasil {"diupdate" if ekstra_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:ekstrakurikuler_list')
    
    return redirect('core:ekstrakurikuler_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def ekstrakurikuler_delete(request, ekstra_id):
    """Delete ekstrakurikuler"""
    ekstra = get_object_or_404(Ekstrakurikuler, id=ekstra_id)
    nama = ekstra.nama
    ekstra.delete()
    messages.success(request, f'Ekstrakurikuler "{nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:ekstrakurikuler_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def ekstrakurikuler_image_add(request, ekstra_id):
    """Tambah gambar untuk ekstrakurikuler (maksimal 5)"""
    ekstra = get_object_or_404(Ekstrakurikuler, id=ekstra_id)
    
    # Cek jumlah gambar yang sudah ada
    existing_count = ekstra.gambar_ekstrakurikuler.count()
    if existing_count >= 5:
        messages.error(request, 'Maksimal 5 gambar per ekstrakurikuler!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:ekstrakurikuler_list')
    
    # Cek apakah ada selected_ekstrakurikuler_gambar_id (dari image picker)
    selected_ekstrakurikuler_gambar_id = request.POST.get('selected_ekstrakurikuler_gambar_id', '').strip()
    if selected_ekstrakurikuler_gambar_id:
        try:
            from admin_panel.models import ConvertedImage
            converted_image = ConvertedImage.objects.get(id=int(selected_ekstrakurikuler_gambar_id))
            
            # Buat order baru
            max_order = ekstra.gambar_ekstrakurikuler.aggregate(db_models_Max('order'))['order__max'] or 0
            
            if converted_image.webp_image:
                EkstrakurikulerImage.objects.create(
                    ekstrakurikuler=ekstra,
                    gambar=converted_image.webp_image,
                    alt_text=converted_image.judul or '',
                    order=max_order + 1
                )
                messages.success(request, 'Gambar berhasil ditambahkan dari gallery!')
            else:
                messages.error(request, 'Gambar WebP tidak ditemukan!')
                if is_htmx_request(request):
                    return HttpResponseClientRefresh()
                return redirect('core:ekstrakurikuler_list')
        except (ConvertedImage.DoesNotExist, ValueError, TypeError):
            messages.error(request, 'Gambar dari gallery tidak ditemukan!')
            if is_htmx_request(request):
                return HttpResponseClientRefresh()
            return redirect('core:ekstrakurikuler_list')
    # Ambil file dari request (upload manual)
    elif 'gambar' in request.FILES and request.FILES['gambar']:
        gambar = request.FILES['gambar']
        
        # Buat order baru
        max_order = ekstra.gambar_ekstrakurikuler.aggregate(db_models_Max('order'))['order__max'] or 0
        
        EkstrakurikulerImage.objects.create(
            ekstrakurikuler=ekstra,
            gambar=gambar,
            alt_text='',
            order=max_order + 1
        )
        messages.success(request, 'Gambar berhasil ditambahkan!')
    else:
        messages.error(request, 'Gambar tidak ditemukan! Pilih dari gallery atau upload manual.')
    
    # Selalu redirect untuk refresh data
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:ekstrakurikuler_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def ekstrakurikuler_image_delete(request, image_id):
    """Hapus gambar ekstrakurikuler"""
    image = get_object_or_404(EkstrakurikulerImage, id=image_id)
    ekstra_nama = image.ekstrakurikuler.nama
    image.delete()
    messages.success(request, f'Gambar untuk "{ekstra_nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:ekstrakurikuler_list')


# Jadwal Harian
@login_required
@user_passes_test(is_staff_user)
def jadwal_harian_list(request):
    """List semua jadwal harian dengan filter Santri/Santriwati"""
    # Filter berdasarkan kategori (santri/santriwati)
    kategori = request.GET.get('kategori', 'santri')  # default santri
    
    # Query berdasarkan kategori
    jadwal = JadwalHarian.objects.filter(kategori=kategori).order_by('order', 'waktu')
    
    search = request.GET.get('search', '')
    if search:
        jadwal = jadwal.filter(Q(judul__icontains=search) | Q(deskripsi__icontains=search))
    
    jadwal_id = request.GET.get('edit', None)
    form = None
    jadwal_obj = None
    if jadwal_id:
        jadwal_obj = get_object_or_404(JadwalHarian, id=jadwal_id)
        form = JadwalHarianForm(instance=jadwal_obj)
    else:
        form = JadwalHarianForm()
        # Set default kategori
        form.fields['kategori'].initial = kategori
    
    return render(request, 'admin-panel/core/jadwal_harian_list.html', {
        'jadwal': jadwal,
        'search': search,
        'kategori': kategori,
        'form': form,
        'jadwal_obj': jadwal_obj,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def jadwal_harian_form(request, jadwal_id=None):
    """Create/Update jadwal harian"""
    if jadwal_id:
        jadwal = get_object_or_404(JadwalHarian, id=jadwal_id)
        form = JadwalHarianForm(request.POST, instance=jadwal)
    else:
        form = JadwalHarianForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Jadwal Harian berhasil {"diupdate" if jadwal_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        # Redirect dengan kategori
        kategori = request.POST.get('kategori', 'santri')
        return redirect(f'{reverse("core:jadwal_harian_list")}?kategori={kategori}')
    
    # Redirect dengan kategori jika form tidak valid
    kategori = request.POST.get('kategori', 'santri')
    return redirect(f'{reverse("core:jadwal_harian_list")}?kategori={kategori}')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def jadwal_harian_delete(request, jadwal_id):
    """Delete jadwal harian"""
    jadwal = get_object_or_404(JadwalHarian, id=jadwal_id)
    judul = jadwal.judul
    kategori = jadwal.kategori
    jadwal.delete()
    messages.success(request, f'Jadwal Harian "{judul}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    # Redirect dengan kategori
    return redirect(f'{reverse("core:jadwal_harian_list")}?kategori={kategori}')


# Persyaratan
@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def persyaratan_form(request):
    """Create/Update Persyaratan (Singleton)"""
    persyaratan = Persyaratan.load()
    form = PersyaratanForm(request.POST or None, instance=persyaratan)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Persyaratan berhasil diupdate!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:persyaratan_form')
    
    return render(request, 'admin-panel/core/persyaratan_list.html', {
        'form': form,
        'persyaratan': persyaratan,
    })




# Alur Pendaftaran
@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def alur_pendaftaran_form(request):
    """Create/Update Alur Pendaftaran (Singleton)"""
    from admin_panel.models import ConvertedImage
    
    alur = AlurPendaftaran.load()
    form = AlurPendaftaranForm(request.POST or None, request.FILES or None, instance=alur)
    
    if request.method == 'POST' and form.is_valid():
        # Handle selected_image_id dari image picker
        selected_alur_gambar_id = request.POST.get('selected_alur_gambar_id')
        if selected_alur_gambar_id:
            try:
                converted_image = ConvertedImage.objects.get(id=selected_alur_gambar_id)
                if converted_image.webp_image:
                    alur_obj = form.save(commit=False)
                    alur_obj.gambar_utama = converted_image.webp_image
                    alur_obj.save()
                    messages.success(request, 'Alur Pendaftaran berhasil diupdate!')
                    if is_htmx_request(request):
                        return HttpResponseClientRefresh()
                    return redirect('core:alur_pendaftaran_form')
            except ConvertedImage.DoesNotExist:
                pass
        
        form.save()
        messages.success(request, 'Alur Pendaftaran berhasil diupdate!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:alur_pendaftaran_form')
    
    return render(request, 'admin-panel/core/alur_pendaftaran_list.html', {
        'form': form,
        'alur': alur,
    })


# Biaya Pendidikan
@login_required
@user_passes_test(is_staff_user)
def biaya_pendidikan_list(request):
    """List semua biaya pendidikan dengan filter Santri/Santriwati"""
    # Filter berdasarkan kategori (santri/santriwati)
    kategori = request.GET.get('kategori', 'santri')  # default santri
    
    # Query untuk santri (putra) - termasuk tahunan, bulanan, perlengkapan_putra
    if kategori == 'santri':
        biaya = BiayaPendidikan.objects.filter(
            tipe__in=['tahunan', 'bulanan', 'perlengkapan_putra']
        ).order_by('tipe', 'order')
    else:  # santriwati
        biaya = BiayaPendidikan.objects.filter(
            tipe__in=['tahunan', 'bulanan', 'perlengkapan_putri']
        ).order_by('tipe', 'order')
    
    search = request.GET.get('search', '')
    if search:
        biaya = biaya.filter(nama__icontains=search)
    
    tipe = request.GET.get('tipe', '')
    if tipe:
        biaya = biaya.filter(tipe=tipe)
    
    biaya_id = request.GET.get('edit', None)
    form = None
    biaya_obj = None
    if biaya_id:
        biaya_obj = get_object_or_404(BiayaPendidikan, id=biaya_id)
        form = BiayaPendidikanForm(instance=biaya_obj)
        # Filter choices berdasarkan kategori saat edit
        if kategori == 'santri':
            form.fields['tipe'].choices = [
                ('tahunan', 'Biaya Tahunan'),
                ('bulanan', 'Biaya Bulanan'),
                ('perlengkapan_putra', 'Perlengkapan Putra'),
            ]
        else:
            form.fields['tipe'].choices = [
                ('tahunan', 'Biaya Tahunan'),
                ('bulanan', 'Biaya Bulanan'),
                ('perlengkapan_putri', 'Perlengkapan Putri'),
            ]
    else:
        form = BiayaPendidikanForm()
        # Filter choices berdasarkan kategori
        if kategori == 'santri':
            form.fields['tipe'].choices = [
                ('tahunan', 'Biaya Tahunan'),
                ('bulanan', 'Biaya Bulanan'),
                ('perlengkapan_putra', 'Perlengkapan Putra'),
            ]
            form.fields['tipe'].initial = 'perlengkapan_putra'
        else:
            form.fields['tipe'].choices = [
                ('tahunan', 'Biaya Tahunan'),
                ('bulanan', 'Biaya Bulanan'),
                ('perlengkapan_putri', 'Perlengkapan Putri'),
            ]
            form.fields['tipe'].initial = 'perlengkapan_putri'
    
    return render(request, 'admin-panel/core/biaya_pendidikan_list.html', {
        'biaya': biaya,
        'search': search,
        'tipe': tipe,
        'kategori': kategori,
        'form': form,
        'biaya_obj': biaya_obj,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def biaya_pendidikan_form(request, biaya_id=None):
    """Create/Update biaya pendidikan"""
    if biaya_id:
        biaya = get_object_or_404(BiayaPendidikan, id=biaya_id)
        form = BiayaPendidikanForm(request.POST, instance=biaya)
    else:
        form = BiayaPendidikanForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Biaya Pendidikan berhasil {"diupdate" if biaya_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        # Redirect dengan kategori
        kategori = request.POST.get('kategori', 'santri')
        return redirect(f'{reverse("core:biaya_pendidikan_list")}?kategori={kategori}')
    
    # Redirect dengan kategori jika form tidak valid
    kategori = request.POST.get('kategori', 'santri')
    return redirect(f'{reverse("core:biaya_pendidikan_list")}?kategori={kategori}')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def biaya_pendidikan_delete(request, biaya_id):
    """Delete biaya pendidikan"""
    biaya = get_object_or_404(BiayaPendidikan, id=biaya_id)
    nama = biaya.nama
    biaya.delete()
    messages.success(request, f'Biaya Pendidikan "{nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    # Redirect dengan kategori
    kategori = request.POST.get('kategori', 'santri')
    return redirect(f'{reverse("core:biaya_pendidikan_list")}?kategori={kategori}')


# Contact Person
@login_required
@user_passes_test(is_staff_user)
def contact_person_list(request):
    """List semua contact person"""
    contacts = ContactPerson.objects.all().order_by('order', 'nama')
    search = request.GET.get('search', '')
    if search:
        contacts = contacts.filter(Q(nama__icontains=search) | Q(no_hp__icontains=search))
    
    paginator = Paginator(contacts, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    contact_id = request.GET.get('edit', None)
    form = None
    contact = None
    if contact_id:
        contact = get_object_or_404(ContactPerson, id=contact_id)
        form = ContactPersonForm(instance=contact)
    else:
        form = ContactPersonForm()
    
    return render(request, 'admin-panel/core/contact_person_list.html', {
        'contacts': page,
        'search': search,
        'form': form,
        'contact': contact,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def contact_person_form(request, contact_id=None):
    """Create/Update contact person"""
    from admin_panel.models import ConvertedImage
    
    if contact_id:
        contact = get_object_or_404(ContactPerson, id=contact_id)
        form = ContactPersonForm(request.POST, request.FILES, instance=contact)
    else:
        form = ContactPersonForm(request.POST, request.FILES)
    
    if form.is_valid():
        # Handle selected_image_id dari image picker (fallback) atau selected_contact_foto_id (baru)
        selected_contact_foto_id = request.POST.get('selected_contact_foto_id') or request.POST.get('selected_image_id')
        if selected_contact_foto_id:
            try:
                converted_image = ConvertedImage.objects.get(id=selected_contact_foto_id)
                if converted_image.webp_image:
                    contact_obj = form.save(commit=False)
                    contact_obj.foto = converted_image.webp_image
                    contact_obj.save()
                    messages.success(request, f'Contact Person berhasil {"diupdate" if contact_id else "ditambahkan"}!')
                    if is_htmx_request(request):
                        return HttpResponseClientRefresh()
                    return redirect('core:contact_person_list')
            except ConvertedImage.DoesNotExist:
                pass
        
        form.save()
        messages.success(request, f'Contact Person berhasil {"diupdate" if contact_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:contact_person_list')
    
    return redirect('core:contact_person_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def contact_person_delete(request, contact_id):
    """Delete contact person"""
    contact = get_object_or_404(ContactPerson, id=contact_id)
    nama = contact.nama
    contact.delete()
    messages.success(request, f'Contact Person "{nama}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:contact_person_list')


# Social Media
@login_required
@user_passes_test(is_staff_user)
def social_media_list(request):
    """List semua social media"""
    socials = SocialMedia.objects.all().order_by('order', 'platform')
    search = request.GET.get('search', '')
    platform = request.GET.get('platform', '')
    if search:
        socials = socials.filter(Q(username__icontains=search) | Q(url__icontains=search))
    if platform:
        socials = socials.filter(platform=platform)
    
    paginator = Paginator(socials, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    social_id = request.GET.get('edit', None)
    form = None
    social = None
    if social_id:
        social = get_object_or_404(SocialMedia, id=social_id)
        form = SocialMediaForm(instance=social)
    else:
        form = SocialMediaForm()
    
    return render(request, 'admin-panel/core/social_media_list.html', {
        'socials': page,
        'search': search,
        'platform': platform,
        'form': form,
        'social': social,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def social_media_form(request, social_id=None):
    """Create/Update social media"""
    if social_id:
        social = get_object_or_404(SocialMedia, id=social_id)
        form = SocialMediaForm(request.POST, instance=social)
    else:
        form = SocialMediaForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Social Media berhasil {"diupdate" if social_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:social_media_list')
    
    return redirect('core:social_media_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def social_media_delete(request, social_id):
    """Delete social media"""
    social = get_object_or_404(SocialMedia, id=social_id)
    username = social.username
    social.delete()
    messages.success(request, f'Social Media "{username}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:social_media_list')


# Seragam
@login_required
@user_passes_test(is_staff_user)
def seragam_list(request):
    """List semua seragam dengan filter Santri/Santriwati"""
    kategori = request.GET.get('kategori', 'santri')  # default santri
    
    seragam = Seragam.objects.filter(kategori=kategori).order_by('order', 'hari')
    search = request.GET.get('search', '')
    if search:
        seragam = seragam.filter(Q(hari__icontains=search) | Q(seragam__icontains=search))
    
    seragam_id = request.GET.get('edit', None)
    form = None
    seragam_obj = None
    if seragam_id:
        seragam_obj = get_object_or_404(Seragam, id=seragam_id)
        form = SeragamForm(instance=seragam_obj, initial_kategori=kategori)
    else:
        form = SeragamForm(initial_kategori=kategori)
    
    return render(request, 'admin-panel/core/seragam_list.html', {
        'seragam': seragam,
        'search': search,
        'kategori': kategori,
        'form': form,
        'seragam_obj': seragam_obj,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def seragam_form(request, seragam_id=None):
    """Create/Update seragam"""
    if seragam_id:
        seragam = get_object_or_404(Seragam, id=seragam_id)
        form = SeragamForm(request.POST, instance=seragam)
    else:
        form = SeragamForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Seragam berhasil {"diupdate" if seragam_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        kategori = request.POST.get('kategori', 'santri')
        return redirect(f'core:seragam_list?kategori={kategori}')
    
    kategori = request.POST.get('kategori', 'santri')
    return redirect(f'core:seragam_list?kategori={kategori}')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def seragam_delete(request, seragam_id):
    """Delete seragam"""
    seragam = get_object_or_404(Seragam, id=seragam_id)
    hari = seragam.hari
    seragam.delete()
    messages.success(request, f'Seragam "{hari}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:seragam_list')


# KMI
@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["GET", "POST"])
def kmi_form(request):
    """Create/Update KMI (Singleton)"""
    kmi = KMI.load()
    form = KMIForm(request.POST or None, instance=kmi)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'KMI berhasil diupdate!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:kmi_form')
    
    return render(request, 'admin-panel/core/kmi_form.html', {
        'form': form,
        'kmi': kmi,
    })


# Statistik
@login_required
@user_passes_test(is_staff_user)
def statistik_list(request):
    """List semua statistik"""
    statistik = Statistik.objects.all().order_by('order', 'judul')
    search = request.GET.get('search', '')
    if search:
        statistik = statistik.filter(judul__icontains=search)
    
    paginator = Paginator(statistik, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    statistik_id = request.GET.get('edit', None)
    form = None
    statistik_obj = None
    if statistik_id:
        statistik_obj = get_object_or_404(Statistik, id=statistik_id)
        form = StatistikForm(instance=statistik_obj)
    else:
        form = StatistikForm()
    
    return render(request, 'admin-panel/core/statistik_list.html', {
        'statistik': page,
        'search': search,
        'form': form,
        'statistik_obj': statistik_obj,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def statistik_form(request, statistik_id=None):
    """Create/Update statistik"""
    if statistik_id:
        statistik = get_object_or_404(Statistik, id=statistik_id)
        form = StatistikForm(request.POST, instance=statistik)
    else:
        form = StatistikForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Statistik berhasil {"diupdate" if statistik_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:statistik_list')
    
    return redirect('core:statistik_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def statistik_delete(request, statistik_id):
    """Delete statistik"""
    statistik = get_object_or_404(Statistik, id=statistik_id)
    judul = statistik.judul
    statistik.delete()
    messages.success(request, f'Statistik "{judul}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:statistik_list')


# ==================== Media CRUD (Galeri & Video) ====================
@login_required
@user_passes_test(is_staff_user)
def media_list(request):
    """List semua Media (Galeri & Video) dengan modal untuk create/edit"""
    tipe = request.GET.get('tipe', '')
    search = request.GET.get('search', '')
    
    media_list = Media.objects.all().order_by('tipe', 'order', 'created_at')
    
    if tipe:
        media_list = media_list.filter(tipe=tipe)
    if search:
        media_list = media_list.filter(Q(judul__icontains=search) | Q(sub_judul__icontains=search))
    
    paginator = Paginator(media_list, 12)
    page = paginator.get_page(request.GET.get('page', 1))
    
    media_id = request.GET.get('edit', None)
    form = None
    media_obj = None
    if media_id:
        media_obj = get_object_or_404(Media, id=media_id)
        form = MediaForm(instance=media_obj)
    else:
        form = MediaForm()
    
    # Statistics
    gallery_count = Media.objects.filter(tipe='gallery', is_published=True).count()
    video_count = Media.objects.filter(tipe='video', is_published=True).count()
    total_count = Media.objects.filter(is_published=True).count()
    
    return render(request, 'admin-panel/core/media_list.html', {
        'media_list': page,
        'search': search,
        'tipe': tipe,
        'form': form,
        'media_obj': media_obj,
        'gallery_count': gallery_count,
        'video_count': video_count,
        'total_count': total_count,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def media_form(request, media_id=None):
    """Create/Update Media"""
    from admin_panel.models import ConvertedImage
    
    # Cek apakah ada selected_media_gambar_id atau selected_media_featured_id sebelum validasi
    selected_media_gambar_id = request.POST.get('selected_media_gambar_id', '').strip()
    selected_media_featured_id = request.POST.get('selected_media_featured_id', '').strip()
    tipe = request.POST.get('tipe', '')
    
    if media_id:
        media_obj = get_object_or_404(Media, id=media_id)
        form = MediaForm(request.POST, request.FILES, instance=media_obj)
    else:
        form = MediaForm(request.POST, request.FILES)
    
    # Pass selected_media_gambar_id ke form untuk validasi
    if selected_media_gambar_id:
        form._selected_media_gambar_id = selected_media_gambar_id
    
    # Jika tipe gallery dan ada selected_media_gambar_id, gambar tidak wajib
    if tipe == 'gallery' and selected_media_gambar_id:
        # Remove required validation untuk gambar jika sudah dipilih dari gallery
        if 'gambar' in form.fields:
            form.fields['gambar'].required = False
            form.fields['gambar'].blank = True
    
    # Jika tipe video dan ada selected_media_featured_id, featured_image tidak wajib
    if tipe == 'video' and selected_media_featured_id:
        # Remove required validation untuk featured_image jika sudah dipilih dari gallery
        if 'featured_image' in form.fields:
            form.fields['featured_image'].required = False
            form.fields['featured_image'].blank = True
    
    if form.is_valid():
        media_instance = form.save(commit=False)
        
        # Handle selected_image_id untuk gambar (galeri) - SET SEBELUM VALIDASI
        if selected_media_gambar_id:
            try:
                converted_image = ConvertedImage.objects.get(id=int(selected_media_gambar_id))
                if converted_image.webp_image:
                    media_instance.gambar = converted_image.webp_image
                else:
                    messages.error(request, 'Gambar WebP tidak ditemukan di gallery.')
                    if is_htmx_request(request):
                        return HttpResponseClientRefresh()
                    return redirect('core:media_list')
            except (ConvertedImage.DoesNotExist, ValueError, TypeError) as e:
                messages.error(request, 'Gambar dari gallery tidak ditemukan.')
                if is_htmx_request(request):
                    return HttpResponseClientRefresh()
                return redirect('core:media_list')
        
        # Handle selected_image_id untuk featured_image (thumbnail video)
        if selected_media_featured_id:
            try:
                converted_image = ConvertedImage.objects.get(id=int(selected_media_featured_id))
                if converted_image.webp_image:
                    media_instance.featured_image = converted_image.webp_image
            except (ConvertedImage.DoesNotExist, ValueError, TypeError) as e:
                # Featured image tidak wajib, jadi tidak perlu error
                pass
        
        # Validasi: untuk gallery baru, harus ada gambar (dari gallery atau upload)
        if not media_id and tipe == 'gallery':
            has_gambar_from_instance = media_instance.gambar is not None
            has_upload = 'gambar' in request.FILES and request.FILES['gambar']
            
            if not has_gambar_from_instance and not has_upload:
                messages.error(request, 'Gambar wajib diisi untuk galeri. Pilih dari gallery atau upload manual.')
                if is_htmx_request(request):
                    return HttpResponseClientRefresh()
                return redirect('core:media_list')
        
        # Validasi: untuk video baru, harus ada video_file
        if not media_id and tipe == 'video':
            has_video = 'video_file' in request.FILES and request.FILES['video_file']
            has_video_from_instance = media_instance.video_file is not None
            if not has_video and not has_video_from_instance:
                messages.error(request, 'File video wajib diisi untuk video.')
                if is_htmx_request(request):
                    return HttpResponseClientRefresh()
                return redirect('core:media_list')
        
        media_instance.save()
        messages.success(request, f'Media berhasil {"diupdate" if media_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:media_list')
    
    # If form is invalid, show form errors
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            error_messages.append(f"{field}: {error}")
    
    # Debug info
    debug_info = []
    if selected_media_gambar_id:
        debug_info.append(f"selected_media_gambar_id: {selected_media_gambar_id}")
    if selected_media_featured_id:
        debug_info.append(f"selected_media_featured_id: {selected_media_featured_id}")
    if tipe:
        debug_info.append(f"tipe: {tipe}")
    
    if error_messages:
        error_msg = f'Terjadi kesalahan: {", ".join(error_messages)}'
        if debug_info:
            error_msg += f" | Debug: {', '.join(debug_info)}"
        messages.error(request, error_msg)
    else:
        error_msg = 'Terjadi kesalahan saat menyimpan media. Periksa kembali form.'
        if debug_info:
            error_msg += f" | Debug: {', '.join(debug_info)}"
        messages.error(request, error_msg)
    
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:media_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def media_delete(request, media_id):
    """Delete Media"""
    media_obj = get_object_or_404(Media, id=media_id)
    judul = media_obj.judul
    media_obj.delete()
    messages.success(request, f'Media "{judul}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:media_list')


# ==================== Dokumentasi CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def dokumentasi_list(request):
    """List semua Dokumentasi dengan modal untuk create/edit"""
    kategori = request.GET.get('kategori', '')
    search = request.GET.get('search', '')
    
    dokumentasi_list = Dokumentasi.objects.prefetch_related('gambar_dokumentasi').all().order_by('order', '-tanggal_kegiatan', '-created_at')
    
    if kategori:
        dokumentasi_list = dokumentasi_list.filter(kategori=kategori)
    if search:
        dokumentasi_list = dokumentasi_list.filter(Q(judul__icontains=search) | Q(deskripsi__icontains=search))
    
    paginator = Paginator(dokumentasi_list, 12)
    page = paginator.get_page(request.GET.get('page', 1))
    
    dokumentasi_id = request.GET.get('edit', None)
    form = None
    dokumentasi_obj = None
    if dokumentasi_id:
        dokumentasi_obj = get_object_or_404(Dokumentasi.objects.prefetch_related('gambar_dokumentasi'), id=dokumentasi_id)
        form = DokumentasiForm(instance=dokumentasi_obj)
    else:
        form = DokumentasiForm()
    
    # Statistics
    published_count = Dokumentasi.objects.filter(is_published=True).count()
    total_count = Dokumentasi.objects.count()
    
    return render(request, 'admin-panel/core/dokumentasi_list.html', {
        'dokumentasi_list': page,
        'search': search,
        'kategori': kategori,
        'form': form,
        'dokumentasi_obj': dokumentasi_obj,
        'published_count': published_count,
        'total_count': total_count,
    })


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def dokumentasi_form(request, dokumentasi_id=None):
    """Create/Update dokumentasi"""
    if dokumentasi_id:
        dokumentasi = get_object_or_404(Dokumentasi, id=dokumentasi_id)
        form = DokumentasiForm(request.POST, instance=dokumentasi)
    else:
        form = DokumentasiForm(request.POST)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Dokumentasi berhasil {"diupdate" if dokumentasi_id else "ditambahkan"}!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:dokumentasi_list')
    
    messages.error(request, 'Gagal menyimpan dokumentasi. Periksa kembali form.')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:dokumentasi_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def dokumentasi_delete(request, dokumentasi_id):
    """Delete dokumentasi"""
    dokumentasi = get_object_or_404(Dokumentasi, id=dokumentasi_id)
    judul = dokumentasi.judul
    dokumentasi.delete()
    messages.success(request, f'Dokumentasi "{judul}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:dokumentasi_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["POST"])
def dokumentasi_image_add(request, dokumentasi_id):
    """Tambah gambar untuk dokumentasi (maksimal 10)"""
    dokumentasi = get_object_or_404(Dokumentasi, id=dokumentasi_id)
    
    # Cek jumlah gambar yang sudah ada
    existing_count = dokumentasi.gambar_dokumentasi.count()
    if existing_count >= 10:
        messages.error(request, 'Maksimal 10 gambar per dokumentasi!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:dokumentasi_list')
    
    alt_text = request.POST.get('alt_text', '')
    
    # Cek apakah ada selected_dokumentasi_gambar_id (dari image picker)
    selected_dokumentasi_gambar_id = request.POST.get('selected_dokumentasi_gambar_id', '').strip()
    if selected_dokumentasi_gambar_id:
        try:
            from admin_panel.models import ConvertedImage
            converted_image = ConvertedImage.objects.get(id=int(selected_dokumentasi_gambar_id))
            
            # Buat order baru
            max_order = dokumentasi.gambar_dokumentasi.aggregate(db_models_Max('order'))['order__max'] or 0
            
            if converted_image.webp_image:
                DokumentasiImage.objects.create(
                    dokumentasi=dokumentasi,
                    gambar=converted_image.webp_image,
                    alt_text=alt_text or converted_image.judul or '',
                    order=max_order + 1
                )
                messages.success(request, 'Gambar berhasil ditambahkan dari gallery!')
            else:
                messages.error(request, 'Gambar WebP tidak ditemukan!')
                if is_htmx_request(request):
                    return HttpResponseClientRefresh()
                return redirect('core:dokumentasi_list')
        except (ConvertedImage.DoesNotExist, ValueError, TypeError):
            messages.error(request, 'Gambar dari gallery tidak ditemukan!')
            if is_htmx_request(request):
                return HttpResponseClientRefresh()
            return redirect('core:dokumentasi_list')
    # Ambil file dari request (upload manual)
    elif 'gambar' in request.FILES and request.FILES['gambar']:
        gambar = request.FILES['gambar']
        
        # Buat order baru
        max_order = dokumentasi.gambar_dokumentasi.aggregate(db_models_Max('order'))['order__max'] or 0
        
        DokumentasiImage.objects.create(
            dokumentasi=dokumentasi,
            gambar=gambar,
            alt_text=alt_text,
            order=max_order + 1
        )
        messages.success(request, 'Gambar berhasil ditambahkan!')
    else:
        messages.error(request, 'Gambar tidak ditemukan! Pilih dari gallery atau upload manual.')
    
    # Selalu redirect untuk refresh data
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:dokumentasi_list')


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def dokumentasi_image_delete(request, image_id):
    """Hapus gambar dokumentasi"""
    image = get_object_or_404(DokumentasiImage, id=image_id)
    dokumentasi_judul = image.dokumentasi.judul
    image.delete()
    messages.success(request, f'Gambar untuk "{dokumentasi_judul}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:dokumentasi_list')


# ==================== INFORMASI TAMBAHAN CRUD ====================
@login_required
@user_passes_test(is_staff_user)
def informasi_tambahan_list(request):
    """List semua Informasi Tambahan"""
    search = request.GET.get('search', '')
    
    informasi_list = InformasiTambahan.objects.all().order_by('order', 'judul')
    
    if search:
        informasi_list = informasi_list.filter(Q(judul__icontains=search) | Q(deskripsi__icontains=search))
    
    paginator = Paginator(informasi_list, 10)
    page = paginator.get_page(request.GET.get('page', 1))
    
    context = {
        'informasi_list': page,
        'search': search,
    }
    return render(request, 'admin-panel/core/informasi_tambahan_list.html', context)


@login_required
@user_passes_test(is_staff_user)
def informasi_tambahan_form(request, informasi_id=None):
    """Form untuk create/edit Informasi Tambahan"""
    if informasi_id:
        informasi = get_object_or_404(InformasiTambahan, id=informasi_id)
        form = InformasiTambahanForm(request.POST or None, instance=informasi)
        title = 'Edit Informasi Tambahan'
    else:
        informasi = None
        form = InformasiTambahanForm(request.POST or None)
        title = 'Tambah Informasi Tambahan'
    
    if request.method == 'POST' and form.is_valid():
        informasi = form.save()
        messages.success(request, f'Informasi Tambahan "{informasi.judul}" berhasil disimpan!')
        if is_htmx_request(request):
            return HttpResponseClientRefresh()
        return redirect('core:informasi_tambahan_list')
    
    context = {
        'form': form,
        'informasi': informasi,
        'title': title,
    }
    return render(request, 'admin-panel/core/informasi_tambahan_form.html', context)


@login_required
@user_passes_test(is_staff_user)
@require_http_methods(["DELETE", "POST"])
def informasi_tambahan_delete(request, informasi_id):
    """Delete Informasi Tambahan"""
    informasi = get_object_or_404(InformasiTambahan, id=informasi_id)
    judul = informasi.judul
    informasi.delete()
    messages.success(request, f'Informasi Tambahan "{judul}" berhasil dihapus!')
    if is_htmx_request(request):
        return HttpResponseClientRefresh()
    return redirect('core:informasi_tambahan_list')


