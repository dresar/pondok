"""
Admin configuration untuk Core App
"""
from django.contrib import admin
from .models import (
    WebsiteSettings, FAQ, Program, WhatsAppTemplate, WhatsAppTemplateKategori, Kontak, HeroSection,
    SejarahTimeline, VisiMisi, ProgramPendidikan, Fasilitas, Ekstrakurikuler,
    JadwalHarian, Persyaratan, AlurPendaftaran, BiayaPendidikan, ContactPerson,
    SocialMedia, Seragam, KMI, Statistik, Dokumentasi, DokumentasiImage, InformasiTambahan
)


@admin.register(WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    """Admin untuk WebsiteSettings (Singleton)"""
    fieldsets = (
        ('Informasi Umum', {
            'fields': ('nama_pondok', 'alamat', 'logo')
        }),
        ('Kontak', {
            'fields': ('no_telepon', 'email', 'website')
        }),
        ('Bank', {
            'fields': ('nama_bank', 'no_rekening', 'nama_pemilik_rekening')
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'twitter')
        }),
        ('Biaya', {
            'fields': ('biaya_pendaftaran',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['pertanyaan', 'kategori', 'is_published', 'order', 'created_at']
    search_fields = ['pertanyaan', 'jawaban', 'kategori']
    list_filter = ['is_published', 'kategori', 'created_at']
    ordering = ['order', 'kategori', 'pertanyaan']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['nama', 'status', 'is_featured', 'tanggal_mulai', 'order', 'created_at']
    search_fields = ['nama', 'deskripsi']
    list_filter = ['status', 'is_featured', 'tanggal_mulai', 'created_at']
    prepopulated_fields = {'slug': ('nama',)}
    ordering = ['order', '-created_at']


@admin.register(WhatsAppTemplateKategori)
class WhatsAppTemplateKategoriAdmin(admin.ModelAdmin):
    list_display = ['nama', 'order', 'is_active', 'created_at']
    search_fields = ['nama', 'deskripsi']
    list_filter = ['is_active', 'created_at']
    ordering = ['order', 'nama']
    prepopulated_fields = {'slug': ('nama',)}


@admin.register(WhatsAppTemplate)
class WhatsAppTemplateAdmin(admin.ModelAdmin):
    list_display = ['nama', 'kategori', 'tipe', 'order', 'created_at']
    search_fields = ['nama', 'pesan', 'variabel']
    list_filter = ['kategori', 'tipe', 'created_at']
    ordering = ['tipe', 'order', 'kategori', 'nama']


@admin.register(Kontak)
class KontakAdmin(admin.ModelAdmin):
    list_display = ['nama', 'email', 'no_hp', 'subjek', 'status', 'created_at']
    search_fields = ['nama', 'email', 'subjek', 'pesan']
    list_filter = ['status', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    search_fields = ['title']
    list_filter = ['is_active', 'created_at']
    ordering = ['order', '-created_at']


@admin.register(SejarahTimeline)
class SejarahTimelineAdmin(admin.ModelAdmin):
    list_display = ['judul', 'order', 'created_at']
    search_fields = ['judul', 'deskripsi']
    ordering = ['order', '-created_at']


@admin.register(VisiMisi)
class VisiMisiAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'updated_at']
    readonly_fields = ['updated_at']


@admin.register(ProgramPendidikan)
class ProgramPendidikanAdmin(admin.ModelAdmin):
    list_display = ['nama', 'akreditasi', 'order', 'created_at']
    search_fields = ['nama', 'akreditasi']
    ordering = ['order', 'nama']


@admin.register(Fasilitas)
class FasilitasAdmin(admin.ModelAdmin):
    list_display = ['nama', 'order', 'created_at']
    search_fields = ['nama']
    ordering = ['order', 'nama']


@admin.register(Ekstrakurikuler)
class EkstrakurikulerAdmin(admin.ModelAdmin):
    list_display = ['nama', 'order', 'created_at']
    search_fields = ['nama']
    ordering = ['order', 'nama']


@admin.register(JadwalHarian)
class JadwalHarianAdmin(admin.ModelAdmin):
    list_display = ['waktu', 'judul', 'order', 'created_at']
    search_fields = ['waktu', 'judul', 'deskripsi']
    ordering = ['order', 'waktu']


@admin.register(Persyaratan)
class PersyaratanAdmin(admin.ModelAdmin):
    """Admin untuk Persyaratan (Singleton)"""
    list_display = ['__str__', 'updated_at']
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AlurPendaftaran)
class AlurPendaftaranAdmin(admin.ModelAdmin):
    """Admin untuk AlurPendaftaran (Singleton)"""
    list_display = ['__str__', 'updated_at']
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BiayaPendidikan)
class BiayaPendidikanAdmin(admin.ModelAdmin):
    list_display = ['tipe', 'nama', 'jumlah', 'order', 'created_at']
    search_fields = ['nama', 'keterangan']
    list_filter = ['tipe', 'created_at']
    ordering = ['tipe', 'order']


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ['nama', 'no_hp', 'order', 'is_active', 'created_at']
    search_fields = ['nama', 'no_hp']
    list_filter = ['is_active', 'created_at']
    ordering = ['order', 'nama']


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['platform', 'username', 'order', 'is_active', 'created_at']
    search_fields = ['username', 'url']
    list_filter = ['platform', 'is_active', 'created_at']
    ordering = ['order', 'platform']


@admin.register(Seragam)
class SeragamAdmin(admin.ModelAdmin):
    list_display = ['hari', 'seragam_putra', 'seragam_putri', 'order', 'created_at']
    search_fields = ['hari', 'seragam_putra', 'seragam_putri']
    ordering = ['order', 'hari']


@admin.register(KMI)
class KMIAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'updated_at']
    readonly_fields = ['updated_at']


@admin.register(Statistik)
class StatistikAdmin(admin.ModelAdmin):
    list_display = ['judul', 'nilai', 'warna', 'order', 'is_published', 'created_at']
    search_fields = ['judul', 'nilai', 'deskripsi']
    list_filter = ['is_published', 'warna', 'created_at']
    ordering = ['order', 'judul']


@admin.register(Dokumentasi)
class DokumentasiAdmin(admin.ModelAdmin):
    list_display = ['judul', 'kategori', 'tanggal_kegiatan', 'order', 'is_published', 'created_at']
    search_fields = ['judul', 'deskripsi', 'lokasi']
    list_filter = ['kategori', 'is_published', 'tanggal_kegiatan', 'created_at']
    ordering = ['order', '-tanggal_kegiatan', '-created_at']


@admin.register(DokumentasiImage)
class DokumentasiImageAdmin(admin.ModelAdmin):
    list_display = ['dokumentasi', 'order', 'created_at']
    search_fields = ['dokumentasi__judul', 'alt_text']
    list_filter = ['created_at']
    ordering = ['dokumentasi', 'order', 'created_at']


@admin.register(InformasiTambahan)
class InformasiTambahanAdmin(admin.ModelAdmin):
    list_display = ['judul', 'warna', 'order', 'is_published', 'created_at']
    search_fields = ['judul', 'deskripsi']
    list_filter = ['is_published', 'warna', 'created_at']
    ordering = ['order', 'judul']
