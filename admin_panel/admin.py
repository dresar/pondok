from django.contrib import admin
from .models import ConvertedImage, BugNote


@admin.register(ConvertedImage)
class ConvertedImageAdmin(admin.ModelAdmin):
    list_display = ('judul', 'original_filename', 'get_original_size_mb', 'get_converted_size_kb', 'created_at')
    search_fields = ('judul', 'original_filename')
    readonly_fields = ('original_size', 'converted_size', 'compression_ratio', 'quality', 'width', 'height', 'created_at')


@admin.register(BugNote)
class BugNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'page_url', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'page_url')
    readonly_fields = ('created_at',)
