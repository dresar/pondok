"""
Forms untuk Admin Panel dengan Tailwind CSS
Semua form dirancang untuk reusable dengan HTMX
"""
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from admissions.models import Santri
from payments.models import Payment, BankAccount
from core.models import WebsiteSettings, BagianJabatan, TenagaPengajar
from .models import ConvertedImage
from django.contrib.auth import get_user_model
import os

User = get_user_model()


# Tailwind CSS Base Classes
TAILWIND_INPUT = 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition duration-200 leading-relaxed'
TAILWIND_SELECT = 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white transition duration-200 leading-relaxed'
TAILWIND_TEXTAREA = 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none transition duration-200 leading-relaxed'
TAILWIND_FILE_INPUT = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100 transition duration-200'


class SantriForm(forms.ModelForm):
    """Form untuk Create dan Update Santri - reusable untuk HTMX dengan Tailwind CSS"""
    
    class Meta:
        model = Santri
        fields = [
            # Data Pribadi Santri
            'nama_lengkap', 'nama_panggilan', 'nisn', 'tempat_lahir', 'tanggal_lahir', 
            'jenis_kelamin', 'agama', 'kewarganegaraan', 'anak_ke', 'jumlah_saudara', 
            'bahasa_sehari_hari', 'golongan_darah', 'tinggi_badan', 'berat_badan', 
            'riwayat_penyakit', 'tinggal_dengan',
            # Data Ayah
            'nama_ayah', 'nik_ayah', 'tempat_lahir_ayah', 'tanggal_lahir_ayah',
            'agama_ayah', 'kewarganegaraan_ayah', 'pendidikan_ayah', 'pekerjaan_ayah', 
            'no_hp_ayah', 'status_ayah',
            # Data Ibu
            'nama_ibu', 'nik_ibu', 'tempat_lahir_ibu', 'tanggal_lahir_ibu',
            'agama_ibu', 'kewarganegaraan_ibu', 'pendidikan_ibu', 'pekerjaan_ibu', 
            'no_hp_ibu', 'status_ibu', 'alamat_orangtua',
            # Alamat Santri
            'alamat', 'desa', 'kecamatan', 'kabupaten', 'provinsi', 'kode_pos',
            'no_hp', 'email',
            # Data Sekolah
            'asal_sekolah', 'npsn_sekolah', 'kelas_terakhir', 'tahun_lulus', 'no_ijazah',
            'kelas_diterima', 'tanggal_diterima',
            # Dokumen
            'foto_santri', 'foto_ktp', 'foto_akta', 'foto_ijazah', 'surat_sehat',
            # Lainnya
            'catatan', 'status'
        ]
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Masukkan nama lengkap'
            }),
            'nama_panggilan': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama panggilan (opsional)'
            }),
            'nisn': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '10 digit NISN',
                'maxlength': '10'
            }),
            'tempat_lahir': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Tempat lahir'
            }),
            'tanggal_lahir': forms.DateInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'date',
                'format': '%Y-%m-%d'
            }, format='%Y-%m-%d'),
            'jenis_kelamin': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'kewarganegaraan': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'anak_ke': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Anak ke (opsional)',
                'min': '1'
            }),
            'jumlah_saudara': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Jumlah saudara (opsional)',
                'min': '0'
            }),
            'bahasa_sehari_hari': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Bahasa sehari-hari (opsional)'
            }),
            'riwayat_penyakit': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Riwayat penyakit (opsional)'
            }),
            'tinggal_dengan': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'nama_ayah': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama ayah'
            }),
            'nik_ayah': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '16 digit NIK ayah (opsional)',
                'maxlength': '16'
            }),
            'tempat_lahir_ayah': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Tempat lahir ayah (opsional)'
            }),
            'tanggal_lahir_ayah': forms.DateInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'date',
                'format': '%Y-%m-%d'
            }, format='%Y-%m-%d'),
            'agama_ayah': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Agama ayah (opsional)'
            }),
            'kewarganegaraan_ayah': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'pendidikan_ayah': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'status_ayah': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'nama_ibu': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama ibu'
            }),
            'nik_ibu': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '16 digit NIK ibu (opsional)',
                'maxlength': '16'
            }),
            'tempat_lahir_ibu': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Tempat lahir ibu (opsional)'
            }),
            'tanggal_lahir_ibu': forms.DateInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'date',
                'format': '%Y-%m-%d'
            }, format='%Y-%m-%d'),
            'agama_ibu': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Agama ibu (opsional)'
            }),
            'kewarganegaraan_ibu': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'pendidikan_ibu': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'status_ibu': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'pekerjaan_ayah': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Pekerjaan ayah (opsional)'
            }),
            'pekerjaan_ibu': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Pekerjaan ibu (opsional)'
            }),
            'alamat': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Alamat lengkap'
            }),
            'desa': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Desa/Kelurahan (opsional)'
            }),
            'kecamatan': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Kecamatan (opsional)'
            }),
            'kabupaten': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Kabupaten (opsional)'
            }),
            'provinsi': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Provinsi (opsional)'
            }),
            'kode_pos': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Kode Pos (opsional)',
                'maxlength': '10'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'tel',
                'placeholder': '08xxxxxxxxxx'
            }),
            'email': forms.EmailInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'email@example.com (opsional)'
            }),
            'asal_sekolah': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama sekolah asal'
            }),
            'npsn_sekolah': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'NPSN Sekolah (opsional)',
                'maxlength': '20'
            }),
            'kelas_terakhir': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Contoh: 6 SD, 9 SMP, 12 SMA'
            }),
            'agama': forms.HiddenInput(attrs={
                'value': 'Islam'
            }),
            'golongan_darah': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'tinggi_badan': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Tinggi badan dalam cm (opsional)',
                'min': '0'
            }),
            'berat_badan': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Berat badan dalam kg (opsional)',
                'min': '0'
            }),
            'no_hp_ayah': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'tel',
                'placeholder': 'No. HP ayah (opsional)'
            }),
            'no_hp_ibu': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'tel',
                'placeholder': 'No. HP ibu (opsional)'
            }),
            'alamat_orangtua': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 2,
                'placeholder': 'Alamat orang tua (opsional)'
            }),
            'tahun_lulus': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Tahun lulus (opsional)',
                'maxlength': '4'
            }),
            'no_ijazah': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'No. Ijazah/SKHUN (opsional)'
            }),
            'kelas_diterima': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Kelas diterima di pesantren (opsional)'
            }),
            'tanggal_diterima': forms.DateInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'date',
                'format': '%Y-%m-%d'
            }, format='%Y-%m-%d'),
            'foto_santri': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'foto_ktp': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'foto_akta': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'foto_ijazah': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'surat_sehat': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'catatan': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Catatan tambahan (opsional)'
            }),
            'status': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
        }
        labels = {
            'nama_lengkap': 'Nama Lengkap',
            'nama_panggilan': 'Nama Panggilan',
            'nisn': 'NISN',
            'tempat_lahir': 'Tempat Lahir',
            'tanggal_lahir': 'Tanggal Lahir',
            'jenis_kelamin': 'Jenis Kelamin',
            'agama': 'Agama',
            'kewarganegaraan': 'Kewarganegaraan',
            'anak_ke': 'Anak Ke',
            'jumlah_saudara': 'Jumlah Saudara',
            'bahasa_sehari_hari': 'Bahasa Sehari-hari',
            'golongan_darah': 'Golongan Darah',
            'tinggi_badan': 'Tinggi Badan (cm)',
            'berat_badan': 'Berat Badan (kg)',
            'riwayat_penyakit': 'Riwayat Penyakit',
            'tinggal_dengan': 'Tinggal Dengan',
            'nama_ayah': 'Nama Ayah',
            'nik_ayah': 'NIK Ayah',
            'tempat_lahir_ayah': 'Tempat Lahir Ayah',
            'tanggal_lahir_ayah': 'Tanggal Lahir Ayah',
            'agama_ayah': 'Agama Ayah',
            'kewarganegaraan_ayah': 'Kewarganegaraan Ayah',
            'pendidikan_ayah': 'Pendidikan Ayah',
            'pekerjaan_ayah': 'Pekerjaan Ayah',
            'no_hp_ayah': 'No. HP Ayah',
            'status_ayah': 'Status Ayah',
            'nama_ibu': 'Nama Ibu',
            'nik_ibu': 'NIK Ibu',
            'tempat_lahir_ibu': 'Tempat Lahir Ibu',
            'tanggal_lahir_ibu': 'Tanggal Lahir Ibu',
            'agama_ibu': 'Agama Ibu',
            'kewarganegaraan_ibu': 'Kewarganegaraan Ibu',
            'pendidikan_ibu': 'Pendidikan Ibu',
            'pekerjaan_ibu': 'Pekerjaan Ibu',
            'no_hp_ibu': 'No. HP Ibu',
            'status_ibu': 'Status Ibu',
            'alamat_orangtua': 'Alamat Orang Tua',
            'alamat': 'Alamat Lengkap',
            'desa': 'Desa/Kelurahan',
            'kecamatan': 'Kecamatan',
            'kabupaten': 'Kabupaten',
            'provinsi': 'Provinsi',
            'kode_pos': 'Kode Pos',
            'no_hp': 'No. HP',
            'email': 'Email',
            'asal_sekolah': 'Asal Sekolah',
            'npsn_sekolah': 'NPSN Sekolah',
            'kelas_terakhir': 'Kelas Terakhir',
            'tahun_lulus': 'Tahun Lulus',
            'no_ijazah': 'No. Ijazah/SKHUN',
            'kelas_diterima': 'Kelas Diterima',
            'tanggal_diterima': 'Tanggal Diterima',
            'foto_santri': 'Foto Santri',
            'foto_ktp': 'Foto KTP/Kartu Keluarga',
            'foto_akta': 'Foto Akta Kelahiran',
            'foto_ijazah': 'Foto Ijazah/SKHUN',
            'surat_sehat': 'Surat Keterangan Sehat',
            'catatan': 'Catatan Tambahan',
            'status': 'Status',
        }
    
    def clean_nisn(self):
        """Validasi NISN harus 10 digit angka"""
        nisn = self.cleaned_data.get('nisn')
        if nisn and not nisn.isdigit():
            raise ValidationError('NISN harus berupa angka.')
        if nisn and len(nisn) != 10:
            raise ValidationError('NISN harus terdiri dari 10 digit.')
        return nisn
    
    def clean_no_hp(self):
        """Validasi nomor HP"""
        no_hp = self.cleaned_data.get('no_hp')
        if no_hp:
            # Hapus karakter non-digit
            digits_only = ''.join(filter(str.isdigit, no_hp))
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValidationError('Nomor HP harus antara 10-15 digit.')
        return no_hp
    
    def clean_agama(self):
        """Pastikan agama selalu Islam"""
        agama = self.cleaned_data.get('agama', 'Islam')
        if not agama or agama.strip() == '':
            return 'Islam'
        return 'Islam'  # Selalu return Islam


class PaymentForm(forms.ModelForm):
    """Form untuk create dan update Payment - digunakan di form santri (disederhanakan)"""
    
    rekening_tujuan = forms.ModelChoiceField(
        queryset=BankAccount.objects.filter(is_active=True).order_by('order', 'nama_bank'),
        required=False,
        empty_label="Pilih Rekening Tujuan",
        widget=forms.Select(attrs={
            'class': TAILWIND_SELECT
        }),
        label='Rekening Tujuan (Penerima)',
        help_text='Pilih rekening tujuan pembayaran dari daftar rekening yang tersedia'
    )
    
    class Meta:
        model = Payment
        fields = [
            'bank_pengirim', 'nama_pemilik_rekening',
            'jumlah_transfer', 'bukti_transfer', 'status'
        ]
        widgets = {
            'bank_pengirim': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'nama_pemilik_rekening': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama pemilik rekening pengirim'
            }),
            'jumlah_transfer': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '0',
                'step': '1000',
                'min': '0'
            }),
            'bukti_transfer': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
        }
        labels = {
            'bank_pengirim': 'Bank Pengirim',
            'nama_pemilik_rekening': 'Nama Pemilik Rekening',
            'jumlah_transfer': 'Jumlah Transfer (Rp)',
            'bukti_transfer': 'Bukti Transfer',
            'status': 'Status Pembayaran',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format label untuk rekening_tujuan: singkatan bank - nomor rekening
        self.fields['rekening_tujuan'].queryset = BankAccount.objects.filter(is_active=True).order_by('order', 'nama_bank')
        self.fields['rekening_tujuan'].label_from_instance = lambda obj: f"{obj.nama_bank} - {obj.nomor_rekening}"
        
        # Custom choices untuk status
        self.fields['status'].choices = Payment.STATUS_CHOICES
        # Semua field opsional (payment bisa dikosongkan)
        self.fields['bank_pengirim'].required = False
        self.fields['nama_pemilik_rekening'].required = False
        self.fields['jumlah_transfer'].required = False
        self.fields['bukti_transfer'].required = False
        self.fields['status'].required = False
        
        # Set initial rekening_tujuan dari instance jika ada
        if self.instance and self.instance.pk:
            # Cari BankAccount berdasarkan rekening_tujuan yang tersimpan
            if self.instance.rekening_tujuan:
                try:
                    bank_account = BankAccount.objects.get(nomor_rekening=self.instance.rekening_tujuan)
                    self.fields['rekening_tujuan'].initial = bank_account
                except BankAccount.DoesNotExist:
                    pass
    
    def save(self, commit=True):
        payment = super().save(commit=False)
        # Simpan nomor rekening tujuan dari BankAccount yang dipilih
        if self.cleaned_data.get('rekening_tujuan'):
            bank_account = self.cleaned_data['rekening_tujuan']
            payment.rekening_tujuan = bank_account.nomor_rekening
        if commit:
            payment.save()
        return payment


class PaymentVerificationForm(forms.ModelForm):
    """Form untuk verifikasi pembayaran - reusable untuk HTMX dengan Tailwind CSS"""
    
    class Meta:
        model = Payment
        fields = ['status', 'catatan']
        widgets = {
            'status': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'catatan': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 4,
                'placeholder': 'Catatan verifikasi (opsional). Contoh: Bukti transfer sudah sesuai, jumlah sudah benar, dll.'
            }),
        }
        labels = {
            'status': 'Status Verifikasi',
            'catatan': 'Catatan',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom choices untuk status
        self.fields['status'].choices = Payment.STATUS_CHOICES


class WebsiteSettingsForm(forms.ModelForm):
    """Form untuk pengaturan website dengan Tailwind CSS"""
    
    class Meta:
        model = WebsiteSettings
        fields = [
            'nama_pondok', 'arabic_name', 'alamat', 'deskripsi', 'logo', 'header_mobile_image', 'header_mobile_height', 'favicon',
            'no_telepon', 'email', 'website',
            'meta_title', 'meta_description', 'meta_keywords',
            'google_maps_link', 'google_maps_embed_code', 'lokasi_pendaftaran',
            'maintenance_mode', 'maintenance_message'
        ]
        widgets = {
            'nama_pondok': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama Pondok Pesantren'
            }),
            'arabic_name': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama Pondok dalam Bahasa Arab (opsional)'
            }),
            'alamat': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Alamat lengkap pondok pesantren'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 4,
                'placeholder': 'Deskripsi singkat tentang pondok pesantren'
            }),
            'logo': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'header_mobile_image': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'header_mobile_height': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'number',
                'min': '40',
                'max': '200',
                'step': '5'
            }),
            'favicon': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'no_telepon': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'tel',
                'placeholder': '081234567890'
            }),
            'email': forms.EmailInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'email@pondok.com'
            }),
            'website': forms.URLInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'https://www.pondok.com'
            }),
            'meta_title': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Judul untuk SEO (maks 60 karakter)',
                'maxlength': '60'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Deskripsi untuk SEO (maks 160 karakter)',
                'maxlength': '160'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Kata kunci SEO (pisahkan dengan koma)'
            }),
            'google_maps_link': forms.URLInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'https://maps.google.com/...'
            }),
            'google_maps_embed_code': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 6,
                'placeholder': '<iframe src="https://www.google.com/maps/embed?pb=..." width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'
            }),
            'lokasi_pendaftaran': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Lokasi pendaftaran santri baru'
            }),
            'maintenance_mode': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded'
            }),
            'maintenance_message': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 4,
                'placeholder': 'Pesan yang akan ditampilkan saat maintenance mode aktif'
            }),
        }
        labels = {
            'nama_pondok': 'Nama Pondok Pesantren',
            'arabic_name': 'Nama Arab',
            'alamat': 'Alamat Pondok',
            'deskripsi': 'Deskripsi Pondok',
            'logo': 'Logo Website',
            'header_mobile_image': 'Header Mobile (Kop Surat)',
            'header_mobile_height': 'Tinggi Header Mobile (px)',
            'favicon': 'Favicon',
            'no_telepon': 'No. Telepon',
            'email': 'Email',
            'website': 'Website',
            'meta_title': 'Meta Title (SEO)',
            'meta_description': 'Meta Description (SEO)',
            'meta_keywords': 'Meta Keywords (SEO)',
            'google_maps_link': 'Google Maps Link',
            'google_maps_embed_code': 'Google Maps Embed Code',
            'lokasi_pendaftaran': 'Lokasi Pendaftaran',
            'maintenance_mode': 'Mode Maintenance',
            'maintenance_message': 'Pesan Maintenance',
        }
    


class ImageConverterForm(forms.Form):
    """Form untuk konversi gambar ke WebP - Minimalis (hanya judul + gambar)"""
    judul = forms.CharField(
        label='Judul Gambar',
        max_length=200,
        required=True,
        help_text='Judul untuk memudahkan pencarian',
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Contoh: Hero Image 1, Foto Kegiatan, dll'
        })
    )
    image = forms.ImageField(
        label='Pilih Gambar',
        help_text='Format yang didukung: JPG, PNG, GIF. Maksimal 10MB. File asli akan dihapus setelah dikompres.',
        widget=forms.FileInput(attrs={
            'class': TAILWIND_FILE_INPUT,
            'accept': 'image/jpeg,image/jpg,image/png,image/gif',
            'id': 'image-input'
        })
    )


class SaveConvertedImageForm(forms.ModelForm):
    """Form untuk menyimpan metadata gambar yang dikonversi"""
    class Meta:
        model = ConvertedImage
        fields = ['original_filename']
        widgets = {
            'original_filename': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama file (opsional)'
            })
        }


class SantriSearchFilterForm(forms.Form):
    """Form untuk search dan filter santri - digunakan di HTMX dengan Tailwind CSS"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Cari nama, NISN, HP, atau email...',
            'hx-get': '/admin-panel/santri/',
            'hx-trigger': 'keyup changed delay:500ms',
            'hx-target': '#santri-table-container',
            'hx-swap': 'innerHTML',
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Semua Status')] + Santri.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': TAILWIND_SELECT,
            'hx-get': '/admin-panel/santri/',
            'hx-trigger': 'change',
            'hx-target': '#santri-table-container',
            'hx-swap': 'innerHTML',
        })
    )
    order_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Terbaru'),
            ('created_at', 'Terlama'),
            ('nama_lengkap', 'Nama A-Z'),
            ('-nama_lengkap', 'Nama Z-A'),
        ],
        widget=forms.Select(attrs={
            'class': TAILWIND_SELECT,
            'hx-get': '/admin-panel/santri/',
            'hx-trigger': 'change',
            'hx-target': '#santri-table-container',
            'hx-swap': 'innerHTML',
        })
    )


class PaymentSearchFilterForm(forms.Form):
    """Form untuk search dan filter payment - digunakan di HTMX dengan Tailwind CSS"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Cari nama santri, NISN, atau nama rekening...',
            'hx-get': '/admin-panel/payment/',
            'hx-trigger': 'keyup changed delay:500ms',
            'hx-target': '#payment-table-container',
            'hx-swap': 'innerHTML',
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Semua Status')] + Payment.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': TAILWIND_SELECT,
            'hx-get': '/admin-panel/payment/',
            'hx-trigger': 'change',
            'hx-target': '#payment-table-container',
            'hx-swap': 'innerHTML',
        })
    )
    order_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Terbaru'),
            ('created_at', 'Terlama'),
            ('santri__nama_lengkap', 'Nama A-Z'),
            ('-santri__nama_lengkap', 'Nama Z-A'),
        ],
        widget=forms.Select(attrs={
            'class': TAILWIND_SELECT,
            'hx-get': '/admin-panel/payment/',
            'hx-trigger': 'change',
            'hx-target': '#payment-table-container',
            'hx-swap': 'innerHTML',
        })
    )


class BankAccountForm(forms.ModelForm):
    """Form untuk CRUD BankAccount dengan Tailwind CSS"""
    
    class Meta:
        model = BankAccount
        fields = [
            'nama_bank', 'nama_bank_custom', 'nomor_rekening', 
            'nama_pemilik_rekening', 'biaya_pendaftaran', 
            'is_active', 'keterangan', 'order'
        ]
        widgets = {
            'nama_bank': forms.Select(attrs={
                'class': TAILWIND_SELECT,
                'onchange': 'if(this.value === "Lainnya") { document.getElementById("id_nama_bank_custom").parentElement.style.display = "block"; } else { document.getElementById("id_nama_bank_custom").parentElement.style.display = "none"; }'
            }),
            'nama_bank_custom': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Masukkan nama bank jika memilih Bank Lainnya'
            }),
            'nomor_rekening': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nomor rekening'
            }),
            'nama_pemilik_rekening': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama pemilik rekening'
            }),
            'biaya_pendaftaran': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '0',
                'step': '1000',
                'min': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
            'keterangan': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Keterangan tambahan (opsional)'
            }),
            'order': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '0',
                'min': '0'
            }),
        }
        labels = {
            'nama_bank': 'Nama Bank',
            'nama_bank_custom': 'Nama Bank (Custom)',
            'nomor_rekening': 'Nomor Rekening',
            'nama_pemilik_rekening': 'Nama Pemilik Rekening',
            'biaya_pendaftaran': 'Biaya Pendaftaran (Rp)',
            'is_active': 'Aktif',
            'keterangan': 'Keterangan',
            'order': 'Urutan',
        }
    
    def clean_biaya_pendaftaran(self):
        """Validasi biaya pendaftaran tidak boleh negatif"""
        biaya = self.cleaned_data.get('biaya_pendaftaran')
        if biaya and biaya < 0:
            raise ValidationError('Biaya pendaftaran tidak boleh negatif.')
        return biaya
    
    def clean(self):
        cleaned_data = super().clean()
        nama_bank = cleaned_data.get('nama_bank')
        nama_bank_custom = cleaned_data.get('nama_bank_custom')
        
        if nama_bank == 'Lainnya' and not nama_bank_custom:
            raise ValidationError({
                'nama_bank_custom': 'Harap isi nama bank jika memilih Bank Lainnya.'
            })
        
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """Form untuk profil user dengan Tailwind CSS"""
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'phone', 'role', 'avatar'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Username',
                'readonly': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'email@example.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama depan'
            }),
            'last_name': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama belakang'
            }),
            'phone': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'tel',
                'placeholder': '081234567890'
            }),
            'role': forms.Select(attrs={
                'class': TAILWIND_SELECT,
                'disabled': True,
            }),
            'avatar': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'phone': 'No. HP',
            'role': 'Role',
            'avatar': 'Foto Profil',
        }
    
    def __init__(self, *args, **kwargs):
        edit_mode = kwargs.pop('edit_mode', False)
        super().__init__(*args, **kwargs)
        # Role dan username tidak bisa diubah
        # Gunakan readonly untuk username (input text support readonly)
        self.fields['username'].widget.attrs['readonly'] = True
        
        # Untuk role (select), kita tidak bisa menggunakan readonly
        # Jadi kita akan handle di clean_role() dan view
        self.fields['role'].widget.attrs['disabled'] = True
        # Set required=False karena kita akan handle di clean_role()
        self.fields['role'].required = False
        
        # Jika tidak dalam mode edit, set semua field sebagai readonly dan hide avatar
        if not edit_mode:
            # Hide avatar field jika tidak edit mode
            if 'avatar' in self.fields:
                del self.fields['avatar']
            
            for field_name, field in self.fields.items():
                if field_name not in ['role', 'username']:
                    field.widget.attrs['readonly'] = True
                    field.widget.attrs['disabled'] = True
    
    def clean_role(self):
        """Handle role field yang disabled - ambil dari instance jika tidak ada di POST"""
        role = self.cleaned_data.get('role')
        # Jika role tidak ada (karena disabled field tidak mengirimkan nilai), ambil dari instance
        if not role:
            if self.instance and hasattr(self.instance, 'role') and self.instance.role:
                role = self.instance.role
            # Jika masih tidak ada, ambil dari initial data
            elif 'role' in self.initial and self.initial['role']:
                role = self.initial['role']
            # Fallback ke default jika masih tidak ada
            else:
                role = 'petugaspendaftaran'
        return role
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Validasi ukuran file (maksimal 2MB)
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Ukuran file terlalu besar! Maksimal 2MB.')
            
            # Validasi tipe file
            valid_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if avatar.content_type not in valid_types:
                raise forms.ValidationError('Format file tidak didukung! Gunakan JPG, PNG, atau GIF.')
            
            # Sanitize nama file
            import os
            from django.utils.text import slugify
            name, ext = os.path.splitext(avatar.name)
            avatar.name = f"{slugify(name)}{ext}"
        
        return avatar


class UserAccountForm(forms.ModelForm):
    """Form untuk Create dan Update User Account dengan Tailwind CSS"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Password (kosongkan jika tidak ingin mengubah)',
        }),
        required=False,
        help_text='Kosongkan jika tidak ingin mengubah password'
    )
    password2 = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Konfirmasi password',
        }),
        required=False
    )
    santri_id = forms.ModelChoiceField(
        queryset=Santri.objects.all(),
        required=False,
        label='Ambil Data dari Santri',
        widget=forms.Select(attrs={
            'class': TAILWIND_SELECT,
        }),
        help_text='Pilih santri untuk mengisi data otomatis (opsional)'
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'phone', 'is_active', 'avatar'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'email@example.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama depan'
            }),
            'last_name': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama belakang'
            }),
            'phone': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'tel',
                'placeholder': '081234567890'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded'
            }),
            'avatar': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'phone': 'No. HP',
            'is_active': 'Aktif',
            'avatar': 'Foto Profil',
        }
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        # Jika edit mode, password tidak wajib
        if self.is_edit:
            self.fields['password1'].help_text = 'Kosongkan jika tidak ingin mengubah password'
            self.fields['password2'].help_text = 'Kosongkan jika tidak ingin mengubah password'
        else:
            # Jika create mode, password wajib
            self.fields['password1'].required = True
            self.fields['password2'].required = True
            self.fields['password1'].help_text = 'Password wajib diisi'
            self.fields['password2'].help_text = 'Konfirmasi password wajib diisi'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Cek apakah username sudah ada (kecuali jika edit mode dan username sama)
            if self.is_edit and self.instance and self.instance.username == username:
                return username
            if User.objects.filter(username=username).exists():
                raise ValidationError('Username sudah digunakan.')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        # Jika edit mode dan password kosong, skip validasi password
        if self.is_edit and not password1 and not password2:
            return cleaned_data
        
        # Validasi password
        if password1 or password2:
            if password1 != password2:
                raise ValidationError({
                    'password2': 'Password dan konfirmasi password tidak cocok.'
                })
            if password1:
                try:
                    validate_password(password1)
                except ValidationError as e:
                    raise ValidationError({
                        'password1': e.messages
                    })
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        
        # Jika password diisi, set password baru
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user


class UserChangePasswordForm(forms.Form):
    """Form untuk Change Password User"""
    new_password1 = forms.CharField(
        label='Password Baru',
        widget=forms.PasswordInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Password baru'
        }),
        help_text='Password baru untuk user'
    )
    new_password2 = forms.CharField(
        label='Konfirmasi Password Baru',
        widget=forms.PasswordInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Konfirmasi password baru'
        }),
        help_text='Konfirmasi password baru'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError({
                    'new_password2': 'Password dan konfirmasi password tidak cocok.'
                })
            if password1:
                try:
                    validate_password(password1)
                except ValidationError as e:
                    raise ValidationError({
                        'new_password1': e.messages
                    })
        
        return cleaned_data


class StaffForm(forms.ModelForm):
    """Form untuk Create dan Update Staff dengan Role Selection"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Password (kosongkan jika tidak ingin mengubah)',
        }),
        required=False,
        help_text='Kosongkan jika tidak ingin mengubah password'
    )
    password2 = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Konfirmasi password',
        }),
        required=False
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'phone', 'role', 'is_staff', 'is_superuser', 'is_active', 'avatar'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'email@example.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama depan'
            }),
            'last_name': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama belakang'
            }),
            'phone': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'tel',
                'placeholder': '081234567890'
            }),
            'role': forms.Select(attrs={
                'class': TAILWIND_SELECT,
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded'
            }),
            'is_superuser': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded'
            }),
            'avatar': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'Nama Depan',
            'last_name': 'Nama Belakang',
            'phone': 'No. HP',
            'role': 'Role',
            'is_staff': 'Staff',
            'is_superuser': 'Superuser',
            'is_active': 'Aktif',
            'avatar': 'Foto Profil',
        }
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        # Staff selalu is_staff=True
        self.fields['is_staff'].initial = True
        # Jangan disable karena akan tidak tersimpan, cukup readonly secara visual
        
        # Jika edit mode, password tidak wajib
        if self.is_edit:
            self.fields['password1'].help_text = 'Kosongkan jika tidak ingin mengubah password'
            self.fields['password2'].help_text = 'Kosongkan jika tidak ingin mengubah password'
        else:
            # Jika create mode, password wajib
            self.fields['password1'].required = True
            self.fields['password2'].required = True
            self.fields['password1'].help_text = 'Password wajib diisi'
            self.fields['password2'].help_text = 'Konfirmasi password wajib diisi'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Cek apakah username sudah ada (kecuali jika edit mode dan username sama)
            if self.is_edit and self.instance and self.instance.username == username:
                return username
            if User.objects.filter(username=username).exists():
                raise ValidationError('Username sudah digunakan.')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        role = cleaned_data.get('role')
        
        # Jika role adalah superadmin, set is_superuser=True
        if role == 'superadmin':
            cleaned_data['is_superuser'] = True
        
        # Jika edit mode dan password kosong, skip validasi password
        if self.is_edit and not password1 and not password2:
            return cleaned_data
        
        # Validasi password
        if password1 or password2:
            if password1 != password2:
                raise ValidationError({
                    'password2': 'Password dan konfirmasi password tidak cocok.'
                })
            if password1:
                try:
                    validate_password(password1)
                except ValidationError as e:
                    raise ValidationError({
                        'password1': e.messages
                    })
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        
        # Staff selalu is_staff=True
        user.is_staff = True
        
        # Jika role adalah superadmin, set is_superuser=True
        if user.role == 'superadmin':
            user.is_superuser = True
        
        # Jika password diisi, set password baru
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user


class BagianJabatanForm(forms.ModelForm):
    """Form untuk Create dan Update Bagian/Jabatan"""
    
    class Meta:
        model = BagianJabatan
        fields = ['nama', 'deskripsi', 'order', 'is_active']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Contoh: Pendiri, Kepala Sekolah, Pimpinan, Ustadz, Ustadzah'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Deskripsi singkat tentang bagian/jabatan ini'
            }),
            'order': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '0'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }


class TenagaPengajarForm(forms.ModelForm):
    """Form untuk Create dan Update Tenaga Pengajar"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cek jumlah featured pengajar
        instance_id = self.instance.pk if self.instance else None
        featured_count = TenagaPengajar.objects.filter(is_featured=True).exclude(id=instance_id).count()
        
        # Tampilkan info jumlah featured
        if featured_count >= 6:
            if not (self.instance and self.instance.is_featured):
                self.fields['is_featured'].help_text = f'⚠️ Maksimal 6 pengajar unggulan sudah tercapai ({featured_count} pengajar). Silakan hapus featured dari pengajar lain terlebih dahulu.'
            else:
                self.fields['is_featured'].help_text = f'ℹ️ Saat ini ada {featured_count + 1} pengajar unggulan. Maksimal 6.'
        else:
            self.fields['is_featured'].help_text = f'ℹ️ Saat ini ada {featured_count} pengajar unggulan. Maksimal 6.'
    
    def clean_is_featured(self):
        is_featured = self.cleaned_data.get('is_featured', False)
        
        if is_featured:
            # Cek jumlah featured pengajar (exclude instance saat ini jika update)
            instance_id = self.instance.pk if self.instance else None
            featured_count = TenagaPengajar.objects.filter(is_featured=True).exclude(id=instance_id).count()
            if featured_count >= 6:
                raise forms.ValidationError('Maksimal 6 pengajar unggulan sudah tercapai. Silakan hapus featured dari pengajar lain terlebih dahulu.')
        return is_featured
    
    class Meta:
        model = TenagaPengajar
        fields = [
            'nama_lengkap', 'nama_panggilan', 'jenis_kelamin', 'foto',
            'bagian_jabatan',
            'tempat_lahir', 'tanggal_lahir', 'alamat', 'no_hp', 'email',
            'pendidikan_terakhir', 'universitas', 'tahun_lulus',
            'bidang_keahlian', 'mata_pelajaran',
            'pengalaman_mengajar', 'prestasi',
            'riwayat_pendidikan', 'organisasi', 'karya_tulis', 'motto',
            'whatsapp', 'facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok',
            'order', 'is_published', 'is_featured'
        ]
        widgets = {
            'nama_lengkap': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama lengkap tenaga pengajar'
            }),
            'nama_panggilan': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama panggilan (opsional)'
            }),
            'jenis_kelamin': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'foto': forms.FileInput(attrs={
                'class': TAILWIND_FILE_INPUT,
                'accept': 'image/*'
            }),
            'bagian_jabatan': forms.Select(attrs={
                'class': TAILWIND_SELECT
            }),
            'tempat_lahir': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Tempat lahir'
            }),
            'tanggal_lahir': forms.DateInput(attrs={
                'class': TAILWIND_INPUT,
                'type': 'date'
            }),
            'alamat': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Alamat lengkap'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '081234567890'
            }),
            'email': forms.EmailInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'email@example.com'
            }),
            'pendidikan_terakhir': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Contoh: S1 Pendidikan Agama Islam'
            }),
            'universitas': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Nama universitas/institusi'
            }),
            'tahun_lulus': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '2020',
                'maxlength': '4'
            }),
            'bidang_keahlian': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Contoh: Tafsir, Hadits, Fiqih, Bahasa Arab'
            }),
            'mata_pelajaran': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Contoh: Tafsir Al-Qur\'an, Hadits, Fiqih'
            }),
            'pengalaman_mengajar': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 4,
                'placeholder': 'Riwayat pengalaman mengajar'
            }),
            'prestasi': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 4,
                'placeholder': 'Prestasi dan penghargaan yang pernah diraih'
            }),
            'riwayat_pendidikan': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 4,
                'placeholder': 'Riwayat pendidikan lengkap dari SD sampai perguruan tinggi'
            }),
            'organisasi': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Keanggotaan organisasi'
            }),
            'karya_tulis': forms.Textarea(attrs={
                'class': TAILWIND_TEXTAREA,
                'rows': 3,
                'placeholder': 'Karya tulis, buku, atau publikasi'
            }),
            'motto': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'Motto atau kata-kata inspiratif'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '6281234567890 (tanpa + dan spasi)'
            }),
            'facebook': forms.URLInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'https://facebook.com/username'
            }),
            'instagram': forms.URLInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'https://instagram.com/username'
            }),
            'twitter': forms.URLInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'https://twitter.com/username'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'https://linkedin.com/in/username'
            }),
            'youtube': forms.URLInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'https://youtube.com/@username'
            }),
            'tiktok': forms.URLInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'https://tiktok.com/@username'
            }),
            'order': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': '0'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-green-600 border-gray-300 rounded focus:ring-green-500'
            }),
        }
