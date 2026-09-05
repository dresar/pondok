from django.contrib import admin
from .models import Santri


@admin.register(Santri)
class SantriAdmin(admin.ModelAdmin):
    list_display = ['nama_lengkap', 'nisn', 'asal_sekolah', 'status', 'created_at']
    list_filter = ['status', 'jenis_kelamin', 'created_at']
    search_fields = ['nama_lengkap', 'nisn', 'no_hp', 'email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
