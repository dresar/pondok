from django.db import models


class DocumentTemplate(models.Model):
    """Model untuk template dokumen yang bisa di-custom melalui Summernote"""
    
    nama = models.CharField(max_length=200, verbose_name='Nama Template', help_text='Contoh: Form A.1, Surat Pernyataan')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug', help_text='URL-friendly identifier')
    deskripsi = models.TextField(blank=True, verbose_name='Deskripsi', help_text='Deskripsi singkat tentang template ini')
    
    # HTML Template dengan Summernote
    html_template = models.TextField(verbose_name='HTML Template', help_text='''
        Template HTML dengan placeholder untuk data santri. 
        Gunakan placeholder: {{nama_lengkap}}, {{nisn}}, {{tempat_lahir}}, {{tanggal_lahir}}, {{alamat}}, dll.
        Contoh: <h1>Nama: {{nama_lengkap}}</h1>
    ''')
    
    # CSS untuk styling
    css_template = models.TextField(blank=True, verbose_name='CSS Template', help_text='CSS untuk styling dokumen PDF')
    
    # Settings
    ukuran_kertas = models.CharField(
        max_length=20,
        default='A4',
        choices=[
            ('A4', 'A4 (210 x 297 mm)'),
            ('Letter', 'Letter (8.5 x 11 inch)'),
            ('Legal', 'Legal (8.5 x 14 inch)'),
        ],
        verbose_name='Ukuran Kertas'
    )
    
    orientasi = models.CharField(
        max_length=20,
        default='portrait',
        choices=[
            ('portrait', 'Portrait (Tegak)'),
            ('landscape', 'Landscape (Mendatar)'),
        ],
        verbose_name='Orientasi'
    )
    
    margin_top = models.CharField(max_length=20, default='1.5cm', verbose_name='Margin Atas', help_text='Contoh: 1.5cm, 15mm, 0.5in')
    margin_right = models.CharField(max_length=20, default='1.5cm', verbose_name='Margin Kanan')
    margin_bottom = models.CharField(max_length=20, default='1.5cm', verbose_name='Margin Bawah')
    margin_left = models.CharField(max_length=20, default='1.5cm', verbose_name='Margin Kiri')
    
    # Metadata
    is_active = models.BooleanField(default=True, verbose_name='Aktif', help_text='Template aktif bisa digunakan untuk generate PDF')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan', help_text='Urutan tampil di list')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Template Dokumen'
        verbose_name_plural = 'Template Dokumen'
        ordering = ['order', 'nama']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nama)
        if not self.order:
            max_order = DocumentTemplate.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)
