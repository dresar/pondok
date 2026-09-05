from django.db import models
from django.core.validators import RegexValidator


class Santri(models.Model):
    """Model untuk data calon santri"""
    STATUS_CHOICES = [
        ('pending', 'Menunggu Verifikasi'),
        ('verified', 'Pembayaran Terverifikasi'),
        ('accepted', 'Diterima'),
        ('rejected', 'Ditolak'),
    ]
    
    # Data Pribadi
    nama_lengkap = models.CharField(max_length=200, verbose_name='Nama Lengkap')
    nama_panggilan = models.CharField(max_length=100, blank=True, verbose_name='Nama Panggilan')
    nisn = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='NISN harus 10 digit angka')],
        verbose_name='NISN'
    )
    tempat_lahir = models.CharField(max_length=100, verbose_name='Tempat Lahir')
    tanggal_lahir = models.DateField(verbose_name='Tanggal Lahir')
    jenis_kelamin = models.CharField(
        max_length=10,
        choices=[('L', 'Laki-laki'), ('P', 'Perempuan')],
        verbose_name='Jenis Kelamin'
    )
    agama = models.CharField(
        max_length=20,
        default='Islam',
        verbose_name='Agama',
        help_text='Agama santri (default: Islam)'
    )
    kewarganegaraan = models.CharField(
        max_length=10,
        default='WNI',
        choices=[('WNI', 'WNI'), ('WNA', 'WNA')],
        verbose_name='Kewarganegaraan'
    )
    anak_ke = models.PositiveIntegerField(blank=True, null=True, verbose_name='Anak Ke')
    jumlah_saudara = models.PositiveIntegerField(blank=True, null=True, verbose_name='Jumlah Saudara')
    bahasa_sehari_hari = models.CharField(max_length=50, blank=True, default='Indonesia', verbose_name='Bahasa Sehari-hari')
    golongan_darah = models.CharField(
        max_length=3,
        choices=[
            ('A', 'A'),
            ('B', 'B'),
            ('AB', 'AB'),
            ('O', 'O'),
        ],
        blank=True,
        verbose_name='Golongan Darah'
    )
    tinggi_badan = models.PositiveIntegerField(blank=True, null=True, verbose_name='Tinggi Badan (cm)')
    berat_badan = models.PositiveIntegerField(blank=True, null=True, verbose_name='Berat Badan (kg)')
    riwayat_penyakit = models.CharField(max_length=200, blank=True, verbose_name='Riwayat Penyakit')
    tinggal_dengan = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('Orang Tua', 'Orang Tua'),
            ('Wali', 'Wali'),
            ('Lainnya', 'Lainnya'),
        ],
        verbose_name='Tinggal Dengan'
    )
    
    # Data Orang Tua
    nama_ayah = models.CharField(max_length=200, verbose_name='Nama Ayah')
    nik_ayah = models.CharField(max_length=16, blank=True, verbose_name='NIK Ayah (No. KTP)', help_text='16 digit NIK')
    tempat_lahir_ayah = models.CharField(max_length=100, blank=True, verbose_name='Tempat Lahir Ayah')
    tanggal_lahir_ayah = models.DateField(blank=True, null=True, verbose_name='Tanggal Lahir Ayah')
    agama_ayah = models.CharField(max_length=20, blank=True, default='Islam', verbose_name='Agama Ayah')
    kewarganegaraan_ayah = models.CharField(
        max_length=10,
        blank=True,
        default='WNI',
        choices=[('WNI', 'WNI'), ('WNA', 'WNA')],
        verbose_name='Kewarganegaraan Ayah'
    )
    pendidikan_ayah = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('SD SEDERAJAT', 'SD SEDERAJAT'),
            ('SMP SEDERAJAT', 'SMP SEDERAJAT'),
            ('SMA SEDERAJAT', 'SMA SEDERAJAT'),
            ('D3', 'D3'),
            ('S1', 'S1'),
            ('S2', 'S2'),
            ('S3', 'S3'),
        ],
        verbose_name='Pendidikan Ayah'
    )
    pekerjaan_ayah = models.CharField(max_length=100, blank=True, verbose_name='Pekerjaan Ayah')
    no_hp_ayah = models.CharField(max_length=15, blank=True, verbose_name='No. HP Ayah')
    status_ayah = models.CharField(
        max_length=10,
        blank=True,
        default='HIDUP',
        choices=[('HIDUP', 'HIDUP'), ('MENINGGAL', 'MENINGGAL')],
        verbose_name='Status Ayah'
    )
    nama_ibu = models.CharField(max_length=200, verbose_name='Nama Ibu')
    nik_ibu = models.CharField(max_length=16, blank=True, verbose_name='NIK Ibu (No. KTP)', help_text='16 digit NIK')
    tempat_lahir_ibu = models.CharField(max_length=100, blank=True, verbose_name='Tempat Lahir Ibu')
    tanggal_lahir_ibu = models.DateField(blank=True, null=True, verbose_name='Tanggal Lahir Ibu')
    agama_ibu = models.CharField(max_length=20, blank=True, default='Islam', verbose_name='Agama Ibu')
    kewarganegaraan_ibu = models.CharField(
        max_length=10,
        blank=True,
        default='WNI',
        choices=[('WNI', 'WNI'), ('WNA', 'WNA')],
        verbose_name='Kewarganegaraan Ibu'
    )
    pendidikan_ibu = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('SD SEDERAJAT', 'SD SEDERAJAT'),
            ('SMP SEDERAJAT', 'SMP SEDERAJAT'),
            ('SMA SEDERAJAT', 'SMA SEDERAJAT'),
            ('D3', 'D3'),
            ('S1', 'S1'),
            ('S2', 'S2'),
            ('S3', 'S3'),
        ],
        verbose_name='Pendidikan Ibu'
    )
    pekerjaan_ibu = models.CharField(max_length=100, blank=True, verbose_name='Pekerjaan Ibu')
    no_hp_ibu = models.CharField(max_length=15, blank=True, verbose_name='No. HP Ibu')
    status_ibu = models.CharField(
        max_length=10,
        blank=True,
        default='HIDUP',
        choices=[('HIDUP', 'HIDUP'), ('MENINGGAL', 'MENINGGAL')],
        verbose_name='Status Ibu'
    )
    alamat_orangtua = models.TextField(blank=True, verbose_name='Alamat Orang Tua')
    
    # Kontak
    alamat = models.TextField(verbose_name='Alamat Lengkap')
    desa = models.CharField(max_length=100, blank=True, verbose_name='Desa/Kelurahan')
    kecamatan = models.CharField(max_length=100, blank=True, verbose_name='Kecamatan')
    kabupaten = models.CharField(max_length=100, blank=True, verbose_name='Kabupaten')
    provinsi = models.CharField(max_length=100, blank=True, verbose_name='Provinsi')
    kode_pos = models.CharField(max_length=10, blank=True, verbose_name='Kode Pos')
    no_hp = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Format nomor HP tidak valid')],
        verbose_name='No. HP'
    )
    email = models.EmailField(blank=True, verbose_name='Email')
    
    # Data Sekolah
    asal_sekolah = models.CharField(max_length=200, verbose_name='Asal Sekolah')
    npsn_sekolah = models.CharField(max_length=20, blank=True, verbose_name='NPSN Sekolah')
    kelas_terakhir = models.CharField(max_length=50, verbose_name='Kelas Terakhir')
    tahun_lulus = models.CharField(max_length=4, blank=True, verbose_name='Tahun Lulus')
    no_ijazah = models.CharField(max_length=50, blank=True, verbose_name='No. Ijazah/SKHUN')
    kelas_diterima = models.CharField(max_length=50, blank=True, verbose_name='Kelas Diterima (di Pesantren)')
    tanggal_diterima = models.DateField(blank=True, null=True, verbose_name='Tanggal Diterima')
    
    # Dokumen
    foto_santri = models.ImageField(upload_to='santri/foto/', blank=True, null=True, verbose_name='Foto Santri')
    foto_ktp = models.ImageField(upload_to='santri/ktp/', blank=True, null=True, verbose_name='Foto KTP/Kartu Keluarga')
    foto_akta = models.ImageField(upload_to='santri/akta/', blank=True, null=True, verbose_name='Foto Akta Kelahiran')
    foto_ijazah = models.ImageField(upload_to='santri/ijazah/', blank=True, null=True, verbose_name='Foto Ijazah/SKHUN')
    surat_sehat = models.ImageField(upload_to='santri/surat_sehat/', blank=True, null=True, verbose_name='Surat Keterangan Sehat')
    
    # Status Approval Dokumen
    foto_santri_approved = models.BooleanField(default=False, verbose_name='Foto Santri Disetujui')
    foto_ktp_approved = models.BooleanField(default=False, verbose_name='Foto KTP/KK Disetujui')
    foto_akta_approved = models.BooleanField(default=False, verbose_name='Foto Akta Disetujui')
    foto_ijazah_approved = models.BooleanField(default=False, verbose_name='Foto Ijazah Disetujui')
    surat_sehat_approved = models.BooleanField(default=False, verbose_name='Surat Sehat Disetujui')
    
    catatan = models.TextField(blank=True, verbose_name='Catatan Tambahan')
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Daftar')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Terakhir Diupdate')
    
    class Meta:
        verbose_name = 'Santri'
        verbose_name_plural = 'Santri'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nama_lengkap} - {self.nisn}"
    
    def get_status_display_class(self):
        """Mengembalikan class CSS untuk status badge"""
        status_classes = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'verified': 'bg-blue-100 text-blue-800',
            'accepted': 'bg-green-100 text-green-800',
            'rejected': 'bg-red-100 text-red-800',
        }
        return status_classes.get(self.status, 'bg-gray-100 text-gray-800')
