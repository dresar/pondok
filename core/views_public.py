"""
Public Views untuk Website
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import models as db_models
from .models import (
    WebsiteSettings, FAQ, SejarahTimeline, VisiMisi, ProgramPendidikan, Program,
    Fasilitas, Ekstrakurikuler, JadwalHarian, Persyaratan, AlurPendaftaran,
    BiayaPendidikan, ContactPerson, Seragam, KMI, HeroSection, Statistik, Media,
    Dokumentasi, WhatsAppTemplate, Kontak, TenagaPengajar, BagianJabatan, InformasiTambahan
)
from .forms import KontakPublicForm
try:
    from blog.models import Pengumuman, Testimoni, BlogPost
except ImportError:
    Pengumuman = None
    Testimoni = None
    BlogPost = None


def home(request):
    """Halaman utama public website"""
    # Get all data from database with safe handling
    try:
        hero_images = HeroSection.objects.filter(is_active=True).exclude(image='').order_by('order', '-created_at')[:5]
    except Exception:
        hero_images = []
    
    try:
        faqs = FAQ.objects.filter(is_published=True).order_by('order', 'id')[:10]
    except Exception:
        faqs = []
    
    try:
        sejarah = SejarahTimeline.objects.prefetch_related('gambar').all().order_by('order', '-created_at')[:10]
    except Exception:
        sejarah = []
    
    try:
        visi_misi = VisiMisi.load()
    except Exception:
        visi_misi = None
    
    try:
        programs = ProgramPendidikan.objects.prefetch_related('gambar_program').all().order_by('order', 'nama')[:10]
    except Exception:
        programs = []
    
    # Program/Kegiatan (bukan Program Pendidikan)
    try:
        program_kegiatan = Program.objects.filter(status='published').order_by('order', '-is_featured', '-created_at')[:12]
    except Exception:
        program_kegiatan = []
    
    try:
        fasilitas = Fasilitas.objects.all().order_by('order', 'nama')[:12]
    except Exception:
        fasilitas = []
    
    try:
        ekstrakurikuler = Ekstrakurikuler.objects.prefetch_related('gambar_ekstrakurikuler').all().order_by('order', 'nama')[:10]
    except Exception:
        ekstrakurikuler = []
    
    try:
        jadwal_santri = list(JadwalHarian.objects.filter(kategori='santri').order_by('order', 'waktu'))
    except Exception as e:
        print(f"Error loading jadwal_santri: {e}")
        jadwal_santri = []
    
    try:
        jadwal_santriwati = list(JadwalHarian.objects.filter(kategori='santriwati').order_by('order', 'waktu'))
    except Exception as e:
        print(f"Error loading jadwal_santriwati: {e}")
        jadwal_santriwati = []
    
    try:
        persyaratan = Persyaratan.load()
    except Exception:
        persyaratan = None
    
    try:
        alur = AlurPendaftaran.load()
    except Exception:
        alur = None
    
    try:
        biaya_tahunan = BiayaPendidikan.objects.filter(tipe='tahunan').order_by('order')
    except Exception:
        biaya_tahunan = []
    
    try:
        biaya_bulanan = BiayaPendidikan.objects.filter(tipe='bulanan').order_by('order')
    except Exception:
        biaya_bulanan = []
    
    try:
        biaya_perlengkapan_putra = BiayaPendidikan.objects.filter(tipe='perlengkapan_putra').order_by('order')
    except Exception:
        biaya_perlengkapan_putra = []
    
    try:
        biaya_perlengkapan_putri = BiayaPendidikan.objects.filter(tipe='perlengkapan_putri').order_by('order')
    except Exception:
        biaya_perlengkapan_putri = []
    
    try:
        contact_persons = ContactPerson.objects.filter(is_active=True)[:5]
    except Exception:
        contact_persons = []
    
    try:
        seragam_santri = Seragam.objects.filter(kategori='santri').order_by('order', 'hari')
    except Exception:
        seragam_santri = []
    
    try:
        seragam_santriwati = Seragam.objects.filter(kategori='santriwati').order_by('order', 'hari')
    except Exception:
        seragam_santriwati = []
    
    try:
        kmi = KMI.load()
    except Exception:
        kmi = None
    
    try:
        if Pengumuman:
            pengumuman = Pengumuman.objects.filter(status='published').order_by('-is_penting', '-published_at', '-created_at')[:5]
        else:
            pengumuman = []
    except Exception:
        pengumuman = []
    
    try:
        if Testimoni:
            testimoni = Testimoni.objects.filter(is_published=True).order_by('-created_at')[:3]
        else:
            testimoni = []
    except Exception:
        testimoni = []
    
    try:
        if BlogPost:
            featured_blog = BlogPost.objects.filter(status='published', is_featured=True).order_by('-published_at', '-created_at')[:4]
        else:
            featured_blog = []
    except Exception:
        featured_blog = []
    
    try:
        statistik = Statistik.objects.filter(is_published=True).order_by('order', 'judul')[:6]
    except Exception:
        statistik = []
    
    # Media (Galeri & Video)
    try:
        from .models import Media
        import random
        gallery_media = Media.objects.filter(tipe='gallery', is_published=True).order_by('order', 'created_at')
        video_media = Media.objects.filter(tipe='video', is_published=True).order_by('order', 'created_at')
        # Gabungkan gallery dan video, lalu shuffle untuk random layout
        all_media = list(gallery_media) + list(video_media)
        random.shuffle(all_media)
    except Exception:
        gallery_media = []
        video_media = []
        all_media = []
    
    # Website Settings
    try:
        settings = WebsiteSettings.load()
    except Exception:
        settings = None
    
    # Social Media
    try:
        from .models import SocialMedia
        social_media = SocialMedia.objects.filter(is_active=True).order_by('order', 'platform')
    except Exception:
        social_media = []
    
    # Dokumentasi
    try:
        dokumentasi = Dokumentasi.objects.prefetch_related('gambar_dokumentasi').filter(is_published=True).order_by('order', '-tanggal_kegiatan', '-created_at')[:12]
    except Exception:
        dokumentasi = []
    
    # WhatsApp Templates
    try:
        # Hanya ambil template public untuk website
        whatsapp_templates = WhatsAppTemplate.objects.filter(tipe='public').order_by('order', 'kategori', 'nama')
        # Jika tidak ada template, buat dummy data untuk testing
        if not whatsapp_templates.exists():
            from django.utils.functional import SimpleLazyObject
            class DummyTemplate:
                def __init__(self, id, nama, pesan, kategori_display='Umum'):
                    self.id = id
                    self.nama = nama
                    self.pesan = pesan
                    self.kategori_display = kategori_display
                def get_kategori_display(self):
                    return self.kategori_display
            whatsapp_templates = [
                DummyTemplate(1, 'Pertanyaan Umum', 'Halo, saya ingin bertanya tentang pendaftaran santri baru. Apakah masih dibuka?', 'Umum'),
                DummyTemplate(2, 'Informasi Biaya', 'Halo, saya ingin mengetahui informasi lengkap tentang biaya pendaftaran dan biaya bulanan. Terima kasih.', 'Informasi'),
                DummyTemplate(3, 'Jadwal Pendaftaran', 'Halo, saya ingin mengetahui jadwal pendaftaran santri baru dan persyaratan yang diperlukan.', 'Jadwal'),
                DummyTemplate(4, 'Kunjungan Pesantren', 'Halo, saya ingin mengunjungi pesantren untuk melihat fasilitas dan bertemu dengan pengurus. Kapan waktu yang tepat?', 'Kunjungan'),
            ]
    except Exception:
        whatsapp_templates = []
    
    # Tenaga Pengajar (untuk slide di home, maksimal 5, sesuai urutan)
    # Prioritas: featured dulu, lalu yang lain, diurutkan berdasarkan order
    try:
        from django.db.models import Case, When, IntegerField
        featured_pengajar = TenagaPengajar.objects.filter(
            is_published=True,
            is_featured=True
        ).select_related('bagian_jabatan').order_by('order', 'bagian_jabatan__order', 'nama_lengkap')[:6]
    except Exception:
        featured_pengajar = []
    
    # Informasi Tambahan
    try:
        informasi_tambahan = InformasiTambahan.objects.filter(is_published=True).order_by('order', 'judul')
    except Exception:
        informasi_tambahan = []
    
    context = {
        'hero_images': hero_images,
        'faqs': faqs,
        'sejarah': sejarah,
        'visi_misi': visi_misi,
        'programs': programs,
        'program_kegiatan': program_kegiatan,
        'fasilitas': fasilitas,
        'ekstrakurikuler': ekstrakurikuler,
        'jadwal_santri': jadwal_santri,
        'jadwal_santriwati': jadwal_santriwati,
        'persyaratan': persyaratan,
        'alur': alur,
        'biaya_tahunan': biaya_tahunan,
        'biaya_bulanan': biaya_bulanan,
        'biaya_perlengkapan_putra': biaya_perlengkapan_putra,
        'biaya_perlengkapan_putri': biaya_perlengkapan_putri,
        'contact_persons': contact_persons,
        'seragam_santri': seragam_santri,
        'seragam_santriwati': seragam_santriwati,
        'kmi': kmi,
        'pengumuman': pengumuman,
        'testimoni': testimoni,
        'statistik': statistik,
        'featured_blog': featured_blog,
        'gallery_media': gallery_media,
        'video_media': video_media,
        'all_media': all_media,
        'settings': settings,
        'social_media': social_media,
        'dokumentasi': dokumentasi,
        'whatsapp_templates': whatsapp_templates,
        'featured_pengajar': featured_pengajar,
        'informasi_tambahan': informasi_tambahan,
    }
    
    # Handle kontak form submission
    kontak_form = KontakPublicForm()
    if request.method == 'POST' and 'kontak_submit' in request.POST:
        kontak_form = KontakPublicForm(request.POST)
        if kontak_form.is_valid():
            kontak = kontak_form.save(commit=False)
            kontak.status = 'baru'
            kontak.save()
            messages.success(request, 'Terima kasih! Pesan Anda telah terkirim. Kami akan segera menghubungi Anda.')
            return redirect('public:home')
        else:
            messages.error(request, 'Mohon lengkapi semua field yang wajib diisi.')
    
    # Add kontak_form to context
    context['kontak_form'] = kontak_form
    
    return render(request, 'public/home.html', context)


def blog_list(request):
    """Halaman list semua blog/artikel public"""
    try:
        if BlogPost:
            # Get all published blog posts
            blog_posts = BlogPost.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags').order_by('-published_at', '-created_at')
            
            # Search functionality
            search_query = request.GET.get('search', '')
            if search_query:
                from django.db.models import Q
                blog_posts = blog_posts.filter(
                    Q(title__icontains=search_query) |
                    Q(content__icontains=search_query) |
                    Q(excerpt__icontains=search_query)
                )
            
            # Category filter
            category_slug = request.GET.get('category', '')
            if category_slug:
                try:
                    from blog.models import Category
                    category = Category.objects.get(slug=category_slug)
                    blog_posts = blog_posts.filter(category=category)
                except:
                    pass
            
            # Pagination
            from django.core.paginator import Paginator
            paginator = Paginator(blog_posts, 12)  # 12 posts per page
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            
            # Get categories for filter
            try:
                from blog.models import Category
                categories = Category.objects.all().order_by('order', 'name')
            except:
                categories = []
        else:
            page_obj = None
            categories = []
            search_query = ''
            category_slug = ''
    except Exception as e:
        page_obj = None
        categories = []
        search_query = ''
        category_slug = ''
    
    try:
        settings = WebsiteSettings.load()
    except:
        settings = None
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_slug': category_slug,
        'settings': settings,
    }
    
    # HTMX dan non-HTMX menggunakan template yang sama
    # HTMX akan swap hanya bagian #blog-content-container
    return render(request, 'public/blog_list.html', context)


def blog_detail(request, slug):
    """Halaman detail blog/artikel public"""
    try:
        if BlogPost:
            blog_post = BlogPost.objects.filter(status='published', slug=slug).select_related('author', 'category').prefetch_related('tags').first()
            
            if not blog_post:
                from django.http import Http404
                raise Http404("Blog post tidak ditemukan")
            
            # Increment views count
            blog_post.increment_views()
            
            # Get related posts (same category, exclude current)
            related_posts = BlogPost.objects.filter(
                status='published',
                category=blog_post.category
            ).exclude(id=blog_post.id).order_by('-published_at', '-created_at')[:3]
            
            # Get blog images if any
            try:
                images = blog_post.images.all().order_by('order')
            except:
                images = []
        else:
            from django.http import Http404
            raise Http404("Blog tidak tersedia")
    except Exception as e:
        from django.http import Http404
        raise Http404("Blog post tidak ditemukan")
    
    try:
        settings = WebsiteSettings.load()
    except:
        settings = None
    
    context = {
        'blog_post': blog_post,
        'related_posts': related_posts,
        'images': images,
        'settings': settings,
    }
    
    return render(request, 'public/blog_detail.html', context)


def tenaga_pengajar_list(request):
    """Halaman lengkap semua tenaga pengajar"""
    try:
        # Get all published tenaga pengajar
        pengajar_list = TenagaPengajar.objects.filter(
            is_published=True
        ).select_related('bagian_jabatan')
        
        # Filter by bagian/jabatan
        bagian_id = request.GET.get('bagian', '')
        if bagian_id:
            pengajar_list = pengajar_list.filter(bagian_jabatan_id=bagian_id)
        
        # Filter by jenis kelamin
        jenis_kelamin = request.GET.get('jenis_kelamin', '')
        if jenis_kelamin:
            pengajar_list = pengajar_list.filter(jenis_kelamin=jenis_kelamin)
        
        # Search
        search_query = request.GET.get('search', '')
        if search_query:
            from django.db.models import Q
            pengajar_list = pengajar_list.filter(
                Q(nama_lengkap__icontains=search_query) |
                Q(nama_panggilan__icontains=search_query) |
                Q(bidang_keahlian__icontains=search_query) |
                Q(mata_pelajaran__icontains=search_query) |
                Q(bagian_jabatan__nama__icontains=search_query)
            )
        
        # Order setelah filter
        pengajar_list = pengajar_list.order_by('bagian_jabatan__order', 'order', 'nama_lengkap')
        
        # Get all bagian for filter
        bagian_list = BagianJabatan.objects.filter(is_active=True).order_by('order', 'nama')
        
        # Convert to list untuk memastikan bisa diiterasi
        pengajar_list = list(pengajar_list)
        
        # Group by bagian/jabatan
        pengajar_by_bagian = {}
        for pengajar in pengajar_list:
            bagian_nama = pengajar.bagian_jabatan.nama if pengajar.bagian_jabatan else 'Lainnya'
            if bagian_nama not in pengajar_by_bagian:
                pengajar_by_bagian[bagian_nama] = []
            pengajar_by_bagian[bagian_nama].append(pengajar)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        pengajar_list = []
        bagian_list = []
        pengajar_by_bagian = {}
        search_query = ''
        bagian_id = ''
        jenis_kelamin = ''
    
    try:
        settings = WebsiteSettings.load()
    except:
        settings = None
    
    context = {
        'pengajar_list': pengajar_list,  # Sudah di-convert ke list di atas
        'pengajar_by_bagian': pengajar_by_bagian,
        'bagian_list': bagian_list,
        'search_query': search_query,
        'bagian_filter': bagian_id,
        'jenis_kelamin_filter': jenis_kelamin,
        'settings': settings,
    }
    
    # Jika request AJAX, return JSON dengan HTML sederhana
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        
        # Generate HTML sederhana langsung dari context
        html_parts = []
        if pengajar_by_bagian:
            html_parts.append('<div class="space-y-8">')
            for bagian_nama, p_list in pengajar_by_bagian.items():
                html_parts.append(f'<div><h2 class="text-xl md:text-2xl font-bold text-gray-900 mb-4 flex items-center"><i class="fas fa-users mr-2 text-green-600"></i>{bagian_nama}</h2><div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-4">')
                for p in p_list:
                    foto_html = f'<img src="{p.foto.url}" alt="{p.nama_lengkap}" class="w-full h-48 md:h-56 object-cover">' if p.foto else '<div class="w-full h-48 md:h-56 bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center"><i class="fas fa-user text-6xl md:text-7xl text-white/50"></i></div>'
                    badge_color = 'bg-blue-600' if p.jenis_kelamin == 'L' else 'bg-pink-600'
                    nama_panggilan_html = f'<p class="text-xs md:text-sm text-gray-600 mb-2">{p.nama_panggilan}</p>' if p.nama_panggilan else ''
                    bidang_html = f'<p class="text-xs text-gray-600 line-clamp-2"><i class="fas fa-graduation-cap mr-1 text-green-600"></i>{p.bidang_keahlian[:80]}</p>' if p.bidang_keahlian else ''
                    html_parts.append(f'''<div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow cursor-pointer border border-gray-100" onclick="openPengajarModal({p.id})" style="opacity: 1 !important; visibility: visible !important;">
                        <div class="relative">{foto_html}
                            <div class="absolute top-2 right-2 z-10"><span class="px-2 py-1 text-xs font-semibold rounded-full {badge_color} text-white">{p.get_jenis_kelamin_display_short()}</span></div>
                        </div>
                        <div class="p-3 md:p-4 bg-white">
                            <h3 class="font-bold text-gray-900 text-sm md:text-base mb-1">{p.nama_lengkap}</h3>
                            {nama_panggilan_html}
                            {bidang_html}
                            <div class="mt-2 pt-2 border-t border-gray-100"><span class="text-xs md:text-sm text-green-600 hover:text-green-700 font-semibold flex items-center"><span>Lihat Detail</span><i class="fas fa-arrow-right ml-2"></i></span></div>
                        </div>
                    </div>''')
                html_parts.append('</div></div>')
            html_parts.append('</div>')
        elif pengajar_list:
            html_parts.append('<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-4">')
            for p in pengajar_list:
                foto_html = f'<img src="{p.foto.url}" alt="{p.nama_lengkap}" class="w-full h-48 md:h-56 object-cover">' if p.foto else '<div class="w-full h-48 md:h-56 bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center"><i class="fas fa-user text-6xl md:text-7xl text-white/50"></i></div>'
                badge_color = 'bg-blue-600' if p.jenis_kelamin == 'L' else 'bg-pink-600'
                nama_panggilan_html = f'<p class="text-xs md:text-sm text-gray-600 mb-2">{p.nama_panggilan}</p>' if p.nama_panggilan else ''
                bidang_html = f'<p class="text-xs text-gray-600 line-clamp-2"><i class="fas fa-graduation-cap mr-1 text-green-600"></i>{p.bidang_keahlian[:80]}</p>' if p.bidang_keahlian else ''
                html_parts.append(f'''<div class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow cursor-pointer border border-gray-100" onclick="openPengajarModal({p.id})" style="opacity: 1 !important; visibility: visible !important;">
                    <div class="relative">{foto_html}
                        <div class="absolute top-2 right-2 z-10"><span class="px-2 py-1 text-xs font-semibold rounded-full {badge_color} text-white">{p.get_jenis_kelamin_display_short()}</span></div>
                    </div>
                    <div class="p-3 md:p-4 bg-white">
                        <h3 class="font-bold text-gray-900 text-sm md:text-base mb-1">{p.nama_lengkap}</h3>
                        {nama_panggilan_html}
                        {bidang_html}
                        <div class="mt-2 pt-2 border-t border-gray-100"><span class="text-xs md:text-sm text-green-600 hover:text-green-700 font-semibold flex items-center"><span>Lihat Detail</span><i class="fas fa-arrow-right ml-2"></i></span></div>
                    </div>
                </div>''')
            html_parts.append('</div>')
        else:
            html_parts.append('<div class="text-center py-12 text-gray-500"><i class="fas fa-search text-6xl mb-4 text-gray-300"></i><p class="text-lg font-semibold mb-2">Data tidak ditemukan</p><p class="text-sm text-gray-400">Coba ubah filter atau kata kunci pencarian</p></div>')
        
        return JsonResponse({'html': ''.join(html_parts)})
    
    return render(request, 'public/tenaga_pengajar_list.html', context)


def tenaga_pengajar_detail_json(request, pengajar_id):
    """JSON endpoint untuk detail tenaga pengajar (untuk modal)"""
    from django.http import JsonResponse
    
    try:
        pengajar = TenagaPengajar.objects.select_related('bagian_jabatan').get(
            id=pengajar_id,
            is_published=True
        )
        
        data = {
            'id': pengajar.id,
            'nama_lengkap': pengajar.nama_lengkap,
            'nama_panggilan': pengajar.nama_panggilan or '',
            'jenis_kelamin': pengajar.get_jenis_kelamin_display(),
            'jenis_kelamin_short': pengajar.get_jenis_kelamin_display_short(),
            'foto': pengajar.foto.url if pengajar.foto else '',
            'bagian_jabatan': pengajar.bagian_jabatan.nama if pengajar.bagian_jabatan else '',
            'tempat_lahir': pengajar.tempat_lahir or '',
            'tanggal_lahir': pengajar.tanggal_lahir.strftime('%d %B %Y') if pengajar.tanggal_lahir else '',
            'alamat': pengajar.alamat or '',
            'no_hp': pengajar.no_hp or '',
            'email': pengajar.email or '',
            'pendidikan_terakhir': pengajar.pendidikan_terakhir or '',
            'universitas': pengajar.universitas or '',
            'tahun_lulus': pengajar.tahun_lulus or '',
            'bidang_keahlian': pengajar.bidang_keahlian or '',
            'mata_pelajaran': pengajar.mata_pelajaran or '',
            'pengalaman_mengajar': pengajar.pengalaman_mengajar or '',
            'prestasi': pengajar.prestasi or '',
            'riwayat_pendidikan': pengajar.riwayat_pendidikan or '',
            'organisasi': pengajar.organisasi or '',
            'karya_tulis': pengajar.karya_tulis or '',
            'motto': pengajar.motto or '',
            'whatsapp': pengajar.whatsapp or '',
            'facebook': pengajar.facebook or '',
            'instagram': pengajar.instagram or '',
            'twitter': pengajar.twitter or '',
            'linkedin': pengajar.linkedin or '',
            'youtube': pengajar.youtube or '',
            'tiktok': pengajar.tiktok or '',
        }
        
        return JsonResponse(data)
    except TenagaPengajar.DoesNotExist:
        return JsonResponse({'error': 'Tenaga pengajar tidak ditemukan'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Error Handlers
def error_404(request, exception):
    # Skip error handler untuk static/media files
    if request.path.startswith('/static/') or request.path.startswith('/media/'):
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound('File not found')
    return render(request, '404.html', status=404)

def error_500(request):
    # Skip error handler untuk static/media files - return plain text
    if request.path.startswith('/static/') or request.path.startswith('/media/'):
        from django.http import HttpResponseServerError
        return HttpResponseServerError('Internal Server Error')
    try:
        return render(request, '500.html', status=500)
    except Exception:
        # Fallback jika template error
        from django.http import HttpResponseServerError
        return HttpResponseServerError('Internal Server Error')

def error_403(request, exception):
    if request.path.startswith('/static/') or request.path.startswith('/media/'):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden('Forbidden')
    return render(request, '403.html', status=403)

def error_400(request, exception):
    if request.path.startswith('/static/') or request.path.startswith('/media/'):
        from django.http import HttpResponseBadRequest
        return HttpResponseBadRequest('Bad Request')
    return render(request, '400.html', status=400)

