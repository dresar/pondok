from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import DocumentTemplate


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(SummernoteModelAdmin):
    """Admin untuk DocumentTemplate dengan Summernote"""
    list_display = ['nama', 'slug', 'ukuran_kertas', 'orientasi', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'ukuran_kertas', 'orientasi', 'created_at']
    search_fields = ['nama', 'slug', 'deskripsi']
    prepopulated_fields = {'slug': ('nama',)}
    ordering = ['order', 'nama']
    
    summernote_fields = ('html_template',)
    
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('nama', 'slug', 'deskripsi', 'is_active', 'order')
        }),
        ('Template HTML', {
            'fields': ('html_template',),
            'description': 'Gunakan placeholder seperti {{nama_lengkap}}, {{nisn}}, {{alamat}}, dll.'
        }),
        ('CSS Styling', {
            'fields': ('css_template',),
            'description': 'CSS untuk styling dokumen PDF'
        }),
        ('Pengaturan Halaman', {
            'fields': ('ukuran_kertas', 'orientasi', 'margin_top', 'margin_right', 'margin_bottom', 'margin_left')
        }),
    )
