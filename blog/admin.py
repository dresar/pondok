"""
Django Admin untuk Blog Management
"""
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import BlogPost, Category, Tag, Testimoni, Pengumuman


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['order', 'name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['order', 'name']


@admin.register(Testimoni)
class TestimoniAdmin(admin.ModelAdmin):
    list_display = ['nama', 'jabatan', 'rating', 'is_published', 'order', 'created_at']
    search_fields = ['nama', 'jabatan', 'testimoni']
    list_filter = ['is_published', 'rating', 'created_at']
    ordering = ['order', '-created_at']


@admin.register(Pengumuman)
class PengumumanAdmin(admin.ModelAdmin):
    list_display = ['judul', 'status', 'is_penting', 'published_at', 'created_at']
    search_fields = ['judul', 'konten']
    list_filter = ['status', 'is_penting', 'published_at', 'created_at']
    prepopulated_fields = {'slug': ('judul',)}
    ordering = ['-is_penting', '-published_at', '-created_at']


@admin.register(BlogPost)
class BlogPostAdmin(SummernoteModelAdmin):
    """Admin untuk Blog Post dengan Summernote"""
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views_count', 'likes_count', 'shares_count', 'published_at', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt', 'meta_title', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'likes_count', 'shares_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('title', 'slug', 'author', 'status', 'is_featured', 'published_at')
        }),
        ('Konten', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ('Kategori & Tag', {
            'fields': ('category', 'tags')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Media Tambahan', {
            'fields': ('video_file',)
        }),
        ('Statistik', {
            'fields': ('views_count', 'likes_count', 'shares_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    summernote_fields = ('content',)
