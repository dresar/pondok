from django.db import models
from admissions.models import Santri


class BankAccount(models.Model):
    """Model untuk rekening bank tujuan pembayaran"""
    BANK_CHOICES = [
        ('BCA', 'Bank Central Asia (BCA)'),
        ('BNI', 'Bank Negara Indonesia (BNI)'),
        ('BRI', 'Bank Rakyat Indonesia (BRI)'),
        ('Mandiri', 'Bank Mandiri'),
        ('BSI', 'Bank Syariah Indonesia (BSI)'),
        ('CIMB', 'CIMB Niaga'),
        ('Permata', 'Bank Permata'),
        ('Danamon', 'Bank Danamon'),
        ('Lainnya', 'Bank Lainnya'),
    ]
    
    nama_bank = models.CharField(
        max_length=100,
        choices=BANK_CHOICES,
        verbose_name='Nama Bank'
    )
    nama_bank_custom = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Nama Bank (Custom)',
        help_text='Isi jika memilih Bank Lainnya'
    )
    nomor_rekening = models.CharField(
        max_length=50,
        verbose_name='Nomor Rekening'
    )
    nama_pemilik_rekening = models.CharField(
        max_length=200,
        verbose_name='Nama Pemilik Rekening'
    )
    biaya_pendaftaran = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        verbose_name='Biaya Pendaftaran (Rp)',
        help_text='Biaya pendaftaran yang harus dibayar ke rekening ini'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Aktif',
        help_text='Rekening aktif akan ditampilkan di form pembayaran'
    )
    keterangan = models.TextField(
        blank=True,
        verbose_name='Keterangan',
        help_text='Catatan tambahan tentang rekening ini'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Urutan',
        help_text='Urutan tampil di form pembayaran'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Diupdate')
    
    class Meta:
        verbose_name = 'Rekening Bank'
        verbose_name_plural = 'Rekening Bank'
        ordering = ['order', 'nama_bank', 'nomor_rekening']
    
    def __str__(self):
        bank_name = self.nama_bank_custom if self.nama_bank == 'Lainnya' and self.nama_bank_custom else self.get_nama_bank_display()
        return f"{bank_name} - {self.nomor_rekening} ({self.nama_pemilik_rekening})"
    
    def get_display_name(self):
        """Mengembalikan nama bank untuk ditampilkan"""
        if self.nama_bank == 'Lainnya' and self.nama_bank_custom:
            return self.nama_bank_custom
        return self.get_nama_bank_display()


class Payment(models.Model):
    """Model untuk bukti pembayaran pendaftaran"""
    STATUS_CHOICES = [
        ('pending', 'Menunggu Verifikasi'),
        ('verified', 'Terverifikasi'),
        ('rejected', 'Ditolak'),
    ]
    
    BANK_CHOICES = [
        ('BCA', 'Bank Central Asia (BCA)'),
        ('BNI', 'Bank Negara Indonesia (BNI)'),
        ('BRI', 'Bank Rakyat Indonesia (BRI)'),
        ('Mandiri', 'Bank Mandiri'),
        ('BSI', 'Bank Syariah Indonesia (BSI)'),
        ('Lainnya', 'Bank Lainnya'),
    ]
    
    santri = models.OneToOneField(
        Santri,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='Santri'
    )
    bank_pengirim = models.CharField(
        max_length=50,
        choices=BANK_CHOICES,
        verbose_name='Bank Pengirim'
    )
    no_rekening_pengirim = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='No. Rekening Pengirim',
        help_text='Nomor rekening yang digunakan untuk transfer'
    )
    nama_pemilik_rekening = models.CharField(
        max_length=200,
        verbose_name='Nama Pemilik Rekening'
    )
    rekening_tujuan = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Rekening Tujuan',
        help_text='Nomor rekening tujuan transfer'
    )
    jumlah_transfer = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Jumlah Transfer (Rp)'
    )
    bukti_transfer = models.ImageField(
        upload_to='bukti_transfer/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Bukti Transfer'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status Verifikasi'
    )
    catatan = models.TextField(blank=True, verbose_name='Catatan (Opsional)')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Upload')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Terakhir Diupdate')
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name='Tanggal Verifikasi')
    verified_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_payments',
        verbose_name='Diverifikasi Oleh'
    )
    
    class Meta:
        verbose_name = 'Pembayaran'
        verbose_name_plural = 'Pembayaran'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pembayaran - {self.santri.nama_lengkap} ({self.get_status_display()})"
    
    def get_status_display_class(self):
        """Mengembalikan class CSS untuk status badge"""
        status_classes = {
            'pending': 'bg-yellow-100 text-yellow-800',
            'verified': 'bg-green-100 text-green-800',
            'rejected': 'bg-red-100 text-red-800',
        }
        return status_classes.get(self.status, 'bg-gray-100 text-gray-800')
