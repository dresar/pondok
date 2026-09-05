from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import os

User = get_user_model()


class ConvertedImage(models.Model):
    """Model untuk menyimpan gambar yang dikonversi ke WebP - Pusat semua gambar"""
    judul = models.CharField(max_length=200, default='', blank=True, verbose_name='Judul', help_text='Judul gambar untuk memudahkan pencarian')
    original_filename = models.CharField(max_length=255, verbose_name='Nama File Asli')
    webp_image = models.ImageField(upload_to='converted/%Y/%m/%d/', verbose_name='Gambar WebP')
    original_size = models.BigIntegerField(verbose_name='Ukuran Asli (bytes)')
    converted_size = models.BigIntegerField(verbose_name='Ukuran WebP (bytes)')
    compression_ratio = models.FloatField(verbose_name='Rasio Kompresi (%)')
    quality = models.IntegerField(default=85, verbose_name='Kualitas WebP')
    width = models.IntegerField(null=True, blank=True, verbose_name='Lebar (px)')
    height = models.IntegerField(null=True, blank=True, verbose_name='Tinggi (px)')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Dibuat Oleh')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat Pada')
    
    class Meta:
        verbose_name = 'Gambar yang Dikonversi'
        verbose_name_plural = 'Gambar yang Dikonversi'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.judul or self.original_filename
    
    def save(self, *args, **kwargs):
        # Auto-generate judul dari original_filename jika kosong
        if not self.judul and self.original_filename:
            # Hapus extension dan format judul
            import os
            self.judul = os.path.splitext(self.original_filename)[0].replace('_', ' ').replace('-', ' ').title()
        super().save(*args, **kwargs)
    
    def get_original_size_mb(self):
        """Mengembalikan ukuran asli dalam MB"""
        return round(self.original_size / (1024 * 1024), 2)
    
    def get_converted_size_kb(self):
        """Mengembalikan ukuran WebP dalam KB"""
        return round(self.converted_size / 1024, 2)
    
    def get_savings_mb(self):
        """Mengembalikan penghematan dalam MB"""
        savings = self.original_size - self.converted_size
        return round(savings / (1024 * 1024), 2)
    
    def get_cdn_url(self):
        """Mengembalikan URL CDN untuk akses publik"""
        if self.webp_image:
            return self.webp_image.url
        return None


class BugNote(models.Model):
    """Catatan bug/notepad singkat untuk admin panel."""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=200, verbose_name='Judul')
    description = models.TextField(verbose_name='Deskripsi', blank=True)
    page_url = models.URLField(verbose_name='URL Halaman', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bug_notes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Catatan Bug'
        verbose_name_plural = 'Catatan Bug'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"