"""
Models untuk Blog/Artikel Management dengan SEO
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import URLValidator

User = get_user_model()


class Category(models.Model):
    """Kategori untuk blog artikel"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nama')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Slug')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategori'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.order:
            max_order = Category.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Tag untuk blog artikel"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Nama')
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name='Slug')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tag'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.order:
            max_order = Tag.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Model untuk Blog/Artikel dengan SEO dan fitur lengkap"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Informasi Dasar
    title = models.CharField(max_length=200, verbose_name='Judul')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Slug')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Penulis')
    
    # Konten
    content = models.TextField(verbose_name='Konten')
    excerpt = models.TextField(max_length=500, blank=True, verbose_name='Ringkasan')
    featured_image = models.ImageField(
        upload_to='blog/featured/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Gambar Utama'
    )
    
    # Kategori & Tag
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name='Kategori')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Tag')
    
    # SEO Fields
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='Meta Title')
    meta_description = models.TextField(max_length=300, blank=True, verbose_name='Meta Description')
    meta_keywords = models.CharField(max_length=255, blank=True, verbose_name='Meta Keywords')
    
    # Media Tambahan
    video_file = models.FileField(
        upload_to='blog/videos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='File Video'
    )
    
    # Statistik
    views_count = models.PositiveIntegerField(default=0, verbose_name='Views')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Likes')
    shares_count = models.PositiveIntegerField(default=0, verbose_name='Shares')
    
    # Status & Publikasi
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Status')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Publikasi')
    is_featured = models.BooleanField(default=False, verbose_name='Unggulan')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Artikel Blog'
        verbose_name_plural = 'Artikel Blog'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at', 'status']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:300]
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_likes(self):
        self.likes_count += 1
        self.save(update_fields=['likes_count'])
    
    def increment_shares(self):
        self.shares_count += 1
        self.save(update_fields=['shares_count'])
    


class Testimoni(models.Model):
    """Model untuk Testimoni/Alumni"""
    nama = models.CharField(max_length=200, verbose_name='Nama')
    foto = models.ImageField(upload_to='testimoni/%Y/%m/%d/', blank=True, null=True, verbose_name='Foto')
    jabatan = models.CharField(max_length=200, blank=True, verbose_name='Jabatan/Alumni')
    testimoni = models.TextField(verbose_name='Testimoni')
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)], verbose_name='Rating')
    is_published = models.BooleanField(default=True, verbose_name='Published')
    order = models.PositiveIntegerField(default=0, verbose_name='Urutan')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    
    class Meta:
        verbose_name = 'Testimoni'
        verbose_name_plural = 'Testimoni'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.order:
            max_order = Testimoni.objects.aggregate(models.Max('order'))['order__max'] or 0
            self.order = max_order + 1
        super().save(*args, **kwargs)


class Pengumuman(models.Model):
    """Model untuk Pengumuman"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    judul = models.CharField(max_length=200, verbose_name='Judul')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Slug')
    konten = models.TextField(verbose_name='Konten')
    gambar = models.ImageField(upload_to='pengumuman/%Y/%m/%d/', blank=True, null=True, verbose_name='Gambar')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Status')
    is_penting = models.BooleanField(default=False, verbose_name='Penting')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Publikasi')
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='Meta Title')
    meta_description = models.TextField(max_length=300, blank=True, verbose_name='Meta Description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Pengumuman'
        verbose_name_plural = 'Pengumuman'
        ordering = ['-is_penting', '-published_at', '-created_at']
    
    def __str__(self):
        return self.judul
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        if not self.meta_title:
            self.meta_title = self.judul
        super().save(*args, **kwargs)
