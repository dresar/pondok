"""
Forms untuk Core App
"""
from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import (
    FAQ, Program, WhatsAppTemplate, WhatsAppTemplateKategori, Kontak, HeroSection, SejarahTimeline, SejarahTimelineImage,
    VisiMisi, ProgramPendidikan, ProgramPendidikanImage, Fasilitas, Ekstrakurikuler, JadwalHarian,
    Persyaratan, AlurPendaftaran, BiayaPendidikan, ContactPerson, SocialMedia,
    Seragam, KMI, WebsiteSettings, Statistik, Media, Dokumentasi, DokumentasiImage, InformasiTambahan
)


class FAQForm(forms.ModelForm):
    """Form untuk FAQ"""
    
    class Meta:
        model = FAQ
        fields = ['pertanyaan', 'jawaban', 'kategori', 'order', 'is_published']
        widgets = {
            'pertanyaan': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'jawaban': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 5
            }),
            'kategori': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }


class ProgramForm(forms.ModelForm):
    """Form untuk Program"""
    
    class Meta:
        model = Program
        fields = ['nama', 'slug', 'deskripsi', 'gambar', 'tanggal_mulai', 'tanggal_selesai', 'status', 'is_featured', 'meta_title', 'meta_description']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'deskripsi': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '400',
                }
            }),
            'gambar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'tanggal_mulai': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'date'
            }),
            'tanggal_selesai': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 3
            }),
        }


class WhatsAppTemplateKategoriForm(forms.ModelForm):
    """Form untuk Kategori Template WhatsApp"""
    
    class Meta:
        model = WhatsAppTemplateKategori
        fields = ['nama', 'deskripsi', 'order']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Contoh: Verifikasi, Pengumuman, Reminder'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 3,
                'placeholder': 'Deskripsi kategori (opsional)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'min': '0'
            }),
        }


class WhatsAppTemplateForm(forms.ModelForm):
    """Form untuk WhatsApp Template"""
    
    class Meta:
        model = WhatsAppTemplate
        fields = ['nama', 'kategori', 'tipe', 'pesan', 'variabel']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all',
                'placeholder': 'Masukkan nama template'
            }),
            'kategori': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white transition-all',
                'id': 'id_kategori'
            }),
            'tipe': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white transition-all'
            }),
            'pesan': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none transition-all',
                'rows': 10,
                'placeholder': 'Contoh: Halo {nama}, terima kasih telah mendaftar. Link verifikasi: {link}'
            }),
            'variabel': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all',
                'placeholder': 'Contoh: nama, tanggal, link (pisahkan dengan koma)'
            }),
        }


class KontakForm(forms.ModelForm):
    """Form untuk Kontak/Inquiry (Admin Panel)"""
    
    class Meta:
        model = Kontak
        fields = ['nama', 'email', 'no_hp', 'subjek', 'pesan', 'status', 'balasan']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'subjek': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'pesan': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 5
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'balasan': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 5
            }),
        }


class KontakPublicForm(forms.ModelForm):
    """Form untuk Kontak/Inquiry (Public Website)"""
    
    class Meta:
        model = Kontak
        fields = ['nama', 'email', 'no_hp', 'subjek', 'pesan']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all',
                'placeholder': 'Masukkan nama lengkap Anda'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all',
                'placeholder': 'contoh@email.com'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all',
                'placeholder': '081234567890'
            }),
            'subjek': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all',
                'placeholder': 'Subjek pertanyaan atau permintaan'
            }),
            'pesan': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none transition-all',
                'rows': 6,
                'placeholder': 'Tuliskan pesan atau pertanyaan Anda di sini...'
            }),
        }


class HeroSectionForm(forms.ModelForm):
    """Form untuk Hero Section"""
    
    class Meta:
        model = HeroSection
        fields = ['title', 'subtitle', 'image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Buat field image menjadi optional
        self.fields['image'].required = False
        self.fields['image'].help_text = 'Gambar dapat dipilih dari gallery atau diupload manual'


class SejarahTimelineForm(forms.ModelForm):
    """Form untuk Sejarah Timeline"""
    
    class Meta:
        model = SejarahTimeline
        fields = ['judul', 'icon', 'deskripsi', 'order']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'fas fa-history'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 4
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }


class SejarahTimelineImageForm(forms.ModelForm):
    """Form untuk Gambar Timeline Sejarah"""
    
    class Meta:
        model = SejarahTimelineImage
        fields = ['gambar', 'order']
        widgets = {
            'gambar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'min': '0',
                'value': '0'
            }),
        }
        labels = {
            'gambar': 'Gambar',
            'order': 'Urutan',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Buat field gambar menjadi optional
        self.fields['gambar'].required = False
        self.fields['gambar'].help_text = 'Gambar dapat dipilih dari gallery atau diupload manual'


class VisiMisiForm(forms.ModelForm):
    """Form untuk Visi Misi dengan Summernote"""
    
    class Meta:
        model = VisiMisi
        fields = ['visi', 'misi']
        widgets = {
            'visi': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '300',
                }
            }),
            'misi': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '400',
                }
            }),
        }


class ProgramPendidikanForm(forms.ModelForm):
    """Form untuk Program Pendidikan"""
    
    class Meta:
        model = ProgramPendidikan
        fields = ['nama', 'akreditasi', 'icon', 'gambar', 'order']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'akreditasi': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'fas fa-school'
            }),
            'gambar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }


class ProgramPendidikanImageForm(forms.ModelForm):
    """Form untuk Gambar Program Pendidikan"""
    
    class Meta:
        model = ProgramPendidikanImage
        fields = ['gambar', 'alt_text']
        widgets = {
            'gambar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Deskripsi gambar untuk SEO'
            }),
        }


class FasilitasForm(forms.ModelForm):
    """Form untuk Fasilitas"""
    
    class Meta:
        model = Fasilitas
        fields = ['nama', 'icon', 'gambar', 'order']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'fas fa-mosque'
            }),
            'gambar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }


class EkstrakurikulerForm(forms.ModelForm):
    """Form untuk Ekstrakurikuler"""
    
    class Meta:
        model = Ekstrakurikuler
        fields = ['nama', 'icon', 'order']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'fas fa-campground'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }


class DokumentasiForm(forms.ModelForm):
    """Form untuk Dokumentasi"""
    
    class Meta:
        model = Dokumentasi
        fields = ['judul', 'deskripsi', 'kategori', 'tanggal_kegiatan', 'lokasi', 'order', 'is_published']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 4
            }),
            'kategori': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'tanggal_kegiatan': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'date'
            }),
            'lokasi': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }


class JadwalHarianForm(forms.ModelForm):
    """Form untuk Jadwal Harian"""
    
    class Meta:
        model = JadwalHarian
        fields = ['waktu', 'judul', 'deskripsi', 'kategori', 'order']
        widgets = {
            'waktu': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '04.00-06.00'
            }),
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 3
            }),
            'kategori': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }


class PersyaratanForm(forms.ModelForm):
    """Form untuk Persyaratan dengan Summernote"""
    
    class Meta:
        model = Persyaratan
        fields = ['persyaratan_santri', 'persyaratan_santriwati']
        widgets = {
            'persyaratan_santri': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '400',
                }
            }),
            'persyaratan_santriwati': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '400',
                }
            }),
        }


class AlurPendaftaranForm(forms.ModelForm):
    """Form untuk Alur Pendaftaran dengan Summernote"""
    
    class Meta:
        model = AlurPendaftaran
        fields = ['gambar_utama', 'alur_pendaftaran', 'tahapan_tes']
        widgets = {
            'gambar_utama': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'alur_pendaftaran': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '400',
                }
            }),
            'tahapan_tes': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '300',
                }
            }),
        }


class BiayaPendidikanForm(forms.ModelForm):
    """Form untuk Biaya Pendidikan"""
    
    class Meta:
        model = BiayaPendidikan
        fields = ['tipe', 'nama', 'jumlah', 'keterangan', 'order']
        widgets = {
            'tipe': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'jumlah': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'keterangan': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }


class ContactPersonForm(forms.ModelForm):
    """Form untuk Contact Person"""
    
    class Meta:
        model = ContactPerson
        fields = ['nama', 'foto', 'no_hp', 'order', 'is_active']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100',
                'accept': 'image/*'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': '+62 812-3456-7890'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }


class SocialMediaForm(forms.ModelForm):
    """Form untuk Social Media"""
    
    class Meta:
        model = SocialMedia
        fields = ['platform', 'username', 'url', 'order', 'is_active']
        widgets = {
            'platform': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }


class SeragamForm(forms.ModelForm):
    """Form untuk Seragam"""
    
    class Meta:
        model = Seragam
        fields = ['hari', 'kategori', 'seragam', 'order']
        widgets = {
            'hari': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'kategori': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'seragam': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        initial_kategori = kwargs.pop('initial_kategori', None)
        super().__init__(*args, **kwargs)
        if initial_kategori:
            self.fields['kategori'].initial = initial_kategori
            # Set label untuk seragam berdasarkan kategori
            if initial_kategori == 'santri':
                self.fields['seragam'].label = 'Seragam Putra'
            else:
                self.fields['seragam'].label = 'Seragam Putri'


class KMIForm(forms.ModelForm):
    """Form untuk KMI dengan Summernote"""
    
    class Meta:
        model = KMI
        fields = ['visi_kmi', 'profil_kmi']
        widgets = {
            'visi_kmi': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '300',
                }
            }),
            'profil_kmi': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '500',
                }
            }),
        }


class MediaForm(forms.ModelForm):
    """Form untuk Media (Galeri & Video)"""
    
    class Meta:
        model = Media
        fields = ['tipe', 'judul', 'sub_judul', 'gambar', 'video_file', 'featured_image', 'order', 'is_published']
        widgets = {
            'tipe': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'onchange': 'toggleMediaFields(this.value)',
                'id': 'id_tipe'
            }),
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'sub_judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'gambar': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'accept': 'video/*'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        tipe = cleaned_data.get('tipe')
        gambar = cleaned_data.get('gambar')
        video_file = cleaned_data.get('video_file')
        
        # Cek apakah ada selected_media_gambar_id dari image picker (dari request.POST)
        # Kita perlu akses request melalui form instance
        if hasattr(self, '_selected_media_gambar_id'):
            selected_media_gambar_id = self._selected_media_gambar_id
        else:
            selected_media_gambar_id = None
        
        if tipe == 'gallery':
            # Gambar wajib jika: tidak ada instance (create baru) DAN tidak ada gambar upload DAN tidak ada selected_media_gambar_id
            if not self.instance.pk and not gambar and not selected_media_gambar_id:
                raise forms.ValidationError('Gambar wajib diisi untuk tipe Galeri. Pilih dari gallery atau upload manual.')
        elif tipe == 'video':
            if not video_file and not self.instance.pk:
                raise forms.ValidationError('File Video wajib diisi untuk tipe Video.')
        
        return cleaned_data


class StatistikForm(forms.ModelForm):
    """Form untuk Statistik"""
    
    class Meta:
        model = Statistik
        fields = ['judul', 'nilai', 'icon', 'deskripsi', 'warna', 'order', 'is_published']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'nilai': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Contoh: 1000, 500+, 95%'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'fas fa-chart-bar'
            }),
            'deskripsi': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Deskripsi singkat (opsional)'
            }),
            'warna': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }


class InformasiTambahanForm(forms.ModelForm):
    """Form untuk Informasi Tambahan"""
    
    class Meta:
        model = InformasiTambahan
        fields = ['judul', 'deskripsi', 'icon', 'warna', 'order', 'is_published']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'Contoh: Waktu Pendaftaran, Dokumen yang Diperlukan'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'rows': 5,
                'placeholder': 'Isi informasi yang akan ditampilkan'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'fas fa-calendar-check'
            }),
            'warna': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }