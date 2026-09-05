"""
Models untuk Core App - Settings Website
"""
from django.db import models
from django.utils.text import slugify


class WebsiteSettings(models.Model):
    """Model untuk pengaturan website (Singleton)"""
    nama_pondok = models.CharField(max_length=200, default='Pondok Pesantren', verbose_name='Nama Pondok')
    arabic_name = models.CharField(max_length=500, blank=True, verbose_name='Nama Arab')
    alamat = models.TextField(default='', verbose_name='Alamat')
    logo = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name='Logo')
    header_mobile_image = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name='Header Mobile (Kop Surat)', help_text='Gambar header khusus untuk tampilan mobile. Ukuran disarankan: lebar 800-1200px, tinggi 80-100px. Aspect ratio: 10:1 atau 12:1')
    header_mobile_height = models.PositiveIntegerField(default=80, verbose_name='Tinggi Header Mobile (px)', help_text='Tinggi maksimal header mobile dalam pixel. Default: 80px. Disarankan: 60-120px')
    no_telepon = models.CharField(max_length=20, blank=True, verbose_name='No. Telepon')
    email = models.EmailField(blank=True, verbose_name='Email')
    website = models.URLField(blank=True, verbose_name='Website')
    facebook = models.URLField(blank=True, verbose_name='Facebook')
    instagram = models.URLField(blank=True, verbose_name='Instagram')
    twitter = models.URLField(blank=True, verbose_name='Twitter')
    tiktok = models.URLField(blank=True, verbose_name='TikTok')
    hero_title = models.CharField(max_length=200, default='Pendaftaran Santri Baru', verbose_name='Hero Title')
    hero_subtitle = models.CharField(max_length=200, default='2025/2026', verbose_name='Hero Subtitle')
    hero_tagline = models.CharField(max_length=300, default='Membentuk Generasi Unggul yang Berkarakter Islami', verbose_name='Hero Tagline')
    hero_cta_primary_text = models.CharField(max_length=100, default='DAFTAR SEKARANG!', verbose_name='CTA Primary Text')
    hero_cta_primary_link = models.URLField(blank=True, verbose_name='CTA Primary Link')
    hero_cta_secondary_text = models.CharField(max_length=100, default='ALUR PENDAFTARAN', verbose_name='CTA Secondary Text')
    hero_cta_secondary_link = models.URLField(blank=True, verbose_name='CTA Secondary Link')
    lokasi_pendaftaran = models.TextField(blank=True, verbose_name='Lokasi Pendaftaran')
    google_maps_link = models.URLField(blank=True, verbose_name='Google Maps Link')
    google_maps_embed_code = models.TextField(blank=True, verbose_name='Google Maps Embed Code', help_text='Paste kode iframe dari Google Maps Embed API')
    qr_code_image = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name='QR Code')
    deskripsi = models.TextField(blank=True, verbose_name='Deskripsi Pondok')
    favicon = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name='Favicon')
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='Meta Title (SEO)')
    meta_description = models.TextField(max_length=300, blank=True, verbose_name='Meta Description (SEO)')
    meta_keywords = models.CharField(max_length=500, blank=True, verbose_name='Meta Keywords (SEO)')
    # Maintenance Mode
    maintenance_mode = models.BooleanField(default=False, verbose_name='Mode Maintenance', help_text='Aktifkan untuk menampilkan halaman maintenance')
    maintenance_message = models.TextField(blank=True, default='Website sedang dalam perawatan. Kami akan kembali segera.', verbose_name='Pesan Maintenance', help_text='Pesan yang akan ditampilkan saat maintenance mode aktif')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Pengaturan Website'
        verbose_name_plural = 'Pengaturan Website'
    
    def __str__(self):
        return self.nama_pondok
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj




class FAQ(models.Model):
    """Model untuk FAQ"""
    pertanyaan = models.CharField(max_length=500, verbose_name='Pertanyaan')
    jawaban = models.TextField(verbose_name='Jawaban')
    kategori = models.CharField(max_length=100, blank=True, verbose_name='Kategori')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    is_published = models.BooleanField(default=True, verbose_name='Published')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order', 'kategori', 'pertanyaan']
    
    def __str__(self):
        return self.pertanyaan
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = FAQ.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class Program(models.Model):
    """Model untuk Program/Kegiatan"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    nama = models.CharField(max_length=200, verbose_name='Nama Program')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Slug')
    deskripsi = models.TextField(verbose_name='Deskripsi')
    gambar = models.ImageField(upload_to='program/%Y/%m/%d/', blank=True, null=True, verbose_name='Gambar')
    tanggal_mulai = models.DateField(null=True, blank=True, verbose_name='Tanggal Mulai')
    tanggal_selesai = models.DateField(null=True, blank=True, verbose_name='Tanggal Selesai')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Status')
    is_featured = models.BooleanField(default=False, verbose_name='Unggulan')
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='Meta Title')
    meta_description = models.TextField(max_length=300, blank=True, verbose_name='Meta Description')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Program'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        if not self.meta_title:
            self.meta_title = self.nama
        if not self.order:
            max_order = Program.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class WhatsAppTemplateKategori(models.Model):
    """Model untuk Kategori Template WhatsApp"""
    nama = models.CharField(max_length=100, unique=True, verbose_name='Nama Kategori')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Slug')
    deskripsi = models.TextField(blank=True, verbose_name='Deskripsi')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Kategori Template WhatsApp'
        verbose_name_plural = 'Kategori Template WhatsApp'
        ordering = ['order', 'nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)


class WhatsAppTemplate(models.Model):
    """Model untuk Template WhatsApp"""
    TIPE_CHOICES = [
        ('public', 'Public (Website)'),
        ('system', 'System (Admin Panel)'),
    ]
    
    nama = models.CharField(max_length=200, verbose_name='Nama Template')
    kategori = models.ForeignKey('WhatsAppTemplateKategori', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Kategori', related_name='templates')
    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES, default='public', verbose_name='Tipe', help_text='Public: untuk website, System: untuk admin panel')
    pesan = models.TextField(verbose_name='Pesan Template')
    variabel = models.CharField(max_length=500, blank=True, verbose_name='Variabel', help_text='Contoh: {nama}, {tanggal}, {link} - pisahkan dengan koma')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Template WhatsApp'
        verbose_name_plural = 'Template WhatsApp'
        ordering = ['order', 'kategori', 'nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = WhatsAppTemplate.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)
    
    def get_variabel_list(self):
        """Mengembalikan list variabel yang tersedia"""
        if self.variabel:
            return [v.strip() for v in self.variabel.split(',')]
        return []
    
    def render_pesan(self, **kwargs):
        """Render pesan dengan mengganti variabel"""
        pesan = self.pesan
        for key, value in kwargs.items():
            # Replace semua variabel dengan format {key}
            # Gunakan str(value) untuk memastikan tidak ada error
            replacement = str(value) if value is not None else ''
            pesan = pesan.replace(f'{{{key}}}', replacement)
        return pesan


class Kontak(models.Model):
    """Model untuk Kontak/Inquiry dari Website"""
    STATUS_CHOICES = [
        ('baru', 'Baru'),
        ('dibaca', 'Dibaca'),
        ('dibalas', 'Dibalas'),
        ('selesai', 'Selesai'),
    ]
    
    nama = models.CharField(max_length=200, verbose_name='Nama')
    email = models.EmailField(verbose_name='Email')
    no_hp = models.CharField(max_length=20, blank=True, verbose_name='No. HP')
    subjek = models.CharField(max_length=200, verbose_name='Subjek')
    pesan = models.TextField(verbose_name='Pesan')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='baru', verbose_name='Status')
    balasan = models.TextField(blank=True, verbose_name='Balasan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Kontak'
        verbose_name_plural = 'Kontak'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nama} - {self.subjek}"
    
    def get_whatsapp_link(self):
        """Generate WhatsApp link untuk balasan"""
        if self.no_hp:
            # Hapus karakter non-digit
            nomor = ''.join(filter(str.isdigit, self.no_hp.replace('+', '').replace(' ', '')))
            if nomor:
                pesan = f"Halo {self.nama}, terima kasih telah menghubungi kami. {self.balasan or 'Kami akan segera menindaklanjuti pesan Anda.'}"
                from urllib.parse import quote
                pesan_encoded = quote(pesan)
                return f"https://wa.me/{nomor}?text={pesan_encoded}"
        return None


class HeroSection(models.Model):
    """Model untuk Hero Section Slideshow"""
    title = models.CharField(max_length=200, blank=True, verbose_name='Judul')
    subtitle = models.CharField(max_length=200, blank=True, verbose_name='Sub Judul')
    image = models.ImageField(upload_to='hero/%Y/%m/%d/', blank=True, null=True, verbose_name='Gambar', help_text='Gambar dapat dipilih dari gallery atau diupload manual')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Section'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title or f'Hero {self.id}'
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = HeroSection.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class SejarahTimeline(models.Model):
    """Model untuk Timeline Sejarah"""
    judul = models.CharField(max_length=200, verbose_name='Judul')
    icon = models.CharField(max_length=100, default='fas fa-history', verbose_name='Icon (Font Awesome)')
    deskripsi = models.TextField(verbose_name='Deskripsi')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Timeline Sejarah'
        verbose_name_plural = 'Timeline Sejarah'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.judul
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = SejarahTimeline.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class SejarahTimelineImage(models.Model):
    """Model untuk Gambar Timeline Sejarah"""
    timeline = models.ForeignKey(SejarahTimeline, on_delete=models.CASCADE, related_name='gambar', verbose_name='Timeline')
    gambar = models.ImageField(upload_to='sejarah/%Y/%m/%d/', verbose_name='Gambar')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Gambar Timeline Sejarah'
        verbose_name_plural = 'Gambar Timeline Sejarah'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"Gambar untuk {self.timeline.judul}"


class VisiMisi(models.Model):
    """Model untuk Visi dan Misi"""
    visi = models.TextField(verbose_name='Visi')
    misi = models.TextField(verbose_name='Misi', help_text='Daftar misi menggunakan format HTML')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Visi Misi'
        verbose_name_plural = 'Visi Misi'
    
    def __str__(self):
        return 'Visi Misi'
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ProgramPendidikan(models.Model):
    """Model untuk Program Pendidikan (SDIT, MDTA, MTs, MA, dll)"""
    nama = models.CharField(max_length=200, verbose_name='Nama Program')
    akreditasi = models.CharField(max_length=50, blank=True, verbose_name='Akreditasi')
    icon = models.CharField(max_length=100, default='fas fa-school', verbose_name='Icon')
    gambar = models.ImageField(upload_to='program-pendidikan/%Y/%m/%d/', blank=True, null=True, verbose_name='Gambar Utama')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Program Pendidikan'
        verbose_name_plural = 'Program Pendidikan'
        ordering = ['order', 'nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = ProgramPendidikan.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)
    
    def get_images(self):
        """Mendapatkan semua gambar program (maksimal 3)"""
        return self.gambar_program.all().order_by('order')[:3]


class ProgramPendidikanImage(models.Model):
    """Model untuk Gambar Program Pendidikan (maksimal 3 per program)"""
    program = models.ForeignKey(ProgramPendidikan, on_delete=models.CASCADE, related_name='gambar_program', verbose_name='Program Pendidikan')
    gambar = models.ImageField(upload_to='program-pendidikan/gallery/%Y/%m/%d/', verbose_name='Gambar')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Alt Text')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Gambar Program Pendidikan'
        verbose_name_plural = 'Gambar Program Pendidikan'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Gambar untuk {self.program.nama} - {self.order}"


class Fasilitas(models.Model):
    """Model untuk Fasilitas Pesantren"""
    nama = models.CharField(max_length=200, verbose_name='Nama Fasilitas')
    icon = models.CharField(max_length=100, verbose_name='Icon (Font Awesome)')
    gambar = models.ImageField(upload_to='fasilitas/%Y/%m/%d/', blank=True, null=True, verbose_name='Gambar')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Fasilitas'
        verbose_name_plural = 'Fasilitas'
        ordering = ['order', 'nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = Fasilitas.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class Ekstrakurikuler(models.Model):
    """Model untuk Ekstrakurikuler"""
    nama = models.CharField(max_length=200, verbose_name='Nama Ekstrakurikuler')
    icon = models.CharField(max_length=100, verbose_name='Icon (Font Awesome)')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Ekstrakurikuler'
        verbose_name_plural = 'Ekstrakurikuler'
        ordering = ['order', 'nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = Ekstrakurikuler.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class EkstrakurikulerImage(models.Model):
    """Model untuk gambar ekstrakurikuler"""
    ekstrakurikuler = models.ForeignKey(Ekstrakurikuler, on_delete=models.CASCADE, related_name='gambar_ekstrakurikuler', verbose_name='Ekstrakurikuler')
    gambar = models.ImageField(upload_to='ekstrakurikuler/%Y/%m/%d/', verbose_name='Gambar')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Alt Text (Deskripsi Gambar)')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Gambar Ekstrakurikuler'
        verbose_name_plural = 'Gambar Ekstrakurikuler'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.ekstrakurikuler.nama} - Gambar {self.order}"


class Dokumentasi(models.Model):
    """Model untuk Dokumentasi Rekam Jejak Kegiatan Pesantren"""
    KATEGORI_CHOICES = [
        ('kegiatan', 'Kegiatan'),
        ('acara', 'Acara'),
        ('pembelajaran', 'Pembelajaran'),
        ('ekstrakurikuler', 'Ekstrakurikuler'),
        ('prestasi', 'Prestasi'),
        ('lainnya', 'Lainnya'),
    ]
    
    judul = models.CharField(max_length=200, verbose_name='Judul Dokumentasi')
    deskripsi = models.TextField(blank=True, verbose_name='Deskripsi')
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, default='kegiatan', verbose_name='Kategori')
    tanggal_kegiatan = models.DateField(null=True, blank=True, verbose_name='Tanggal Kegiatan')
    lokasi = models.CharField(max_length=200, blank=True, verbose_name='Lokasi')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    is_published = models.BooleanField(default=True, verbose_name='Published')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Dokumentasi'
        verbose_name_plural = 'Dokumentasi'
        ordering = ['order', '-tanggal_kegiatan', '-created_at']
    
    def __str__(self):
        return self.judul
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = Dokumentasi.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class DokumentasiImage(models.Model):
    """Model untuk gambar dokumentasi (maksimal 10 gambar per dokumentasi)"""
    dokumentasi = models.ForeignKey(Dokumentasi, on_delete=models.CASCADE, related_name='gambar_dokumentasi', verbose_name='Dokumentasi')
    gambar = models.ImageField(upload_to='dokumentasi/%Y/%m/%d/', verbose_name='Gambar')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Alt Text (Deskripsi Gambar)')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Gambar Dokumentasi'
        verbose_name_plural = 'Gambar Dokumentasi'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.dokumentasi.judul} - Gambar {self.order}"


class JadwalHarian(models.Model):
    """Model untuk Jadwal Harian Santri"""
    KATEGORI_CHOICES = [
        ('santri', 'Santri (Putra)'),
        ('santriwati', 'Santriwati (Putri)'),
    ]
    
    waktu = models.CharField(max_length=50, verbose_name='Waktu (contoh: 04.00-06.00)')
    judul = models.CharField(max_length=200, verbose_name='Judul Aktivitas')
    deskripsi = models.TextField(verbose_name='Deskripsi')
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='santri', verbose_name='Kategori')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Jadwal Harian'
        verbose_name_plural = 'Jadwal Harian'
        ordering = ['order', 'waktu']
    
    def __str__(self):
        return f"{self.waktu} - {self.judul}"
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = JadwalHarian.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class Persyaratan(models.Model):
    """Model untuk Persyaratan Penerimaan (Singleton)"""
    persyaratan_santri = models.TextField(blank=True, verbose_name='Persyaratan Santri (Putra)', help_text='Gunakan editor untuk membuat daftar persyaratan dengan format HTML')
    persyaratan_santriwati = models.TextField(blank=True, verbose_name='Persyaratan Santriwati (Putri)', help_text='Gunakan editor untuk membuat daftar persyaratan dengan format HTML')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Persyaratan Penerimaan'
        verbose_name_plural = 'Persyaratan Penerimaan'
    
    def __str__(self):
        return 'Persyaratan Penerimaan'
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class AlurPendaftaran(models.Model):
    """Model untuk Alur Pendaftaran (Singleton)"""
    gambar_utama = models.ImageField(upload_to='alur_pendaftaran/', blank=True, null=True, verbose_name='Gambar Utama Alur Pendaftaran')
    alur_pendaftaran = models.TextField(blank=True, verbose_name='Alur Pendaftaran', help_text='Gunakan editor untuk membuat alur pendaftaran dengan format HTML')
    tahapan_tes = models.TextField(blank=True, verbose_name='Tahapan Tes Seleksi', help_text='Gunakan editor untuk membuat tahapan tes seleksi dengan format HTML')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Alur Pendaftaran'
        verbose_name_plural = 'Alur Pendaftaran'
    
    def __str__(self):
        return 'Alur Pendaftaran'
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class BiayaPendidikan(models.Model):
    """Model untuk Biaya Pendidikan"""
    TIPE_CHOICES = [
        ('tahunan', 'Biaya Tahunan'),
        ('bulanan', 'Biaya Bulanan'),
        ('perlengkapan_putra', 'Perlengkapan Putra'),
        ('perlengkapan_putri', 'Perlengkapan Putri'),
    ]
    
    tipe = models.CharField(max_length=50, choices=TIPE_CHOICES, verbose_name='Tipe Biaya')
    nama = models.CharField(max_length=200, verbose_name='Nama Biaya')
    jumlah = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Jumlah (Rp)')
    keterangan = models.CharField(max_length=200, blank=True, verbose_name='Keterangan')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Biaya Pendidikan'
        verbose_name_plural = 'Biaya Pendidikan'
        ordering = ['tipe', 'order']
    
    def __str__(self):
        return f"{self.get_tipe_display()} - {self.nama}"


class ContactPerson(models.Model):
    """Model untuk Contact Person Panitia Pendaftaran"""
    nama = models.CharField(max_length=200, verbose_name='Nama')
    foto = models.ImageField(upload_to='contact/%Y/%m/%d/', blank=True, null=True, verbose_name='Foto')
    no_hp = models.CharField(max_length=20, verbose_name='No. HP')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Contact Person'
        verbose_name_plural = 'Contact Person'
        ordering = ['order', 'nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = ContactPerson.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)
    
    def get_whatsapp_number(self):
        """Get WhatsApp number without + and spaces"""
        return ''.join(filter(str.isdigit, self.no_hp.replace('+', '').replace(' ', '')))


class SocialMedia(models.Model):
    """Model untuk Social Media Links"""
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
    ]
    
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, verbose_name='Platform')
    username = models.CharField(max_length=200, verbose_name='Username')
    url = models.URLField(verbose_name='URL')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'
        ordering = ['order', 'platform']
    
    def __str__(self):
        return f"{self.get_platform_display()} - {self.username}"
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = SocialMedia.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class Seragam(models.Model):
    """Model untuk Pakaian/Seragam"""
    KATEGORI_CHOICES = [
        ('santri', 'Santri (Putra)'),
        ('santriwati', 'Santriwati (Putri)'),
    ]
    hari = models.CharField(max_length=50, verbose_name='Hari')
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='santri', verbose_name='Kategori')
    seragam_putra = models.CharField(max_length=200, blank=True, verbose_name='Seragam Putra')
    seragam_putri = models.CharField(max_length=200, blank=True, verbose_name='Seragam Putri')
    seragam = models.CharField(max_length=200, default='', blank=True, verbose_name='Seragam', help_text='Isi seragam sesuai kategori')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Seragam'
        verbose_name_plural = 'Seragam'
        ordering = ['kategori', 'order', 'hari']
    
    def __str__(self):
        return f"{self.hari} - {self.get_kategori_display()}"


class KMI(models.Model):
    """Model untuk KMI (Kulliyatu-l-Mu'allimin wal Mu'alliat Al-Islamiyah)"""
    visi_kmi = models.TextField(blank=True, verbose_name='Visi KMI', help_text='Gunakan editor untuk membuat visi KMI dengan format HTML')
    profil_kmi = models.TextField(blank=True, verbose_name='Profil KMI', help_text='Gunakan editor untuk membuat profil KMI dengan format HTML')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'KMI'
        verbose_name_plural = 'KMI'
    
    def __str__(self):
        return 'KMI'
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Statistik(models.Model):
    """Model untuk Statistik dan Prestasi Pesantren"""
    judul = models.CharField(max_length=200, verbose_name='Judul Statistik')
    nilai = models.CharField(max_length=100, verbose_name='Nilai/Angka', help_text='Contoh: 1000, 500+, 95%')
    icon = models.CharField(max_length=100, default='fas fa-chart-bar', verbose_name='Icon (Font Awesome)')
    deskripsi = models.CharField(max_length=300, blank=True, verbose_name='Deskripsi Singkat')
    warna = models.CharField(max_length=50, default='green', choices=[
        ('green', 'Hijau'),
        ('blue', 'Biru'),
        ('purple', 'Ungu'),
        ('orange', 'Oranye'),
        ('red', 'Merah'),
    ], verbose_name='Warna Background')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    is_published = models.BooleanField(default=True, verbose_name='Publikasikan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Statistik'
        verbose_name_plural = 'Statistik'
        ordering = ['order', 'judul']
    
    def __str__(self):
        return self.judul
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = Statistik.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class Media(models.Model):
    """Model untuk Media Galeri dan Video Pesantren"""
    TIPE_CHOICES = [
        ('gallery', 'Galeri (Gambar)'),
        ('video', 'Video'),
    ]
    
    tipe = models.CharField(
        max_length=10,
        choices=TIPE_CHOICES,
        verbose_name='Tipe Media'
    )
    judul = models.CharField(max_length=200, verbose_name='Judul')
    sub_judul = models.CharField(max_length=300, blank=True, verbose_name='Sub Judul')
    
    # Untuk Galeri
    gambar = models.ImageField(
        upload_to='media/gallery/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Gambar',
        help_text='Upload gambar untuk galeri'
    )
    
    # Untuk Video
    video_file = models.FileField(
        upload_to='media/videos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='File Video',
        help_text='Upload file video (MP4, AVI, MOV)'
    )
    featured_image = models.ImageField(
        upload_to='media/videos/thumbnails/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Thumbnail Video',
        help_text='Gambar thumbnail untuk video (jika tidak ada, akan menggunakan default)'
    )
    
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    is_published = models.BooleanField(default=True, verbose_name='Publikasikan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Media'
        ordering = ['tipe', 'order', 'created_at']
    
    def __str__(self):
        return f"{self.get_tipe_display()} - {self.judul}"
    
    def save(self, *args, **kwargs):
        if not self.order:
            # Get max order for this type
            max_order = Media.objects.filter(tipe=self.tipe).aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class BagianJabatan(models.Model):
    """Model untuk Bagian/Jabatan Tenaga Pengajar"""
    nama = models.CharField(max_length=200, unique=True, verbose_name='Nama Bagian/Jabatan', help_text='Contoh: Pendiri, Kepala Sekolah, Pimpinan, Ustadz, Ustadzah, dll')
    deskripsi = models.TextField(blank=True, verbose_name='Deskripsi', help_text='Deskripsi singkat tentang bagian/jabatan ini')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan', help_text='Urutan tampil (angka lebih kecil tampil lebih dulu)')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Bagian/Jabatan'
        verbose_name_plural = 'Bagian/Jabatan'
        ordering = ['order', 'nama']
    
    def __str__(self):
        return self.nama


class TenagaPengajar(models.Model):
    """Model untuk Tenaga Pengajar (Ustadz/Ustadzah)"""
    JENIS_KELAMIN_CHOICES = [
        ('L', 'Laki-laki (Ustadz)'),
        ('P', 'Perempuan (Ustadzah)'),
    ]
    
    # Data Dasar
    nama_lengkap = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    nama_panggilan = models.CharField(max_length=100, blank=True, verbose_name='Nama Panggilan')
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN_CHOICES, verbose_name='Jenis Kelamin')
    foto = models.ImageField(upload_to='tenaga_pengajar/%Y/%m/%d/', blank=True, null=True, verbose_name='Foto')
    
    # Bagian/Jabatan
    bagian_jabatan = models.ForeignKey(
        BagianJabatan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tenaga_pengajar',
        verbose_name='Bagian/Jabatan'
    )
    
    # Biodata Lengkap
    tempat_lahir = models.CharField(max_length=100, blank=True, verbose_name='Tempat Lahir')
    tanggal_lahir = models.DateField(blank=True, null=True, verbose_name='Tanggal Lahir')
    alamat = models.TextField(blank=True, verbose_name='Alamat')
    no_hp = models.CharField(max_length=20, blank=True, verbose_name='No. HP')
    email = models.EmailField(blank=True, verbose_name='Email')
    
    # Pendidikan
    pendidikan_terakhir = models.CharField(max_length=200, blank=True, verbose_name='Pendidikan Terakhir', help_text='Contoh: S1 Pendidikan Agama Islam, S2 Tafsir Al-Qur\'an')
    universitas = models.CharField(max_length=200, blank=True, verbose_name='Universitas/Institusi')
    tahun_lulus = models.CharField(max_length=4, blank=True, verbose_name='Tahun Lulus')
    
    # Keahlian & Bidang
    bidang_keahlian = models.CharField(max_length=200, blank=True, verbose_name='Bidang Keahlian', help_text='Contoh: Tafsir, Hadits, Fiqih, Bahasa Arab, Matematika')
    mata_pelajaran = models.CharField(max_length=300, blank=True, verbose_name='Mata Pelajaran yang Diampu', help_text='Contoh: Tafsir Al-Qur\'an, Hadits, Fiqih, Bahasa Arab')
    
    # Pengalaman
    pengalaman_mengajar = models.TextField(blank=True, verbose_name='Pengalaman Mengajar', help_text='Riwayat pengalaman mengajar')
    prestasi = models.TextField(blank=True, verbose_name='Prestasi', help_text='Prestasi dan penghargaan yang pernah diraih')
    
    # Biodata Tambahan
    riwayat_pendidikan = models.TextField(blank=True, verbose_name='Riwayat Pendidikan', help_text='Riwayat pendidikan lengkap dari SD sampai perguruan tinggi')
    organisasi = models.TextField(blank=True, verbose_name='Organisasi', help_text='Keanggotaan organisasi')
    karya_tulis = models.TextField(blank=True, verbose_name='Karya Tulis', help_text='Karya tulis, buku, atau publikasi')
    motto = models.CharField(max_length=300, blank=True, verbose_name='Motto')
    
    # Media Sosial
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name='WhatsApp', help_text='Nomor WhatsApp (contoh: 6281234567890)')
    facebook = models.URLField(blank=True, verbose_name='Facebook', help_text='URL profil Facebook')
    instagram = models.URLField(blank=True, verbose_name='Instagram', help_text='URL profil Instagram')
    twitter = models.URLField(blank=True, verbose_name='Twitter/X', help_text='URL profil Twitter/X')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn', help_text='URL profil LinkedIn')
    youtube = models.URLField(blank=True, verbose_name='YouTube', help_text='URL channel YouTube')
    tiktok = models.URLField(blank=True, verbose_name='TikTok', help_text='URL profil TikTok')
    
    # Pengaturan
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan', help_text='Urutan tampil (angka lebih kecil tampil lebih dulu)')
    is_published = models.BooleanField(default=True, verbose_name='Publikasikan', help_text='Tampilkan di halaman public')
    is_featured = models.BooleanField(default=False, verbose_name='Unggulan', help_text='Tampilkan di slide home (maksimal 5)')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Tenaga Pengajar'
        verbose_name_plural = 'Tenaga Pengajar'
        ordering = ['order', 'bagian_jabatan__order', 'nama_lengkap']
    
    def __str__(self):
        return f"{self.nama_lengkap} - {self.bagian_jabatan.nama if self.bagian_jabatan else 'Tanpa Jabatan'}"
    
    def get_jenis_kelamin_display_short(self):
        """Mengembalikan jenis kelamin singkat"""
        return 'Ustadz' if self.jenis_kelamin == 'L' else 'Ustadzah'
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = TenagaPengajar.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class InformasiTambahan(models.Model):
    """Model untuk Informasi Tambahan (Waktu Pendaftaran, Dokumen, dll)"""
    WARNA_CHOICES = [
        ('green', 'Hijau'),
        ('blue', 'Biru'),
        ('purple', 'Ungu'),
        ('orange', 'Oranye'),
        ('red', 'Merah'),
        ('teal', 'Teal'),
        ('pink', 'Pink'),
    ]
    
    judul = models.CharField(max_length=200, verbose_name='Judul', help_text='Contoh: Waktu Pendaftaran, Dokumen yang Diperlukan')
    deskripsi = models.TextField(verbose_name='Deskripsi/Isi', help_text='Isi informasi yang akan ditampilkan')
    icon = models.CharField(max_length=100, default='fas fa-info-circle', verbose_name='Icon', help_text='Font Awesome icon class (contoh: fas fa-calendar-check)')
    warna = models.CharField(max_length=20, choices=WARNA_CHOICES, default='green', verbose_name='Warna Icon', help_text='Warna untuk icon dan background')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan', help_text='Urutan tampil (angka lebih kecil tampil lebih dulu)')
    is_published = models.BooleanField(default=True, verbose_name='Publikasikan', help_text='Tampilkan di halaman public')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Informasi Tambahan'
        verbose_name_plural = 'Informasi Tambahan'
        ordering = ['order', 'judul']
    
    def __str__(self):
        return self.judul
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = InformasiTambahan.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)
        return '-'
    
